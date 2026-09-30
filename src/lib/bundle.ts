/**
 * Сборка копируемого .py из файлов задачи.
 * Зеркало scripts/validate.py::build_bundle — результат должен совпадать байт в байт
 * (проверяется командой `npm run check:bundles`).
 */

export const DIFFICULTY_RU = { easy: 'лёгкая', medium: 'средняя', hard: 'сложная' } as const;
export const TYPE_RU = {
  implement: 'реализовать',
  'fix-bug': 'найти ошибку',
  complete: 'дописать',
  complexity: 'оценить сложность',
} as const;

export type Difficulty = keyof typeof DIFFICULTY_RU;
export type ChallengeType = keyof typeof TYPE_RU;

const SEPARATOR = '# ════ Тесты — ниже этой линии ничего менять не нужно ' + '═'.repeat(19);

/** Нормативные разделы task.md, которые попадают в docstring. */
export const DOCSTRING_SECTIONS = ['Ограничения', 'Правила'];

/** Убирает **жирный** и *курсив* вне `кода`. */
export function stripEmphasis(text: string): string {
  return text
    .split('`')
    .map((part, i) =>
      i % 2 ? part : part.replace(/\*\*(.+?)\*\*/g, '$1').replace(/\*(\S(?:.*?\S)?)\*/g, '$1'),
    )
    .join('`');
}

/** Первый абзац Markdown-текста одной строкой. */
export function firstParagraph(markdown: string): string {
  const lines: string[] = [];
  for (const line of markdown.trim().split('\n')) {
    if (!line.trim()) {
      if (lines.length) break;
      continue;
    }
    lines.push(line.trim());
  }
  return stripEmphasis(lines.join(' '));
}

type Item = { marker: string; text: string }; // marker: «- », «1. » или пусто

/** Разделы «Ограничения»/«Правила» как списки пунктов. */
export function docstringSections(markdown: string): { title: string; items: Item[] }[] {
  const result: { title: string; items: Item[] }[] = [];
  let items: Item[] | null = null;
  let newParagraph = true;
  for (const line of markdown.split('\n')) {
    if (line.startsWith('## ')) {
      const title = line.slice(3).trim();
      items = DOCSTRING_SECTIONS.includes(title) ? [] : null;
      if (items) result.push({ title, items });
      newParagraph = true;
      continue;
    }
    if (!items) continue;
    const stripped = line.trim();
    if (!stripped) {
      newParagraph = true;
    } else if (/^(- |\d+\. )/.test(stripped)) {
      const marker = stripped.match(/^(- |\d+\. )/)![1];
      items.push({ marker, text: stripped.slice(marker.length).trim() });
      newParagraph = false;
    } else if (items.length && !newParagraph) {
      items[items.length - 1].text += ' ' + stripped;
    } else {
      items.push({ marker: '', text: stripped });
      newParagraph = false;
    }
  }
  return result
    .filter((s) => s.items.length)
    .map((s) => ({ title: s.title, items: s.items.map((it) => ({ ...it, text: stripEmphasis(it.text) })) }));
}

/** Жадный перенос по ASCII-пробелам, как textwrap.fill(break_on_hyphens=False, break_long_words=False). */
export function wrap(text: string, width = 76, initial = '', subsequent = ''): string {
  const words = text.split(/[ \t\n\r\f\v]+/).filter(Boolean);
  const lines: string[] = [];
  let line = '';
  for (const word of words) {
    if (!line) {
      line = (lines.length ? subsequent : initial) + word;
    } else if ([...`${line} ${word}`].length > width) {
      lines.push(line);
      line = subsequent + word;
    } else {
      line = `${line} ${word}`;
    }
  }
  if (line) lines.push(line);
  return lines.join('\n');
}

export interface BundleInput {
  title: string;
  id: string;
  difficulty: Difficulty;
  type: ChallengeType;
  bookTitle: string;
  chapterLabel: string; // «Глава 3. Рекурсия» (у темы — «Раздел 2. Индексация»)
  slug: string;
  taskMd: string;
  code: string; // starter.py или solution.py
  tests: string;
  runner: string;
}

const TESTS_LIST_COMMENT = '# Тесты задачи по порядку — запускаются только они';

/**
 * Явный список тестов после tests.py: функция test_… из кода решения тестом не становится.
 * Имена — функции test_* верхнего уровня tests.py по порядку (зеркало validate.py::tests_list).
 */
export function testsList(tests: string): string {
  const names = [...tests.matchAll(/^def (test_\w+)\s*\(/gm)].map((m) => m[1]);
  return [TESTS_LIST_COMMENT, '_TESTS = [', ...names.map((n) => `    ${n},`), ']'].join('\n');
}

/** Части копируемого файла: шапка-docstring и всё, что идёт после кода решения (тесты и раннер). */
export function bundleParts(i: Omit<BundleInput, 'code'>): { header: string; footer: string } {
  const header = [
    '"""',
    i.title,
    `${i.bookTitle} → ${i.chapterLabel}`,
    `Сложность: ${DIFFICULTY_RU[i.difficulty]} · Тип: ${TYPE_RU[i.type]} · id: ${i.id}`,
    '',
    wrap(firstParagraph(i.taskMd)),
    '',
    ...docstringSections(i.taskMd).flatMap((section) => [
      `${section.title}:`,
      ...section.items.map((it) => wrap(it.text, 76, it.marker, ' '.repeat(it.marker.length))),
      '',
    ]),
    `Запуск: python3 ${i.slug.replaceAll('-', '_')}.py (на Windows: python ${i.slug.replaceAll('-', '_')}.py)`,
    '"""',
  ].join('\n');
  return { header, footer: bundleFooter(i.tests, i.runner) };
}

/** Всё, что идёт после кода решения: разделитель, tests.py, список _TESTS и раннер. Его же выполняет сайт. */
export function bundleFooter(tests: string, runner: string): string {
  return `${SEPARATOR}\n\n${tests.trim()}\n\n\n${testsList(tests.trim())}\n\n\n${runner.trim()}\n`;
}

/** Склеивает копируемый файл из частей; тот же код собирает файл с кодом из редактора на странице задачи. */
export function joinBundle(header: string, code: string, footer: string): string {
  return `${header}\n\n${code.trim()}\n\n\n${footer}`;
}

export function buildBundle(i: BundleInput): string {
  const { header, footer } = bundleParts(i);
  return joinBundle(header, i.code, footer);
}
