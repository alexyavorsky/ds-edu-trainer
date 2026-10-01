/**
 * Индекс поиска по справочнику: строится при сборке, на клиенте ищется по началу слов.
 * Текст статьи хранится как набор уникальных основ слов (см. stem.ts) — для поиска по префиксу этого достаточно,
 * а индекс в разы меньше. Заголовок, summary и функции хранятся как есть: они нужны для показа результатов.
 */
import type { Article } from './reference-content';
import { articleUrl, type Level } from './reference';
import { stem } from './stem';

export interface SearchDoc {
  u: string; // адрес
  t: string; // заголовок
  s: string; // «зачем это нужно»
  p: string; // тема: NumPy / pandas / Английская грамматика
  l: Level;
  c?: string; // уровень CEFR (грамматика английского) — показывается вместо общего уровня
  f: string; // функции через пробел; у грамматики — формы и слова из patterns
  h: string; // разделы, заголовки примеров и подводных камней — уникальные основы слов
  w: string; // остальной текст — уникальные основы слов
}

export const normalize = (text: string) => text.toLowerCase().replaceAll('ё', 'е');
const WORD_RE = /[\p{L}\p{N}_]+/gu;
export const words = (text: string) => normalize(text).match(WORD_RE) ?? [];
/** Слова текста, приведённые к основам: так их сравнивает поиск. */
export const terms = (text: string) => words(text).map(stem);

function uniqueTerms(parts: string[], exclude: Set<string> = new Set()): string {
  const seen = new Set<string>();
  for (const w of parts.flatMap(terms)) if (w.length > 1 && !exclude.has(w)) seen.add(w);
  return [...seen].join(' ');
}

/** Разбирает MDX статьи на «заголовочный» и обычный текст без разметки и JSX. */
function splitBody(body: string): { heads: string[]; text: string[] } {
  const heads: string[] = [];
  const text: string[] = [];
  for (const m of body.matchAll(/^#{2,3} (.+)$/gm)) heads.push(m[1]);
  for (const m of body.matchAll(/\btitle="([^"]+)"/g)) heads.push(m[1]);
  for (const m of body.matchAll(/\b(?:was|now)="([^"]+)"/g)) text.push(m[1]);
  for (const m of body.matchAll(/\['([^']+)',\s*'([^']*)'/g)) text.push(m[1], m[2]); // строки Params
  const prose = body
    .replace(/<Syntax[\s\S]*?\/>/g, ' ')
    .replace(/<Params[\s\S]*?\/>/g, ' ')
    .replace(/<[^>]+>/g, ' ')
    .replace(/^#{1,6} .*$/gm, ' ')
    .replace(/\]\([^)]*\)/g, ']')
    .replace(/[*_`|>#[\]-]/g, ' ');
  text.push(prose);
  return { heads, text };
}

export function buildSearchIndex(articles: Article[], topicTitle: (id: string) => string): SearchDoc[] {
  return articles.map((a) => {
    const { heads, text } = splitBody(a.body ?? '');
    const h = uniqueTerms(heads);
    return {
      u: articleUrl(a.id),
      t: a.data.title,
      s: a.data.summary,
      p: topicTitle(a.id.split('/')[0]),
      l: a.data.level,
      ...(a.data.cefr ? { c: a.data.cefr } : {}),
      f: [...a.data.functions, ...a.data.patterns].join(' '),
      h,
      w: uniqueTerms([...text, a.data.summary], new Set([...h.split(' '), ...terms(a.data.title)])),
    };
  });
}
