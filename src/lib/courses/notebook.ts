/**
 * Урок → Jupyter-ноутбук (.ipynb) для Jupyter и Google Colab: текст, демонстрации, упражнения
 * (заготовка + ячейка проверки) и вопросы. Первая ячейка готовит урок: проверяет версии пакетов,
 * записывает файлы данных (встроены сжатыми) и определяет _check — проверку упражнений тем же раннером,
 * что у задач (runtime/runner.py). Сохранённый вывод в ноутбук не кладётся: его даёт выполнение.
 *
 * Валидатор (scripts/validate_courses.ts) собирает ноутбук с эталонами вместо заготовок и выполняет его
 * в CPython: все ячейки без ошибок, каждая проверка — «Прошло N из N».
 */
import { readFileSync } from 'node:fs';
import { join } from 'node:path';
import { deflateSync } from 'node:zlib';
import type { Block, CodeCell, ExerciseCell } from './format.ts';
import { DATA_DIR, type CourseSource, type LessonSource } from './load.ts';
import { sourceLines as lines } from './notebook-fill.ts';

/** Минимальные версии: ниже — предупреждение в первой ячейке (урок написан для этих версий и новее). */
export const MIN_VERSIONS: Record<string, string> = { numpy: '2.0', pandas: '3.0' };

interface NotebookCell {
  cell_type: 'markdown' | 'code';
  metadata: Record<string, unknown>;
  source: string[];
  execution_count?: null;
  outputs?: never[];
  id: string;
}

function markdown(id: string, text: string): NotebookCell {
  return { cell_type: 'markdown', metadata: {}, source: lines(text), id };
}

function code(id: string, text: string, metadata: Record<string, unknown> = {}): NotebookCell {
  return { cell_type: 'code', metadata, source: lines(text), execution_count: null, outputs: [], id };
}

/** runtime/runner.py без блока запуска: в Jupyter __name__ == "__main__", он запустил бы тесты сразу. */
function runnerSource(root: string): string {
  const source = readFileSync(join(root, 'runtime', 'runner.py'), 'utf-8');
  return source.slice(0, source.indexOf('\nif __name__ == "__main__":')).trimEnd();
}

function setupCell(course: CourseSource, lesson: LessonSource, root: string): string {
  const packages = [...new Set(['numpy', course.meta.package])];
  const data = lesson.meta.data.map((name) => {
    const packed = deflateSync(readFileSync(join(DATA_DIR, name)), { level: 9 }).toString('base64');
    return `    ${JSON.stringify(name)}: """\n${packed.match(/.{1,100}/g)!.join('\n')}\n""",`;
  });
  return [
    '# @title Подготовка урока — выполните эту ячейку первой',
    '# Проверяет версии пакетов, записывает файлы данных в папку data/ и определяет _check — проверку упражнений.',
    'import base64, os, zlib',
    '',
    `for _name, _min in ${JSON.stringify(Object.fromEntries(packages.map((p) => [p, MIN_VERSIONS[p] ?? '0'])))}.items():`,
    '    try:',
    '        _have = __import__(_name).__version__',
    '    except ImportError:',
    '        print(f"Нет пакета {_name}: выполните %pip install {_name} и перезапустите ядро")',
    '        continue',
    '    if tuple(int(x) for x in _have.split(".")[:2]) < tuple(int(x) for x in _min.split(".")):',
    '        print(f"Урок написан для {_name} {_min} и новее, у вас {_have}: выполните %pip install -U {_name} и перезапустите ядро")',
    '',
    ...(data.length
      ? [
          '_DATA = {',
          ...data,
          '}',
          'os.makedirs("data", exist_ok=True)',
          'for _name, _packed in _DATA.items():',
          '    with open(os.path.join("data", _name), "wb") as _f:',
          '        _f.write(zlib.decompress(base64.b64decode(_packed)))',
          'print("Файлы данных:", ", ".join(sorted(_DATA)))',
          '',
        ]
      : []),
    '# ─── Проверка упражнений: тот же раннер, что у задач на сайте ───',
    runnerSource(root),
    '',
    '',
    'def _check(*tests, names=()):',
    '    """Запускает проверки упражнения и печатает ✓ / ✗ и итог — как на сайте."""',
    '    for name in names:',
    '        if name not in globals():',
    '            print(f"✗ переменная {name} не создана — выполните ячейку упражнения")',
    '            return',
    '        if globals()[name] is Ellipsis:',
    '            print(f"✗ {name} пока равна ... — замените многоточие своим кодом")',
    '            return',
    '    globals()["_TESTS"] = list(tests)',
    '    _run_tests()',
  ].join('\n');
}

function componentMarkdown(block: Extract<Block, { type: 'component' }>, siteUrl: string | null, lessonPath: string): string {
  if (block.name === 'Mistake') return quote(`**Типичная ошибка: ${block.attrs.title ?? ''}.**\n\n${block.body ?? ''}`);
  if (block.name === 'Note') return quote(`${block.attrs.title ? `**${block.attrs.title}.** ` : ''}${block.body ?? ''}`);
  return siteUrl ? `*Схема — в уроке на сайте: ${siteUrl}${lessonPath}*` : '*Схема — в уроке на сайте.*';
}

const quote = (text: string) =>
  text
    .split('\n')
    .map((l) => (l ? `> ${l}` : '>'))
    .join('\n');

/** Ссылки сайта (/reference/…) в ноутбуке — абсолютные, если адрес сайта известен. */
function absolutize(text: string, siteUrl: string | null): string {
  return siteUrl ? text.replace(/\]\(\//g, `](${siteUrl}/`) : text;
}

export interface NotebookOptions {
  root: string; // корень репозитория
  siteUrl: string | null; // https://… — для ссылок на справочник
  solutions?: boolean; // эталоны вместо заготовок — так ноутбук проверяет валидатор
}

export function buildNotebook(course: CourseSource, lesson: LessonSource, o: NotebookOptions): object {
  const cells: NotebookCell[] = [];
  const cellOf = (id: string) => lesson.cells.find((c) => c.id === id) as CodeCell;
  const lessonPath = `/courses/${course.slug}/${lesson.slug}`;
  const intro = [
    `# ${lesson.meta.title}`,
    '',
    lesson.meta.summary,
    '',
    `Курс ${course.meta.title} · урок \`${lesson.meta.id}\`${o.siteUrl ? ` · [урок на сайте](${o.siteUrl}${lessonPath})` : ''}.`,
    '',
    'Выполняйте ячейки по порядку (Shift+Enter), начиная с первой — она готовит урок. После каждого упражнения идёт',
    'ячейка проверки: она печатает ✓ / ✗ и итог.',
  ];
  cells.push(markdown('intro', intro.join('\n')));
  cells.push(code('setup', setupCell(course, lesson, o.root), { cellView: 'form', jupyter: { source_hidden: true } }));

  let exercise = 0;
  for (const block of lesson.blocks) {
    const id = `${block.type}-${block.line}`;
    if (block.type === 'text') cells.push(markdown(id, absolutize(block.text, o.siteUrl)));
    else if (block.type === 'component') cells.push(markdown(id, absolutize(componentMarkdown(block, o.siteUrl, lessonPath), o.siteUrl)));
    else if (block.type === 'demo') {
      const cell = cellOf(block.id);
      const raises = cell.flags.raises;
      const body = cell.kind === 'demo' ? cell.code : '';
      // намеренная ошибка перехвачена и напечатана: «Выполнить всё» (Run all) нигде на ней не останавливается
      const source = raises
        ? [
            ...(block.title ? [`# ${block.title}`] : []),
            `# Эта ячейка показывает ошибку ${raises}: она перехвачена, чтобы «Выполнить всё» не останавливалось.`,
            'try:',
            ...body.split('\n').map((l) => (l ? `    ${l}` : '')),
            'except Exception as error:',
            '    print(f"{type(error).__name__}: {error}")',
          ].join('\n')
        : `${block.title ? `# ${block.title}\n` : ''}${body}`;
      cells.push(code(block.id, source));
    } else if (block.type === 'exercise') {
      const cell = cellOf(block.id) as ExerciseCell;
      exercise++;
      const hints = block.hints.map((h, i) => `<details><summary>Подсказка ${i + 1}</summary>\n\n${h}\n\n</details>`);
      cells.push(markdown(`${block.id}-task`, absolutize([`### Упражнение ${exercise}. ${block.title}`, '', block.prompt, ...(hints.length ? ['', ...hints] : [])].join('\n'), o.siteUrl)));
      cells.push(code(block.id, o.solutions ? cell.solution : cell.starter));
      const names = cell.targets.length ? `, names=${JSON.stringify(cell.targets)}` : '';
      const tests = cell.tests.match(/^def (test_\w+)/gm)?.map((d) => d.slice(4)) ?? [];
      cells.push(code(`${block.id}-check`, `# Проверка упражнения ${exercise} — выполните после своего решения\n${cell.tests}\n\n_check(${tests.join(', ')}${names})`));
      cells.push(markdown(`${block.id}-solution`, `<details><summary>Решение</summary>\n\n\`\`\`python\n${cell.solution}\n\`\`\`\n\n</details>`));
    } else if (block.type === 'quiz') {
      const options = block.options.map((opt) => `- ${opt.text}`);
      const answer = block.options.filter((opt) => opt.correct).map((opt) => opt.text).join('; ');
      cells.push(
        markdown(id, [`**Вопрос.** ${block.question}`, '', ...options, '', `<details><summary>Ответ</summary>\n\n${answer}${block.explain ? `\n\n${block.explain}` : ''}\n\n</details>`].join('\n')),
      );
    }
  }
  if (lesson.meta.reference.length) {
    const refs = lesson.meta.reference.map((r) => (o.siteUrl ? `[${r}](${o.siteUrl}/reference/${r})` : `\`${r}\``));
    cells.push(markdown('more', `**Подробнее в справочнике:** ${refs.join(' · ')}`));
  }
  return {
    cells,
    metadata: {
      kernelspec: { display_name: 'Python 3', language: 'python', name: 'python3' },
      language_info: { name: 'python' },
      colab: { provenance: [] },
    },
    nbformat: 4,
    nbformat_minor: 5,
  };
}
