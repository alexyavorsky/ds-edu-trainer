/**
 * Таблица случаев для check.ts — юнит-проверка нормализации и сравнения: `node scripts/validate_english.ts --selftest`.
 * Каждый случай — пункт упражнения, ввод ученика и ожидаемый итог (и, где важно, замечания и отметки пропусков).
 */
import { check, DEFAULT_SETTINGS, type Exercise, type Input, type Item, type Kind, type Result, type Settings } from './check.ts';

export interface Case {
  name: string;
  kind: Kind;
  item: Partial<Item>;
  input: Input;
  expect: Result['status'];
  settings?: Partial<Settings>;
  note?: RegExp | false; // ожидаемое замечание или false — замечаний быть не должно
  gaps?: boolean[];
  why?: string; // ожидаемое объяснение предусмотренной ошибки (часть текста)
  allowCorrect?: boolean;
}

const gap = (text: string, answer: string | string[], input: Input, expect: Result['status'], extra: Partial<Case> = {}): Case => ({
  name: `gap «${text}» ← ${JSON.stringify(input)}`,
  kind: 'gap',
  input,
  expect,
  ...extra,
  item: { text, answer: Array.isArray(answer) ? answer : [answer], ...extra.item },
});
const gaps = (text: string, g: string[][], input: string[], expect: Result['status'], extra: Partial<Case> = {}): Case => ({
  name: `gaps «${text}» ← ${JSON.stringify(input)}`,
  kind: 'gap',
  input,
  expect,
  ...extra,
  item: { text, answer: [], gaps: g, ...extra.item },
});
const sentence = (kind: Kind, answer: string | string[], input: string, expect: Result['status'], extra: Partial<Case> = {}): Case => ({
  name: `${kind} «${Array.isArray(answer) ? answer[0] : answer}» ← «${input}»`,
  kind,
  input,
  expect,
  ...extra,
  item: { answer: Array.isArray(answer) ? answer : [answer], ...extra.item },
});
const strictC = { settings: { contractions: 'strict' as const } };
const strictP = { settings: { punctuation: 'strict' as const } };

export const CASES: Case[] = [
  // ─── Типографика и пробелы ───
  sentence('transform', 'They did not buy a new car.', 'They did not buy a new car.', 'ok'),
  sentence('transform', 'They did not buy a new car.', 'they did not buy a new car', 'ok'),
  sentence('transform', 'They did not buy a new car.', 'They  did   not buy a new car .', 'ok'),
  sentence('transform', 'They did not buy a new car.', '  They did not buy a new car!  ', 'ok'),
  sentence('transform', 'They did not buy a new car.', 'They did not buy a new car.', 'ok'),
  sentence('transform', 'They did not buy a new car.', 'They didn’t buy a new car.', 'ok'),
  sentence('transform', 'They did not buy a new car.', 'They didn‘t buy a new car.', 'ok'),
  sentence('transform', 'They did not buy a new car.', 'They didnʼt buy a new car.', 'ok'),
  sentence('transform', 'They did not buy a new car.', 'They didn`t buy a new car.', 'ok'),
  sentence('transform', 'They did not buy a new car.', 'They didn´t buy a new car.', 'ok'),
  sentence('transform', 'They did not buy a new car.', "They don ' t buy a new car.", 'wrong'),
  sentence('transform', 'They do not buy new cars.', "They don ' t buy new cars.", 'ok'),
  sentence('transform', 'They do not buy new cars.', 'They do n’t buy new cars.', 'ok'),
  sentence('transform', 'I am tired.', "I 'm tired.", 'ok'),
  sentence('transform', 'I am tired.', "I ' m tired.", 'ok'),
  sentence('transform', 'She said, "Wait."', 'She said “Wait”', 'ok'),
  sentence('transform', 'She said, "Wait."', 'She said «Wait»', 'ok'),
  sentence('transform', 'It was a well-known song.', 'It was a well–known song.', 'ok'),
  sentence('transform', 'Wait...', 'Wait…', 'ok'),
  sentence('transform', 'He came home late.', 'He came home late...', 'ok'),
  sentence('transform', 'He came home late.', 'He came home late?!', 'ok'),
  sentence('transform', 'He came home late.', 'He came home, late.', 'ok'),
  sentence('transform', 'He came home late.', 'He came late home.', 'wrong'),
  sentence('transform', 'He came home late.', 'He come home late.', 'wrong'),

  // ─── Внутренняя пунктуация ───
  sentence('transform', 'When I got home, I called her.', 'When I got home I called her.', 'ok'),
  sentence('transform', 'When I got home, I called her.', 'When I got home; I called her.', 'ok'),
  sentence('transform', 'My brother, who lives in Oslo, is a doctor.', 'My brother who lives in Oslo is a doctor.', 'wrong', strictP),
  sentence('transform', 'My brother, who lives in Oslo, is a doctor.', 'My brother, who lives in Oslo, is a doctor', 'ok', strictP),
  sentence('transform', 'My brother, who lives in Oslo, is a doctor.', 'my brother , who lives in oslo , is a doctor.', 'ok', { ...strictP, note: /Oslo/ }),
  sentence('transform', 'Where do you live?', 'Where do you live', 'wrong', strictP),
  sentence('transform', 'Where do you live?', 'Where do you live?', 'ok', strictP),
  sentence('transform', 'Hello - how are you?', 'Hello how are you?', 'ok'),

  // ─── Регистр и замечания ───
  sentence('transform', 'I went to London on Monday.', 'i went to london on monday', 'ok', { note: /заглавн/ }),
  sentence('transform', 'I went to London on Monday.', 'I went to London on Monday', 'ok', { note: false }),
  sentence('transform', 'I went to London on Monday.', 'I went to london on Monday.', 'ok', { note: /London/ }),
  sentence('transform', 'Tom and I are friends.', 'Tom and i are friends.', 'ok', { note: /«I»/ }),
  sentence('transform', 'I am late.', "i'm late", 'ok', { note: /«I»/ }),
  sentence('transform', 'Where did you go last summer?', 'where did you go last summer', 'ok', { note: /«\?»/ }),
  sentence('order', 'Where did you go last summer?', 'Where did you go last summer', 'ok', { note: /«\?»/ }),
  sentence('order', 'Where did you go last summer?', 'Where did you go last summer?', 'ok', { note: false }),
  sentence('transform', 'He is ready.', 'HE IS READY', 'ok'),

  // ─── Сокращения: однозначные ───
  sentence('transform', 'I am not hungry.', "I'm not hungry.", 'ok'),
  sentence('transform', "I'm not hungry.", 'I am not hungry.', 'ok'),
  sentence('transform', 'You are late.', "You're late.", 'ok'),
  sentence('transform', 'We have finished.', "We've finished.", 'ok'),
  sentence('transform', 'They will call.', "They'll call.", 'ok'),
  sentence('transform', 'She does not know.', "She doesn't know.", 'ok'),
  sentence('transform', 'He is not here.', "He isn't here.", 'ok'),
  sentence('transform', 'He is not here.', "He's not here.", 'ok'),
  sentence('transform', 'They are not here.', "They aren't here.", 'ok'),
  sentence('transform', 'They are not here.', "They're not here.", 'ok'),
  sentence('transform', 'I cannot swim.', "I can't swim.", 'ok'),
  sentence('transform', 'I cannot swim.', 'I can not swim.', 'wrong'),
  sentence('transform', 'I cannot swim.', "I can'not swim.", 'wrong'),
  sentence('transform', 'It will not work.', "It won't work.", 'ok'),
  sentence('transform', 'We shall not fail.', "We shan't fail.", 'ok'),
  sentence('transform', 'You must not run.', "You mustn't run.", 'ok'),
  sentence('transform', 'She has not called.', "She hasn't called.", 'ok'),
  sentence('transform', 'She had not called.', "She hadn't called.", 'ok'),
  sentence('transform', 'I would not go.', "I wouldn't go.", 'ok'),
  sentence('transform', 'I am not going to go.', "I ain't going to go.", 'wrong'),
  sentence('transform', 'I am going to leave.', "I'm gonna leave.", 'wrong'),
  sentence('transform', 'I want to leave.', 'I wanna leave.', 'wrong'),
  sentence('transform', 'Is he not coming?', "Isn't he coming?", 'wrong'),
  sentence('transform', ['Is he not coming?', "Isn't he coming?"], "Isn't he coming?", 'ok'),

  // ─── Сокращения: неоднозначные 's и 'd ───
  sentence('transform', 'It is raining.', "It's raining", 'ok'),
  sentence('transform', 'He has gone.', "He's gone.", 'ok'),
  sentence('transform', 'He has gone.', 'He is gone.', 'wrong'),
  sentence('transform', 'I would go.', "I'd go.", 'ok'),
  sentence('transform', 'I would go.', 'I had go.', 'wrong'),
  sentence('transform', 'I had gone.', "I'd gone.", 'ok'),
  sentence('transform', 'There is a cat.', "There's a cat.", 'ok'),
  sentence('transform', 'What is it?', "What's it?", 'ok'),
  sentence('transform', 'Who is there?', "Who's there?", 'ok'),
  sentence('transform', 'That is mine.', "That's mine.", 'ok'),
  sentence('transform', 'John is here.', "John's here.", 'wrong'),
  sentence('transform', "John's car is red.", 'John is car is red.', 'wrong'),
  sentence('transform', "John's car is red.", "John's car's red.", 'wrong'),
  sentence('transform', 'It is not easy.', "It's not easy.", 'ok'),
  sentence('transform', 'It is not easy.', "It isn't easy.", 'ok'),
  sentence('transform', 'She would have come.', "She'd have come.", 'ok'),
  sentence('transform', 'She would have come.', "She would've come.", 'ok'),
  sentence('transform', 'He is sure that it is true.', "He's sure that it's true.", 'ok'),
  sentence('transform', 'He is sure that it is true.', "He's sure that it is true.", 'ok'),

  // ─── Сокращения: strict ───
  sentence('transform', "I'm tired.", 'I am tired.', 'wrong', strictC),
  sentence('transform', "I'm tired.", 'I’m tired', 'ok', strictC),
  sentence('transform', 'I am tired.', "I'm tired.", 'wrong', strictC),
  sentence('transform', "She doesn't know.", "She doesn't know", 'ok', strictC),
  sentence('transform', "She doesn't know.", 'She does not know.', 'wrong', strictC),
  gap('She ___ (not / know) the answer.', "doesn't", ['does not'], 'wrong', strictC),
  gap('She ___ (not / know) the answer.', "doesn't", ['doesn’t'], 'ok', strictC),

  // ─── Пропуски ───
  gap('I ___ (be) tired.', 'am', ["'m"], 'ok'),
  gap('I ___ (be) tired.', 'am', ['’m'], 'ok'),
  gap('I ___ (be) tired.', 'am', ['am'], 'ok'),
  gap('I ___ (be) tired.', 'am', ['is'], 'wrong'),
  gap('She ___ (not / call) me yesterday.', 'did not call', ["didn't call"], 'ok'),
  gap('She ___ (not / call) me yesterday.', 'did not call', ['didn’t  call'], 'ok'),
  gap('She ___ (not / call) me yesterday.', 'did not call', ['did not called'], 'wrong'),
  gap('She ___ (not / call) me yesterday.', 'did not call', ['Did not call'], 'ok'),
  gap('He ___ (go) home.', ['went'], ['goed'], 'wrong'),
  gap('I saw ___ elephant.', 'an', ['an'], 'ok'),
  gap('I saw ___ elephant.', 'an', ['a'], 'wrong'),
  gap('She plays ___ tennis.', '—', ['-'], 'ok'),
  gap('She plays ___ tennis.', '—', ['—'], 'ok'),
  gap('She plays ___ tennis.', '—', ['–'], 'ok'),
  gap('She plays ___ tennis.', '—', ['the'], 'wrong'),
  gap('She plays ___ tennis.', '—', [''], 'empty'),
  gap('She plays ___ tennis.', '—', ['   '], 'empty'),
  gap('He ___ home.', ['has gone', 'went'], ['went'], 'ok'),
  gap('He ___ home.', 'has gone', ["'s gone"], 'ok'),
  gap('It ___ (rain) now.', 'is raining', ["'s raining"], 'ok'),
  gap('I ___ (go) if I had time.', 'would go', ["'d go"], 'ok'),
  gap('I ___ (go) if I had time.', 'would go', ["'d went"], 'wrong'),
  gap('Look! It ___ .', 'is snowing', ['is snowing.'], 'ok'),
  gap('___ you like it?', 'Do', ['do'], 'ok'),
  gaps('___ you ___ (enjoy) the concert?', [['Did'], ['enjoy']], ['Did', 'enjoy'], 'ok', { gaps: [true, true] }),
  gaps('___ you ___ (enjoy) the concert?', [['Did'], ['enjoy']], ['did', 'enjoy'], 'ok'),
  gaps('___ you ___ (enjoy) the concert?', [['Did'], ['enjoy']], ['Did', 'enjoyed'], 'wrong', {
    gaps: [true, false],
    item: { wrong: [{ answer: ['Did', 'enjoyed'], why: 'Прошедшее время уже есть в did' }] },
    why: 'уже есть в did',
  }),
  gaps('___ you ___ (enjoy) the concert?', [['Did'], ['enjoy']], ['Do', 'enjoy'], 'wrong', { gaps: [false, true] }),
  gaps('___ you ___ (enjoy) the concert?', [['Did'], ['enjoy']], ['Did', ''], 'empty'),
  gaps('If I ___ you, I ___ (go).', [['were', 'was'], ['would go']], ['was', "'d go"], 'ok'),
  gaps('If I ___ you, I ___ (go).', [['were', 'was'], ['would go']], ['were', 'will go'], 'wrong', { gaps: [true, false] }),
  {
    name: 'combos: наборы зависят друг от друга',
    kind: 'gap',
    item: { text: 'I ___ there, and she ___ too.', answer: [], combos: [['was', 'was'], ['have been', 'has been']] },
    input: ['was', 'has been'],
    expect: 'wrong',
    gaps: [true, false],
  },
  {
    name: 'combos: верный набор',
    kind: 'gap',
    item: { text: 'I ___ there, and she ___ too.', answer: [], combos: [['was', 'was'], ['have been', 'has been']] },
    input: ["'ve been", "'s been"],
    expect: 'ok',
  },

  // ─── Выбор и пары ───
  { name: 'choice верный', kind: 'choice', item: { text: 'I ___ him two days ago.', options: ['saw', 'have seen', 'see'], answer: ['saw'] }, input: 'saw', expect: 'ok' },
  {
    name: 'choice неверный с why',
    kind: 'choice',
    item: { text: 'I ___ him two days ago.', options: ['saw', 'have seen', 'see'], answer: ['saw'], why: { 'have seen': 'С ago Present Perfect не употребляется' } },
    input: 'have seen',
    expect: 'wrong',
    why: 'ago',
  },
  { name: 'choice неверный без why', kind: 'choice', item: { text: 'I ___ him.', options: ['saw', 'see'], answer: ['saw'] }, input: 'see', expect: 'wrong' },
  { name: 'choice «—»', kind: 'choice', item: { text: 'She plays ___ tennis.', options: ['a', 'the', '—'], answer: ['—'] }, input: '—', expect: 'ok' },
  { name: 'match верная пара', kind: 'match', item: { text: 'I was cooking dinner', answer: ['when the lights went out.'] }, input: 'when the lights went out.', expect: 'ok' },
  { name: 'match неверная пара', kind: 'match', item: { text: 'I was cooking dinner', answer: ['when the lights went out.'] }, input: 'it started to rain.', expect: 'wrong' },

  // ─── Порядок слов ───
  sentence('order', ['Where did you go last summer?', 'Last summer, where did you go?'], 'Last summer where did you go?', 'ok'),
  sentence('order', 'Where did you go last summer?', 'Where you did go last summer?', 'wrong'),
  sentence('order', 'She never eats meat.', 'She never eats meat', 'ok', { note: false }),
  sentence('order', 'She never eats meat.', 'Never she eats meat.', 'wrong'),
  sentence('order', 'My brother, who lives in Oslo, is a doctor.', 'My brother who lives in Oslo is a doctor.', 'ok', strictP),

  // ─── Переделать предложение ───
  sentence('transform', 'The bridge was built in 1990.', 'The bridge was build in 1990.', 'wrong', { item: { source: 'They built the bridge in 1990.' } }),
  sentence('transform', 'The bridge was built in 1990.', 'The brige was built in 1990.', 'almost', { item: { source: 'They built the bridge in 1990.' } }),
  sentence('transform', 'The bridge was built in 1990.', 'The bridge was built in 1990 year.', 'wrong', { item: { source: 'They built the bridge in 1990.' } }),
  sentence('transform', 'She said that she was tired.', 'She said that she was tierd.', 'almost', { item: { source: 'She said, "I am tired."' } }),
  sentence('transform', 'She said that she was tired.', 'She said that she is tired.', 'wrong', { item: { source: 'She said, "I am tired."' } }),
  sentence('transform', 'She said that she was tired.', 'She said that she were tired.', 'wrong', { item: { source: 'She said, "I am tired."' } }),
  sentence('transform', 'The letter was sent yesterday.', 'The leter was sent yesterday.', 'almost', { item: { source: 'Somebody sent the letter yesterday.' } }),
  sentence('transform', 'The letter was sent yesterday.', 'The letter was sended yesterday.', 'wrong', { item: { source: 'Somebody sent the letter yesterday.' } }),
  sentence('transform', 'The letter was sent yesterday.', 'The letter were sent yesterday.', 'wrong', { item: { source: 'Somebody sent the letter yesterday.' } }),
  sentence('transform', 'He has lived here since 2020.', 'He has lived here since 2020', 'ok', {
    item: { wrong: [{ answer: ['He lives here since 2020.'], why: 'Период продолжается — нужен Present Perfect' }] },
  }),
  sentence('transform', 'He has lived here since 2020.', 'He lives here since 2020.', 'wrong', {
    item: { wrong: [{ answer: ['He lives here since 2020.'], why: 'Период продолжается — нужен Present Perfect' }] },
    why: 'Present Perfect',
  }),

  // ─── Найти ошибку ───
  { name: 'find-error: исправлено', kind: 'find-error', item: { text: 'Did she went to the party?', error: 'went', fix: ['go'] }, input: 'Did she go to the party?', expect: 'ok' },
  { name: 'find-error: без «?» тоже верно', kind: 'find-error', item: { text: 'Did she went to the party?', error: 'went', fix: ['go'] }, input: 'did she go to the party', expect: 'ok' },
  { name: 'find-error: не исправлено', kind: 'find-error', item: { text: 'Did she went to the party?', error: 'went', fix: ['go'] }, input: 'Did she went to the party?', expect: 'wrong' },
  { name: 'find-error: исправлено не то', kind: 'find-error', item: { text: 'Did she went to the party?', error: 'went', fix: ['go'] }, input: 'Does she went to the party?', expect: 'wrong' },
  {
    name: 'find-error: лишнее слово стёрто',
    kind: 'find-error',
    item: { text: 'I am agree with you.', error: 'am', fix: [''] },
    input: 'I agree with you.',
    expect: 'ok',
  },
  {
    name: 'find-error: вариант из also',
    kind: 'find-error',
    item: { text: 'She have two brothers.', error: 'have', fix: ['has'], also: ['She has got two brothers.'] },
    input: 'She has got two brothers.',
    expect: 'ok',
  },
  {
    name: 'find-error: ошибки нет (allow_correct)',
    kind: 'find-error',
    item: { text: 'We went home early.' },
    input: 'We went home early.',
    expect: 'ok',
    allowCorrect: true,
  },
  {
    name: 'find-error: «исправлено» верное предложение',
    kind: 'find-error',
    item: { text: 'We went home early.' },
    input: 'We go home early.',
    expect: 'wrong',
    allowCorrect: true,
  },
  {
    name: 'find-error: опечатка в другом слове',
    kind: 'find-error',
    item: { text: 'Did she went to the party yesterday?', error: 'went', fix: ['go'] },
    input: 'Did she go to the party yesterdy?',
    expect: 'almost',
  },
  {
    name: 'find-error: опечатка в исправлении',
    kind: 'find-error',
    item: { text: 'He buyed a car.', error: 'buyed', fix: ['bought'] },
    input: 'He bougth a car.',
    expect: 'wrong',
  },
  { name: 'пустой ввод предложения', kind: 'transform', item: { answer: ['It is late.'] }, input: '  ', expect: 'empty' },
];

/** Прогоняет таблицу; возвращает описания несовпадений. */
export function runCases(cases: Case[] = CASES): string[] {
  const failures: string[] = [];
  for (const c of cases) {
    const settings = { ...DEFAULT_SETTINGS, ...c.settings };
    const item: Item = { n: 1, answer: [], explain: '', wrong: [], why: {}, ref: [], ...c.item };
    const ex: Exercise = { id: 'case', kind: c.kind, task: '', ref: [], allowCorrect: !!c.allowCorrect, settings, items: [item] };
    const r = check(ex, item, c.input);
    const problems: string[] = [];
    if (r.status !== c.expect) problems.push(`итог ${r.status}, ожидался ${c.expect}`);
    if (c.note === false && r.notes.length) problems.push(`лишние замечания: ${r.notes.join(' ')}`);
    if (c.note instanceof RegExp && !r.notes.some((n) => (c.note as RegExp).test(n))) problems.push(`нет замечания ${c.note} (есть: ${r.notes.join(' ') || '—'})`);
    if (c.gaps && JSON.stringify(r.gaps) !== JSON.stringify(c.gaps)) problems.push(`отметки пропусков ${JSON.stringify(r.gaps)}, ожидались ${JSON.stringify(c.gaps)}`);
    if (c.why && !r.why?.includes(c.why)) problems.push(`нет объяснения «${c.why}» (есть: ${r.why ?? '—'})`);
    if (problems.length) failures.push(`${c.name}: ${problems.join('; ')}`);
  }
  return failures;
}
