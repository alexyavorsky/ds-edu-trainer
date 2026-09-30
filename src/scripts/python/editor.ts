/**
 * Редактор кода (CodeMirror 6) для задач и примеров справочника. Грузится отдельным чанком
 * через import() — только на страницах, где есть что запускать.
 */
import { closeBrackets, closeBracketsKeymap } from '@codemirror/autocomplete';
import { defaultKeymap, history, historyKeymap, indentWithTab } from '@codemirror/commands';
import { python } from '@codemirror/lang-python';
import { bracketMatching, HighlightStyle, indentOnInput, indentUnit, syntaxHighlighting } from '@codemirror/language';
import { EditorSelection, EditorState, Prec, StateEffect, StateField } from '@codemirror/state';
import {
  Decoration,
  drawSelection,
  EditorView,
  highlightActiveLine,
  highlightActiveLineGutter,
  highlightSpecialChars,
  keymap,
  lineNumbers,
} from '@codemirror/view';
import { tags as t } from '@lezer/highlight';

/** Цвета темы vitesse-dark — как у блоков кода Shiki на сайте. */
const highlight = HighlightStyle.define([
  { tag: [t.keyword, t.controlKeyword, t.definitionKeyword, t.moduleKeyword, t.operatorKeyword], color: '#4d9375' },
  { tag: [t.string, t.special(t.string)], color: '#c98a7d' },
  { tag: [t.number, t.bool, t.null, t.atom], color: '#4c9a91' },
  { tag: t.comment, color: '#758575', fontStyle: 'italic' },
  { tag: [t.function(t.variableName), t.function(t.propertyName)], color: '#80a665' },
  { tag: [t.definition(t.variableName), t.variableName], color: '#bd976a' },
  { tag: [t.className, t.typeName, t.definition(t.className)], color: '#5da994' },
  { tag: [t.propertyName, t.attributeName], color: '#b8a965' },
  { tag: [t.self, t.standard(t.variableName)], color: '#c99076' },
  { tag: [t.operator, t.compareOperator, t.arithmeticOperator, t.logicOperator], color: '#cb7676' },
  { tag: [t.punctuation, t.bracket, t.separator], color: '#666666' },
  { tag: t.meta, color: '#bd976a' },
  { tag: t.invalid, color: '#f07a7d' },
]);

const theme = EditorView.theme(
  {
    '&': { color: '#dbd7caee', backgroundColor: 'var(--surface)', fontSize: '13px' },
    '&.cm-focused': { outline: 'none' },
    '.cm-scroller': { fontFamily: 'var(--font-mono)', lineHeight: '1.65' },
    '.cm-content': { padding: '12px 0', caretColor: 'var(--accent)' },
    '.cm-line': { padding: '0 16px 0 10px' },
    '.cm-gutters': { backgroundColor: 'var(--surface)', color: 'var(--faint)', border: 'none', paddingLeft: '6px' },
    '.cm-lineNumbers .cm-gutterElement': { minWidth: '26px' },
    '.cm-activeLine': { backgroundColor: 'rgb(255 255 255 / 0.03)' },
    '.cm-activeLineGutter': { backgroundColor: 'transparent', color: 'var(--text-2)' },
    '.cm-cursor': { borderLeftColor: 'var(--accent)', borderLeftWidth: '2px' },
    '&.cm-focused .cm-selectionBackground, .cm-selectionBackground, ::selection': { backgroundColor: 'rgb(141 149 255 / 0.28) !important' },
    '.cm-matchingBracket': { backgroundColor: 'rgb(141 149 255 / 0.18)', outline: '1px solid rgb(141 149 255 / 0.35)' },
    '.cm-error-line': { backgroundColor: 'rgb(240 122 125 / 0.12)' },
  },
  { dark: true },
);

const setErrorLine = StateEffect.define<number | null>();
const errorLine = StateField.define({
  create: () => Decoration.none,
  update(deco, tr) {
    deco = deco.map(tr.changes);
    for (const effect of tr.effects) {
      if (!effect.is(setErrorLine)) continue;
      const line = effect.value;
      deco =
        line && line <= tr.state.doc.lines
          ? Decoration.set([Decoration.line({ class: 'cm-error-line' }).range(tr.state.doc.line(line).from)])
          : Decoration.none;
    }
    return tr.docChanged ? Decoration.none : deco; // правка кода — подсветка ошибки больше не актуальна
  },
  provide: (field) => EditorView.decorations.from(field),
});

export interface EditorOptions {
  parent: HTMLElement;
  doc: string;
  label: string; // подпись для экранных дикторов
  onChange?(code: string): void;
  onRun?(): void;
}

export function createEditor(o: EditorOptions): EditorView {
  return new EditorView({
    parent: o.parent,
    state: EditorState.create({
      doc: o.doc,
      extensions: [
        lineNumbers(),
        highlightActiveLineGutter(),
        highlightSpecialChars(),
        history(),
        drawSelection(),
        indentOnInput(),
        bracketMatching(),
        closeBrackets(),
        highlightActiveLine(),
        errorLine,
        python(),
        syntaxHighlighting(highlight),
        theme,
        EditorState.tabSize.of(4),
        indentUnit.of('    '),
        Prec.highest(keymap.of([{ key: 'Mod-Enter', run: () => (o.onRun?.(), true) }])),
        keymap.of([...closeBracketsKeymap, ...defaultKeymap, ...historyKeymap, indentWithTab]),
        EditorView.contentAttributes.of({ 'aria-label': o.label, autocapitalize: 'off', autocorrect: 'off', spellcheck: 'false' }),
        EditorView.updateListener.of((u) => {
          if (u.docChanged) o.onChange?.(u.state.doc.toString());
        }),
      ],
    }),
  });
}

export function getCode(view: EditorView): string {
  return view.state.doc.toString();
}

export function setCode(view: EditorView, code: string): void {
  view.dispatch({ changes: { from: 0, to: view.state.doc.length, insert: code } });
}

/** Подсвечивает строку с ошибкой (null — снять подсветку). */
export function markLine(view: EditorView, line: number | null): void {
  view.dispatch({ effects: setErrorLine.of(line) });
}

/** Ставит курсор в начало строки и прокручивает к ней. */
export function goToLine(view: EditorView, line: number): void {
  if (line < 1 || line > view.state.doc.lines) return;
  const pos = view.state.doc.line(line).from;
  view.dispatch({ selection: EditorSelection.cursor(pos), effects: EditorView.scrollIntoView(pos, { y: 'center' }) });
  view.focus();
}

export type { EditorView };
