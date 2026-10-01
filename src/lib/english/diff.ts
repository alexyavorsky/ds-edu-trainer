/** Разница по словам для <Fix wrong right>: какие слова ошибки и исправления отличаются (НОП по словам). */
export interface Token {
  text: string;
  changed: boolean;
}

const split = (s: string) => s.split(/(\s+)/).filter(Boolean);
const key = (w: string) => w.toLowerCase().replace(/[.,!?;:"«»]/g, '');

export function wordDiff(wrong: string, right: string): { wrong: Token[]; right: Token[] } {
  const a = split(wrong);
  const b = split(right);
  const wa = a.filter((t) => !/^\s+$/.test(t));
  const wb = b.filter((t) => !/^\s+$/.test(t));
  const n = wa.length;
  const m = wb.length;
  const lcs = Array.from({ length: n + 1 }, () => new Array<number>(m + 1).fill(0));
  for (let i = n - 1; i >= 0; i--)
    for (let j = m - 1; j >= 0; j--) lcs[i][j] = key(wa[i]) === key(wb[j]) ? lcs[i + 1][j + 1] + 1 : Math.max(lcs[i + 1][j], lcs[i][j + 1]);
  const keepA = new Set<number>();
  const keepB = new Set<number>();
  for (let i = 0, j = 0; i < n && j < m; ) {
    if (key(wa[i]) === key(wb[j])) {
      keepA.add(i++);
      keepB.add(j++);
    } else if (lcs[i + 1][j] >= lcs[i][j + 1]) i++;
    else j++;
  }
  const mark = (tokens: string[], keep: Set<number>): Token[] => {
    let w = 0;
    return tokens.map((t) => (/^\s+$/.test(t) ? { text: t, changed: false } : { text: t, changed: !keep.has(w++) }));
  };
  return { wrong: mark(a, keepA), right: mark(b, keepB) };
}
