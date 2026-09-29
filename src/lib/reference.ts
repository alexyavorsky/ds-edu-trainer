/**
 * Справочник: оглавления тем и файлы примеров reference/<тема>/<статья>.py.
 * Формат файла примеров описан в scripts/validate_reference.py; разбор здесь повторяет Python-версию.
 */
import { existsSync, readdirSync, readFileSync } from 'node:fs';
import { join } from 'node:path';
import { REFERENCE_DIR } from './challenges';

/** Графики примеров: public/reference/plots/<тема>/<статья>/<id>.svg — их пишет validate_reference.py. */
const PLOTS_DIR = join(process.cwd(), 'public', 'reference', 'plots');

export type Level = 'basic' | 'medium' | 'advanced';
export const LEVEL_LABEL: Record<Level, string> = { basic: 'базовый', medium: 'средний', advanced: 'продвинутый' };
export const LEVEL_TONE = { basic: 'easy', medium: 'medium', advanced: 'hard' } as const;

export interface ExampleCell {
  id: string;
  flags: Record<string, string>;
  code: string;
  output: string | null;
}

const OUTPUT_MARK = '# ─── вывод ───';
const CELL_RE = /^# %% ([a-z0-9]+(?:-[a-z0-9]+)*)(?: \[([^\]]*)\])?$/;

export function parseExamples(text: string): Map<string, ExampleCell> {
  const cells = new Map<string, ExampleCell>();
  let current: { id: string; flags: Record<string, string>; code: string[]; out: string[] | null } | null = null;
  const trimEnd = (lines: string[]) => {
    while (lines.length && !lines[lines.length - 1].trim()) lines.pop();
    return lines;
  };
  const finish = () => {
    if (!current) return;
    const out = current.out && trimEnd(current.out).map((l) => (l.startsWith('# ') ? l.slice(2) : ''));
    cells.set(current.id, { id: current.id, flags: current.flags, code: trimEnd(current.code).join('\n'), output: out ? out.join('\n') : null });
  };
  for (const line of text.split(/\r?\n/)) {
    const m = CELL_RE.exec(line);
    if (m) {
      finish();
      const flags: Record<string, string> = {};
      for (const part of (m[2] ?? '').split(',').map((p) => p.trim()).filter(Boolean)) {
        const [key, value = ''] = part.split('=');
        flags[key.trim()] = value.trim();
      }
      current = { id: m[1], flags, code: [], out: null };
    } else if (!current) {
      continue;
    } else if (line === OUTPUT_MARK) {
      current.out = [];
    } else if (current.out) {
      current.out.push(line);
    } else {
      current.code.push(line);
    }
  }
  finish();
  return cells;
}

const cache = new Map<string, Map<string, ExampleCell>>();

/** Примеры статьи по её id («numpy/broadcasting»). В режиме разработки файл читается заново. */
export function getExamples(articleId: string): Map<string, ExampleCell> {
  const cached = import.meta.env.PROD ? cache.get(articleId) : undefined;
  if (cached) return cached;
  const path = join(REFERENCE_DIR, `${articleId}.py`);
  const cells = existsSync(path) ? parseExamples(readFileSync(path, 'utf-8')) : new Map<string, ExampleCell>();
  cache.set(articleId, cells);
  return cells;
}

export interface Plot {
  src: string;
  width: number;
  height: number;
}

/** SVG-графики примера по порядку фигур: «<id>.svg», «<id>-2.svg»… */
export function getPlots(articleId: string, cellId: string): Plot[] {
  const dir = join(PLOTS_DIR, articleId);
  if (!existsSync(dir)) return [];
  const order = (name: string) => Number(name.slice(cellId.length + 1, -4) || 1);
  return readdirSync(dir)
    .filter((name) => name === `${cellId}.svg` || new RegExp(`^${cellId}-\\d+\\.svg$`).test(name))
    .sort((a, b) => order(a) - order(b))
    .map((name) => {
      const head = readFileSync(join(dir, name), 'utf-8').slice(0, 1000);
      const size = (attr: string) => Math.round(Number(new RegExp(`${attr}="([\\d.]+)pt"`).exec(head)?.[1] ?? 0) * (4 / 3)); // pt → px
      return { src: `/reference/plots/${articleId}/${name}`, width: size('width'), height: size('height') };
    });
}

/** «замер на Apple M3 Pro · macOS · Python 3.14, 29.09.2026» — подпись к выводу примера [timing]. */
export function timingNote(flags: Record<string, string>): string | null {
  if (!('timing' in flags)) return null;
  const [y, m, d] = flags.timing.split('-');
  return `замер на ${flags.machine ?? 'неизвестной машине'}${y ? `, ${d}.${m}.${y}` : ''}`;
}

/** Самодостаточный код для копирования (и будущей кнопки «Запустить»): импорты + общие данные + пример. */
export function runnableCode(articleId: string, code: string): string {
  const setup = getExamples(articleId).get('setup')?.code ?? '';
  const body = [setup, code].filter(Boolean).join('\n\n');
  const imports = [];
  if (articleId.startsWith('numpy/') || /\bnp\./.test(body)) imports.push('import numpy as np');
  if (articleId.startsWith('pandas/') || /\bpd\./.test(body)) imports.push('import pandas as pd');
  return `${imports.join('\n')}\n\n${body}\n`;
}

export function articleUrl(id: string): string {
  return `/reference/${id}`;
}
