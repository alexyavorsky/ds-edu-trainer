/** Индекс поиска по справочнику: /reference/search.json, загружается при первом открытии поиска. */
import type { APIRoute } from 'astro';
import { getCollection } from 'astro:content';
import { getToc, getTopics, readingOrder } from '../../lib/reference-content';
import { buildSearchIndex } from '../../lib/search-index';

export const GET: APIRoute = async () => {
  const topics = await getTopics();
  const ordered = (await Promise.all(topics.map(async (t) => readingOrder(await getToc(t))))).flat();
  const titles = new Map(topics.map((t) => [t.id, t.data.title]));
  const all = await getCollection('reference');
  const docs = buildSearchIndex(ordered.length ? ordered : all, (id) => titles.get(id) ?? id);
  return new Response(JSON.stringify(docs), { headers: { 'Content-Type': 'application/json; charset=utf-8' } });
};
