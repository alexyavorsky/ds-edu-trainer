/**
 * Локальные данные в виде, общем с Supabase: ключ синхронизации → {id записи: запись с t}.
 * Формат ключей — supabase/migrations/20261001000000_user_data.sql. Слияние по записям: побеждает
 * бо́льшее t, при равенстве остаётся своё; код с d: true — удалённый (вернули заготовку).
 */
import { listCodeIds, loadCode, putCode } from '../code-store';
import * as course from '../course/progress';
import { readSolvedMarks, writeSolvedMarks } from '../progress';
import { readPending } from './pending';

export interface Entry {
  t: number;
  [field: string]: unknown;
}
export type Entries = Record<string, Entry>;

/** Ключи, которые принимает сервер (check в миграции). */
export const KEY_PATTERN = /^(solved|course\.(ex|done|last)|code:[a-z0-9][a-z0-9/_.-]{0,150})$/;

const COURSE_PARTS = ['ex', 'done', 'last'] as const;
type CoursePart = (typeof COURSE_PARTS)[number];
const coursePart = (key: string) => key.slice('course.'.length) as CoursePart;

export function allLocalKeys(): string[] {
  return ['solved', ...COURSE_PARTS.map((p) => `course.${p}`), ...listCodeIds().map((id) => `code:${id}`)].filter((k) =>
    KEY_PATTERN.test(k),
  );
}

export function localEntries(key: string): Entries {
  if (key === 'solved') return readSolvedMarks();
  if (key.startsWith('course.')) return course.read()[coursePart(key)] as Entries;
  if (key.startsWith('code:')) {
    const id = key.slice('code:'.length);
    const saved = loadCode(id);
    return saved ? { [id]: { code: saved.code, starter: saved.starter, t: saved.t ?? 0 } } : {};
  }
  return {};
}

const isEntry = (e: unknown): e is Entry => typeof e === 'object' && e !== null && typeof (e as Entry).t === 'number';
const newer = (remote: Entry, local: Entry | undefined) => !local || remote.t > local.t;

/** Применить записи из облака там, где они новее локальных. */
export function applyRemote(key: string, remote: Record<string, unknown>): void {
  const entries = Object.entries(remote).filter((pair): pair is [string, Entry] => isEntry(pair[1]));

  if (key === 'solved') {
    const marks = readSolvedMarks();
    let changed = false;
    for (const [id, e] of entries) {
      if (typeof e.v === 'boolean' && newer(e, marks[id])) {
        marks[id] = { v: e.v, t: e.t };
        changed = true;
      }
    }
    if (changed) writeSolvedMarks(marks);
    return;
  }

  if (key.startsWith('course.')) {
    const part = coursePart(key);
    const store = course.read();
    const target = store[part] as Entries;
    let changed = false;
    for (const [id, e] of entries) {
      const valid = part === 'ex' ? typeof e.hash === 'string' : part === 'done' ? typeof e.v === 'boolean' : typeof e.lesson === 'string';
      if (valid && newer(e, target[id])) {
        target[id] = e;
        changed = true;
      }
    }
    if (changed) course.write(store);
    return;
  }

  if (key.startsWith('code:')) {
    for (const [id, e] of entries) {
      if (`code:${id}` !== key) continue;
      const local = loadCode(id);
      // локально кода нет: если удаление ещё в очереди, сравниваем с ним, иначе берём код из облака
      const deletedAt = local ? undefined : readPending()[key]?.[id];
      const localT = local ? (local.t ?? 0) : (deletedAt ?? -1);
      if (e.d === true) {
        if (local && e.t > localT) putCode(id, null);
      } else if (typeof e.code === 'string' && typeof e.starter === 'string' && e.t > localT && local?.code !== e.code) {
        putCode(id, { code: e.code, starter: e.starter, t: e.t });
      }
    }
  }
}
