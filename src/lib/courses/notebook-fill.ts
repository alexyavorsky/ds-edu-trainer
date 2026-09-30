/**
 * «Скачать с моим кодом»: в готовый ноутбук урока (заготовки) подставляется код ученика из браузера.
 * Без зависимостей от Node.js — модуль работает и на странице урока, и в валидаторе.
 */

/** Текст ячейки → строки ноутбука: у каждой, кроме последней, в конце перевод строки. */
export const sourceLines = (text: string) => text.split('\n').map((l, i, all) => (i < all.length - 1 ? `${l}\n` : l));

interface Cell {
  id: string;
  cell_type: string;
  source: string[];
}

/** Возвращает копию ноутбука, где у ячеек-упражнений с id из codes исходник заменён кодом ученика. */
export function fillNotebook<T extends { cells: Cell[] }>(notebook: T, codes: Record<string, string>): T {
  return {
    ...notebook,
    cells: notebook.cells.map((cell) =>
      cell.cell_type === 'code' && Object.hasOwn(codes, cell.id) ? { ...cell, source: sourceLines(codes[cell.id]) } : cell,
    ),
  };
}
