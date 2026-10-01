/** Содержимое выпадающих меню шапки: разделы каждого вида (задачи, курсы, справочник), сгруппированные по направлениям. */
import { getBooks } from './content';
import { getCourses } from './courses/site';
import { groupByDirection, type DirectionGroup } from './directions';
import { getTopics } from './reference-content';

export interface NavItem {
  title: string;
  href: string;
  beta: boolean;
}

export interface NavMenus {
  tasks: DirectionGroup<NavItem>[];
  courses: DirectionGroup<NavItem>[];
  reference: DirectionGroup<NavItem>[];
}

let cache: NavMenus | null = null;

export async function getNavMenus(): Promise<NavMenus> {
  if (cache && import.meta.env.PROD) return cache;
  const books = (await getBooks()).map((b) => ({ title: b.data.title, href: `/${b.id}`, beta: b.data.beta, direction: b.data.direction }));
  const courses = getCourses().map((c) => ({ title: c.meta.title, href: `/courses/${c.slug}`, beta: !!c.meta.beta, direction: c.meta.direction }));
  const topics = (await getTopics()).map((t) => ({ title: t.data.title, href: `/reference/${t.id}`, beta: t.data.beta, direction: t.data.direction }));
  cache = {
    tasks: groupByDirection(books, (b) => b.direction),
    courses: groupByDirection(courses, (c) => c.direction),
    reference: groupByDirection(topics, (t) => t.direction),
  };
  return cache;
}
