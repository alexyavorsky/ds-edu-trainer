/**
 * Направления сайта: разделы задач, курсы и темы справочника группируются по ним на главной, в /courses,
 * /reference и в выпадающих меню шапки. Поле `direction` — в book.toml, course.toml, topic.toml.
 * Порядок здесь — порядок групп на страницах. Список значений повторяют валидаторы
 * (scripts/validate.py, scripts/validate_reference.py, scripts/validate_courses.ts).
 */
export const DIRECTIONS = [
  { id: 'python', title: 'Python и алгоритмы' },
  { id: 'data', title: 'Данные' },
  { id: 'git', title: 'Git' },
  { id: 'english', title: 'Английский' },
] as const;

export type Direction = (typeof DIRECTIONS)[number]['id'];
export const DIRECTION_IDS = DIRECTIONS.map((d) => d.id) as [Direction, ...Direction[]];

/** Пояснение к пометке «бета»: показывается рядом с ней и по наведению. */
export const BETA_NOTE = 'Раздел новый, возможны неточности';

export interface DirectionGroup<T> {
  id: Direction;
  title: string;
  items: T[];
}

/** Элементы по направлениям в порядке DIRECTIONS; порядок внутри группы сохраняется, пустые группы не возвращаются. */
export function groupByDirection<T>(items: T[], direction: (item: T) => Direction): DirectionGroup<T>[] {
  return DIRECTIONS.map((d) => ({ id: d.id, title: d.title, items: items.filter((item) => direction(item) === d.id) })).filter(
    (g) => g.items.length > 0,
  );
}
