/** Выборки для страниц справочника. */
import { getCollection, type CollectionEntry } from 'astro:content';

export type Topic = CollectionEntry<'topics'>;
export type Article = CollectionEntry<'reference'>;

export interface TocEntry {
  id: string; // «numpy/broadcasting»
  slug: string;
  article?: Article; // нет — статья запланирована, но не написана
}

export interface TocSection {
  title: string;
  entries: TocEntry[];
}

export async function getTopics(): Promise<Topic[]> {
  return (await getCollection('topics')).sort((a, b) => a.data.order - b.data.order);
}

export async function getToc(topic: Topic): Promise<TocSection[]> {
  const articles = new Map((await getCollection('reference', (a) => a.id.startsWith(`${topic.id}/`))).map((a) => [a.id, a]));
  return topic.data.sections.map((section) => ({
    title: section.title,
    entries: section.articles.map((slug) => {
      const id = `${topic.id}/${slug}`;
      return { id, slug, article: articles.get(id) };
    }),
  }));
}

/** Статьи темы в порядке изучения (только написанные). */
export function readingOrder(toc: TocSection[]): Article[] {
  return toc.flatMap((s) => s.entries.flatMap((e) => (e.article ? [e.article] : [])));
}

/** Подпись версии темы: «2.5.3» у темы с пакетом, «Python 3.10+» у темы на стандартной библиотеке. */
export function topicVersion(topic: Topic): string {
  return topic.data.package ? (topic.data.version ?? '') : `Python ${topic.data.python}+`;
}

/** «NumPy 2.5.3» или «Python 3.10+» — для шапки статьи и страницы темы. */
export function topicVersionLabel(topic: Topic): string {
  return topic.data.package ? `${topic.data.title} ${topic.data.version}` : `Python ${topic.data.python}+`;
}
