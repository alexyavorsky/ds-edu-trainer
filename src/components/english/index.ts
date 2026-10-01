/** Компоненты английского без import: статьи справочника и уроки курса получают их через <Content components>. */
import Explain from '../course/Explain.astro';
import Hint from '../course/Hint.astro';
import Mistake from '../course/Mistake.astro';
import Note from '../course/Note.astro';
import Quiz from '../course/Quiz.astro';
import Examples from './Examples.astro';
import Fix from './Fix.astro';
import Formula from './Formula.astro';
import Level from './Level.astro';
import Practice from './Practice.astro';

export const englishReferenceComponents = { Examples, Formula, Fix, Level };
export const englishLessonComponents = { Examples, Formula, Fix, Level, Practice, Quiz, Explain, Hint, Note, Mistake };
