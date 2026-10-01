/**
 * Сверяет сборку копируемого .py на TypeScript (src/lib/bundle.ts, её использует сайт)
 * со сборкой в Python (scripts/validate.py, её проверяют тесты). Должны совпадать байт в байт.
 *
 *   node scripts/check-bundles.ts
 */
import { execFileSync } from 'node:child_process';
import { existsSync, readdirSync, readFileSync, statSync } from 'node:fs';
import { join, resolve } from 'node:path';
import { parse } from 'smol-toml';
import { buildBundle, parsePins } from '../src/lib/bundle.ts';

const root = join(import.meta.dirname, '..');
// EDU_CONTENT_ROOT — образцы платформы (tests/platform), как в src/lib/paths.ts
const content = process.env.EDU_CONTENT_ROOT ? resolve(root, process.env.EDU_CONTENT_ROOT) : root;
const dirs = (p: string) => readdirSync(p).filter((n) => !n.startsWith('.') && statSync(join(p, n)).isDirectory()).sort();
const read = (p: string) => readFileSync(p, 'utf-8');
const runner = read(join(root, 'runtime', 'runner.py'));
const pins = parsePins(read(join(root, 'requirements-dev.txt')));

let checked = 0;
let failed = 0;
for (const book of dirs(join(content, 'challenges'))) {
  const bookMeta = parse(read(join(content, 'challenges', book, 'book.toml'))) as Record<string, any>;
  for (const chapter of dirs(join(content, 'challenges', book))) {
    const chapterDir = join(content, 'challenges', book, chapter);
    const chapterMeta = parse(read(join(chapterDir, 'chapter.toml'))) as Record<string, any>;
    for (const slug of dirs(chapterDir)) {
      const dir = join(chapterDir, slug);
      const meta = parse(read(join(dir, 'meta.toml'))) as Record<string, any>;
      if (meta.type === 'complexity') continue;
      for (const [file, flag] of [['starter.py', []], ['solution.py', ['--solution']]] as const) {
        if (!existsSync(join(dir, file))) continue;
        const ts = buildBundle({
          title: meta.title,
          id: meta.id,
          difficulty: meta.difficulty,
          type: meta.type,
          bookTitle: bookMeta.title,
          chapterLabel: `${bookMeta.kind === 'topic' ? 'Раздел' : 'Глава'} ${Number(chapter.slice(0, 2))}. ${chapterMeta.title}`,
          slug,
          taskMd: read(join(dir, 'task.md')),
          code: read(join(dir, file)),
          tests: read(join(dir, 'tests.py')),
          runner,
          data: existsSync(join(dir, 'data.py')) ? read(join(dir, 'data.py')) : undefined,
          packages: bookMeta.packages ?? [],
          pins,
        });
        const py = execFileSync('python3', [join(root, 'scripts', 'validate.py'), '--bundle', dir, ...flag], { encoding: 'utf-8', env: process.env });
        checked++;
        if (ts !== py) {
          failed++;
          const tsLines = ts.split('\n');
          const pyLines = py.split('\n');
          const line = tsLines.findIndex((l, i) => l !== pyLines[i]);
          console.log(`✗ ${book}/${chapter}/${slug} (${file}), строка ${line + 1}:\n  TS: ${tsLines[line]}\n  PY: ${pyLines[line]}`);
        }
      }
    }
  }
}
console.log(`${failed ? '✗' : '✓'} Совпало ${checked - failed} из ${checked} сборок`);
process.exit(failed ? 1 : 0);
