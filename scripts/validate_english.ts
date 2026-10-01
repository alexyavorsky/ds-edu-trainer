/**
 * Проверка направления «Английский» (docs/ENGLISH_PLAN.md): справочник грамматики reference/english и курсы
 * без Python (courses/<курс>, runtime = "none"). Без Python и Pyodide — секунды на весь раздел.
 *
 *   node scripts/validate_english.ts                       # справочник и курсы
 *   node scripts/validate_english.ts --reference           # только справочник
 *   node scripts/validate_english.ts --courses [id…]       # только курсы (или выбранные уроки, модули)
 *   node scripts/validate_english.ts --strict              # статьи оглавления и ссылки на ненаписанное — ошибки
 *   node scripts/validate_english.ts --selftest            # таблица случаев нормализации (src/lib/english/check-cases.ts)
 *   node scripts/validate_english.ts --blind-export <папка> [модуль | урок…]   # задания без ключей для решателя
 *   node scripts/validate_english.ts --blind-check <папка>/answers.json [--report путь]   # сверка ответов решателя
 *
 * Правила — в плане, разделы «Что проверяет валидатор» (С4) и «Валидатор» (0.3). Ответы проверяются той же
 * функцией check() из src/lib/english/check.ts, что и на странице урока.
 */
import { existsSync, mkdirSync, readdirSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, join, relative, resolve } from 'node:path';
import { parse as parseToml } from 'smol-toml';
import { parse as parseYaml } from 'yaml';
import { splitFrontmatter } from '../src/lib/courses/format.ts';
import { courseLessons, isPythonCourse, loadCourses, type CourseSource, type LessonSource } from '../src/lib/courses/load.ts';
import { runCases, CASES } from '../src/lib/english/check-cases.ts';
import {
  acceptedSentences,
  canon,
  check,
  CLOSED_WORDS,
  countWords,
  displayAnswers,
  fillGaps,
  gapCount,
  gapSets,
  same,
  tidy,
  type Exercise,
  type Input,
  type Item,
} from '../src/lib/english/check.ts';
import { CEFR_LEVELS, CEFR_TO_LEVEL, cefrRank, isCefr, moduleLevels } from '../src/lib/english/cefr.ts';
import { matchOrder } from '../src/lib/english/shuffle.ts';

const root = resolve('.'); // корень репозитория — как COURSES_DIR в src/lib/courses/load.ts
const REFERENCE = join(root, 'reference');
const read = (path: string) => readFileSync(path, 'utf-8');
const shown = (path: string) => (relative(root, path).startsWith('..') ? path : relative(root, path));
const CYRILLIC = /[А-Яа-яЁё]/;
const END_PUNCT = /[.!?…]["”)]?$/;

// ─── Отчёт ──────────────────────────────────────────────────────────────────

class Report {
  errors: string[] = [];
  warnings: string[] = [];
  readonly strict: boolean;
  constructor(strict: boolean) {
    this.strict = strict;
  }
  error(where: string, message: string): void {
    this.errors.push(`${where}: ${message}`);
  }
  warn(where: string, message: string): void {
    this.warnings.push(`${where}: ${message}`);
  }
  /** Предупреждение, а с --strict — ошибка. */
  soft(where: string, message: string): void {
    if (this.strict) this.error(where, message);
    else this.warn(where, message);
  }
}

function annotate(level: 'error' | 'warning', message: string): void {
  if (process.env.GITHUB_ACTIONS === 'true') console.log(`::${level} title=Английский::${message.replaceAll('\n', '%0A')}`);
}

// ─── Глоссарий: нежелательные варианты ──────────────────────────────────────

/** docs/glossary/english.md, последний раздел; исключения — статьи, где вариант упоминается один раз. */
const DISCOURAGED: { re: RegExp; label: string; allowed?: string[] }[] = [
  { re: /\bFuture Simple\b/, label: 'Future Simple', allowed: ['english/will', 'english/tenses-overview'] },
  { re: /\bFuture Indefinite\b/, label: 'Future Indefinite', allowed: ['english/will', 'english/tenses-overview'] },
  { re: /\bPresent Indefinite\b/, label: 'Present Indefinite', allowed: ['english/tenses-overview'] },
  { re: /\bSimple Present\b/, label: 'Simple Present', allowed: ['english/british-american'] },
  { re: /\bSimple Past\b/, label: 'Simple Past', allowed: ['english/british-american'] },
  { re: /\bPresent Progressive\b/, label: 'Present Progressive', allowed: ['english/present-continuous', 'english/tenses-overview'] },
  { re: /причасти[еяю] II/i, label: 'причастие II' },
  { re: /голы[йм] инфинитив/i, label: 'голый инфинитив' },
  { re: /инговая форма|инговую форму|инговой форм/i, label: 'инговая форма' },
  { re: /перв(ая|ую|ой) форм/i, label: 'первая форма' },
  { re: /\bV1\b/, label: 'V1' },
  { re: /субъект/i, label: 'субъект' },
  { re: /клауз/i, label: 'клауза' },
  { re: /хвостик/i, label: 'хвостик' },
];

function checkStyle(where: string, id: string, text: string, r: Report): void {
  for (const d of DISCOURAGED) {
    if (d.allowed?.includes(id)) continue;
    if (d.re.test(text)) r.error(where, `нежелательный вариант «${d.label}» (docs/glossary/english.md)`);
  }
  if (/[’‘]/.test(text)) r.error(where, 'в английском тексте — прямой апостроф \', а не ’');
}

/** Пары британского и американского написания: в ответе одно — автор должен перечислить и второе. */
const BRE_AME: [string, string][] = [
  ['colour', 'color'],
  ['favourite', 'favorite'],
  ['centre', 'center'],
  ['theatre', 'theater'],
  ['travelled', 'traveled'],
  ['travelling', 'traveling'],
  ['cancelled', 'canceled'],
  ['learnt', 'learned'],
  ['dreamt', 'dreamed'],
  ['spelt', 'spelled'],
  ['burnt', 'burned'],
  ['organise', 'organize'],
  ['organised', 'organized'],
  ['realise', 'realize'],
  ['realised', 'realized'],
  ['grey', 'gray'],
  ['programme', 'program'],
  ['neighbour', 'neighbor'],
];

// ─── Справочник ─────────────────────────────────────────────────────────────

interface Article {
  id: string; // english/past-simple
  slug: string;
  section: string;
  path: string;
  meta: Record<string, unknown>;
  body: string;
}

interface EnglishTopic {
  id: string;
  sections: { title: string; articles: string[] }[];
  articles: Map<string, Article>; // написанные
  planned: Set<string>; // в оглавлении, но файла нет
}

const FRONTMATTER = new Set(['title', 'cefr', 'level', 'summary', 'kind', 'requires', 'related', 'contrasts', 'patterns']);
const SECTION_ORDER = ['Коротко', 'Формулы', 'Когда употребляется', 'Как выбрать', 'Частые ошибки', 'Сравнение', 'Проверьте себя'];
const REQUIRED: Record<string, string[]> = {
  article: ['Коротко', 'Когда употребляется', 'Частые ошибки'],
  contrast: ['Коротко', 'Как выбрать', 'Частые ошибки'],
  overview: ['Коротко'],
};
const FORMULA_SYMBOLS = new Set(['S', 'V', 'V-s', 'V-ing', 'V2', 'V3', 'I']);

function englishTopics(): string[] {
  if (!existsSync(REFERENCE)) return [];
  return readdirSync(REFERENCE).filter((t) => {
    const path = join(REFERENCE, t, 'topic.toml');
    return existsSync(path) && (parseToml(read(path)) as { direction?: string }).direction === 'english';
  });
}

function loadTopic(id: string, r: Report): EnglishTopic {
  const meta = parseToml(read(join(REFERENCE, id, 'topic.toml'))) as Record<string, unknown>;
  const where = `${id}/topic.toml`;
  for (const key of ['title', 'summary', 'direction', 'sections']) if (!(key in meta)) r.error(where, `нет поля ${key}`);
  for (const key of ['package', 'version', 'docs']) if (key in meta) r.error(where, `у темы без Python поля ${key} не нужно`);
  if (meta.beta !== undefined && typeof meta.beta !== 'boolean') r.error(where, 'beta — true или false');
  const sections = (meta.sections as { title: string; articles: string[] }[]) ?? [];
  const topic: EnglishTopic = { id, sections, articles: new Map(), planned: new Set() };
  const seen = new Set<string>();
  for (const s of sections) {
    for (const slug of s.articles ?? []) {
      const aid = `${id}/${slug}`;
      if (seen.has(slug)) r.error(where, `статья ${slug} в оглавлении дважды`);
      seen.add(slug);
      if (!/^[a-z0-9]+(-[a-z0-9]+)*$/.test(slug)) r.error(where, `имя статьи «${slug}» — только a-z, 0-9 и дефисы`);
      if (slug === 'index') r.error(where, 'имя «index» занято страницей темы');
      const path = join(REFERENCE, id, `${slug}.mdx`);
      if (!existsSync(path)) {
        topic.planned.add(aid);
        continue;
      }
      const text = read(path);
      const { frontmatter, body } = splitFrontmatter(text);
      let fm: Record<string, unknown> = {};
      try {
        fm = (parseYaml(frontmatter) as Record<string, unknown>) ?? {};
      } catch (e) {
        r.error(aid, `frontmatter не читается: ${(e as Error).message.split('\n')[0]}`);
      }
      topic.articles.set(aid, { id: aid, slug, section: s.title, path, meta: fm, body });
    }
  }
  for (const file of readdirSync(join(REFERENCE, id))) {
    if (file.endsWith('.mdx') && !seen.has(file.slice(0, -4))) r.error(id, `файл ${file} не указан в оглавлении topic.toml`);
    if (file.endsWith('.py')) r.error(id, `файл ${file}: у грамматики нет примеров кода`);
  }
  return topic;
}

/** Ссылка на статью: написана — ок; в оглавлении, но не написана — предупреждение (--strict: ошибка); иначе — ошибка. */
function checkRef(where: string, ref: string, topics: Map<string, EnglishTopic>, r: Report, what = 'ссылка'): boolean {
  const topic = topics.get(ref.split('/')[0]);
  if (topic?.articles.has(ref)) return true;
  if (topic?.planned.has(ref)) r.soft(where, `${what} на ${ref} — статья ещё не написана`);
  else r.error(where, `${what} на ${ref} — такой статьи нет в оглавлении`);
  return false;
}

interface Block {
  name: string;
  attrs: Record<string, string>;
  lines: string[];
  line: number;
}

/** Блоки компонентов статьи: <Examples>, <Formula>, <Fix …> — каждый с отдельной строки до закрывающего тега. */
function blocks(body: string): Block[] {
  const lines = body.split('\n');
  const out: Block[] = [];
  for (let i = 0; i < lines.length; i++) {
    const m = /^<(Examples|Formula|Fix)((?:\s+\w+="[^"]*")*)\s*>\s*$/.exec(lines[i].trim());
    if (!m) continue;
    const end = lines.findIndex((l, j) => j > i && l.trim() === `</${m[1]}>`);
    const attrs = Object.fromEntries([...m[2].matchAll(/(\w+)="([^"]*)"/g)].map((a) => [a[1], a[2]]));
    out.push({ name: m[1], attrs, lines: end < 0 ? [] : lines.slice(i + 1, end), line: i + 1 });
    if (end > 0) i = end;
  }
  return out;
}

/** Разделы ## и подразделы ### по порядку (вне блоков кода). */
function headings(body: string): { depth: number; text: string; start: number; end: number }[] {
  const lines = body.split('\n');
  const out: { depth: number; text: string; start: number; end: number }[] = [];
  let fence = false;
  lines.forEach((l, i) => {
    if (/^\s*```/.test(l)) fence = !fence;
    const m = !fence && /^(##|###) (.+)$/.exec(l);
    if (m) out.push({ depth: m[1].length, text: m[2].replace(/<Level>.*?<\/Level>/, '').trim(), start: i, end: lines.length });
  });
  for (let i = 0; i < out.length; i++) {
    const next = out.slice(i + 1).find((h) => h.depth <= out[i].depth);
    out[i].end = next ? next.start : lines.length;
  }
  return out;
}

function checkExamples(where: string, block: Block, r: Report): number {
  let n = 0;
  for (const raw of block.lines) {
    const line = raw.trim();
    if (!line) continue;
    if (!line.startsWith('- ')) {
      r.error(where, `<Examples>, строка ${block.line}: каждая строка — «- английский — русский»`);
      continue;
    }
    n++;
    const text = line.slice(2);
    const at = text.indexOf(' — ');
    if (at < 0) {
      r.error(where, `пример без перевода через « — »: ${text}`);
      continue;
    }
    const en = text.slice(0, at).replace(/\s*\((амер|брит)\.\)\s*$/, '');
    const ru = text.slice(at + 3);
    if (!CYRILLIC.test(ru)) r.error(where, `перевод примера не по-русски: ${text}`);
    if (CYRILLIC.test(en)) r.error(where, `в английской части примера кириллица: ${text}`);
    if (!END_PUNCT.test(en.replace(/\*+$/, ''))) r.error(where, `английская часть примера не заканчивается знаком препинания: ${en}`);
    for (const m of en.matchAll(/\*\*(.+?)\*\*/g)) {
      const before = en[m.index - 1] ?? ' ';
      const after = en[m.index + m[0].length] ?? ' ';
      if (/[\w']/.test(before) || /[\w']/.test(after)) r.error(where, `**жирным** — только целые слова: ${en}`);
    }
    if ((en.match(/\*\*/g) ?? []).length % 2) r.error(where, `непарные ** в примере: ${en}`);
  }
  return n;
}

function checkFormula(where: string, block: Block, r: Report): void {
  for (const raw of block.lines) {
    const line = raw.trim();
    if (!line) continue;
    if (/^-\s/.test(line)) r.error(where, `<Formula>: отрицание обозначается «−» (минус), а не «-»: ${line}`);
    if (CYRILLIC.test(line)) r.error(where, `<Formula>: русских слов в формуле нет — пояснения под формулой: ${line}`);
    const body = line.replace(/^[+−?]\s+/, '');
    for (const token of body.split(/[\s+/()…?.,]+/).filter(Boolean)) {
      if (token === 'to' || FORMULA_SYMBOLS.has(token)) continue;
      if (/^(V\d|V-\w+|[A-Z]\d?)$/.test(token)) r.error(where, `<Formula>: обозначение «${token}» не из глоссария (S, V, V-s, V-ing, V2, V3, to V)`);
    }
  }
}

function wordCount(body: string): number {
  return body
    .replace(/<[^>]+>/g, ' ')
    .replace(/[#*|`>-]/g, ' ')
    .split(/\s+/)
    .filter((w) => /[\p{L}\p{N}]/u.test(w)).length;
}

function checkArticle(a: Article, topics: Map<string, EnglishTopic>, r: Report): void {
  const where = a.id;
  const m = a.meta;
  for (const key of Object.keys(m)) if (!FRONTMATTER.has(key)) r.error(where, `неизвестное поле frontmatter «${key}»`);
  for (const key of ['title', 'cefr', 'level', 'summary']) if (!m[key]) r.error(where, `во frontmatter нет поля ${key}`);
  const cefr = String(m.cefr ?? '');
  if (m.cefr && !isCefr(cefr)) r.error(where, `cefr — одно из ${CEFR_LEVELS.join(', ')}`);
  if (isCefr(cefr) && m.level !== CEFR_TO_LEVEL[cefr]) r.error(where, `level: ${m.level}, а для ${cefr} — ${CEFR_TO_LEVEL[cefr]}`);
  const kind = String(m.kind ?? 'article');
  if (!REQUIRED[kind]) r.error(where, 'kind — article, contrast или overview');
  const list = (key: string): string[] => {
    const v = m[key];
    if (v === undefined) return [];
    if (!Array.isArray(v) || !v.every((x) => typeof x === 'string')) {
      r.error(where, `${key} — список строк`);
      return [];
    }
    return v;
  };
  const requires = list('requires');
  const contrasts = list('contrasts');
  if (requires.length > 3) r.error(where, 'requires — не больше 3 статей');
  for (const ref of requires) {
    if (!checkRef(where, ref, topics, r, 'requires')) continue;
    const other = topics.get(ref.split('/')[0])!.articles.get(ref)!;
    if (cefrRank(String(other.meta.cefr)) > cefrRank(cefr)) r.error(where, `requires: ${ref} (${other.meta.cefr}) уровнем выше статьи (${cefr})`);
  }
  for (const ref of list('related')) checkRef(where, ref, topics, r, 'related');
  for (const ref of contrasts) {
    if (!checkRef(where, ref, topics, r, 'contrasts')) continue;
    const other = topics.get(ref.split('/')[0])!.articles.get(ref)!;
    const back = ['requires', 'related', 'contrasts'].flatMap((k) => (Array.isArray(other.meta[k]) ? (other.meta[k] as string[]) : []));
    if (!back.includes(a.id)) r.warn(where, `контраст ${ref} не ссылается обратно на ${a.id} (requires, related или contrasts)`);
  }
  list('patterns');

  // ссылки в тексте
  for (const link of a.body.matchAll(/\]\(\/reference\/([a-z0-9-]+\/[a-z0-9-]+)(#[^)]*)?\)/g)) checkRef(where, link[1], topics, r);

  // разделы
  const heads = headings(a.body);
  const h2 = heads.filter((h) => h.depth === 2);
  const names = h2.map((h) => h.text);
  for (const name of REQUIRED[kind] ?? []) if (!names.includes(name)) r.error(where, `нет раздела «## ${name}»`);
  if (contrasts.length && kind === 'article' && !names.includes('Сравнение')) r.error(where, 'есть contrasts — нужен раздел «## Сравнение»');
  if (kind === 'contrast' && names.includes('Когда употребляется')) r.warn(where, 'у статьи-сравнения вместо «Когда употребляется» — «Как выбрать»');
  const known = names.filter((n) => SECTION_ORDER.includes(n));
  const sorted = [...known].sort((x, y) => SECTION_ORDER.indexOf(x) - SECTION_ORDER.indexOf(y));
  if (known.join() !== sorted.join()) r.error(where, `порядок разделов: ${sorted.join(' → ')}`);
  for (const n of new Set(names)) if (names.filter((x) => x === n).length > 1) r.error(where, `раздел «${n}» дважды`);
  const lines = a.body.split('\n');
  const sectionText = (name: string) => {
    const h = h2.find((x) => x.text === name);
    return h ? lines.slice(h.start + 1, h.end).join('\n') : '';
  };
  const short = sectionText('Коротко');
  const bullets = short.split('\n').filter((l) => /^- /.test(l)).length;
  if (names.includes('Коротко') && (bullets < 2 || bullets > 5)) r.error(where, `«Коротко» — 2–5 пунктов, а их ${bullets}`);
  if (names.includes('Когда употребляется')) {
    const when = h2.find((x) => x.text === 'Когда употребляется')!;
    const subs = heads.filter((x) => x.depth === 3 && x.start > when.start && x.start < when.end);
    if (!subs.length) r.error(where, '«Когда употребляется» — подраздел ### на каждый случай');
    for (const s of subs) {
      if (!lines.slice(s.start + 1, s.end).some((l) => l.trim() === '<Examples>')) r.error(where, `подраздел «${s.text}» без <Examples>`);
    }
  }
  const mistakes = blocks(sectionText('Частые ошибки')).filter((b) => b.name === 'Fix').length;
  if (names.includes('Частые ошибки') && mistakes < 3) r.error(where, `«Частые ошибки» — не меньше 3 <Fix>, а их ${mistakes}`);
  if (names.includes('Сравнение')) {
    const cmp = sectionText('Сравнение');
    if (!/^\|.*\|$/m.test(cmp)) r.error(where, '«Сравнение» — нужна таблица');
    if (!cmp.includes('<Examples>')) r.error(where, '«Сравнение» — нужны пары примеров в <Examples>');
  }

  // компоненты
  let examples = 0;
  for (const b of blocks(a.body)) {
    if (!b.lines.length) r.error(where, `<${b.name}> (строка ${b.line}) без содержимого или без закрывающего тега`);
    if (b.name === 'Examples') examples += checkExamples(where, b, r);
    if (b.name === 'Formula') checkFormula(where, b, r);
    if (b.name === 'Fix') {
      if (!b.attrs.wrong || !b.attrs.right) r.error(where, '<Fix> — нужны wrong="…" и right="…"');
      else if (tidy(b.attrs.wrong) === tidy(b.attrs.right)) r.error(where, `<Fix>: wrong и right совпадают — ${b.attrs.wrong}`);
      if (!b.lines.join('').trim()) r.error(where, `<Fix wrong="${b.attrs.wrong}">: объясните ошибку в теле`);
    }
  }
  const minExamples = kind === 'overview' ? 5 : 8;
  if (examples < minExamples) r.error(where, `примеров с переводом ${examples}, нужно не меньше ${minExamples}`);
  for (const lv of a.body.matchAll(/<Level>([^<]*)<\/Level>/g)) {
    if (!isCefr(lv[1])) r.error(where, `<Level>${lv[1]}</Level> — уровень CEFR`);
    else if (cefrRank(lv[1]) < cefrRank(cefr)) r.error(where, `<Level>${lv[1]}</Level> ниже уровня статьи (${cefr})`);
    else if (lv[1] === cefr) r.warn(where, `<Level>${lv[1]}</Level> совпадает с уровнем статьи — плашка не нужна`);
  }
  for (const tag of a.body.matchAll(/^\s*<([A-Z]\w*)/gm)) {
    if (!['Examples', 'Formula', 'Fix', 'Level'].includes(tag[1])) r.error(where, `неизвестный компонент <${tag[1]}>`);
  }

  // оформление и объём
  checkStyle(where, a.id, a.body, r);
  for (const l of lines) {
    if (/^\s*</.test(l) || /^- /.test(l.trim())) continue;
    if (/["“][^"”\n]*[А-Яа-яЁё][^"”\n]*["”]/.test(l)) r.warn(where, `в русском тексте кавычки — «ёлочки»: ${l.trim().slice(0, 80)}`);
  }
  const words = wordCount(a.body);
  if (kind !== 'overview' && (words < 500 || words > 1200)) r.warn(where, `объём ${words} слов — ориентир 500–1200`);
}

function validateReference(r: Report): Map<string, EnglishTopic> {
  const topics = new Map(englishTopics().map((id) => [id, loadTopic(id, r)]));
  for (const topic of topics.values()) {
    for (const a of topic.articles.values()) checkArticle(a, topics, r);
    if (topic.planned.size) r.soft(topic.id, `не написано статей оглавления: ${topic.planned.size}`);
    const byLevel = new Map<string, number>();
    for (const a of topic.articles.values()) byLevel.set(String(a.meta.cefr), (byLevel.get(String(a.meta.cefr)) ?? 0) + 1);
    console.log(
      `Справочник ${topic.id}: написано ${topic.articles.size} из ${topic.articles.size + topic.planned.size} · ` +
        CEFR_LEVELS.map((l) => `${l}: ${byLevel.get(l) ?? 0}`).join(', '),
    );
    for (const s of topic.sections) {
      const done = s.articles.filter((slug) => topic.articles.has(`${topic.id}/${slug}`)).length;
      if (done) console.log(`  ${s.title}: ${done} из ${s.articles.length}`);
    }
  }
  return topics;
}

// ─── Курсы ──────────────────────────────────────────────────────────────────

const INPUT_KINDS = new Set(['gap', 'order', 'transform', 'find-error']);
const RESERVED_IDS = new Set(['result']);

/** Ответ пункта в виде ввода ученика: для самопроверки ключа и слепой проверки. */
function asInputs(ex: Exercise, item: Item): Input[] {
  switch (ex.kind) {
    case 'gap':
      return gapSets(item);
    case 'find-error':
      return acceptedSentences(ex, item);
    default:
      return item.answer;
  }
}

/** Содержит ли текст ответ целым словом (утечка в task, hint, why). */
function leaks(ex: Exercise, item: Item | null, text: string | undefined): string | null {
  if (!text) return null;
  const plain = text.replace(/[*_`]/g, '').toLowerCase();
  const items = item ? [item] : ex.items;
  for (const it of items) {
    if (ex.kind === 'gap') {
      for (const set of gapSets(it)) {
        const values = set.filter((v) => v.trim() && v !== '—');
        if (values.length && values.every((v) => countWords(plain, v.toLowerCase()) > 0)) return set.join(' … ');
      }
    } else if (ex.kind === 'find-error') {
      for (const f of it.fix ?? []) if (f && countWords(plain, f.toLowerCase()) > 0) return f;
    } else if (ex.kind !== 'match') {
      for (const a of it.answer) {
        const value = tidy(a).replace(/[.!?]+$/, '').toLowerCase();
        if (value && countWords(plain, value) > 0) return a;
      }
    }
  }
  return null;
}

const tokensOf = (s: string) =>
  tidy(s)
    .toLowerCase()
    .replace(/[.,!?;:"]/g, ' ')
    .split(/\s+/)
    .filter(Boolean);

function checkItem(where: string, ex: Exercise, item: Item, r: Report): void {
  const at = `${where}/${item.n}`;
  const s = ex.settings;
  if (ex.kind !== 'match' && !item.explain.trim()) r.error(at, 'нет explain — объяснения, почему верно');
  if (item.explain && !CYRILLIC.test(item.explain)) r.error(at, 'explain — по-русски');
  for (const w of item.wrong) if (!CYRILLIC.test(w.why)) r.error(at, 'why у wrong — по-русски');

  // вид
  if (ex.kind === 'gap') {
    const n = gapCount(item.text ?? '');
    if (!item.text) r.error(at, 'нет text');
    if (n === 0) r.error(at, 'в text нет пропуска ___');
    const sources = [item.answer.length > 0, !!item.gaps, !!item.combos].filter(Boolean).length;
    if (sources !== 1) r.error(at, 'ответ — ровно одно из answer, gaps, combos');
    if (item.answer.length && n !== 1) r.error(at, `answer — для одного пропуска, а их ${n}: используйте gaps или combos`);
    if (item.gaps && item.gaps.length !== n) r.error(at, `пропусков ${n}, а в gaps ${item.gaps.length}`);
    for (const c of item.combos ?? []) if (c.length !== n) r.error(at, `пропусков ${n}, а в наборе combos ${c.length}: ${JSON.stringify(c)}`);
    for (const g of item.gaps ?? []) if (!g.length) r.error(at, 'пустой список в gaps');
    for (const v of gapSets(item).flat()) if (v.includes('—') && v.trim() !== '—') r.error(at, `«—» — только как целый ответ: «${v}»`);
    for (const w of item.wrong) if (w.answer.length !== n) r.error(at, `wrong: пропусков ${n}, а в ответе ${w.answer.length}`);
  } else if (ex.kind === 'choice') {
    const options = item.options ?? [];
    if (!item.text) r.error(at, 'нет text');
    if (options.length < 2) r.error(at, 'options — не меньше двух вариантов (у пункта или у упражнения)');
    if (item.answer.length !== 1) r.error(at, 'answer у choice — одна строка');
    else if (!options.includes(item.answer[0])) r.error(at, `ответ «${item.answer[0]}» не из options`);
    const norm = options.map((o) => canon(o, s));
    if (new Set(norm).size !== norm.length) r.error(at, 'варианты совпадают после нормализации');
    const answer = item.answer[0];
    for (const o of options) {
      if (o === answer) continue;
      const a = gapCount(item.text ?? '') ? fillGaps(item.text ?? '', [answer]) : answer;
      const b = gapCount(item.text ?? '') ? fillGaps(item.text ?? '', [o]) : o;
      if (same(b, a, s)) r.error(at, `неверный вариант «${o}» даёт то же предложение, что и ответ (после нормализации и сокращений)`);
      if (!item.why[o]) r.warn(at, `нет why для неверного варианта «${o}»`);
    }
    for (const k of Object.keys(item.why)) {
      if (!options.includes(k)) r.error(at, `why: «${k}» — не вариант из options`);
      if (k === answer) r.error(at, `why для верного варианта «${k}»`);
      if (!CYRILLIC.test(item.why[k])) r.error(at, `why «${k}» — по-русски`);
    }
  } else if (ex.kind === 'order') {
    const words = item.words ?? [];
    if (words.length < 2) r.error(at, 'words — не меньше двух фишек');
    const bank = words.flatMap(tokensOf).sort().join(' ');
    for (const a of item.answer) {
      if (tokensOf(a).sort().join(' ') !== bank) r.error(at, `слова ответа «${a}» не совпадают с words — каждая фишка ровно один раз, лишних слов нет`);
    }
    if (item.answer.some((a) => canon(a, { ...s, punctuation: 'loose' }) === canon(words.join(' '), { ...s, punctuation: 'loose' }))) {
      r.error(at, 'фишки уже стоят в порядке ответа — перемешайте words');
    }
  } else if (ex.kind === 'transform') {
    if (!item.source) r.error(at, 'нет source');
    for (const a of item.answer) {
      if (item.source && canon(a, s) === canon(item.source, s)) r.error(at, `ответ совпадает с source: «${a}»`);
      if (item.start && !tidy(a).toLowerCase().startsWith(tidy(item.start).toLowerCase())) r.error(at, `ответ «${a}» не начинается со start «${item.start}»`);
      if (item.keyword && !countWords(tidy(a).toLowerCase(), tidy(item.keyword).toLowerCase())) r.error(at, `в ответе «${a}» нет keyword «${item.keyword}»`);
      if (item.maxWords) {
        const rest = item.start ? tidy(a).slice(tidy(item.start).length) : a;
        const n = tokensOf(rest).length;
        if (n > item.maxWords) r.error(at, `дописано ${n} слов, а max_words = ${item.maxWords}: «${a}»`);
      }
    }
  } else if (ex.kind === 'find-error') {
    if (!item.text) r.error(at, 'нет text');
    if (!item.error) {
      if (!ex.allowCorrect) r.error(at, 'нет error (верные предложения — только с allow_correct = true)');
      if (item.fix?.length) r.error(at, 'fix без error');
    } else {
      const n = countWords(item.text ?? '', item.error);
      if (n !== 1) r.error(at, `error «${item.error}» встречается в предложении ${n} раз — нужно ровно один, целыми словами`);
      if (!item.fix?.length) r.error(at, 'нет fix (пустая строка "" — «стереть лишнее слово»)');
      for (const f of item.fix ?? []) if (f === item.error) r.error(at, `fix «${f}» совпадает с error`);
    }
    for (const sentence of acceptedSentences(ex, item)) {
      if (item.error && canon(sentence, s) === canon(item.text ?? '', s)) r.error(at, `исправленное предложение совпадает с исходным: «${sentence}»`);
    }
    for (const a of item.also ?? []) if (canon(a, s) === canon(item.text ?? '', s)) r.error(at, `also совпадает с исходным предложением: «${a}»`);
  }

  // ответы не противоречат друг другу
  const accepted = acceptedSentences(ex, item);
  if (ex.kind !== 'choice' && ex.kind !== 'match') {
    const norm = accepted.map((a) => canon(a, s));
    norm.forEach((x, i) => {
      if (norm.indexOf(x) !== i) r.error(at, `допустимые ответы неразличимы после нормализации: «${accepted[i]}»`);
    });
  }
  if (!accepted.length) r.error(at, 'нет допустимого ответа');
  for (const input of asInputs(ex, item)) {
    const res = check(ex, item, input);
    if (res.status !== 'ok') r.error(at, `ответ «${Array.isArray(input) ? input.join(' … ') : input}» не проходит собственную проверку (${res.status})`);
  }
  for (const w of item.wrong) {
    const input: Input = ex.kind === 'gap' ? w.answer : (w.answer[0] ?? '');
    if (check(ex, item, input).status === 'ok') r.error(at, `wrong «${w.answer.join(' … ')}» засчитывается как верный`);
  }
  if (s.contractions === 'equal') {
    for (const a of accepted) {
      const m = new RegExp(`\\b(${[...CLOSED_WORDS].join('|')})'(s|d)\\b`, 'i').exec(tidy(a));
      if (m) r.error(at, `в ответе неоднозначное «${m[0]}» — напишите полностью (${m[2] === 's' ? 'is / has' : 'would / had'}): краткие формы проверка добавит сама`);
    }
  }

  // оформление
  const sentences = [ex.kind === 'match' ? undefined : item.text, item.source, ...(ex.kind === 'order' || ex.kind === 'transform' ? item.answer : []), ...(item.also ?? [])].filter(
    (x): x is string => !!x,
  );
  for (const x of sentences) {
    if (!END_PUNCT.test(tidy(x))) r.error(at, `предложение не заканчивается знаком препинания: «${x}»`);
    if (/[’‘]/.test(x)) r.error(at, `прямой апостроф ' вместо ’: «${x}»`);
  }
  const answerWords = new Set(accepted.flatMap(tokensOf));
  for (const [bre, ame] of BRE_AME) {
    if (answerWords.has(bre) !== answerWords.has(ame)) r.warn(at, `в ответах есть «${answerWords.has(bre) ? bre : ame}», но нет «${answerWords.has(bre) ? ame : bre}» — перечислите оба написания`);
  }

  // утечки
  const hintLeak = leaks(ex, item, item.hint);
  if (hintLeak) r.error(at, `hint содержит ответ «${hintLeak}»`);
  if (INPUT_KINDS.has(ex.kind)) {
    for (const w of item.wrong) {
      const leak = leaks(ex, item, w.why);
      if (leak) r.error(at, `why у wrong содержит ответ «${leak}»`);
    }
  }
}

function checkExercise(where: string, ex: Exercise, r: Report): void {
  const at = `${where}/${ex.id}`;
  if (RESERVED_IDS.has(ex.id)) r.error(at, `id «${ex.id}» зарезервирован (баллы контрольной хранятся под ним)`);
  if (!ex.task.trim() || !CYRILLIC.test(ex.task)) r.error(at, 'task — задание по-русски');
  if (!ex.ref.length) r.error(at, 'ref — хотя бы одна статья справочника');
  const leak = leaks(ex, null, ex.task) ?? leaks(ex, null, ex.hint);
  if (leak) r.error(at, `task или hint содержит ответ «${leak}»`);
  if (ex.kind === 'match') {
    if (!ex.explain?.trim()) r.error(at, 'у match explain — у упражнения');
    const lefts = ex.items.map((i) => canon(i.text ?? ''));
    const rights = ex.items.map((i) => canon(i.answer[0] ?? ''));
    if (new Set(lefts).size !== lefts.length) r.error(at, 'левые части повторяются');
    if (new Set(rights).size !== rights.length) r.error(at, 'правые части повторяются');
    if (ex.items.length < 3 || ex.items.length > 6) r.error(at, `пар ${ex.items.length}, нужно 3–6`);
    for (const i of ex.items) {
      if (/[’‘]/.test(`${i.text}${i.answer[0]}`)) r.error(at, 'прямой апостроф \' вместо ’');
    }
  } else if (ex.items.length < 3 || ex.items.length > 10) {
    r.error(at, `пунктов ${ex.items.length}, нужно 3–10`);
  }
  for (const item of ex.items) checkItem(at, ex, item, r);
}

interface Usage {
  introduced: string; // урок
  module: number;
  used: { lesson: string; module: number }[];
}

function validateCourses(selected: string[], topics: Map<string, EnglishTopic>, r: Report): void {
  const courses = loadCourses().filter((c) => !isPythonCourse(c));
  for (const course of courses) {
    const c = course.meta;
    const where = `${course.slug}/course.toml`;
    for (const key of ['title', 'code', 'summary', 'audience', 'reference', 'direction'] as const) if (!c[key]) r.error(where, `нет поля ${key}`);
    if (c.direction !== 'english') r.warn(where, 'курс без Python вне направления english — проверьте direction');
    if (c.package) r.error(where, 'у курса с runtime = "none" нет package');
    if (!c.prerequisites?.length) r.error(where, 'пустой prerequisites');
    if (c.reference && !topics.has(c.reference)) r.error(where, `reference = "${c.reference}" — нет такой темы грамматики`);
    const strict = r.strict || c.complete === true;
    const counts = (where: string, message: string) => (strict ? r.error(where, message) : r.warn(where, message));

    const introduced = new Set<string>();
    const usage = new Map<string, Usage>();
    const kinds = new Map<string, number>();
    let itemsTotal = 0;
    for (const module of course.modules) {
      const mwhere = `${course.slug}/${module.slug}`;
      if (!module.meta.title || !module.meta.summary) r.error(mwhere, 'module.toml: нужны title и summary');
      const levels = moduleLevels(module.meta.level);
      if (!levels.length) r.error(mwhere, 'module.toml: level — «A1–A2», «B1», «B2»');
      for (const lesson of module.lessons) {
        const at = lesson.meta.id || `${mwhere}/${lesson.slug}`;
        for (const p of lesson.problems) r.error(at, p);
        if (!lesson.meta.id.startsWith(`${c.code}-`)) r.error(at, `id урока начинается с «${c.code}-»`);
        if (lesson.meta.kind === 'project') r.error(at, 'kind: project — только у курсов Python; у английского lesson, review, test, placement');
        if (existsSync(join(lesson.dir, 'lesson.py'))) r.error(at, 'lesson.py у курса без Python не нужен');
        if (!existsSync(join(lesson.dir, 'exercises.toml'))) r.error(at, 'нет exercises.toml');
        const raw = read(join(lesson.dir, 'lesson.mdx'));
        for (const key of ['introduces', 'data', 'packages']) if (new RegExp(`^${key}:`, 'm').test(splitFrontmatter(raw).frontmatter)) r.error(at, `поле ${key} — только у уроков Python`);
        for (const ref of lesson.meta.reference) {
          if (checkRef(at, ref, topics, r, 'reference')) introduced.add(ref);
          if (!usage.has(ref)) usage.set(ref, { introduced: lesson.meta.id, module: module.number, used: [] });
        }
        checkStyle(at, '', raw, r);

        const exs = lesson.exercises;
        const kind = lesson.meta.kind;
        const items = exs.reduce((n, e) => n + e.items.length, 0);
        itemsTotal += items;
        if (kind === 'lesson' && (exs.length < 4 || exs.length > 6)) counts(at, `упражнений ${exs.length}, в уроке — 4–6`);
        if (kind === 'review' && (exs.length < 5 || exs.length > 8)) counts(at, `упражнений ${exs.length}, в повторении — 5–8`);
        if (kind === 'test' && items !== 40) counts(at, `пунктов ${items}, в контрольной — ровно 40`);
        if (kind === 'placement' && items !== 30) counts(at, `пунктов ${items}, во входной проверке — 30`);
        if (kind === 'lesson' && new Set(exs.map((e) => e.kind)).size < 3) counts(at, 'в уроке — не меньше трёх видов упражнений');
        const ids = exs.map((e) => e.id);
        ids.forEach((id, i) => ids.indexOf(id) !== i && r.error(at, `упражнение ${id} дважды`));
        for (const ex of exs) {
          kinds.set(ex.kind, (kinds.get(ex.kind) ?? 0) + 1);
          checkExercise(at, ex, r);
          const refs = new Set([...ex.ref, ...ex.items.flatMap((i) => i.ref)]);
          for (const ref of refs) {
            if (!introduced.has(ref)) {
              if (topics.get(ref.split('/')[0])?.articles.has(ref) || topics.get(ref.split('/')[0])?.planned.has(ref)) {
                r.error(`${at}/${ex.id}`, `ref ${ref} не введён этим уроком или раньше (поле reference уроков)`);
              } else checkRef(`${at}/${ex.id}`, ref, topics, r, 'ref');
            }
            const u = usage.get(ref);
            if (u && u.introduced !== lesson.meta.id && !u.used.some((x) => x.lesson === lesson.meta.id)) u.used.push({ lesson: lesson.meta.id, module: module.number });
          }
          if (kind === 'review' || kind === 'test' || kind === 'placement') {
            for (const item of ex.items) if (!item.ref.length && ex.kind !== 'match') r.error(`${at}/${ex.id}/${item.n}`, 'в повторении и контрольной у каждого пункта — ref');
          }
          if (kind === 'test') {
            const max = Math.max(...levels.map(cefrRank));
            for (const ref of refs) {
              const article = topics.get(ref.split('/')[0])?.articles.get(ref);
              if (article && cefrRank(String(article.meta.cefr)) > max) r.error(`${at}/${ex.id}`, `${ref} (${article.meta.cefr}) выше уровня модуля (${module.meta.level})`);
            }
          }
        }
        const blocks = lesson.blocks.filter((b) => b.type === 'practice').length;
        if (!blocks && exs.length) r.error(at, 'в lesson.mdx нет <Practice id="…" />');
        if (!selected.length || selected.includes(at) || selected.includes(module.slug) || selected.includes(course.slug)) {
          console.log(`${r.errors.some((e) => e.startsWith(at)) ? '✗' : '✓'} ${at} (${kind}): упражнений ${exs.length}, пунктов ${items} — ${exs.map((e) => e.kind).join(', ')}`);
        }
      }
    }
    console.log(`Курс ${course.slug}: пунктов ${itemsTotal}; упражнения по видам — ${[...kinds].map(([k, n]) => `${k} ${n}`).join(', ') || '—'}`);
    for (const [ref, u] of usage) {
      console.log(`  ${ref}: введена в ${u.introduced}; повторяется — ${u.used.map((x) => x.lesson).join(', ') || 'нигде'}`);
      const later = course.modules.filter((m) => m.number > u.module).slice(0, 2);
      if (later.length && !u.used.some((x) => later.some((m) => m.number === x.module))) r.warn(ref, `тема не повторяется в следующих двух модулях (${later.map((m) => m.slug).join(', ')})`);
    }
  }
}

// ─── Слепое решение ─────────────────────────────────────────────────────────

const itemKey = (lesson: string, ex: string, n: number) => `${lesson}/${ex}/${n}`;
const letter = (i: number) => String.fromCharCode(1040 + (i >= 9 ? i + 1 : i));

function englishLessons(selected: string[]): { course: CourseSource; lesson: LessonSource }[] {
  return loadCourses()
    .filter((c) => !isPythonCourse(c))
    .flatMap((course) =>
      courseLessons(course)
        .filter((l) => !selected.length || selected.includes(l.meta.id) || selected.includes(l.module) || selected.includes(course.slug))
        .map((lesson) => ({ course, lesson })),
    );
}

function blindExport(dir: string, selected: string[]): void {
  mkdirSync(dir, { recursive: true });
  const template: Record<string, { answer: null; also: string[]; note: string }> = {};
  const chosen = englishLessons(selected);
  for (const { lesson } of chosen) {
    const out: string[] = [`# ${lesson.meta.id}`, '', 'Ответы — в answers.json по id пункта. Для пропусков — список по пропускам (["did", "go"]); если ничего не нужно — "—".', ''];
    for (const ex of lesson.exercises) {
      out.push(`## ${ex.id} — ${ex.kind}`, '', ex.task, '');
      if (ex.kind === 'transform') out.push('Ответ — предложение целиком.', '');
      if (ex.kind === 'find-error') out.push(`Ответ — исправленное предложение целиком${ex.allowCorrect ? '; если ошибки нет — исходное предложение без изменений' : ''}.`, '');
      if (ex.kind === 'match') {
        const rights = matchOrder(ex);
        out.push('Концы:', ...rights.map((x, i) => `- ${letter(i)}. ${x}`), '', 'Ответ — буква или текст конца.', '');
        for (const item of ex.items) {
          const id = itemKey(lesson.meta.id, ex.id, item.n);
          out.push(`- \`${id}\` ${item.text}`);
          template[id] = { answer: null, also: [], note: '' };
        }
        out.push('');
        continue;
      }
      for (const item of ex.items) {
        const id = itemKey(lesson.meta.id, ex.id, item.n);
        template[id] = { answer: null, also: [], note: '' };
        out.push(`- \`${id}\``);
        if (item.text) out.push(`  - text: ${item.text}`);
        if (item.options) out.push(`  - options: ${item.options.join(' | ')}`);
        if (item.words) out.push(`  - words: ${item.words.join(' | ')}`);
        if (item.source) out.push(`  - source: ${item.source}`);
        if (item.start) out.push(`  - start: ${item.start}`);
        if (item.keyword) out.push(`  - keyword: ${item.keyword}`);
        if (item.maxWords) out.push(`  - max_words: ${item.maxWords}`);
      }
      out.push('');
    }
    writeFileSync(join(dir, `${lesson.meta.id}.md`), `${out.join('\n')}\n`);
  }
  writeFileSync(join(dir, 'answers.json'), `${JSON.stringify(template, null, 2)}\n`);
  console.log(`Выгружено уроков: ${chosen.length}, пунктов: ${Object.keys(template).length} → ${shown(dir)}`);
}

function blindCheck(path: string, reportPath: string): number {
  const answers = JSON.parse(read(path)) as Record<string, { answer: Input | null; also?: Input[]; note?: string }>;
  const index = new Map<string, { ex: Exercise; item: Item }>();
  for (const { lesson } of englishLessons([])) for (const ex of lesson.exercises) for (const item of ex.items) index.set(itemKey(lesson.meta.id, ex.id, item.n), { ex, item });
  const matched: string[] = [];
  const missed: string[] = [];
  const rejected: string[] = [];
  const notes: string[] = [];
  let unknown = 0;
  const show = (v: Input | null) => (v === null ? '—' : Array.isArray(v) ? v.join(' … ') : v);
  for (const [id, a] of Object.entries(answers)) {
    const found = index.get(id);
    if (!found) {
      unknown++;
      continue;
    }
    const { ex, item } = found;
    const normalize = (v: Input | null): Input => {
      if (v === null) return '';
      if (ex.kind === 'match' && typeof v === 'string') {
        const rights = matchOrder(ex);
        const i = [...rights.keys()].find((k) => letter(k).toLowerCase() === v.trim().replace(/\.$/, '').toLowerCase());
        return i === undefined ? v : rights[i];
      }
      if (ex.kind === 'gap' && typeof v === 'string') return [v];
      return v;
    };
    const res = check(ex, item, normalize(a.answer));
    const key = displayAnswers(ex, item)[0];
    if (res.status === 'ok') matched.push(id);
    else missed.push(`| \`${id}\` | ${show(a.answer)} | ${key} | ${item.explain || ex.explain || ''} |`);
    for (const alt of a.also ?? []) {
      if (check(ex, item, normalize(alt)).status !== 'ok') rejected.push(`| \`${id}\` | ${show(alt)} | ${key} |`);
    }
    if (a.note?.trim()) notes.push(`- \`${id}\`: ${a.note.trim()}`);
  }
  const total = matched.length + missed.length;
  const percent = total ? Math.round((matched.length / total) * 1000) / 10 : 0;
  const lines = [
    `## Слепая проверка ${new Date().toISOString().slice(0, 10)} — ${shown(path)}`,
    '',
    `Совпало ${matched.length} из ${total} (${percent} %)${unknown ? `; неизвестных id: ${unknown}` : ''}. Порог — 97 %.`,
    '',
    '### Не засчитано',
    '',
    ...(missed.length ? ['| Пункт | Ответ решателя | Ключ | Объяснение |', '| --- | --- | --- | --- |', ...missed] : ['—']),
    '',
    '### Отвергнутые «also» — кандидаты в допустимые ответы',
    '',
    ...(rejected.length ? ['| Пункт | Вариант решателя | Ключ |', '| --- | --- | --- |', ...rejected] : ['—']),
    '',
    '### Заметки решателя',
    '',
    ...(notes.length ? notes : ['—']),
    '',
    '### Решения автора',
    '',
    'По каждому расхождению: ключ неверен / добавить допустимый ответ / уточнить задание / ошибка решателя.',
    '',
  ];
  mkdirSync(dirname(reportPath), { recursive: true });
  const prev = existsSync(reportPath) ? read(reportPath) : '# Слепое решение курса английского\n\nОтчёты `node scripts/validate_english.ts --blind-check` (docs/ENGLISH_PLAN.md, «Слепое решение»).\n\n';
  writeFileSync(reportPath, `${prev.trimEnd()}\n\n${lines.join('\n')}`);
  console.log(lines.slice(0, 3).join('\n'));
  console.log(`Не засчитано: ${missed.length}, отвергнутых also: ${rejected.length}, заметок: ${notes.length} → ${shown(reportPath)}`);
  return percent >= 97 ? 0 : 1;
}

// ─── Запуск ─────────────────────────────────────────────────────────────────

function selftest(): number {
  const failures = runCases();
  console.log(`Нормализация (check.ts): случаев ${CASES.length}, расхождений ${failures.length}`);
  for (const f of failures) {
    console.log(`  ✗ ${f}`);
    annotate('error', f);
  }
  if (CASES.length < 100) {
    console.log('  ✗ случаев меньше 100 — дополните src/lib/english/check-cases.ts');
    return 1;
  }
  return failures.length ? 1 : 0;
}

function main(argv: string[]): number {
  const flag = (name: string) => argv.includes(name);
  const value = (name: string) => (argv.includes(name) ? argv[argv.indexOf(name) + 1] : undefined);
  const valued = new Set(['--blind-export', '--blind-check', '--report']);
  const selected = argv.filter((a, i) => !a.startsWith('--') && !valued.has(argv[i - 1]));

  const exportDir = value('--blind-export');
  if (exportDir) {
    blindExport(exportDir, selected);
    return 0;
  }
  const answers = value('--blind-check');
  if (answers) return blindCheck(answers, value('--report') ?? join(root, 'docs', 'reports', 'course-english-blind.md'));

  if (flag('--selftest') && !flag('--reference') && !flag('--courses')) return selftest();
  const r = new Report(flag('--strict'));
  const started = performance.now();
  const self = selftest();
  const both = !flag('--reference') && !flag('--courses');
  const topics = flag('--reference') || both ? validateReference(r) : new Map(englishTopics().map((id) => [id, loadTopic(id, new Report(false))]));
  if (flag('--courses') || both) validateCourses(selected, topics, r);

  for (const w of r.warnings) {
    console.log(`  · ${w}`);
    annotate('warning', w);
  }
  for (const e of r.errors) {
    console.log(`  ✗ ${e}`);
    annotate('error', e);
  }
  const seconds = ((performance.now() - started) / 1000).toFixed(1);
  const failed = r.errors.length > 0 || self !== 0;
  console.log(`\n${failed ? '✗' : '✓'} Ошибок: ${r.errors.length}, предупреждений: ${r.warnings.length} (${seconds} с)`);
  return failed ? 1 : 0;
}

process.exitCode = main(process.argv.slice(2));
