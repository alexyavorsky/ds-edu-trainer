/** Подписи для интерфейса. */
export const DIFFICULTY_LABEL = { easy: 'Лёгкая', medium: 'Средняя', hard: 'Сложная' } as const;
export const DIFFICULTY_PLURAL = { easy: 'Лёгкие', medium: 'Средние', hard: 'Сложные' } as const;
export const TYPE_LABEL = {
  implement: 'Реализация',
  'fix-bug': 'Найти ошибку',
  complete: 'Дописать',
  complexity: 'Оценка сложности',
} as const;

export const TELEGRAM_USER = 'yavorsky1000';

export function pluralRu(n: number, one: string, few: string, many: string): string {
  const mod10 = n % 10;
  const mod100 = n % 100;
  if (mod10 === 1 && mod100 !== 11) return one;
  if (mod10 >= 2 && mod10 <= 4 && (mod100 < 12 || mod100 > 14)) return few;
  return many;
}

export function bugsLabel(n: number): string {
  return `${n} ${pluralRu(n, 'ошибка', 'ошибки', 'ошибок')}`;
}

export function tasksLabel(n: number): string {
  return `${n} ${pluralRu(n, 'задача', 'задачи', 'задач')}`;
}

export function modulesLabel(n: number): string {
  return `${n} ${pluralRu(n, 'модуль', 'модуля', 'модулей')}`;
}

export function lessonsLabel(n: number): string {
  return `${n} ${pluralRu(n, 'урок', 'урока', 'уроков')}`;
}

/** Длительность курса: «≈ 40 мин», «≈ 12 ч». */
export function durationLabel(minutes: number): string {
  return minutes < 90 ? `≈ ${minutes} мин` : `≈ ${Math.round(minutes / 60)} ч`;
}
