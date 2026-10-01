/**
 * Строчный Markdown для полей упражнений (task, explain, why, hint): **жирный**, *курсив*, `код`, [ссылка](адрес).
 * Блочной разметки в этих полях нет, поэтому полный процессор не нужен; HTML экранируется.
 */
const escape = (s: string) => s.replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[c]!);

export function inlineMarkdown(text: string): string {
  const codes: string[] = [];
  let s = escape(text).replace(/`([^`]+)`/g, (_, code: string) => `\u0000${codes.push(`<code>${code}</code>`) - 1}\u0000`);
  s = s
    .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
    .replace(/(^|[^*\w])\*([^*\s][^*]*?)\*(?![*\w])/g, '$1<em>$2</em>')
    .replace(/\[([^\]]+)\]\(([^)\s]+)\)/g, (_, label: string, href: string) =>
      /^(\/|https:\/\/)/.test(href) ? `<a href="${href}">${label}</a>` : label,
    );
  return s.replace(/\u0000(\d+)\u0000/g, (_, i: string) => codes[Number(i)]);
}
