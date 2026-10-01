/**
 * Проверка возможностей платформы на образцах tests/platform (на сайт они не попадают): тема справочника без
 * пакета со своим prelude, задачи без пакетов и с пакетом (data.py, lessons, классы), курс без пакета
 * (понятия для курса по языку, цель-класс в заготовке). Запускает обычные валидаторы и сборку сайта
 * (во временную папку) с EDU_CONTENT_ROOT=tests/platform.
 *
 *   node scripts/validate_platform.ts [--python путь]   # CPython с пакетами requirements-dev.txt (по умолчанию .venv)
 */
import { spawnSync } from 'node:child_process';
import { existsSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';

const root = join(import.meta.dirname, '..');
const argv = process.argv.slice(2);
const venv = join(root, '.venv', 'bin', 'python');
const python = argv.includes('--python') ? argv[argv.indexOf('--python') + 1] : existsSync(venv) ? venv : 'python3';
const env = { ...process.env, EDU_CONTENT_ROOT: 'tests/platform' };

const steps: [string, string, string[]][] = [
  ['задачи', python, ['scripts/validate.py']],
  ['сборки задач', process.execPath, ['scripts/check-bundles.ts']],
  ['справочник', python, ['scripts/validate_reference.py', '--strict']],
  ['Pyodide', process.execPath, ['scripts/validate_pyodide.ts']],
  ['курсы', process.execPath, ['scripts/validate_courses.ts', '--python', python]],
  ['сборка сайта', join(root, 'node_modules', '.bin', 'astro'), ['build', '--outDir', join(tmpdir(), 'edu-platform-samples')]],
];

let failed = 0;
for (const [name, cmd, args] of steps) {
  const run = spawnSync(cmd, args, { cwd: root, env, encoding: 'utf-8' });
  const ok = run.status === 0;
  failed += Number(!ok);
  console.log(`${ok ? '✓' : '✗'} ${name}`);
  if (!ok) console.log(`${run.stdout}${run.stderr}`.trim().split('\n').slice(-25).map((l) => `    ${l}`).join('\n'));
}
console.log(failed ? `✗ Не прошло: ${failed} из ${steps.length}` : `✓ Образцы платформы в порядке (${steps.length} проверок)`);
process.exit(failed ? 1 : 0);
