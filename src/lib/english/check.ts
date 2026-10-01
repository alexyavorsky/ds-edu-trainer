/**
 * Проверка ответов упражнений по английскому — docs/ENGLISH_PLAN.md, 0.3 «Нормализация и сравнение».
 * Без зависимостей: один и тот же модуль работает на странице урока, в валидаторе (scripts/validate_english.ts)
 * и в слепой проверке, поэтому поведение везде одинаково.
 *
 * Ввод ученика и допустимые ответы проходят одни шаги: юникод и типографика → пробелы → конечная пунктуация и
 * кавычки → внутренняя пунктуация (loose/strict) → регистр → сокращения (equal/strict). У пропусков ответы
 * подставляются в предложение, и сравнивается всё предложение: «I ___ (be) tired» + «'m» = «I'm tired».
 */

export type Kind = 'gap' | 'choice' | 'order' | 'transform' | 'find-error' | 'match';
export const KINDS: Kind[] = ['gap', 'choice', 'order', 'transform', 'find-error', 'match'];

export interface Settings {
  contractions: 'equal' | 'strict'; // equal — краткая и полная форма равны; strict — как написано
  punctuation: 'loose' | 'strict'; // loose — запятые, «;», «:», тире не учитываются
}
export const DEFAULT_SETTINGS: Settings = { contractions: 'equal', punctuation: 'loose' };

/** Предусмотренная ошибка: у gap — значения по пропускам, у остальных — одно предложение. */
export interface Wrong {
  answer: string[];
  why: string;
}

export interface Item {
  n: number; // номер пункта в упражнении, с 1
  text?: string; // gap, choice, find-error; у match — левая часть
  answer: string[]; // допустимые ответы, первый — основной (gap: варианты единственного пропуска)
  gaps?: string[][]; // gap: независимые пропуски
  combos?: string[][]; // gap: полные наборы зависящих друг от друга пропусков
  options?: string[]; // choice, match
  explain: string;
  wrong: Wrong[];
  why: Record<string, string>; // choice: «вариант» → почему нет
  hint?: string;
  ref: string[];
  words?: string[]; // order
  source?: string; // transform
  start?: string;
  keyword?: string;
  maxWords?: number;
  error?: string; // find-error; нет — предложение верное (allow_correct)
  fix?: string[];
  also?: string[];
}

export interface Exercise {
  id: string;
  kind: Kind;
  title?: string;
  task: string;
  ref: string[];
  hint?: string;
  explain?: string; // match — объяснение упражнения целиком
  allowCorrect: boolean; // find-error: есть верные предложения, кнопка «Ошибки нет»
  settings: Settings;
  items: Item[];
}

/** Ввод: у gap — значения по пропускам, у остальных — строка (вариант, предложение). */
export type Input = string | string[];

export interface Result {
  status: 'ok' | 'wrong' | 'almost' | 'empty';
  gaps?: boolean[]; // gap: отметка «верно / неверно» у каждого пропуска (по ближайшему допустимому набору)
  notes: string[]; // мягкие замечания к засчитанному ответу
  why?: string; // объяснение предусмотренной ошибки
  matched?: string; // совпавший допустимый ответ (для «Также верно»)
}

// ─── Нормализация ───────────────────────────────────────────────────────────

export const GAP = '___';
const GAP_RE = /_{3,}/g;
const EMPTY_ANSWER = '—';
const OTHER_SPACES = /[   -​  　﻿\t\r\n\f\v]/g;

/** Пустой ответ («артикль не нужен»): в файле — «—», ученик вводит «-», «–» или «—». */
export const isEmptyMark = (s: string) => /^\s*[-–—]\s*$/.test(s);

/** Шаги 1–3: юникод, типографика, пробелы. Регистр и пунктуацию не трогает — для показа и замечаний. */
export function tidy(text: string): string {
  let s = text.normalize('NFC').replace(OTHER_SPACES, ' ');
  s = s.replace(/[’‘ʼ′´`]/g, "'").replace(/[“”„«»″]/g, '"').replace(/[–—]/g, '-').replace(/…/g, '...');
  s = s.replace(/ {2,}/g, ' ').trim();
  // пробелы вокруг апострофа внутри слова: «don ' t», «I 'm», «do n't»
  s = s.replace(/(\w) ?' ?(t)\b/gi, (m, a: string, t: string) => (/ /.test(m) ? `${a}'${t}` : m));
  s = s.replace(/(\w) '(m|re|ve|ll|s|d)\b/gi, "$1'$2");
  s = s.replace(/(\w) ' (m|re|ve|ll|s|d)\b/gi, "$1'$2");
  s = s.replace(/(\w) n't\b/gi, "$1n't");
  s = s.replace(/ +([,.!?;:])/g, '$1');
  return s;
}

const FINAL_RE = /[\s.!?]+$/;
const CONTRACTIONS: [RegExp, string][] = [
  [/\bcan't\b/g, 'cannot'],
  [/\bwon't\b/g, 'will not'],
  [/\bshan't\b/g, 'shall not'],
  [/\b(\w+)n't\b/g, '$1 not'],
  [/\b(\w+)'m\b/g, '$1 am'],
  [/\b(\w+)'re\b/g, '$1 are'],
  [/\b(\w+)'ve\b/g, '$1 have'],
  [/\b(\w+)'ll\b/g, '$1 will'],
];

/** Шаги 1–7: строка для сравнения. */
export function canon(text: string, settings: Settings = DEFAULT_SETTINGS): string {
  let s = tidy(text).replace(/"/g, '');
  const question = /\?\s*$/.test(s);
  s = s.replace(FINAL_RE, '');
  if (settings.punctuation === 'loose') {
    s = s.replace(/[,;:]/g, ' ').replace(/(^| )-( |$)/g, ' ');
  } else if (question) {
    s += '?'; // в строгом режиме вопрос без «?» — ошибка, а не замечание
  }
  s = s.toLowerCase();
  if (settings.contractions === 'equal') for (const [re, to] of CONTRACTIONS) s = s.replace(re, to);
  return s.replace(/\s+/g, ' ').trim();
}

/** Слова, после которых краткие 's и 'd однозначно значат is/has и would/had (в ответах их пишут полностью). */
export const CLOSED_WORDS = new Set(['i', 'you', 'he', 'she', 'it', 'we', 'they', 'there', 'here', 'that', 'what', 'who', 'where', 'how']);
const SHORT: Record<string, string> = { is: "'s", has: "'s", would: "'d", had: "'d" };
const MAX_SPOTS = 4;

/** Формы допустимого ответа: сам ответ и варианты с краткими 's/'d после слов закрытого списка (не больше 2⁴). */
export function answerForms(answer: string, settings: Settings = DEFAULT_SETTINGS): string[] {
  const base = canon(answer, settings);
  if (settings.contractions === 'strict') return [base];
  const words = base.split(' ');
  const spots = words
    .map((w, i) => (CLOSED_WORDS.has(w.replace(/\?$/, '')) && SHORT[words[i + 1]?.replace(/\?$/, '')] ? i : -1))
    .filter((i) => i >= 0)
    .slice(0, MAX_SPOTS);
  const forms = new Set<string>();
  for (let mask = 0; mask < 1 << spots.length; mask++) {
    const out: string[] = [];
    for (let i = 0; i < words.length; i++) {
      const k = spots.indexOf(i);
      if (k >= 0 && mask & (1 << k)) {
        out.push(words[i] + SHORT[words[i + 1].replace(/\?$/, '')] + (words[i + 1].endsWith('?') ? '?' : ''));
        i++;
      } else out.push(words[i]);
    }
    forms.add(out.join(' '));
  }
  return [...forms];
}

/** Совпадает ли ввод с ответом после нормализации (с краткими формами ответа). */
export function same(input: string, answer: string, settings: Settings = DEFAULT_SETTINGS): boolean {
  return answerForms(answer, settings).includes(canon(input, settings));
}

// ─── Предложения пунктов ────────────────────────────────────────────────────

/** Подставляет значения пропусков; подсказка в скобках сразу после пропуска «(be)» убирается. */
export function fillGaps(text: string, values: string[]): string {
  let i = 0;
  const filled = text.replace(/_{3,}(\s*\([^)]*\))?/g, () => {
    const v = values[i++] ?? '';
    return isEmptyMark(v) ? '' : v;
  });
  return filled.replace(/ {2,}/g, ' ').replace(/ ([,.!?;:])/g, '$1').trim();
}

export const gapCount = (text: string) => (text.match(GAP_RE) ?? []).length;

const MAX_COMBOS = 64;

/** Все допустимые наборы значений пропусков (у независимых пропусков — произведение, не больше 64). */
export function gapSets(item: Item): string[][] {
  if (item.combos) return item.combos;
  if (item.gaps) {
    let sets: string[][] = [[]];
    for (const options of item.gaps) {
      sets = sets.flatMap((s) => options.map((o) => [...s, o])).slice(0, MAX_COMBOS);
    }
    return sets;
  }
  return item.answer.map((a) => [a]);
}

/** Верные предложения find-error: ошибка заменена каждым исправлением, плюс полные варианты из also. */
export function fixedSentences(item: Item): string[] {
  const text = item.text ?? '';
  if (!item.error) return [text];
  return [...(item.fix ?? []).map((f) => replaceWords(text, item.error!, f)), ...(item.also ?? [])];
}

/** Заменяет фрагмент целыми словами (первое вхождение). Пустая замена убирает слово вместе с пробелом. */
export function replaceWords(text: string, fragment: string, replacement: string): string {
  const at = findWords(text, fragment);
  if (at < 0) return text;
  const joined = text.slice(0, at) + replacement + text.slice(at + fragment.length);
  return joined.replace(/ {2,}/g, ' ').replace(/ ([,.!?;:])/g, '$1').trim();
}

/** Позиция фрагмента целыми словами или -1. */
export function findWords(text: string, fragment: string): number {
  if (!fragment) return -1;
  const re = new RegExp(`(?<![\\w'])${fragment.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}(?![\\w'])`, 'g');
  const m = re.exec(text);
  return m ? m.index : -1;
}

export function countWords(text: string, fragment: string): number {
  if (!fragment) return 0;
  const re = new RegExp(`(?<![\\w'])${fragment.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}(?![\\w'])`, 'g');
  return (text.match(re) ?? []).length;
}

/** Допустимые ответы пункта как предложения (у gap — с подставленными пропусками), первый — основной. */
export function acceptedSentences(ex: Pick<Exercise, 'kind'>, item: Item): string[] {
  switch (ex.kind) {
    case 'gap':
      return gapSets(item).map((set) => fillGaps(item.text ?? '', set));
    case 'find-error':
      return fixedSentences(item);
    default:
      return item.answer;
  }
}

/** Что показать как ответ: у gap — значения пропусков через « … », у остальных — сам ответ. */
export function displayAnswers(ex: Pick<Exercise, 'kind'>, item: Item): string[] {
  if (ex.kind === 'gap') return gapSets(item).map((set) => set.join(' … '));
  if (ex.kind === 'find-error') return item.error ? fixedSentences(item) : ['Ошибки нет'];
  return item.answer;
}

// ─── Проверка ───────────────────────────────────────────────────────────────

const words = (s: string) => tidy(s).replace(/[,.!?;:"]/g, ' ').split(/\s+/).filter(Boolean);

/** Расстояние Дамерау — Левенштейна не больше 1 (одна буква заменена, вставлена, удалена или переставлена). */
function oneEdit(a: string, b: string): boolean {
  if (a === b || Math.abs(a.length - b.length) > 1) return false;
  if (a.length === b.length) {
    const diff = [...a].map((c, i) => (c !== b[i] ? i : -1)).filter((i) => i >= 0);
    if (diff.length === 1) return true;
    return diff.length === 2 && diff[1] === diff[0] + 1 && a[diff[0]] === b[diff[1]] && a[diff[1]] === b[diff[0]];
  }
  const [s, l] = a.length < b.length ? [a, b] : [b, a];
  let i = 0;
  while (i < s.length && s[i] === l[i]) i++;
  return s.slice(i) === l.slice(i + 1);
}

/**
 * «Почти верно»: ввод отличается от допустимого ответа одной буквой в одном слове, и это слово — не проверяемая
 * форма (его нет среди tested). Сами формы нечётко не сравниваются: goed — ошибка.
 */
function almost(input: string, answer: string, tested: Set<string>): boolean {
  const a = words(input).map((w) => w.toLowerCase());
  const b = words(answer).map((w) => w.toLowerCase());
  if (a.length !== b.length) return false;
  const diff = a.map((w, i) => (w !== b[i] ? i : -1)).filter((i) => i >= 0);
  if (diff.length !== 1) return false;
  const [i] = diff;
  return b[i].length >= 3 && !tested.has(b[i]) && oneEdit(a[i], b[i]) && !inflection(a[i], b[i]);
}

const ENDINGS = new Set(['', 's', 'es', 'd', 'ed', 't', 'n', 'en', 'ing', 'r', 'er', 'st', 'est', 'y', 'ly']);

/** Слова различаются только окончанием (build/built, work/works) — это грамматика, а не опечатка. */
function inflection(a: string, b: string): boolean {
  let p = 0;
  while (p < a.length && p < b.length && a[p] === b[p]) p++;
  return ENDINGS.has(a.slice(p)) && ENDINGS.has(b.slice(p));
}

/** Проверяемые слова: то, чего нет в исходном предложении (transform), исправление (find-error), пропуски. */
function testedWords(ex: Exercise, item: Item): Set<string> {
  const lower = (list: string[]) => new Set(list.flatMap((s) => words(s).map((w) => w.toLowerCase())));
  if (ex.kind === 'transform') {
    const source = lower([item.source ?? '']);
    return new Set([...lower(item.answer)].filter((w) => !source.has(w)));
  }
  if (ex.kind === 'find-error') return lower([...(item.fix ?? []), item.error ?? '']);
  if (ex.kind === 'gap') return lower(gapSets(item).flat());
  return new Set();
}

/** Мягкие замечания: ответ засчитан, но написан небрежно. */
function softNotes(ex: Exercise, input: string, answer: string): string[] {
  const notes: string[] = [];
  const raw = tidy(input);
  const ans = tidy(answer);
  if (/(^|[^\w'])i('|\b)(?!\.)/.test(raw) && /(^|[^\w'])I('|\b)/.test(ans)) notes.push('«I» (я) всегда пишется с заглавной буквы.');
  const answerWords = words(ans);
  const inputWords = new Set(words(raw));
  const names = answerWords.filter((w, i) => i > 0 && /^[A-Z][a-z]/.test(w) && !/^I'/.test(w) && inputWords.has(w.toLowerCase()) && !inputWords.has(w));
  if (names.length) notes.push(`Имена и названия пишутся с заглавной: ${[...new Set(names)].join(', ')}.`);
  if ((ex.kind === 'transform' || ex.kind === 'order') && ex.settings.punctuation === 'loose' && /\?$/.test(ans) && !/\?\s*$/.test(raw)) {
    notes.push('Вопрос заканчивается знаком «?».');
  }
  return notes;
}

/** Ищет предусмотренную ошибку: у choice — why[вариант], у остальных — wrong. */
function wrongWhy(ex: Exercise, item: Item, sentence: string, settings: Settings): string | undefined {
  for (const w of item.wrong) {
    const target = ex.kind === 'gap' ? fillGaps(item.text ?? '', w.answer) : w.answer[0];
    if (same(sentence, target, settings)) return w.why;
  }
  return undefined;
}

const isEmpty = (input: Input) => (Array.isArray(input) ? input.some((v) => !v.trim()) || input.length === 0 : !input.trim());

/** Проверка одного пункта. Для match пункт — пара, ввод — выбранная правая часть. */
export function check(ex: Exercise, item: Item, input: Input): Result {
  if (isEmpty(input)) return { status: 'empty', notes: [] };
  const settings = ex.kind === 'order' ? { ...ex.settings, punctuation: 'loose' as const } : ex.settings;

  if (ex.kind === 'choice' || ex.kind === 'match') {
    const value = String(input);
    const ok = item.answer.some((a) => tidy(a) === tidy(value));
    return ok ? { status: 'ok', notes: [], matched: item.answer[0] } : { status: 'wrong', notes: [], why: item.why[value] };
  }

  if (ex.kind === 'gap') {
    const values = Array.isArray(input) ? input : [input];
    const text = item.text ?? '';
    const sentence = fillGaps(text, values);
    const sets = gapSets(item);
    const hit = sets.find((set) => same(sentence, fillGaps(text, set), settings));
    if (hit) {
      return { status: 'ok', gaps: values.map(() => true), notes: softNotes(ex, sentence, fillGaps(text, hit)), matched: hit.join(' … ') };
    }
    // отметки у пропусков — по ближайшему набору: пропуск верен, если с ним (и остальными из набора) предложение сходится
    let best: boolean[] = values.map(() => false);
    for (const set of sets) {
      const marks = values.map((v, i) => same(fillGaps(text, set.map((s, j) => (j === i ? v : s))), fillGaps(text, set), settings));
      if (marks.filter(Boolean).length > best.filter(Boolean).length) best = marks;
    }
    const why = wrongWhy(ex, item, sentence, settings);
    const near = !why && sets.some((set) => almost(sentence, fillGaps(text, set), testedWords(ex, item)));
    return { status: near ? 'almost' : 'wrong', gaps: best, notes: [], why };
  }

  const sentence = String(input);
  const accepted = acceptedSentences(ex, item);
  const hit = accepted.find((a) => same(sentence, a, settings));
  if (hit) return { status: 'ok', notes: softNotes(ex, sentence, hit), matched: hit };
  const why = wrongWhy(ex, item, sentence, settings);
  const near = !why && accepted.some((a) => almost(sentence, a, testedWords(ex, item)));
  return { status: near ? 'almost' : 'wrong', notes: [], why };
}

/** Пункт для подсчёта баллов: у match каждая пара — пункт. */
export const itemCount = (ex: Exercise) => ex.items.length;
