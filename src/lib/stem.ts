/**
 * Простой стемминг для поиска: у слова отрезается одно типичное окончание, чтобы «окно», «окна» и «окнами»
 * сводились к «окн», а «группировка» и «группировки» — к «группировк». Применяется одинаково к индексу
 * (при сборке) и к запросу (в браузере). Основа — не короче 3 букв, поэтому 3-буквенные слова не меняются.
 * Латинские слова (справочник грамматики английского) — своя, английская обработка: срезаются -s/-es/-ed/-ing,
 * так «played», «playing» и «plays» находят «play»; русский стеммер к ним не применяется.
 */
const ENDINGS = [
  // прилагательные и причастия
  'ыми', 'ими', 'ого', 'его', 'ому', 'ему', 'ая', 'яя', 'ое', 'ее', 'ые', 'ие', 'ый', 'ий', 'ой', 'ую', 'юю',
  'ых', 'их', 'ым', 'им',
  // существительные
  'иями', 'ями', 'ами', 'иях', 'ях', 'ах', 'ией', 'ием', 'ов', 'ев', 'ей', 'ам', 'ям', 'ом', 'ем', 'ию', 'ью',
  'ия', 'ья', 'ье', 'ии', 'а', 'я', 'о', 'е', 'и', 'ы', 'у', 'ю', 'ь', 'й',
  // глаголы
  'ать', 'ять', 'ить', 'еть', 'уть', 'ыть', 'ешь', 'ете', 'ишь', 'ите', 'ют', 'ут', 'ят', 'ет', 'ит', 'ть',
].sort((a, b) => b.length - a.length);

const MIN_STEM = 3;
const CYRILLIC = /^[а-яё]+$/;

const LATIN = /^[a-z]+$/;

/** Английские окончания: -ies → -y, -ing, -ed, -es (после s, x, z, ch, sh), -s (не -ss, -us, -is). */
export function stemEnglish(word: string): string {
  if (word.length <= MIN_STEM + 1 || !LATIN.test(word)) return word;
  if (word.endsWith('ies') && word.length - 3 >= MIN_STEM) return `${word.slice(0, -3)}y`;
  if (word.endsWith('ied') && word.length - 3 >= MIN_STEM) return `${word.slice(0, -3)}y`;
  if (word.endsWith('ing') && word.length - 3 >= MIN_STEM) return word.slice(0, -3);
  if (word.endsWith('ed') && word.length - 2 >= MIN_STEM) return word.slice(0, -2);
  if (/(s|x|z|ch|sh)es$/.test(word) && word.length - 2 >= MIN_STEM) return word.slice(0, -2);
  if (word.endsWith('s') && !/(ss|us|is)$/.test(word)) return word.slice(0, -1);
  return word;
}

export function stem(word: string): string {
  if (LATIN.test(word)) return stemEnglish(word);
  if (word.length <= MIN_STEM || !CYRILLIC.test(word)) return word;
  let w = word;
  if ((w.endsWith('ся') || w.endsWith('сь')) && w.length - 2 >= MIN_STEM) w = w.slice(0, -2);
  const ending = ENDINGS.find((e) => w.endsWith(e) && w.length - e.length >= MIN_STEM);
  return ending ? w.slice(0, -ending.length) : w;
}
