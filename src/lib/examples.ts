/**
 * Разбор файла примеров справочника reference/<тема>/<статья>.py — повторяет Python-версию
 * (scripts/validate_reference.py). Без зависимостей от Astro: его использует и scripts/validate_pyodide.ts.
 */

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
