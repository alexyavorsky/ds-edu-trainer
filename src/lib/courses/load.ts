/**
 * Курсы с диска: courses/<курс>/course.toml, <NN-модуль>/module.toml, <NN-урок>/lesson.mdx + lesson.py
 * (+ output.json — пишет валидатор). Папка = сущность, реестров нет. Общее для сайта и scripts/*.ts.
 */
import { existsSync, readdirSync, readFileSync, statSync } from 'node:fs';
import { join, resolve } from 'node:path';
import { parse as parseToml } from 'smol-toml';
import { parse as parseYaml } from 'yaml';
import { parseLessonMdx, parseLessonPy, splitFrontmatter, type Block, type CodeCell, type OutputFile } from './format.ts';

export const COURSES_DIR = join(resolve('.'), 'courses');
export const DATA_DIR = join(COURSES_DIR, 'data');
const NUMBERED_RE = /^(\d{2})-([a-z0-9]+(?:-[a-z0-9]+)*)$/;

export interface CourseMeta {
  title: string;
  code: string; // префикс id уроков: np, pd
  order: number;
  package: string; // numpy · pandas — версия в Pyodide и в requirements-dev.txt
  summary: string;
  audience: string; // для кого курс
  prerequisites: string[]; // что нужно знать
  reference: string; // тема справочника
  requires: string[]; // курсы, которые нужно пройти раньше: их понятия считаются известными (у pandas — нет)
}

export interface ModuleMeta {
  title: string;
  summary: string;
  outcomes: string[]; // что человек умеет после модуля
}

export interface LessonMeta {
  id: string;
  title: string;
  summary: string;
  minutes: number;
  kind: 'lesson' | 'project';
  introduces: string[]; // новые понятия урока: np.array, .shape, axis=
  reference: string[]; // статьи справочника «тема/статья»
  data: string[]; // файлы из courses/data
  packages: string[]; // пакеты сверх пакета курса (matplotlib)
}

export interface LessonSource {
  course: string;
  module: string; // папка модуля «01-start»
  slug: string; // «first-array» — адрес урока
  number: number; // номер в модуле
  dir: string;
  meta: LessonMeta;
  blocks: Block[];
  cells: CodeCell[];
  output: OutputFile | null;
  problems: string[]; // ошибки формата — их показывает валидатор
}

export interface ModuleSource {
  course: string;
  slug: string; // «01-start»
  number: number;
  meta: ModuleMeta;
  lessons: LessonSource[];
}

export interface CourseSource {
  slug: string; // «numpy»
  meta: CourseMeta;
  modules: ModuleSource[];
}

const read = (path: string) => readFileSync(path, 'utf-8');
const subdirs = (path: string) =>
  existsSync(path) ? readdirSync(path).filter((n) => NUMBERED_RE.test(n) && statSync(join(path, n)).isDirectory()).sort() : [];

export function lessonMeta(raw: Record<string, unknown>): LessonMeta {
  return {
    id: String(raw.id ?? ''),
    title: String(raw.title ?? ''),
    summary: String(raw.summary ?? ''),
    minutes: Number(raw.minutes ?? 0),
    kind: raw.kind === 'project' ? 'project' : 'lesson',
    introduces: (raw.introduces as string[]) ?? [],
    reference: (raw.reference as string[]) ?? [],
    data: (raw.data as string[]) ?? [],
    packages: (raw.packages as string[]) ?? [],
  };
}

export function loadLesson(course: string, module: string, folder: string): LessonSource {
  const dir = join(COURSES_DIR, course, module, folder);
  const problems: string[] = [];
  const mdx = existsSync(join(dir, 'lesson.mdx')) ? read(join(dir, 'lesson.mdx')) : '';
  let raw: Record<string, unknown> = {};
  try {
    raw = (parseYaml(splitFrontmatter(mdx).frontmatter) as Record<string, unknown>) ?? {};
  } catch (e) {
    problems.push(`lesson.mdx: frontmatter не читается — ${(e as Error).message}`);
  }
  const blocks = parseLessonMdx(mdx);
  const py = existsSync(join(dir, 'lesson.py')) ? parseLessonPy(read(join(dir, 'lesson.py'))) : { value: [], problems: [] };
  problems.push(...blocks.problems.map((p) => `lesson.mdx: ${p}`), ...py.problems.map((p) => `lesson.py: ${p}`));
  const outputPath = join(dir, 'output.json');
  const [, number, slug] = NUMBERED_RE.exec(folder)!;
  return {
    course,
    module,
    slug,
    number: Number(number),
    dir,
    meta: lessonMeta(raw),
    blocks: blocks.value,
    cells: py.value,
    output: existsSync(outputPath) ? (JSON.parse(read(outputPath)) as OutputFile) : null,
    problems,
  };
}

export function loadCourses(): CourseSource[] {
  const courses: CourseSource[] = [];
  for (const slug of existsSync(COURSES_DIR) ? readdirSync(COURSES_DIR).sort() : []) {
    const metaPath = join(COURSES_DIR, slug, 'course.toml');
    if (!existsSync(metaPath)) continue;
    const meta = parseToml(read(metaPath)) as unknown as CourseMeta;
    const modules = subdirs(join(COURSES_DIR, slug))
      .filter((m) => existsSync(join(COURSES_DIR, slug, m, 'module.toml')))
      .map((m) => ({
        course: slug,
        slug: m,
        number: Number(m.slice(0, 2)),
        meta: parseToml(read(join(COURSES_DIR, slug, m, 'module.toml'))) as unknown as ModuleMeta,
        lessons: subdirs(join(COURSES_DIR, slug, m))
          .filter((l) => existsSync(join(COURSES_DIR, slug, m, l, 'lesson.mdx')))
          .map((l) => loadLesson(slug, m, l)),
      }));
    courses.push({ slug, meta: { ...meta, order: meta.order ?? 100, requires: meta.requires ?? [] }, modules });
  }
  return courses.sort((a, b) => a.meta.order - b.meta.order);
}

/** Уроки курса в порядке прохождения. */
export function courseLessons(course: CourseSource): LessonSource[] {
  return course.modules.flatMap((m) => m.lessons);
}

export function lessonUrl(lesson: { course: string; slug: string }): string {
  return `/courses/${lesson.course}/${lesson.slug}`;
}

/** Файлы данных урока с адресами, по которым их берёт Python в браузере. */
export function lessonFiles(meta: LessonMeta): { name: string; url: string }[] {
  return meta.data.map((name) => ({ name, url: `/courses/data/${name}` }));
}

/** Пакеты урока в браузере: пакет курса (pandas тянет numpy) и дополнительные. */
export function lessonPackages(course: CourseMeta, meta: LessonMeta): string[] {
  return [...new Set(['numpy', course.package, ...meta.packages])];
}
