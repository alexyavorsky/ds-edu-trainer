declare namespace App {
  interface Locals {
    /** id статьи справочника, которая сейчас рендерится («numpy/broadcasting»): по нему <Example> находит файл примеров. */
    referenceArticle?: string;
    /** id урока курса, который сейчас рендерится («np-first-array»): по нему <Demo>/<Exercise> находят ячейки lesson.py. */
    lesson?: string;
  }
}
