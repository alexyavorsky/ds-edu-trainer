/**
 * Какие пакеты нужны примеру справочника в браузере. Грузим только нужное: статья NumPy не тянет pandas
 * и matplotlib, пока пример их не использует. Явные import распознаёт сам Pyodide (loadPackagesFromImports),
 * здесь — неявные: pd из prelude, графики через .plot, форматы файлов pandas.
 * Если правило что-то пропустит, воркер поставит пакет после ModuleNotFoundError и повторит пример,
 * а scripts/validate_pyodide.ts сообщит о таком примере — правило нужно дополнить.
 */
const RULES: [string, RegExp][] = [
  ['pandas', /\bpd\.|\bpandas\b/],
  ['matplotlib', /\bplt\b|\bmatplotlib\b|\.plot\b|\.hist\s*\(|\.boxplot\s*\(/],
  ['pyarrow', /pyarrow|parquet|feather|\.orc\b/],
  ['openpyxl', /excel|xlsx/i],
];

/**
 * Пакеты для примера: пакет темы (numpy или pandas; pandas тянет numpy) и распознанные по коду.
 * У темы без пакета (ООП, алгоритмы) — только распознанные: пример на стандартной библиотеке ничего не грузит.
 */
export function examplePackages(topicPackage: string | undefined, code: string): string[] {
  const packages = new Set<string>(topicPackage ? ['numpy', topicPackage] : []);
  for (const [name, re] of RULES) if (re.test(code)) packages.add(name);
  return [...packages];
}
