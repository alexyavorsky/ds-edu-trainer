/** Выборки из коллекций, общие для страниц. */
import { getCollection, type CollectionEntry } from 'astro:content';

export type Book = CollectionEntry<'books'>;
export type Chapter = CollectionEntry<'chapters'>;
export type Challenge = CollectionEntry<'challenges'>;

const DIFFICULTY_ORDER = { easy: 0, medium: 1, hard: 2 } as const;

export function sortChallenges(list: Challenge[]): Challenge[] {
  return [...list].sort(
    (a, b) =>
      (a.data.order ?? 1e9) - (b.data.order ?? 1e9) ||
      DIFFICULTY_ORDER[a.data.difficulty] - DIFFICULTY_ORDER[b.data.difficulty] ||
      a.data.title.localeCompare(b.data.title, 'ru'),
  );
}

export async function getBooks(): Promise<Book[]> {
  return (await getCollection('books')).sort((a, b) => a.data.order - b.data.order || a.data.title.localeCompare(b.data.title, 'ru'));
}

export async function getChapters(book: string): Promise<Chapter[]> {
  return (await getCollection('chapters', (c) => c.data.book === book)).sort((a, b) => a.data.slug.localeCompare(b.data.slug));
}

export async function getChallenges(book: string, chapter?: string): Promise<Challenge[]> {
  const list = await getCollection(
    'challenges',
    (c) => c.data.book === book && (chapter === undefined || c.data.chapter === chapter),
  );
  return sortChallenges(list);
}

export function challengeUrl(c: Challenge): string {
  return `/tasks/${c.data.book}/${c.data.chapter}/${c.data.slug}`;
}

export function chapterUrl(c: Chapter): string {
  return `/tasks/${c.data.book}/${c.data.slug}`;
}

/** «Глава 3» у книги, «Раздел 3» у темы: главы темы повторяют разделы справочника. */
export function chapterLabel(c: Chapter, kind: 'book' | 'topic' = 'book'): string {
  return `${kind === 'topic' ? 'Раздел' : 'Глава'} ${c.data.number}`;
}
