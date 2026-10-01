/** Уровни CEFR справочника и курса английского: подписи, порядок, связь с общим уровнем статей справочника. */
export const CEFR_LEVELS = ['A1', 'A2', 'B1', 'B2', 'C1'] as const;
export type Cefr = (typeof CEFR_LEVELS)[number];

/** Общий уровень статьи (для списков и поиска) выводится из CEFR: A1–A2 базовый, B1–B2 средний, C1 продвинутый. */
export const CEFR_TO_LEVEL: Record<Cefr, 'basic' | 'medium' | 'advanced'> = { A1: 'basic', A2: 'basic', B1: 'medium', B2: 'medium', C1: 'advanced' };
export const CEFR_TONE: Record<Cefr, 'easy' | 'medium' | 'hard'> = { A1: 'easy', A2: 'easy', B1: 'medium', B2: 'medium', C1: 'hard' };

export const cefrRank = (c: string) => CEFR_LEVELS.indexOf(c as Cefr);
export const isCefr = (c: unknown): c is Cefr => CEFR_LEVELS.includes(c as Cefr);

/** Уровни, которые охватывает уровень модуля: «A1–A2» → A1, A2; «B1» → B1. */
export function moduleLevels(level: string | undefined): Cefr[] {
  if (!level) return [];
  const [from, to = from] = level.split(/[–-]/).map((s) => s.trim());
  const a = cefrRank(from);
  const b = cefrRank(to);
  return a < 0 || b < 0 ? [] : CEFR_LEVELS.slice(a, b + 1);
}
