/**
 * Курсы с диска: courses/<курс>/course.toml, <NN-модуль>/module.toml, <NN-урок>/lesson.mdx + lesson.py
 * (+ output.json — пишет валидатор). Папка = сущность, реестров нет. Общее для сайта и scripts/*.ts.
 * Курс с runtime = "none" (английский): у урока вместо lesson.py — exercises.toml (src/lib/english).
 */
import { existsSync, readdirSync, readFileSync, statSync } from 'node:fs';
import { join, resolve } from 'node:path';
import { parse as parseToml } from 'smol-toml';
import { parse as parseYaml } from 'yaml';
import type { Exercise } from '../english/check.ts';
import { parseExercises } from '../english/exercises.ts';
import { parseLessonMdx, parseLessonPy, splitFrontmatter, type Block, type CodeCell, type OutputFile } from './format.ts';

export const COURSES_DIR = join(resolve('.'), 'courses');
export const DATA_DIR = join(COURSES_DIR, 'data');
const NUMBERED_RE = /^(\d{2})-([a-z0-9]+(?:-[a-z0-9]+)*)$/;

export interface CourseMeta {
  title: string;
  code: string; // префикс id уроков: np, pd, en
  order: number;
  runtime: 'python' | 'none'; // none — курс без Python (английский): упражнения из exercises.toml, Pyodide не грузится
  beta: boolean;
  package: string; // numpy · pandas — версия в Pyodide и в requirements-dev.txt (у runtime = "none" — пусто)
  summary: string;
  audience: string; // для кого курс
  prerequisites: string[]; // что нужно знать
  reference: string; // тема справочника
  requires: string[]; // курсы, которые нужно пройти раньше: их понятия считаются известными (у pandas — нет)
  complete?: boolean; // программа написана целиком: строгие проверки структуры (validate_courses --strict) — всегда
}

export interface ModuleMeta {
  title: string;
  summary: string;
  outcomes: string[]; // что человек умеет после модуля
  level?: string; // уровень модуля в курсе английского: «A1–A2», «B1», «B2» — страница курса группирует по нему
}

export type LessonKind = 'lesson' | 'project' | 'review' | 'test' | 'placement';
/** Уроки с проверкой в конце (баллы, зачёт 80 %), а не по ходу. */
export const isTestKind = (kind: LessonKind) => kind === 'test' || kind === 'placement';

export interface LessonMeta {
  id: string;
  title: string;
  summary: string;
  minutes: number;
  kind: LessonKind; // review · test · placement — у курса английского
  optional: boolean; // «дополнительно»: дальше по курсу не понадобится, можно пропустить
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
  exercises: Exercise[]; // упражнения по английскому (exercises.toml), у уроков Python — пусто
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
    kind: (['project', 'review', 'test', 'placement'] as const).find((k) => k === raw.kind) ?? 'lesson',
    optional: raw.optional === true,
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
  const ex = existsSync(join(dir, 'exercises.toml')) ? parseExercises(read(join(dir, 'exercises.toml'))) : { value: [], problems: [] };
  problems.push(...blocks.problems.map((p) => `lesson.mdx: ${p}`), ...py.problems.map((p) => `lesson.py: ${p}`), ...ex.problems.map((p) => `exercises.toml: ${p}`));
  const practice = blocks.value.flatMap((b) => (b.type === 'practice' ? [b.id] : []));
  const order = ex.value.map((e) => e.id);
  if (practice.join() !== order.join()) {
    problems.push(`порядок <Practice> в lesson.mdx (${practice.join(', ') || '—'}) не совпадает с [[exercise]] в exercises.toml (${order.join(', ') || '—'})`);
  }
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
    exercises: ex.value,
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
    courses.push({
      slug,
      meta: { ...meta, order: meta.order ?? 100, requires: meta.requires ?? [], runtime: meta.runtime ?? 'python', beta: meta.beta ?? false, package: meta.package ?? '' },
      modules,
    });
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

/** Упражнения урока, по которым он засчитывается: ячейки [exercise] у Python, <Practice> у английского. */
export function lessonExerciseIds(lesson: LessonSource): string[] {
  return lesson.exercises.length ? lesson.exercises.map((e) => e.id) : lesson.cells.filter((c) => c.kind === 'exercise').map((c) => c.id);
}

/** Курсы с Python: им нужны Pyodide, .ipynb, проверки validate_courses/validate_browsers. */
export const isPythonCourse = (course: CourseSource) => course.meta.runtime !== 'none';

/** Файлы данных урока с адресами, по которым их берёт Python в браузере. */
export function lessonFiles(meta: LessonMeta): { name: string; url: string }[] {
  return meta.data.map((name) => ({ name, url: `/courses/data/${name}` }));
}

/** Пакеты урока в браузере: пакет курса (pandas тянет numpy) и дополнительные. */
export function lessonPackages(course: CourseMeta, meta: LessonMeta): string[] {
  return [...new Set(['numpy', course.package, ...meta.packages])];
}
