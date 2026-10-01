/**
 * Курсы для страниц сайта: структура с диска (load.ts), в production читается один раз за сборку.
 * В режиме разработки — заново при каждом запросе: правка lesson.py сразу видна.
 */
import { createHash } from 'node:crypto';
import type { CodeCell, StoredOutput } from './format.ts';
import { exerciseFingerprint } from '../english/exercises.ts';
import type { Exercise } from '../english/check.ts';
import { courseLessons, isTestKind, lessonFiles, lessonPackages, lessonUrl, loadCourses, type CourseSource, type LessonSource } from './load.ts';

let cache: CourseSource[] | null = null;

export function getCourses(): CourseSource[] {
  if (cache && import.meta.env.PROD) return cache;
  cache = loadCourses();
  return cache;
}

export function getCourse(slug: string): CourseSource | undefined {
  return getCourses().find((c) => c.slug === slug);
}

export function findLesson(id: string): { course: CourseSource; lesson: LessonSource } {
  for (const course of getCourses()) {
    const lesson = courseLessons(course).find((l) => l.meta.id === id);
    if (lesson) return { course, lesson };
  }
  throw new Error(`урок ${id} не найден в courses/`);
}

export function cellOf(lesson: LessonSource, id: string): CodeCell {
  const cell = lesson.cells.find((c) => c.id === id);
  if (!cell) throw new Error(`${lesson.meta.id}: в lesson.py нет ячейки «${id}»`);
  return cell;
}

export function storedOutput(lesson: LessonSource, id: string): StoredOutput | null {
  return lesson.output?.cells[id] ?? null;
}

export const hash = (text: string) => createHash('sha256').update(text).digest('hex').slice(0, 16);

export interface DemoData {
  id: string;
  kind: 'demo';
  code: string;
  raises: string | null; // ячейка [raises=…]: ожидаемая ошибка
}

export interface ExerciseData {
  id: string;
  kind: 'exercise';
  starter: string;
  starterHash: string;
  solution: string;
  tests: string;
  targets: string[];
}

export interface LessonPageData {
  lesson: string;
  course: string;
  packages: string[];
  files: { name: string; url: string }[];
  cells: (DemoData | ExerciseData)[];
}

/** Данные урока для скрипта страницы: ячейки по порядку, пакеты, файлы. */
export function lessonPageData(course: CourseSource, lesson: LessonSource): LessonPageData {
  const cells = lesson.blocks.flatMap((b): (DemoData | ExerciseData)[] => {
    if (b.type !== 'demo' && b.type !== 'exercise') return [];
    const cell = cellOf(lesson, b.id);
    if (cell.kind === 'demo') return [{ id: cell.id, kind: 'demo', code: cell.code, raises: cell.flags.raises ?? null }];
    if (cell.kind !== 'exercise') return [];
    return [
      {
        id: cell.id,
        kind: 'exercise',
        starter: cell.starter,
        starterHash: hash(cell.starter),
        solution: cell.solution,
        tests: cell.tests,
        targets: cell.targets,
      },
    ];
  });
  return {
    lesson: lesson.meta.id,
    course: course.slug,
    packages: lessonPackages(course.meta, lesson.meta),
    files: lessonFiles(lesson.meta),
    cells,
  };
}

// ─── Уроки английского ──────────────────────────────────────────────────────

/** Данные урока английского для src/scripts/english/practice.ts (тип — EnglishPageData там же). */
export function englishPageData(course: CourseSource, lesson: LessonSource, cefr: Map<string, string>) {
  const mode = lesson.meta.kind === 'placement' ? 'placement' : isTestKind(lesson.meta.kind) ? 'test' : 'drill';
  const exercises = lesson.exercises.map((e: Exercise) => ({ ...e, hash: hash(exerciseFingerprint(e)) }));
  const refs = [...new Set(lesson.exercises.flatMap((e) => [...e.ref, ...e.items.flatMap((i) => i.ref)]))];
  return {
    lesson: lesson.meta.id,
    course: course.slug,
    mode,
    exercises,
    placement:
      mode === 'placement'
        ? {
            cefr: Object.fromEntries(refs.map((r) => [r, cefr.get(r) ?? ''])),
            modules: course.modules
              .filter((m) => m.meta.level && m.lessons.length)
              .map((m) => ({ level: m.meta.level!, number: m.number, title: m.meta.title, href: lessonUrl(m.lessons[0]) })),
          }
        : undefined,
  };
}
