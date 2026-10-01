interface ImportMetaEnv {
  /** Адрес проекта Supabase; без него и ключа вход не показывается (scripts/sync/config.ts). */
  readonly PUBLIC_SUPABASE_URL?: string;
  /** Публичный ключ Supabase (anon / publishable). Service role key — никогда. */
  readonly PUBLIC_SUPABASE_ANON_KEY?: string;
}

declare namespace App {
  interface Locals {
    /** id статьи справочника, которая сейчас рендерится («numpy/broadcasting»): по нему <Example> находит файл примеров. */
    referenceArticle?: string;
    /** id урока курса, который сейчас рендерится («np-first-array»): по нему <Demo>/<Exercise> находят ячейки lesson.py. */
    lesson?: string;
  }
}
