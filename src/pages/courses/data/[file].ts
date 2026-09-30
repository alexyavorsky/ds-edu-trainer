/** Файлы данных курсов (courses/data/*.csv) — отдаются статикой; Python в браузере берёт их отсюда. */
import type { APIRoute } from 'astro';
import { readdirSync, readFileSync } from 'node:fs';
import { join } from 'node:path';
import { DATA_DIR } from '../../../lib/courses/load';

export function getStaticPaths() {
  return readdirSync(DATA_DIR)
    .filter((name) => name.endsWith('.csv'))
    .map((file) => ({ params: { file } }));
}

export const GET: APIRoute = ({ params }) =>
  new Response(readFileSync(join(DATA_DIR, params.file!)), { headers: { 'Content-Type': 'text/csv; charset=utf-8' } });
