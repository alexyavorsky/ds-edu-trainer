/**
 * Примеры справочника: «Запустить» выполняет пример в браузере, как ячейку Jupyter (prelude + общие данные
 * статьи + пример, вывод и repr последнего выражения — тем же кодом, что у валидатора), «Изменить» открывает
 * редактор. Изменённый код не сохраняется: справочник остаётся шпаргалкой. Запуск — только по нажатию.
 */
import { python, type RunEnd } from '../../lib/python/client';
import { PYTHON_CONFIG } from '../../lib/python/config';
import { examplePackages } from '../../lib/python/packages';
import type { ExampleDone } from '../../lib/python/protocol';
import type * as EditorApi from './editor';

interface RunData {
  article: string;
  topicPackage: string | null; // null — тема на стандартной библиотеке (ООП, алгоритмы): numpy не грузится
  prelude: { source: string; filename: string } | null; // свой prelude темы; null — общий reference/prelude.py
  setup: string;
  filename: string;
  library: string; // «pandas» или «Python»
  browserVersion: string | null; // версия пакета в Pyodide
  referenceVersion: string | null; // версия, под которую написан справочник
  matplotlibVersion: string;
}

let editorModule: Promise<typeof EditorApi> | null = null;
const loadEditor = () => (editorModule ??= import('./editor'));

function el<K extends keyof HTMLElementTagNameMap>(tag: K, className?: string, text?: string): HTMLElementTagNameMap[K] {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}

export function initExamples(): void {
  const dataNode = document.getElementById('reference-run-data');
  const figures = [...document.querySelectorAll<HTMLElement>('figure[data-cell]')];
  if (!dataNode || !figures.length) return;
  const data = JSON.parse(dataNode.textContent!) as RunData;
  for (const figure of figures) initExample(figure, data);
  python.preloadWhenIdle();
}

function initExample(figure: HTMLElement, data: RunData): void {
  const original = figure.dataset.runCode ?? '';
  const cell = figure.dataset.cell!;
  const browser = figure.dataset.browser; // differs · unavailable · timing
  const runButton = figure.querySelector<HTMLButtonElement>('[data-ex-run]')!;
  const editButton = figure.querySelector<HTMLButtonElement>('[data-ex-edit]')!;
  const editLabel = figure.querySelector<HTMLElement>('[data-ex-edit-label]')!;
  const codeBox = figure.querySelector<HTMLElement>('[data-ex-code]')!;
  const staticCode = codeBox.firstElementChild as HTMLElement;
  const stored = [...figure.querySelectorAll<HTMLElement>('[data-ex-stored]')];
  const live = figure.querySelector<HTMLElement>('[data-ex-live]')!;
  let view: EditorApi.EditorView | null = null;
  let editor: typeof EditorApi | null = null;
  let running = false;
  let plotUrls: string[] = [];

  const code = () => (view && editor ? editor.getCode(view) : original);

  const showStored = () => {
    live.hidden = true;
    live.replaceChildren();
    plotUrls.forEach((u) => URL.revokeObjectURL(u));
    plotUrls = [];
    stored.forEach((s) => (s.hidden = false));
  };

  const showLive = (children: Node[]) => {
    stored.forEach((s) => (s.hidden = true));
    live.replaceChildren(...children);
    live.hidden = false;
  };

  const head = (label: string, isError: boolean) => {
    const row = el('div', 'live-head');
    row.append(el('span', `label${isError ? ' is-error-label' : ''}`, label));
    const close = el('button', 'btn btn-ghost live-close', 'Скрыть');
    close.type = 'button';
    close.title = 'Показать сохранённый вывод';
    close.addEventListener('click', showStored);
    row.append(close);
    return row;
  };

  editButton.addEventListener('click', async () => {
    if (view && editor) {
      // «Вернуть»: исходный пример и его вывод
      view.destroy();
      view = null;
      staticCode.hidden = false;
      editLabel.textContent = 'Изменить';
      editButton.title = 'Изменить код примера и запустить свой вариант';
      showStored();
      return;
    }
    editor = await loadEditor();
    staticCode.hidden = true;
    view = editor.createEditor({ parent: codeBox, doc: original, label: 'Код примера', onRun: () => void run() });
    view.focus();
    editLabel.textContent = 'Вернуть';
    editButton.title = 'Вернуть исходный пример';
  });

  runButton.addEventListener('click', () => void run());

  async function run(): Promise<void> {
    if (running) return;
    running = true;
    runButton.classList.add('is-running');
    const source = code();
    if (view && editor) editor.markLine(view, null);
    const status = el('p', 'status', python.state === 'ready' ? 'Выполняется…' : 'Загружаем Python…');
    showStored();
    showLive([status]);
    const end = await python.run(
      {
        kind: 'example',
        packages: examplePackages(data.topicPackage ?? undefined, `${data.setup}\n${source}`),
        setup: data.setup,
        code: source,
        filename: data.filename,
        cell,
        ...(data.prelude ? { prelude: data.prelude } : {}),
      },
      {
        onStatus: (text) => (status.textContent = text || 'Выполняется…'),
        onStarted: () => (status.textContent = 'Выполняется…'),
      },
    );
    running = false;
    runButton.classList.remove('is-running');
    render(end, source !== original);
  }

  function render(end: RunEnd, edited: boolean): void {
    const copyHint = 'Можно скопировать код кнопкой «Копировать» и выполнить у себя.';
    if (end.type !== 'done') {
      const message =
        end.type === 'timeout'
          ? `Пример выполнялся дольше ${end.seconds} с и был остановлен. Python перезапущен.`
          : end.type === 'crash'
            ? /call stack|stack size|too much recursion/i.test(end.message)
              ? 'Кончился стек браузера — слишком глубокая рекурсия (через C-функции вроде lru_cache в Safari доступно около 60 уровней). Python перезапущен.'
              : `Python в браузере аварийно остановился (${end.message}). Python перезапущен — можно запустить снова.`
            : end.type === 'package-error'
              ? `Не удалось загрузить пакеты: ${end.message}. ${copyHint}`
              : `Не удалось загрузить Python: ${end.message}. ${copyHint}`;
      showLive([head('Ошибка', true), el('pre', 'is-error', message)]);
      return;
    }
    const d = end.data as ExampleDone;
    const expected = figure.dataset.raises;
    const failed = !!d.error && !(expected && d.error.mro.includes(expected) && !edited);
    const children: Node[] = [];
    const seconds = d.elapsed < 0.01 ? '<0,01' : d.elapsed.toFixed(2).replace('.', ',');
    children.push(head(`${d.error ? 'Ошибка' : 'Вывод'} · в браузере, ${seconds} с`, !!d.error));
    if (browser === 'differs' && !edited) {
      // причина — из reference/browser.json: «вывод», «график» или «вывод и график»
      const note =
        figure.dataset.browserReason === 'график'
          ? `В браузере matplotlib ${data.matplotlibVersion} — график может немного отличаться от показанного.`
          : data.browserVersion
            ? `В браузере ${data.library} ${data.browserVersion} (32-битная сборка), справочник написан для ${data.referenceVersion} — вывод может отличаться от показанного.`
            : 'В браузере 32-битный Python — вывод может отличаться от показанного.';
      children.push(el('p', 'live-note', note));
    }
    if (browser === 'timing') children.push(el('p', 'live-note', 'Замер в браузере: цифры будут другими, чем в сохранённом выводе.'));
    if (d.lines.length || !d.plots.length) {
      const pre = el('pre');
      const lines = d.lines.length ? d.lines : ['(нет вывода)'];
      if (d.error) {
        pre.append(lines.slice(0, -1).join('\n') + (lines.length > 1 ? '\n' : ''));
        const last = el('span', 'err', lines[lines.length - 1]);
        pre.append(last);
        if (d.error.line && view) last.append(` (строка ${d.error.line})`);
      } else {
        pre.textContent = lines.join('\n');
      }
      children.push(pre);
    }
    if (d.truncated) children.push(el('p', 'live-note', `Вывод обрезан: больше ${PYTHON_CONFIG.maxLines.toLocaleString('ru')} строк или 1 МБ.`));
    for (const svg of d.plots) {
      const url = URL.createObjectURL(new Blob([svg], { type: 'image/svg+xml' }));
      plotUrls.push(url);
      const img = el('img');
      img.src = url;
      img.alt = 'График, построенный в браузере';
      children.push(img);
    }
    showLive(children);
    if (failed && d.error?.line && view && editor) editor.markLine(view, d.error.line);
  }
}
