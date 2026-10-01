/**
 * Файл упражнений урока exercises.toml (docs/ENGLISH_PLAN.md, 0.3): разбор в типы check.ts и проверка формы
 * полей. Общий для сайта (src/lib/courses/load.ts) и валидатора (scripts/validate_english.ts); смысловые
 * проверки ответов — в валидаторе.
 */
import { parse as parseToml } from 'smol-toml';
import { DEFAULT_SETTINGS, KINDS, type Exercise, type Item, type Kind, type Wrong } from './check.ts';

export interface Parsed<T> {
  value: T;
  problems: string[];
}

const EXERCISE_FIELDS = new Set(['id', 'kind', 'title', 'task', 'ref', 'hint', 'options', 'explain', 'contractions', 'punctuation', 'allow_correct', 'pairs', 'item']);
const ITEM_FIELDS: Record<Kind, string[]> = {
  gap: ['text', 'answer', 'gaps', 'combos'],
  choice: ['text', 'options', 'answer', 'why'],
  order: ['words', 'answer'],
  transform: ['source', 'answer', 'start', 'keyword', 'max_words'],
  'find-error': ['text', 'error', 'fix', 'also'],
  match: [],
};
const COMMON_ITEM_FIELDS = ['explain', 'wrong', 'hint', 'ref'];
const ID_RE = /^[a-z0-9]+(-[a-z0-9]+)*$/;

type Raw = Record<string, unknown>;
const isStr = (v: unknown): v is string => typeof v === 'string';
const isStrList = (v: unknown): v is string[] => Array.isArray(v) && v.every(isStr);

/** Строка или список строк → список (answer = "…" и answer = ["…", "…"] равноправны). */
function strings(v: unknown, where: string, problems: string[]): string[] {
  if (v === undefined) return [];
  if (isStr(v)) return [v];
  if (isStrList(v)) return v;
  problems.push(`${where}: ожидается строка или список строк`);
  return [];
}

function lists(v: unknown, where: string, problems: string[]): string[][] | undefined {
  if (v === undefined) return undefined;
  if (Array.isArray(v) && v.every(isStrList)) return v as string[][];
  problems.push(`${where}: ожидается список списков строк, например [["were", "was"], ["would go"]]`);
  return undefined;
}

function parseItem(raw: Raw, kind: Kind, n: number, where: string, problems: string[]): Item {
  const at = `${where}, пункт ${n}`;
  const allowed = new Set([...ITEM_FIELDS[kind], ...COMMON_ITEM_FIELDS]);
  for (const key of Object.keys(raw)) if (!allowed.has(key)) problems.push(`${at}: поле «${key}» не бывает у ${kind}`);
  const wrong: Wrong[] = [];
  if (raw.wrong !== undefined) {
    if (!Array.isArray(raw.wrong)) problems.push(`${at}: wrong — список { answer = …, why = "…" }`);
    else
      for (const w of raw.wrong as Raw[]) {
        if (!w || typeof w !== 'object' || !isStr(w.why)) {
          problems.push(`${at}: у wrong нужны answer и why`);
          continue;
        }
        wrong.push({ answer: strings(w.answer, `${at}, wrong.answer`, problems), why: w.why });
      }
  }
  const why: Record<string, string> = {};
  if (raw.why !== undefined) {
    if (typeof raw.why !== 'object' || Array.isArray(raw.why)) problems.push(`${at}: why — таблица { "вариант" = "почему нет" }`);
    else for (const [k, v] of Object.entries(raw.why as Raw)) if (isStr(v)) why[k] = v;
  }
  const maxWords = raw.max_words;
  if (maxWords !== undefined && !(Number.isInteger(maxWords) && (maxWords as number) > 0)) problems.push(`${at}: max_words — целое число больше 0`);
  for (const key of ['text', 'explain', 'hint', 'source', 'start', 'keyword', 'error'] as const) {
    if (raw[key] !== undefined && !isStr(raw[key])) problems.push(`${at}: ${key} — строка`);
  }
  if (raw.words !== undefined && !isStrList(raw.words)) problems.push(`${at}: words — список строк`);
  if (raw.options !== undefined && !isStrList(raw.options)) problems.push(`${at}: options — список строк`);
  return {
    n,
    text: isStr(raw.text) ? raw.text : undefined,
    answer: strings(raw.answer, `${at}, answer`, problems),
    gaps: lists(raw.gaps, `${at}, gaps`, problems),
    combos: lists(raw.combos, `${at}, combos`, problems),
    options: isStrList(raw.options) ? raw.options : undefined,
    explain: isStr(raw.explain) ? raw.explain : '',
    wrong,
    why,
    hint: isStr(raw.hint) ? raw.hint : undefined,
    ref: strings(raw.ref, `${at}, ref`, problems),
    words: isStrList(raw.words) ? raw.words : undefined,
    source: isStr(raw.source) ? raw.source : undefined,
    start: isStr(raw.start) ? raw.start : undefined,
    keyword: isStr(raw.keyword) ? raw.keyword : undefined,
    maxWords: Number.isInteger(maxWords) ? (maxWords as number) : undefined,
    error: isStr(raw.error) ? raw.error : undefined,
    fix: raw.fix === undefined ? undefined : strings(raw.fix, `${at}, fix`, problems),
    also: raw.also === undefined ? undefined : strings(raw.also, `${at}, also`, problems),
  };
}

function parseExercise(raw: Raw, index: number, problems: string[]): Exercise | null {
  const id = isStr(raw.id) ? raw.id : '';
  const where = `упражнение ${id || `№${index + 1}`}`;
  if (!ID_RE.test(id)) problems.push(`${where}: id — kebab-case (a-z, 0-9, дефисы)`);
  const kind = raw.kind as Kind;
  if (!KINDS.includes(kind)) {
    problems.push(`${where}: kind — один из ${KINDS.join(', ')}`);
    return null;
  }
  for (const key of Object.keys(raw)) if (!EXERCISE_FIELDS.has(key)) problems.push(`${where}: неизвестное поле «${key}»`);
  if (!isStr(raw.task) || !raw.task.trim()) problems.push(`${where}: нет task (задание по-русски)`);
  const contractions = raw.contractions ?? DEFAULT_SETTINGS.contractions;
  const punctuation = raw.punctuation ?? DEFAULT_SETTINGS.punctuation;
  if (contractions !== 'equal' && contractions !== 'strict') problems.push(`${where}: contractions — "equal" или "strict"`);
  if (punctuation !== 'loose' && punctuation !== 'strict') problems.push(`${where}: punctuation — "loose" или "strict"`);
  if (raw.allow_correct !== undefined && typeof raw.allow_correct !== 'boolean') problems.push(`${where}: allow_correct — true или false`);
  if (raw.options !== undefined && !isStrList(raw.options)) problems.push(`${where}: options — список строк`);

  const shared = isStrList(raw.options) ? raw.options : undefined;
  let items: Item[];
  if (kind === 'match') {
    if (raw.item !== undefined) problems.push(`${where}: у match нет пунктов [[exercise.item]] — пары в поле pairs`);
    const pairs = Array.isArray(raw.pairs) && raw.pairs.every((p) => isStrList(p) && p.length === 2) ? (raw.pairs as [string, string][]) : [];
    if (!pairs.length) problems.push(`${where}: pairs — список пар [["начало", "конец"], …]`);
    const rights = pairs.map((p) => p[1]);
    items = pairs.map(([left, right], i) => ({ n: i + 1, text: left, answer: [right], options: rights, explain: '', wrong: [], why: {}, ref: [] }));
  } else {
    if (raw.pairs !== undefined) problems.push(`${where}: pairs бывают только у match`);
    const rawItems = Array.isArray(raw.item) ? (raw.item as Raw[]) : [];
    items = rawItems.map((it, i) => parseItem(it, kind, i + 1, where, problems));
    if (kind === 'choice') for (const it of items) it.options ??= shared;
  }
  return {
    id,
    kind,
    title: isStr(raw.title) ? raw.title : undefined,
    task: isStr(raw.task) ? raw.task : '',
    ref: strings(raw.ref, `${where}, ref`, problems),
    hint: isStr(raw.hint) ? raw.hint : undefined,
    explain: isStr(raw.explain) ? raw.explain : undefined,
    allowCorrect: raw.allow_correct === true,
    settings: { contractions: contractions as Exercise['settings']['contractions'], punctuation: punctuation as Exercise['settings']['punctuation'] },
    items,
  };
}

/** Разбор exercises.toml. Ошибки синтаксиса и формы полей — в problems (их показывает валидатор). */
export function parseExercises(text: string): Parsed<Exercise[]> {
  const problems: string[] = [];
  let data: Raw;
  try {
    data = parseToml(text) as Raw;
  } catch (e) {
    return { value: [], problems: [`exercises.toml не читается: ${(e as Error).message.split('\n')[0]}`] };
  }
  for (const key of Object.keys(data)) if (key !== 'exercise') problems.push(`exercises.toml: неизвестный раздел «${key}» — только [[exercise]]`);
  const raw = Array.isArray(data.exercise) ? (data.exercise as Raw[]) : [];
  const value = raw.map((r, i) => parseExercise(r, i, problems)).filter((e): e is Exercise => !!e);
  return { value, problems };
}

/**
 * Каноническая форма упражнения для хеша версии: вид, задание, настройки, пункты и ответы. Объяснения и
 * подсказки не входят — их правка не сбрасывает состояние ученика.
 */
export function exerciseFingerprint(ex: Exercise): string {
  const items = ex.items.map((i) => [i.text, i.answer, i.gaps, i.combos, i.options, i.words, i.source, i.start, i.keyword, i.maxWords, i.error, i.fix, i.also]);
  return JSON.stringify([ex.kind, ex.task, ex.settings, ex.allowCorrect, items]);
}
