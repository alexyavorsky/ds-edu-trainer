/** «Скачать как .ipynb»: урок как Jupyter-ноутбук (src/lib/courses/notebook.ts), собирается при сборке сайта. */
import type { APIRoute } from 'astro';
import { resolve } from 'node:path';
import { courseLessons } from '../../../lib/courses/load';
import { buildNotebook } from '../../../lib/courses/notebook';
import { getCourses } from '../../../lib/courses/site';

export function getStaticPaths() {
  return getCourses().flatMap((course) => courseLessons(course).map((lesson) => ({ params: { course: course.slug, lesson: lesson.slug }, props: { course, lesson } })));
}

/** Адрес сайта для ссылок из ноутбука: на Vercel — production-домен проекта. */
const site = process.env.VERCEL_PROJECT_PRODUCTION_URL ? `https://${process.env.VERCEL_PROJECT_PRODUCTION_URL}` : null;

export const GET: APIRoute = ({ props }) => {
  const notebook = buildNotebook(props.course, props.lesson, { root: resolve('.'), siteUrl: site });
  return new Response(`${JSON.stringify(notebook, null, 1)}\n`, { headers: { 'Content-Type': 'application/x-ipynb+json' } });
};
