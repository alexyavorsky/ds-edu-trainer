/** Детерминированное перемешивание (от id упражнения): одинаковый порядок с JS и без, на сервере и в браузере. */
import type { Exercise } from './check.ts';

function seed(text: string): () => number {
  let h = 2166136261;
  for (const c of text) h = Math.imul(h ^ c.charCodeAt(0), 16777619);
  return () => {
    h = Math.imul(h ^ (h >>> 15), 2246822507);
    h = Math.imul(h ^ (h >>> 13), 3266489909);
    return ((h ^= h >>> 16) >>> 0) / 4294967296;
  };
}

export function shuffled<T>(list: T[], key: string): T[] {
  const random = seed(key);
  const out = [...list];
  for (let i = out.length - 1; i > 0; i--) {
    const j = Math.floor(random() * (i + 1));
    [out[i], out[j]] = [out[j], out[i]];
  }
  // порядок совпал с исходным — сдвиг на одну позицию, иначе пары стояли бы напротив своих начал
  if (out.length > 1 && out.every((x, i) => x === list[i])) out.push(out.shift()!);
  return out;
}

/** Правые части match в порядке показа. */
export const matchOrder = (ex: Exercise) => shuffled(ex.items.map((i) => i.answer[0]), ex.id);
