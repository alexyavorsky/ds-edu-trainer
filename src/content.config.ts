import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';
import { booksLoader, chaptersLoader, challengesLoader, topicsLoader } from './lib/challenges';

const books = defineCollection({
  loader: booksLoader(),
  schema: z.object({
    title: z.string(),
    kind: z.enum(['book', 'topic']).default('book'), // книга или тема (NumPy, pandas)
    author: z.string().optional(),
    code: z.string(),
    edition: z.string().optional(),
    description: z.string().optional(),
    order: z.number().int().default(100),
    packages: z.array(z.string()).default([]), // у темы — нужные пакеты; у книги пусто (только stdlib)
    reference: z.string().optional(), // тема справочника, по разделам которой строятся главы
  }),
});

const chapters = defineCollection({
  loader: chaptersLoader(),
  schema: z.object({
    title: z.string(),
    summary: z.string(),
    book: z.string(),
    slug: z.string(),
    number: z.number().int(),
  }),
});

const challenges = defineCollection({
  loader: challengesLoader(),
  schema: z
    .object({
      taskId: z.string().regex(/^[a-z0-9]+(-[a-z0-9]+)*$/),
      title: z.string().min(1),
      difficulty: z.enum(['easy', 'medium', 'hard']),
      type: z.enum(['implement', 'fix-bug', 'complete', 'complexity']),
      tags: z.array(z.string()).min(1),
      hints: z.array(z.string()),
      bugs: z.number().int().min(1).max(3).optional(),
      order: z.number().int().optional(),
      refs: z.array(z.string()).optional(),
      complexity: z
        .object({
          options: z.array(z.string()).min(3).max(5),
          answer: z.string(),
          explanation: z.string(),
        })
        .optional(),
      book: z.string(),
      chapter: z.string(),
      slug: z.string(),
      starter: z.string().optional(),
      solution: z.string().optional(),
      code: z.string().optional(),
      tests: z.string().optional(),
      packages: z.array(z.string()), // пакеты раздела (у темы); у книги пусто — только стандартная библиотека
      bundleHeader: z.string().optional(), // копируемый файл = шапка + код решения + footer (src/lib/bundle.ts)
      bundleFooter: z.string().optional(),
    })
    .refine((c) => (c.type === 'complexity' ? !!c.complexity && !!c.code : !!c.starter && !!c.solution && !!c.tests && !!c.bundleFooter), {
      message: 'набор файлов не соответствует типу задачи — запустите python3 scripts/validate.py',
    }),
});

const topics = defineCollection({
  loader: topicsLoader(),
  schema: z.object({
    title: z.string(),
    summary: z.string(),
    package: z.string(),
    version: z.string(),
    docs: z.url(),
    order: z.number().int().default(100),
    sections: z.array(z.object({ title: z.string(), articles: z.array(z.string()).min(1) })).min(1),
  }),
});

const articleRef = z.string().regex(/^[a-z0-9-]+\/[a-z0-9-]+$/);

const reference = defineCollection({
  loader: glob({ pattern: '*/*.mdx', base: './reference' }),
  schema: z.object({
    title: z.string(),
    level: z.enum(['basic', 'medium', 'advanced']),
    summary: z.string(),
    requires: z.array(articleRef).max(3).default([]),
    related: z.array(articleRef).default([]),
    functions: z.array(z.string()).default([]),
    docs: z.url(),
    kind: z.enum(['article', 'overview']).default('article'),
  }),
});

/** Уроки курсов: текст — lesson.mdx, код ячеек — lesson.py рядом (src/lib/courses). id — из frontmatter. */
const lessons = defineCollection({
  loader: glob({ pattern: '*/*/*/lesson.mdx', base: './courses', generateId: ({ data }) => String(data.id) }),
  schema: z.object({
    id: z.string().regex(/^[a-z]+-[a-z0-9]+(-[a-z0-9]+)*$/),
    title: z.string(),
    summary: z.string(),
    minutes: z.number().int().min(5).max(30),
    kind: z.enum(['lesson', 'project']).default('lesson'),
    introduces: z.array(z.string()).default([]),
    reference: z.array(articleRef).default([]),
    data: z.array(z.string()).default([]),
    packages: z.array(z.string()).default([]),
  }),
});

export const collections = { books, chapters, challenges, topics, reference, lessons };
