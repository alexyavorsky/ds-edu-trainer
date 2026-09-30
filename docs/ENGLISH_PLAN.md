# Английская грамматика: план направления

Направление «Английский» — справочник грамматики (поток С4) и курс для русскоговорящих (поток К2), плюс
формат упражнений не на Python (0.3), который нужен курсу и дальше пригодится другим разделам. Python и Pyodide
здесь не нужны: упражнения проверяет небольшой модуль на TypeScript, общий для сайта и валидатора.

Термины, названия времён, соглашения об оформлении (британский вариант, перевод, формулы) —
[glossary/english.md](glossary/english.md). Этот план им подчиняется.

| Раздел | Зачем |
| --- | --- |
| **Справочник С4** | быстро вспомнить правило; 88 статей A1 → B2 и выборочно C1 |
| **Курс К2** | довести с A1–A2 до B2 по шагам; 79 уроков, объяснения на русском, упражнения с проверкой |
| **Формат 0.3** | упражнения с вводом и выбором ответа, нормализация, прогресс, валидатор, «слепое решение» |

Порядок работ: П2 (платформа) реализует «Нужно от платформы» → С4 → К2 стартует, когда С4 прошёл первую
треть и ревью. Оба раздела при слиянии помечены «бета».

---

## С4. Справочник «Грамматика английского A1 → B2 (+ C1 выборочно)»

Тема справочника `english`: `reference/english/topic.toml` (разделы и порядок статей) и
`reference/english/<slug>.mdx`. Файлов `.py` нет. URL — `/reference/english/<slug>`, id — `english/<slug>`.

### Оглавление — 18 разделов, 88 статей

Уровень — CEFR, с которого содержание статьи нужно (у статей с разделами разных уровней — уровень основной
части; более поздние разделы помечаются внутри статьи). «↔» — контраст (обязательный раздел «Сравнение»),
«→» — связанные статьи. `обзор` — `kind: overview`.

**1. Настоящее время**

| slug | Заголовок | CEFR | Содержание | Контраст / связи |
| --- | --- | --- | --- | --- |
| to-be | Глагол to be | A1 | am/is/are, отрицание и вопрос без do; «I am agree», пропуск to be | → present-simple, there-is |
| present-simple | Present Simple | A1 | формы, -s/-es, do/does; привычки, факты, расписания; have и have got | ↔ present-continuous; → adverbs |
| present-continuous | Present Continuous | A1 | am/is/are + V-ing, правописание -ing; сейчас, временно, изменения | ↔ present-simple |
| present-simple-vs-continuous | Present Simple или Continuous | A2 | выбор по смыслу; глаголы состояния (know, want, like); think/have с двумя значениями | ↔ present-simple, present-continuous |

**2. Прошедшее время**

| slug | Заголовок | CEFR | Содержание | Контраст / связи |
| --- | --- | --- | --- | --- |
| past-simple | Past Simple | A1 | -ed: правописание и произношение, did в вопросах; «Did you went» | ↔ present-perfect-vs-past-simple; → irregular-verbs |
| irregular-verbs | Неправильные глаголы (обзор) | A1 | ~120 глаголов группами по образцу (cut-cut-cut, sing-sang-sung), learnt/learned | → past-simple, present-perfect |
| past-continuous | Past Continuous | A2 | was/were + V-ing; фон и событие, when/while | ↔ past-simple; → narrative-tenses |
| used-to | used to, would, be used to | B1 | прошлые привычки и состояния; be/get used to doing (B2-раздел) | ↔ past-simple; → gerund-infinitive |
| past-perfect | Past Perfect | B1 | had + V3; «раньше другого прошлого», когда он не нужен | ↔ past-simple; → narrative-tenses |
| past-perfect-continuous | Past Perfect Continuous | B2 | had been V-ing: длительность до момента в прошлом | ↔ past-perfect, present-perfect-continuous |
| narrative-tenses | Времена в рассказе о прошлом | B1 | Past Simple, Continuous и Perfect в одном тексте | ↔ past-continuous, past-perfect |

**3. Present Perfect**

| slug | Заголовок | CEFR | Содержание | Контраст / связи |
| --- | --- | --- | --- | --- |
| present-perfect | Present Perfect | A2 | have/has + V3; опыт, результат, just/already/yet/ever/never, for/since; «I live here since…» | ↔ present-perfect-vs-past-simple |
| present-perfect-vs-past-simple | Present Perfect или Past Simple | B1 | назван ли момент, закончен ли период, вопрос When…?; американское употребление | ↔ present-perfect, past-simple |
| present-perfect-continuous | Present Perfect Continuous | B1 | have been V-ing; длительность и следы действия; сравнение с Simple | ↔ present-perfect |

**4. Будущее время**

| slug | Заголовок | CEFR | Содержание | Контраст / связи |
| --- | --- | --- | --- | --- |
| will | will и shall | A2 | решение в момент речи, прогноз, обещание, предложение; почему не «Future Simple» | ↔ going-to |
| going-to | be going to | A2 | намерение, прогноз по признакам | ↔ will |
| future-comparison | Как говорить о будущем: сравнение | B1 | will, going to, Present Continuous (договорённость), Present Simple (расписание) | ↔ will, going-to, present-continuous |
| time-clauses-future | Будущее после when, if, as soon as | B1 | when/after/until/as soon as + Present; «when I will come» | ↔ zero-first-conditional |
| future-continuous-perfect | Future Continuous и Future Perfect | B2 | will be V-ing, will have V3, by + время | ↔ future-comparison |
| future-in-the-past | Будущее в прошедшем | B2 | was going to, would, was about to | → sequence-of-tenses |

**5. Пассив**

| slug | Заголовок | CEFR | Содержание | Контраст / связи |
| --- | --- | --- | --- | --- |
| passive-basics | Пассив: основы | B1 | be + V3, by; когда пассив естественнее; Present и Past Simple | → passive-tenses |
| passive-tenses | Пассив во всех временах | B1 | is being done, has been done, will be done, с модальными (must be done) | → passive-basics |
| passive-reporting | It is said that / He is said to | B2 | безличные конструкции сообщения, to have done | → reporting-verbs |
| causative | have / get something done | B2 | «сделать чужими руками», have something stolen | ↔ passive-basics; → verb-object-infinitive |

**6. Модальные глаголы**

| slug | Заголовок | CEFR | Содержание | Контраст / связи |
| --- | --- | --- | --- | --- |
| modals-overview | Модальные глаголы (обзор) | A2 | общие свойства (без -s, без do, инфинитив без to); карта значений | → все статьи раздела |
| can-could-ability | can, could, be able to | A1 | умение и возможность; be able to в других временах; could и was able to | ↔ permission-requests |
| permission-requests | Разрешение, просьба, предложение | A2 | can/could/may, Would you mind…?, Shall I…? | ↔ can-could-ability |
| must-have-to | must, have to, need | A2 | обязанность; mustn't и don't have to; needn't и didn't need to (B1) | ↔ should-ought-to |
| should-ought-to | should, ought to, had better | A2 | совет и рекомендация | ↔ must-have-to |
| modals-deduction-present | Предположения: must, might, can't | B1 | степень уверенности о настоящем | ↔ modals-perfect |
| modals-perfect | must have done, should have done | B2 | предположения о прошлом, упрёк и сожаление, needn't have done | ↔ modals-deduction-present; → third-conditional |

**7. Условные предложения и нереальность**

| slug | Заголовок | CEFR | Содержание | Контраст / связи |
| --- | --- | --- | --- | --- |
| conditionals-overview | Условные предложения (обзор) | B1 | Zero–Third и Mixed на одной странице: какое время в какой части | → все статьи раздела |
| zero-first-conditional | Zero и First Conditional | A2 | if + Present, will; «If it will rain» | ↔ time-clauses-future, second-conditional |
| second-conditional | Second Conditional | B1 | нереальное настоящее; If I were | ↔ zero-first-conditional |
| third-conditional | Third Conditional | B1 | нереальное прошлое | ↔ mixed-conditionals |
| mixed-conditionals | Mixed Conditionals | B2 | прошлое условие — настоящий результат и наоборот | ↔ second-conditional, third-conditional |
| unless-provided | unless, provided, in case | B2 | as long as, otherwise; in case ≠ if | ↔ zero-first-conditional |
| wish-if-only | wish, if only, would rather | B1 | wish + Past / Past Perfect / would; would rather, it's time (B2-раздел) | ↔ second-conditional, third-conditional |

**8. Косвенная речь**

| slug | Заголовок | CEFR | Содержание | Контраст / связи |
| --- | --- | --- | --- | --- |
| sequence-of-tenses | Согласование времён | B1 | сдвиг назад, когда не сдвигать, here → there, tomorrow → the next day | → reported-statements |
| reported-statements | Косвенная речь: утверждения | B1 | say и tell, that | ↔ sequence-of-tenses |
| reported-questions | Косвенная речь: вопросы и просьбы | B1 | if/whether, прямой порядок слов; ask/tell somebody to do | ↔ indirect-questions |
| reporting-verbs | Глаголы передачи речи | B2 | suggest, recommend, deny, admit, refuse, promise + конструкции | → gerund-infinitive |

**9. Существительные и артикли**

| slug | Заголовок | CEFR | Содержание | Контраст / связи |
| --- | --- | --- | --- | --- |
| plural-nouns | Множественное число | A1 | -s/-es/-ies, people, children; news, jeans | → countable-uncountable |
| countable-uncountable | Исчисляемые и неисчисляемые | A2 | advice, information, a piece of; a coffee и coffee | → much-many-a-lot |
| possessive-s | Притяжательный падеж | A2 | 's, s', of; my friend's, a friend of mine | → personal-pronouns |
| articles-a-the | Артикли a/an и the | A1 | первое упоминание, единственный в своём роде, a/an по звуку | ↔ zero-article |
| zero-article | Без артикля | A2 | множественное и неисчисляемое в общем смысле, go to school, приёмы пищи | ↔ articles-a-the, articles-generic |
| articles-names | Артикли с названиями | B1 | страны, реки, горы, улицы, организации, the + фамилия | → articles-a-the |
| articles-generic | Артикли в обобщениях | B2 | the tiger / tigers / a tiger, the rich, play the piano | ↔ zero-article |

**10. Количество**

| slug | Заголовок | CEFR | Содержание | Контраст / связи |
| --- | --- | --- | --- | --- |
| some-any-no | some, any, no | A1 | в утверждении, вопросе, отрицании; some в просьбах и предложениях | → indefinite-pronouns |
| much-many-a-lot | much, many, a lot of, a few, a little | A1 | с исчисляемыми и неисчисляемыми; few и a few | → countable-uncountable |
| quantifiers | all, both, each, every, either, neither | B1 | none of, each of; согласование с глаголом | ↔ some-any-no |

**11. Местоимения**

| slug | Заголовок | CEFR | Содержание | Контраст / связи |
| --- | --- | --- | --- | --- |
| personal-pronouns | Личные, притяжательные, указательные | A1 | I/me, my/mine, this/that/these/those | → possessive-s, reflexive-pronouns |
| reflexive-pronouns | myself, each other | A2 | by myself; глаголы без -self (feel, relax, meet) | → personal-pronouns |
| indefinite-pronouns | somebody, anything, nowhere | A2 | сочетания some/any/no/every; одно отрицание | → some-any-no, negatives |
| it-there | it и there; one и ones | B1 | формальное подлежащее; «Is raining»; the red one | ↔ there-is |

**12. Прилагательные и наречия**

| slug | Заголовок | CEFR | Содержание | Контраст / связи |
| --- | --- | --- | --- | --- |
| adjectives | Прилагательные | A2 | место, bored/boring, порядок нескольких прилагательных (B1-раздел) | ↔ adverbs |
| adverbs | Наречия | A1 | -ly, good/well, hard/hardly; частота и место в предложении | ↔ adjectives |
| comparatives | Степени сравнения | A2 | -er/-est, more/most, исключения, than, the | → comparison-structures |
| comparison-structures | Сравнительные конструкции | B1 | as…as, not as…as, the more…the more, much/far + сравнительная | ↔ comparatives |
| too-enough-so-such | too, enough, so, such | B1 | too/enough + to; so + прилагательное, such (a) + существительное | → adjectives |

**13. Предлоги**

| slug | Заголовок | CEFR | Содержание | Контраст / связи |
| --- | --- | --- | --- | --- |
| prepositions-time | Предлоги времени | A1 | in/on/at, for/during, by/until | ↔ prepositions-place |
| prepositions-place | Предлоги места и движения | A1 | in/on/at, to/into/towards, arrive in/at | ↔ prepositions-time |
| dependent-prepositions | Предлоги после слов | B1 | good at, depend on, married to; discuss/enter без предлога | → gerund-infinitive |

**14. Глагольные конструкции**

| slug | Заголовок | CEFR | Содержание | Контраст / связи |
| --- | --- | --- | --- | --- |
| gerund-infinitive | Герундий или инфинитив | B1 | enjoy doing / want to do; -ing после предлогов | ↔ verbs-change-meaning |
| verbs-change-meaning | stop doing или stop to do | B2 | stop, remember, forget, try, regret, mean | ↔ gerund-infinitive |
| verb-object-infinitive | want somebody to do; make и let | A2 | «I want that you…»; make/let + инфинитив без to; help | → causative |
| infinitive-purpose | Цель: to, in order to, so that | B1 | «for to», for + существительное | → linking-cause-result |

**15. Фразовые глаголы**

| slug | Заголовок | CEFR | Содержание | Контраст / связи |
| --- | --- | --- | --- | --- |
| phrasal-verbs | Фразовые глаголы: как устроены | B1 | глагол + частица; разделяемые и нет; turn it off, не «turn off it» | → phrasal-verbs-common |
| phrasal-verbs-common | Частые фразовые глаголы (обзор) | B1 | ~50 глаголов по частицам up/out/off/on/down/back с примерами | → phrasal-verbs |

**16. Предложение и вопросы**

| slug | Заголовок | CEFR | Содержание | Контраст / связи |
| --- | --- | --- | --- | --- |
| word-order | Порядок слов | A1 | подлежащее — сказуемое — дополнение, место обстоятельств, повелительное наклонение, let's | → adverbs, questions |
| there-is | there is / there are | A1 | «In the room is a table»; there was/has been | ↔ it-there |
| negatives | Отрицание | A1 | not, no, never; одно отрицание в предложении | → indefinite-pronouns |
| questions | Вопросы | A1 | общие и специальные, вспомогательный глагол, порядок слов | ↔ subject-questions |
| subject-questions | Вопросы к подлежащему | A2 | Who called? What happened? — без do | ↔ questions |
| indirect-questions | Косвенные вопросы | B1 | Could you tell me where…? — прямой порядок слов | ↔ reported-questions |
| question-tags | Разделительные вопросы | B1 | …, isn't it? / …, do you?; I am → aren't I | → short-answers |
| short-answers | Краткие ответы, so do I | A2 | Yes, I do; So do I / Neither do I; I think so | → question-tags |

**17. Сложное предложение**

| slug | Заголовок | CEFR | Содержание | Контраст / связи |
| --- | --- | --- | --- | --- |
| relative-clauses-defining | Определительные придаточные | B1 | who/which/that/whose/where, пропуск that | ↔ relative-clauses-non-defining |
| relative-clauses-non-defining | Описательные придаточные | B2 | запятые, нельзя that, which о всём предложении | ↔ relative-clauses-defining |
| linking-cause-result | Причина и следствие | A2 | because, so, because of, as, since | → infinitive-purpose |
| linking-contrast | Противопоставление | B1 | but, although, even though, despite, in spite of, however | ↔ linking-cause-result |
| participle-clauses | Причастные обороты | C1 | Having finished…, Seen from…; «висящее» причастие | → relative-clauses-defining |
| emphasis | Выделение: It was… that, What I need is… | C1 | расщеплённые предложения, усилительное do | → inversion |
| inversion | Инверсия | C1 | Never have I…, Not only… but; Had I known, Should you… | → conditionals-overview, emphasis |

**18. Итоги**

| slug | Заголовок | CEFR | Содержание | Контраст / связи |
| --- | --- | --- | --- | --- |
| tenses-overview | Все времена на одной странице (обзор) | B1 | формы, употребление, слова-маркеры, таблица сравнения | → все статьи о временах |
| common-mistakes | Частые ошибки русскоговорящих (обзор) | A2 | ~40 ошибок коротко, каждая со ссылкой на статью | → по ссылкам |
| british-american | Британский и американский (обзор) | B2 | have got, Present Perfect с just, collective nouns, gotten, shall | → present-perfect-vs-past-simple |

### Индекс по уровням

| Уровень | Статей | Разделы с наибольшей долей |
| --- | --- | --- |
| A1 | 18 | настоящее, базовое прошедшее, артикли, местоимения, предлоги, вопросы |
| A2 | 22 | Present Perfect, будущее, модальные, сравнение, исчисляемость |
| B1 | 32 | пассив, условные, косвенная речь, глагольные конструкции, придаточные |
| B2 | 13 | сложные времена, modals perfect, mixed conditionals, reporting verbs |
| C1 | 3 | причастные обороты, выделение, инверсия |

Индекс строится автоматически из `cefr` во frontmatter: страница темы показывает две вкладки — «По темам»
(разделы topic.toml) и «По уровням» (A1 → C1, внутри — в порядке оглавления); на обеих статьи с плашкой уровня.
Фильтр по уровню — через адрес `?level=b1` (только отбор списка, никакого выполнения).

### Формат статьи

Файл: `reference/english/<slug>.mdx`. Frontmatter:

```yaml
---
title: Present Perfect
cefr: A2                          # A1 | A2 | B1 | B2 | C1 — обязательно
level: basic                      # выводится из cefr (A1–A2 basic, B1–B2 medium, C1 advanced) — для общих списков
summary: Прошлое действие, важное сейчас: опыт, результат, незаконченный период.
kind: article                     # article | contrast («X или Y») | overview
requires: [english/past-simple]   # «Нужно знать», не больше 3, уровень не выше своего
related: [english/present-perfect-continuous]
contrasts: [english/present-perfect-vs-past-simple]   # есть — обязателен раздел «Сравнение»
patterns: [have done, has been, already, yet, since]  # для поиска (вместо functions)
---
```

Разделы по порядку (валидатор проверяет):

| Раздел | article | contrast | overview |
| --- | --- | --- | --- |
| `## Коротко` — 2–5 пунктов | обяз. | обяз. | обяз. |
| `## Формулы` — `<Formula>` | если есть формы | — | по желанию |
| `## Когда употребляется` — `###` на каждый случай, в каждом `<Examples>` | обяз. | — | — |
| `## Как выбрать` — правило выбора, таблица | — | обяз. | — |
| свои разделы («Правописание -ing», «Слова-маркеры») | по желанию | по желанию | свободно |
| `## Частые ошибки` — не меньше 3 `<Fix>` | обяз. | обяз. | по желанию |
| `## Сравнение` — таблица + пары примеров | если `contrasts` | — | — |
| `## Проверьте себя` — `<Practice>` (вторая очередь, см. 0.3) | по желанию | по желанию | — |

Объём статьи — 500–1200 слов, в обзорах больше; примеров с переводом не меньше 8 (в обзоре — не меньше 5).
Разделы уровнем выше статьи начинаются с плашки: `### Would rather <Level>B2</Level>`.

Компоненты (без import, их передаёт страница):

- `<Examples>` — список примеров с переводом. Одна строка — пример: английский, ` — `, русский.
  Изучаемая форма — **жирным** (целыми словами), вариант — `(амер.)`/`(брит.)` в конце английской части.
- `<Formula>` — строки формул; первая колонка `+`, `−`, `?` (утверждение, отрицание, вопрос) или без неё.
  Обозначения — только из глоссария (S, V, V-s, V-ing, V2, V3, to V, …) и английские слова.
- `<Fix wrong="…" right="…">` — «ошибка → правильно» с объяснением в теле; отличающиеся слова подсвечиваются
  автоматически (разница по словам), поэтому в атрибутах разметки нет.
- `<Level>B2</Level>` — плашка уровня внутри статьи.
- Таблица Markdown для сравнений; схемы-линии времени — вторая очередь (`TimelineDiagram`, по образцу схем
  справочника: HTML/CSS, перестраивается на телефоне).

```mdx
## Формулы

<Formula>
+ S + have/has + V3
− S + haven't/hasn't + V3
? Have/Has + S + V3?
</Formula>

## Когда употребляется

### Опыт: «когда-нибудь в жизни»

<Examples>
- **I've been** to Rome twice. — Я был в Риме дважды.
- **Have** you ever **tried** sushi? — Ты когда-нибудь пробовал суши?
</Examples>

## Частые ошибки

<Fix wrong="I live here since 2020." right="I have lived here since 2020.">
Период начался в прошлом и продолжается: по-русски «живу с 2020 года», по-английски — Present Perfect.
</Fix>
```

### Что проверяет валидатор (`node scripts/validate_english.ts --reference`)

- **Схема:** поля frontmatter, `cefr` из списка, `level` согласован с `cefr`, `kind`; slug в topic.toml ровно
  один раз, файл есть (с `--strict` — ошибка, если статья оглавления не написана); имя `index` запрещено.
- **Ссылки:** `requires`, `related`, `contrasts`, ссылки `/reference/english/…` в тексте существуют;
  `requires` — не больше 3 и не выше уровнем; контраст симметричен (A ↔ B — предупреждение, если у B нет A).
- **Разделы:** набор и порядок по таблице выше для своего `kind`; «Сравнение» есть, если есть `contrasts`.
- **Компоненты:** в `<Examples>` у каждой строки есть ` — ` и перевод с кириллицей, английская часть
  заканчивается знаком препинания, `**` — только целыми словами; примеров не меньше нормы; `<Formula>` — только
  допустимые обозначения; у `<Fix>` `wrong` ≠ `right` и тело не пустое; `<Level>` — не ниже уровня статьи.
- **Оформление:** в английском тексте — прямой апостроф `'`, в русском — «ёлочки»; нет «Future Simple» и
  других нежелательных вариантов из глоссария вне раздела, где они объясняются (список слов — в глоссарии).
- **Индекс:** печатает число статей по уровням и разделам — сверка с этим планом.

### Объём, проверка, готовность

- **Ориентир:** 88 статей, ~70 000 слов, ≥ 700 примеров с переводом, ≥ 250 «ошибка → правильно».
- **Проверка:** валидатор (`--strict` в CI), ревью `grammar-reviewer` (правила, примеры, переводы — каждый
  пример, а не выборка), ревью `stream-reviewer` (язык, ясность, согласованность с глоссарием).
- **Готово, когда:** все 88 статей в оглавлении написаны, валидатор зелёный, замечания ревью уровня
  «ошибка» и «важно» исправлены и перепроверены, отчёт `docs/reports/ref-english.md`, пометка «бета».
- **Первая треть для раннего ревью (~30 статей):** разделы 1–4 целиком (все времена до будущего: 20 статей,
  включая contrast и overview `irregular-verbs`) и раздел 9 «Существительные и артикли» (7) + `modals-overview`,
  `must-have-to`, `common-mistakes` (начать список). Это все виды статей и все компоненты — ревью проверит формат
  до массового написания; К2 после этого может начинать модули 1–3.

---

## К2. Курс «Английская грамматика A1–A2 → B2» для русскоговорящих

Курс `english` (`code = "en"`, `reference = "english"`, `runtime = "none"`): `courses/english/…`, как курсы
NumPy и pandas, но у урока вместо `lesson.py` — `exercises.toml` (формат — в разделе 0.3).

### Педагогика

- **Вход:** A1–A2 — человек учил английский в школе, читает простые тексты, путается в формах. Первый урок —
  входная проверка (30 пунктов A1–B1): советует, с какого модуля начать. Уроки не блокируются.
- **Язык:** объяснения — по-русски, коротко; примеры — по-английски с переводом; термины — по глоссарию.
  Правило в уроке — рабочий минимум с опорой на русский («по-русски — живу, по-английски — have lived»),
  подробности — ссылкой «Подробнее в справочнике» на статью С4.
- **Урок** — 15 минут (10–20): короткое объяснение → примеры → 4–6 упражнений по 5–8 пунктов (25–40 пунктов).
  Упражнения идут от узнавания к производству: `choice` → `gap` → `order`/`transform` → `find-error`.
  В уроке не меньше трёх видов упражнений.
- **Одна тема за раз.** Упражнение ссылается на статьи (`ref`); каждая должна быть введена этим уроком или
  раньше (поле `reference` уроков) — валидатор проверяет, как `introduces` в курсах Python.
- **Повторение, три уровня:**
  1. последнее упражнение урока «Вперемешку» — 5–8 пунктов, из них 2–3 по темам прошлых уроков;
  2. урок повторения в конце модуля (`kind = "review"`, 15–20 минут, 5–8 упражнений): ~70 % пунктов — темы
     модуля, ~30 % — прошлых модулей, с упором на те, что давно не встречались;
  3. контрольная в конце уровня (`kind = "test"`).
  Валидатор печатает для каждой статьи, в каких уроках после введения она встречается, и предупреждает, если
  тема ни разу не повторилась в следующих двух модулях.
- **Контрольная** — 40 пунктов, все виды упражнений, 25–30 минут, без подсказок и без проверки по ходу:
  «Завершить» → балл, у каждого пункта ваш ответ, верный и объяснение. Зачёт — 80 %. Можно пересдать; хранится
  лучший результат. В контрольной — только темы уровня и ниже.
- **Типичные ошибки русскоговорящих** — в объяснениях и в `wrong`/`why` упражнений: проверка узнаёт заранее
  предусмотренную ошибку и объясняет её конкретно («после did — начальная форма»).

### Программа — 14 модулей, 79 уроков (65 обучающих, 10 повторений, 3 контрольные, входная проверка)

Слаг урока — адрес `/courses/english/<слаг>`, id — `en-<слаг>`. В скобках — статьи С4 (`english/…`).

**0. Старт**
- `start` — Как устроен курс и входная проверка (placement, по желанию)

**Уровень A1–A2**

1. **Настоящее время**
   - `to-be` — Глагол to be (to-be)
   - `present-simple` — Present Simple: утверждение, окончание -s (present-simple)
   - `do-does` — Вопросы и отрицания с do/does; как часто (present-simple, questions, negatives, adverbs, word-order)
   - `present-continuous` — Present Continuous (present-continuous)
   - `simple-or-continuous` — Simple или Continuous; глаголы состояния (present-simple-vs-continuous)
   - `review-present` — Повторение (review)
2. **Существительные, артикли, местоимения**
   - `there-is` — there is / there are, множественное число (there-is, plural-nouns)
   - `a-an-the` — a/an и the (articles-a-the)
   - `no-article` — Когда артикль не нужен (zero-article)
   - `countable` — Исчисляемые и неисчисляемые; some/any (countable-uncountable, some-any-no, indefinite-pronouns)
   - `how-much` — much, many, a lot of, a few, a little (much-many-a-lot)
   - `pronouns` — me, my, mine, myself; 's (personal-pronouns, reflexive-pronouns, possessive-s)
   - `review-nouns` — Повторение (review)
3. **Прошедшее время**
   - `past-simple` — Past Simple: правильные глаголы (past-simple)
   - `irregular` — Неправильные глаголы (irregular-verbs)
   - `did` — Вопросы и отрицания в прошедшем (past-simple, questions)
   - `past-continuous` — Past Continuous: when и while (past-continuous)
   - `used-to` — used to (used-to)
   - `review-past` — Повторение (review)
4. **Будущее, сравнение, вопросы**
   - `going-to-will` — going to и will (going-to, will)
   - `plans` — Договорённости и расписания (future-comparison)
   - `comparatives` — Сравнение: bigger, the biggest (comparatives)
   - `adjectives-adverbs` — bored/boring, good/well (adjectives, adverbs)
   - `who-what` — Вопросы к подлежащему (questions, subject-questions)
   - `in-on-at` — Предлоги времени и места (prepositions-time, prepositions-place)
   - `test-a2` — **Контрольная A1–A2** (test)

**Уровень B1**

5. **Present Perfect**
   - `present-perfect` — Present Perfect: опыт и результат (present-perfect)
   - `for-since` — just, already, yet; for и since (present-perfect)
   - `perfect-or-past` — Present Perfect или Past Simple (present-perfect-vs-past-simple)
   - `been-doing` — Present Perfect Continuous (present-perfect-continuous)
   - `past-perfect` — Past Perfect и рассказ о прошлом (past-perfect, narrative-tenses)
   - `review-perfect` — Повторение (review)
6. **Модальные глаголы**
   - `can-could` — can, could, be able to; просьбы (can-could-ability, permission-requests)
   - `must-have-to` — must, have to, mustn't, don't have to (must-have-to)
   - `should` — should, ought to, had better (should-ought-to, modals-overview)
   - `might-must` — Предположения: must, might, can't (modals-deduction-present)
   - `review-modals` — Повторение (review)
7. **Условия и будущее**
   - `if-when` — First Conditional; when и as soon as (zero-first-conditional, time-clauses-future)
   - `second-conditional` — Second Conditional (second-conditional)
   - `third-conditional` — Third Conditional (third-conditional, conditionals-overview)
   - `wish` — wish и if only (wish-if-only)
   - `future-choice` — Какое будущее выбрать (future-comparison, will, going-to)
   - `review-if` — Повторение (review)
8. **Пассив и косвенная речь**
   - `passive` — Пассив: Present и Past Simple (passive-basics)
   - `passive-tenses` — Пассив в других временах и с модальными (passive-tenses)
   - `reported` — Косвенная речь и согласование времён (reported-statements, sequence-of-tenses)
   - `reported-questions` — Косвенные вопросы и просьбы (reported-questions, indirect-questions)
   - `review-passive` — Повторение (review)
9. **Глагольные конструкции и придаточные**
   - `gerund-or-to` — enjoy doing или want to do (gerund-infinitive)
   - `want-you-to` — want you to, make и let; цель (verb-object-infinitive, infinitive-purpose)
   - `relative` — who, which, that, whose, where (relative-clauses-defining)
   - `although` — although, despite, because of (linking-contrast, linking-cause-result)
   - `phrasal` — Фразовые глаголы (phrasal-verbs, phrasal-verbs-common)
   - `tags` — Разделительные вопросы, so do I (question-tags, short-answers)
   - `test-b1` — **Контрольная B1** (test)

**Уровень B2**

10. **Времена B2**
    - `future-perfect` — Future Continuous и Future Perfect (future-continuous-perfect)
    - `had-been-doing` — Past Perfect Continuous (past-perfect-continuous)
    - `be-used-to` — be used to и get used to (used-to)
    - `was-going-to` — Будущее в прошедшем (future-in-the-past)
    - `all-tenses` — Все времена: выбор формы (tenses-overview)
    - `review-tenses` — Повторение (review)
11. **Модальность и условия B2**
    - `must-have-been` — Предположения о прошлом (modals-perfect)
    - `should-have` — should have, needn't have (modals-perfect, must-have-to)
    - `mixed` — Mixed Conditionals (mixed-conditionals)
    - `unless` — unless, provided, in case (unless-provided)
    - `would-rather` — would rather, it's time, wish + Past Perfect (wish-if-only)
    - `review-b2-if` — Повторение (review)
12. **Пассив и передача слов**
    - `is-said-to` — It is said that / He is said to (passive-reporting)
    - `have-done` — have something done (causative)
    - `reporting-verbs` — suggest, deny, admit, refuse (reporting-verbs)
    - `stop-doing` — stop doing или stop to do (verbs-change-meaning)
    - `review-reporting` — Повторение (review)
13. **Сложное предложение и точность**
    - `non-defining` — Описательные придаточные (relative-clauses-non-defining)
    - `articles-names` — Артикли с названиями и в обобщениях (articles-names, articles-generic)
    - `quantifiers` — both, either, neither, each, every (quantifiers)
    - `so-such` — so, such, too, enough; as…as (too-enough-so-such, comparison-structures)
    - `prepositions-after` — Предлоги после слов (dependent-prepositions)
    - `test-b2` — **Итоговая контрольная B2** (test)

Статьи только для справочника (в курсе — ссылкой): C1 (participle-clauses, emphasis, inversion),
`british-american`, `common-mistakes`, `it-there`. `module.toml` получает поле `level` («A1–A2», «B1», «B2») —
страница курса группирует модули по уровням. В последнем модуле уровня отдельного повторения нет — его роль
играет контрольная.

### Формат урока

```
courses/english/course.toml          title, code = "en", reference = "english", runtime = "none", beta = true, …
courses/english/NN-<модуль>/module.toml    title, summary, outcomes, level
courses/english/NN-<модуль>/NN-<урок>/
  lesson.mdx                          текст урока и места упражнений: <Practice id="…" />
  exercises.toml                      упражнения урока (0.3)
```

`lesson.mdx` — как у курсов Python (`id`, `title`, `summary`, `minutes`, `kind`, `reference`), без `introduces`,
`data`, `packages`; `kind`: `lesson | review | test | placement`. В тексте — Markdown и компоненты справочника
(`Examples`, `Formula`, `Fix`) плюс `Note`, `Mistake` из курсов и `<Practice id>` на отдельной строке.
Порядок `<Practice>` в lesson.mdx совпадает с порядком `[[exercise]]` в exercises.toml (проверяется).
Существующий `<Quiz>` (вопрос по-русски о правиле) допустим, но в прогресс не входит — как в курсах Python.

### Объём, проверка, готовность

- **Ориентир:** 79 уроков, ~400 упражнений, ~2600 пунктов; контрольные 3 × 40, входная — 30 пунктов.
- **Проверка:** `node scripts/validate_english.ts --courses --strict`; «слепое решение» каждого модуля
  (ниже) — совпадение ≥ 97 % с первого прогона, каждое расхождение разобрано; ревью `grammar-reviewer`
  (ключи, допустимые ответы, объяснения) и `stream-reviewer` («глазами ученика A2»).
- **Готово, когда:** все уроки программы есть, валидатор зелёный, слепое решение всех модулей разобрано,
  замечания ревью «ошибка»/«важно» исправлены, отчёт `docs/reports/course-english.md`, пометка «бета».
- **Первая треть для раннего ревью:** уровень A1–A2 целиком — модули 0–4 (27 уроков, включая контрольную A2):
  все виды упражнений, повторения, контрольная и входная проверка — весь формат 0.3 в деле. Ревью и слепое
  решение этой трети — до написания B1.

---

## 0.3. Формат упражнений не на Python

### Решение: `exercises.toml` рядом с `lesson.mdx`

Упражнения хранятся в TOML-файле урока, а lesson.mdx только ставит их на место (`<Practice id="…" />`) —
так же, как `lesson.py` хранит код, а `<Exercise id>` его размещает.

Почему не компоненты в MDX (`<Gap answer="…">`):
- **Ключи — данные, а не разметка.** Валидатор, слепая выгрузка, повторения и контрольные читают TOML одной
  функцией (`smol-toml` уже в зависимостях) без разбора MDX. Правило курсов «атрибуты — только строки в кавычках»
  не выдерживает списков допустимых ответов, пар и таблиц объяснений.
- **Кавычки и апострофы.** Английский полон `'`; в TOML это обычный символ в строке `"…"`, в атрибутах MDX —
  источник ошибок экранирования.
- **Текст урока остаётся текстом:** автор читает объяснение без простыней ключей.

Почему TOML, а не YAML: весь репозиторий на TOML (meta, course, topic), а YAML 1.1 превращает ответы
`no`, `yes`, `on`, `off` в логические значения — для упражнений по английскому это реальная ловушка
(«— Do you smoke? — No, I don't.»).

Markdown внутри строк (`*курсив*`, `**жирный**`, `` `код` ``) допустим в `task`, `explain`, `why`, `hint` —
сайт рендерит его тем же процессором, что и уроки.

### Виды упражнений

| kind | Что делает ученик | Поля пункта | Когда |
| --- | --- | --- | --- |
| `gap` | вписывает слово(а) в пропуск(и) `___` | `text`, `answer` или `gaps`/`combos` | формы: времена, артикли, предлоги |
| `choice` | выбирает один вариант | `text`, `options`, `answer`, `why` | узнавание, выбор между похожими |
| `order` | собирает предложение из слов (кнопки-фишки; можно и набрать) | `words`, `answer` | порядок слов, вопросы |
| `transform` | переписывает предложение по заданию | `source`, `answer`, `start`?, `keyword`?, `max_words`? | пассив, косвенная речь, отрицания |
| `find-error` | находит неверное слово и исправляет | `text`, `error`, `fix`, `also`? | типичные ошибки |
| `match` | соединяет начала и концы (или форму и значение) | на уровне упражнения: `pairs` | условные, фразовые глаголы |
| `translate` | переводит короткое предложение с русского | `source`, `answer` (≥ 3 варианта) | **вторая очередь**: только после опыта слепого решения |

Классификация («исчисляемое или нет», «a / an / the / —») — это `choice` с общими `options` на уровне
упражнения. Вопрос о правиле по-русски — существующий `<Quiz>`.

### Поля

Упражнение (`[[exercise]]`): `id` (kebab-case, уникален в уроке), `kind`, `task` (задание по-русски),
`title`?, `ref` (статьи С4, ≥ 1), `hint`?, `options`? (общие для `choice`), `explain` (для `match`; у других
видов — у пунктов), настройки нормализации `contractions`? и `punctuation`?.

Пункт (`[[exercise.item]]`):
- `answer` — список допустимых ответов; **первый — основной** (его показывает «Показать ответ» и контрольная,
  остальные — «Также верно: …» после ответа). Для `choice` — строка, один из `options`.
- `gaps` — несколько пропусков, независимых друг от друга: `[["were", "was"], ["would go"]]`.
  `combos` — если пропуски зависят друг от друга: список полных наборов `[["were", "would go"], …]`.
- `explain` — почему верно (**обязательно**); показывается после верного ответа и после «Показать ответ».
- `wrong` — заранее предусмотренные неверные ответы: `{ answer = "…" | [пропуски], why = "…" }`; `why` — для
  неверных вариантов `choice`: `{ "вариант" = "почему нет" }`.
- `hint` — подсказка; не содержит ответа (проверяется).
- `ref` — статья, если отличается от упражнения (для повторений и контрольных — обязательно у каждого пункта).
- «Пустой ответ» (артикль не нужен) пишется как `"—"`; ученик вводит `-` или `—`. Пустой ввод не проверяется:
  «впишите ответ или «—», если ничего не нужно».

### Пример `exercises.toml`

```toml
[[exercise]]
id = "regular-ed"
kind = "gap"
title = "Окончание -ed"
task = "Поставьте глагол в скобках в Past Simple."
ref = ["english/past-simple"]

  [[exercise.item]]
  text = "___ you ___ (enjoy) the concert?"
  gaps = [["Did"], ["enjoy"]]
  explain = "В вопросе прошедшее время показывает did, а смысловой глагол остаётся в начальной форме."
  wrong = [{ answer = ["Did", "enjoyed"], why = "Прошедшее время уже есть в did — второй раз его не показывают." }]

  [[exercise.item]]
  text = "She ___ (not / call) me yesterday."
  answer = ["did not call"]            # didn't call засчитывается сам — см. «Сокращения»
  explain = "Отрицание: did not (didn't) + начальная форма."

[[exercise]]
id = "choose-form"
kind = "choice"
task = "Выберите верный вариант."
ref = ["english/past-simple", "english/present-perfect-vs-past-simple"]

  [[exercise.item]]
  text = "I ___ him two days ago."
  options = ["saw", "have seen", "see"]
  answer = "saw"
  explain = "Ago называет законченный момент в прошлом — нужен Past Simple."
  why = { "have seen" = "С ago Present Perfect не употребляется: момент в прошлом назван.", "see" = "Two days ago — прошлое, а see — настоящее время." }

[[exercise]]
id = "make-questions"
kind = "order"
task = "Составьте вопрос из слов."
ref = ["english/questions"]

  [[exercise.item]]
  words = ["go", "where", "you", "did", "last summer"]     # показываются в этом порядке
  answer = ["Where did you go last summer?", "Last summer, where did you go?"]
  explain = "Вопросительное слово → did → подлежащее → глагол в начальной форме."

[[exercise]]
id = "spot-it"
kind = "find-error"
task = "В каждом предложении одна ошибка. Найдите и исправьте её."
ref = ["english/past-simple"]

  [[exercise.item]]
  text = "Did she went to the party?"
  error = "went"
  fix = ["go"]
  explain = "После did глагол стоит в начальной форме: Did she go…?"

[[exercise]]
id = "halves"
kind = "match"
task = "Соедините начало и конец предложения."
ref = ["english/past-continuous"]
explain = "Past Continuous — длительный фон, Past Simple — короткое событие, которое его прерывает."
pairs = [
  ["I was cooking dinner", "when the lights went out."],
  ["While we were walking home,", "it started to rain."],
  ["She broke her arm", "while she was skiing."],
]
```

(Пример разобран `smol-toml` при подготовке плана.)

Особенности видов:
- `order`: фишки показываются в порядке автора (автор сам перемешивает; порядок одинаков с JS и без, на
  сервере и в браузере). Фишка может быть из нескольких слов (`"last summer"`). Конечный знак препинания
  добавляется из ответа, запятые внутри при проверке не учитываются.
- `transform`: `start` — данное начало (ученик дописывает, начало уже в поле); `keyword` — слово, которое
  нужно использовать без изменений; `max_words` — предел слов в дописанной части.
- `find-error`: ученик нажимает на слово (или выделяет несколько подряд), в поле появляется выделенное —
  исправляет его (можно стереть — лишнее слово). Засчитывается, если **получившееся предложение** совпадает
  с одним из верных: `text`, где `error` заменён на любой из `fix`, плюс полные предложения из `also`.
  Поэтому ошибку «пропущено слово» можно исправить, выделив соседнее слово. Альтернатива для клавиатуры и
  экранных читалок — «Исправить целиком»: поле с предложением для правки. Упражнение с `allow_correct = true`
  может содержать верные предложения — кнопка «Ошибки нет».
- `match`: 3–6 пар; правые части перемешаны детерминированно (от `id`); на телефоне — выбор из списка.

### Нормализация и сравнение

Одна функция `check(item, input)` в `src/lib/english/check.ts`; её используют страница, валидатор и
слепая проверка — поведение одинаково везде. Ввод ученика и допустимые ответы проходят одни шаги:

1. **Юникод:** NFC; неразрывные и прочие пробелы — обычный пробел.
2. **Типографика:** `’ ‘ ʼ ′ ´` и обратный апостроф → `'`; `“ ” „ « » ″` → `"`; `– —` между словами → `-`;
   `…` → `...`.
3. **Пробелы:** обрезать по краям, несколько подряд → один; убрать пробелы вокруг апострофа внутри слова
   (`don ' t` → `don't`) и перед `, . ! ? ; :`.
4. **Конечная пунктуация:** `. ! ? ...` в конце — отбрасываются. Кавычки — отбрасываются.
5. **Внутренняя пунктуация** (`punctuation`): по умолчанию `"loose"` — запятые, `;`, `:`, тире не учитываются;
   `"strict"` — учитываются (описательные придаточные, where пунктуация и есть тема).
6. **Регистр:** сравнение без учёта регистра.
7. **Сокращения** (`contractions`): по умолчанию `"equal"` — краткая и полная форма равны; `"strict"` —
   сравнение как написано (упражнения на сами сокращения: «напишите краткую форму»).
8. **Несколько пропусков:** ответы подставляются в предложение, и сравнивается **всё предложение** после шагов
   1–7 — так `I ___ (be) tired` с вводом `'m` даёт `I'm tired` и засчитывается. Отметка «верно / неверно» —
   у каждого пропуска: сравнение с ближайшим допустимым набором.

**Сокращения, как устроено.** Однозначные сокращения раскрываются и у ученика, и в ответах:
`n't → not` (`can't → cannot`, `won't → will not`, `shan't → shall not`), `'m → am`, `'re → are`, `'ve → have`,
`'ll → will`. Неоднозначные `'s` (is / has / притяжательный) и `'d` (would / had) по вводу не раскрыть,
поэтому направление обратное: **в ответах их пишут полностью** (`it is`, `he had`, `she would`), а проверка
сама порождает краткие варианты — только после местоимений и слов закрытого списка (I, you, he, she, it, we,
they, there, here, that, what, who, where, how). Так `I'd go` засчитывается к ответу `I would go`, но
`I had go` — нет, а `John's` (притяжательный) никогда не превращается в `John is`. Вариантов не больше 2⁴
на ответ; `is not` даёт `isn't` и `'s not`. Не приравниваются: `can not` ≠ `cannot`, `ain't`, `gonna`,
`wanna`, `Isn't he?` ↔ `Is he not?` (порядок слов разный — автор перечисляет оба, если нужны).

**Мягкие замечания** — ответ засчитан, но под ним строка: `i` вместо `I`; имена и названия со строчной;
вопрос без `?` в `transform`/`order`; в `strict`-пунктуации — никаких замечаний, там это ошибка.
**Почти верно** — не засчитывается, но вместо «неверно» — «Проверьте написание»: ввод отличается от
допустимого ответа одной буквой в слове, которое не является проверяемой формой (например, опечатка в `yesterday`
при верном `went`). Нечёткого сравнения для самих форм нет: `goed` — ошибка.

**Варианты написания** (colour/color, learnt/learned, gotten) нормализация не трогает: автор перечисляет их в
`answer`, валидатор предупреждает, если в ответе есть слово из списка пар BrE/AmE, а пары нет.

Примеры (`contractions = "equal"`, `punctuation = "loose"`):

| Ответ в файле | Ввод | Итог |
| --- | --- | --- |
| `did not call` | `didn’t  call` | верно |
| `They did not buy a new car.` | `they didn't buy a new car` | верно |
| `It is raining.` | `It's raining` | верно |
| `I would go` | `I had go` | неверно |
| `Where did you go last summer?` | `where did you go last summer` | верно, замечание «вопрос — со знаком ?» |
| `He has gone.` | `He's gone.` | верно |
| `cannot` | `can not` | неверно (если нужно — в `answer`) |

### Объяснение после ответа

- **Верно:** «Верно» + `explain` + «Также верно: …» (другие допустимые ответы) + замечания.
- **Неверно:** если ввод совпал с `wrong`/`why` — конкретное объяснение; иначе «Не совсем» и `hint`
  (если есть). Ответ не раскрывается. После второй неверной попытки — кнопка «Показать ответ».
- **«Показать ответ»:** основной ответ, другие допустимые и `explain`; поле очищается — пункт засчитается,
  когда ученик впишет ответ сам (переписывание тоже закрепляет).
- **Контрольная:** проверки по ходу нет; после «Завершить» у каждого пункта — ответ ученика, верный,
  `explain`, и для неверного — `why`, если есть.

### Когда засчитывается урок и где хранится прогресс

- **Упражнение решено**, когда каждый его пункт хоть раз введён верно. Тогда вызывается существующий
  `setSolved(урок, упражнение, hash)`; `hash` — sha-256 канонического JSON упражнения (задание, пункты, ответы):
  по нему видно, какую версию решали.
- **Урок пройден** — существующее правило `isDone`: решены все упражнения или стоит ручная отметка.
  Для страницы курса в `data-exercises` попадают id `<Practice>` — `renderCourseProgress` работает без изменений.
- **Контрольная пройдена** при ≥ 80 %: все её упражнения помечаются решёнными (`setSolved`), урок — пройденным.
- `edu:course:v1` не меняется. Новые ключи — по образцу `edu:code:v1`:
  - `edu:drill:v1:<урок>/<упражнение>` = `{ hash, items: { "<n>": { ok, tries, shown, input } }, t }` —
    состояние пунктов (что вписано, что верно), чтобы вернуться к упражнению. Изменился `hash` — состояние
    пунктов сбрасывается с плашкой «Упражнение обновилось», отметка «решено» остаётся (как у кода Python).
  - `edu:test:v1:<урок>` = `{ best, last, t }` — баллы контрольной и входной проверки.
- **Синхронизация (Supabase):** схема не меняется — решённые упражнения и уроки уходят в `progress`
  (`exercise:…`, `lesson:…`), состояние пунктов — JSON в таблице `code` под тем же `exercise:<урок>/<упражнение>`
  (`starter_hash` = `hash` упражнения), баллы — в `code` под `exercise:<урок>/result` (id `result` для упражнений
  зарезервирован, проверяет валидатор).

### Без JavaScript

Страница собирается статически: каждый пункт — предложение с пропуском `____` (или варианты, фишки,
пары списком), под ним `<details><summary>Ответ</summary>` с основным и допустимыми ответами и `explain`.
Сверху упражнения — строка «Проверка ответов работает с включённым JavaScript». Так урок можно пройти
«на бумаге» и распечатать. Скрипт заменяет `<details>` полями ввода и кнопками. Ключи в любом случае есть в
исходнике страницы — это самопроверка, а не экзамен; так же устроены вопросы `<Quiz>`.

### Интерфейс

- Упражнение — полоса слева (как упражнение Python), заголовок «Упражнение · 3 из 5 пунктов», задание, пункты.
  Enter — «Проверить» и переход к следующему пропуску; Tab — между пропусками.
- `order`: фишки-кнопки (нажатие переносит в строку ответа, повторное — обратно), «Сбросить»; есть поле
  «Набрать самому». `find-error`: слова — кнопки. Всё доступно с клавиатуры, результат объявляется `aria-live`.
- На 375 px — без горизонтальной прокрутки: пропуск растягивается по вводу, фишки переносятся.
- «Нашли ошибку?» у пункта — с id `en-past-simple/regular-ed/2`.

### Валидатор — `node scripts/validate_english.ts [--reference] [--courses] [id…] [--strict]`

Без Python и Pyodide, секунды на весь раздел. У каждого упражнения:

- **Общее:** поля по виду, `id` уникален в уроке и не `result`, порядок `<Practice>` = порядок в TOML,
  `task` не пуст, `explain` у каждого пункта (у `match` — у упражнения), `ref` существуют и введены этим уроком
  или раньше; 4–6 упражнений в уроке (в review — до 8, в test — ровно 40 пунктов), 3–10 пунктов в упражнении
  (match — 3–6 пар); в review и test у каждого пункта есть `ref`, в test — уровень статьи не выше уровня модуля.
- **Ответы не противоречат друг другу:** допустимые ответы пункта попарно различимы и ни один не совпадает
  после нормализации с `wrong`; в ответах нет неоднозначных `'s`/`'d` после слов закрытого списка («напишите
  полностью: it is / it has»); ответ проходит собственную проверку `check()` (самопроверка ключа).
- `gap`: число `___` = числу пропусков в каждом ответе; `gaps` и `combos` не вместе; «—» только как целый ответ.
- `choice`: верный вариант ровно один и есть в `options`; варианты попарно различны после нормализации;
  **ни один неверный вариант не совпадает с допустимым ответом** (подстановка в предложение даёт другое
  предложение); `why` у каждого неверного — предупреждение, если нет.
- `order`: слова всех ответов (без учёта регистра и знаков препинания) — ровно `words`, **все использованы**
  и ни одного лишнего; порядок автора сам не является ответом.
- `transform`: ответ отличается от `source`; начинается со `start`; содержит `keyword` целым словом;
  дописанная часть не длиннее `max_words`.
- `find-error`: `error` **есть в предложении** ровно один раз целыми словами; каждая замена из `fix` даёт
  предложение, отличное от исходного; `fix` ≠ `error`; `also` отличаются от `text`.
- `match`: левые и правые части попарно различны; 3–6 пар.
- **Утечки:** `hint`, `task` и `why` (у видов с вводом) не содержат допустимого ответа целым словом.
- **Оформление:** предложения заканчиваются знаком препинания; объяснения — по-русски; прямой апостроф.
- **Нормализация:** `--selftest` прогоняет таблицу случаев (≥ 100: типографика, сокращения, пропуски,
  замечания) — это и тест `check.ts`.
- **Отчёт:** число упражнений и пунктов по видам и урокам; для каждой статьи — где введена и где повторяется;
  предупреждение, если тема не встретилась в следующих двух модулях.

### Слепое решение

Цель — поймать неоднозначные задания и недостающие допустимые ответы: отдельный агент решает упражнения, не
видя ключей, а затем его ответы проверяет тот же `check()`.

1. `node scripts/validate_english.ts --blind-export <папка> [модуль | урок…]` пишет:
   - `<папка>/<урок>.md` — задание и пункты с id (`en-past-simple/regular-ed/2`): `text`, `options`, `words`,
     `source`, `start`, `keyword`, `max_words`, пары `match` с буквами; **без** `answer`, `gaps`, `combos`,
     `explain`, `wrong`, `why`, `hint` и без текста урока (задание обязано быть понятным само по себе);
   - `<папка>/answers.json` — шаблон `{ "<id пункта>": { "answer": null, "also": [], "note": "" } }`.
2. Агент-решатель (не автор модуля; в брифе — не открывать `courses/english/`, `dist/` и сайт) заполняет
   `answer` (для пропусков — список по пропускам), в `also` — другие ответы, которые считает верными, в `note` —
   сомнения («подходят оба времени»).
3. `node scripts/validate_english.ts --blind-check <папка>/answers.json` печатает и пишет в
   `docs/reports/course-english-blind.md`: процент совпадений; **не засчитано** (ответ агента, ключ, объяснение);
   **`also` отвергнуты** — кандидаты в недостающие допустимые ответы; все `note`.
4. Разбор каждого расхождения автором с решением: ключ неверен / добавить допустимый ответ / уточнить задание
   (например, дать глагол в скобках или `keyword`) / ошибка решателя. Решение записывается в тот же отчёт.
   Правленые пункты проходят слепое решение ещё раз.

Порог: ≥ 97 % совпадений с первого прогона на модуль; ниже — модуль возвращается на доработку до ревью.

### Объём, проверка, готовность потока 0.3

Поток 0.3 — этот документ и глоссарий. Реализацию делает П2 по разделу «Нужно от платформы».
Готово, когда: П2 реализовал `check.ts` с `--selftest` (≥ 100 случаев), `<Practice>` всех видов, валидатор и
слепую выгрузку, и на одном образцовом уроке (`en-past-simple`) прошли: валидатор, слепое решение, проверка
в трёх браузерах, страница без JS. Образцовый урок пишет К2 первым — как «эталонный урок» курсов Python.

---

## Нужно от платформы

Сам поток платформу не меняет — список для П2.

**Коллекции и схемы (`src/content.config.ts`, загрузчики)**
1. `topics`: `package`, `version`, `docs` — необязательные; новые поля `group` (`"python" | "english"`) и
   `beta` (boolean). `reference/english/topic.toml` без пакета.
2. `reference`: поле `cefr` (`A1…C1`, обязательно для темы `english`), `contrasts: articleRef[]`,
   `patterns: string[]`; `docs` — необязательное; `kind` + `contrast`. Статьи без `.py` — нормальны для темы без пакета.
3. `lessons`: `kind` + `review | test | placement`; урок без `lesson.py` с `exercises.toml`. `course.toml`:
   `runtime = "python" | "none"`, `beta`; `module.toml`: `level`.
4. Загрузчик курсов (`src/lib/courses/load.ts`): чтение `exercises.toml`, сверка порядка с `<Practice>`.

**Проверка ответов**
5. `src/lib/english/check.ts` — нормализация, сокращения, сравнение, замечания, «почти верно»; без
   зависимостей, общий для страницы и валидатора. Таблица случаев для `--selftest`.

**Компоненты**
6. Справочник: `Examples`, `Formula`, `Fix` (подсветка разницы по словам), `Level`; стили таблиц сравнения.
7. Курс: `Practice` (все виды: gap, choice, order, transform, find-error, match; режимы урока и контрольной;
   статический вывод с `<details>` без JS), клиент `src/scripts/english/practice.ts` (ввод, проверка,
   `aria-live`, фишки, выбор слов, хранилище `edu:drill:v1`, `edu:test:v1`, вызовы `setSolved`/`setDone`).
8. Контрольная: «Завершить», балл, разбор, «Пройти заново»; входная проверка — рекомендация модуля.

**Страницы и навигация**
9. `/reference` и `/courses`: группы «Python» и «Английский» (по `group`), плашка «бета» (по `beta`).
   Шапку не менять; по желанию — `/english`, короткая страница-вход в оба раздела.
10. `/reference/english`: вкладки «По темам» / «По уровням», плашка CEFR у статей, фильтр `?level=`.
11. Страница курса английского: модули сгруппированы по уровням, у контрольных — лучший балл.
12. Урок английского: без строки «Выполнено ячеек», без «Выполнить всё», без кнопок .ipynb; «Нашли ошибку?» —
    с id пункта.
13. Поиск: для латинских слов — английская обработка (без русского стеммера из `stem.ts`: срезать -s/-es/-ed/-ing
    либо искать по началу слова); индексировать `patterns`.

**Pyodide — не грузить**
14. На статьях `english/*` не подключать `examples.ts`, CodeMirror и воркер; на уроках с `runtime = "none"` —
    не вызывать `preload()` и не создавать воркер. Проверка в `validate_browsers.ts`: страницы английского не
    делают ни одного запроса к Pyodide (jsDelivr).

**Валидаторы и CI**
15. `scripts/validate_english.ts`: `--reference`, `--courses`, `--strict`, `--selftest`, `--blind-export`,
    `--blind-check`. `validate_reference.py` и `validate_pyodide.ts` пропускают тему без пакета,
    `validate_courses.ts` — курсы с `runtime = "none"`.
16. CI: задание «Английский» (Node, без Python и Pyodide, ~1 минута); уроки английского — в проверке трёх
    браузеров (ввод, проверка, прогресс, страница без JS) на образцовом уроке и контрольной.

**Синхронизация (этап 4)**
17. Включить ключи `edu:drill:v1:*` и `edu:test:v1:*` в синхронизацию (таблица `code`, см. выше); схема
    Supabase не меняется.

---

## Решения по открытым вопросам (оркестратор, 2026-09-30)

1. **Вид translate — не в этой волне.** У перевода слишком много верных вариантов; вернуться после слепого
   решения всего курса, если нормализация покажет себя надёжно.
2. **«Проверьте себя» в статьях справочника — не делаем сейчас** (нет в задании); кандидат на следующий этап.
3. **Навигация:** вкладки шапки остаются по видам (Задачи · Курсы · Справочник); внутри — на главной, на
   страницах разделов и в выпадающих списках — группы по направлениям («Python и алгоритмы», «Данные», «Git»,
   «Английский»). Отдельная вкладка «Английский» смешала бы виды и направления.

## Открытые вопросы (исходная формулировка)

1. **Вид `translate`** — во второй очереди: перевод с русского почти всегда имеет больше верных ответов, чем
   перечислит автор. Вернуться после слепого решения первой трети курса.
2. **«Проверьте себя» в статьях справочника** (`<Practice>` из `reference/english/<slug>.toml`) — формат
   готов, но это +88 файлов ключей для С4. Предлагаю после К2, если останется время.
3. **Озвучка примеров** (Web Speech API) — не в этой волне.
4. **Отдельная вкладка «Английский» в шапке** против групп на страницах «Курсы» и «Справочник» — предлагаю
   группы (шапка короче, «бета» видна в списках); решение за пользователем.
