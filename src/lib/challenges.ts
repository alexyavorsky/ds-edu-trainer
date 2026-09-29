/**
 * Загрузчики контента: книги, главы и задачи читаются прямо из папок challenges/.
 * Папка = сущность, реестров нет.
 */
import { existsSync, readdirSync, readFileSync, statSync } from 'node:fs';
import { join, resolve } from 'node:path';
import type { Loader, LoaderContext } from 'astro/loaders';
import { parse as parseToml } from 'smol-toml';
import { buildBundle, type ChallengeType, type Difficulty } from './bundle';

const ROOT = resolve('.');
export const CHALLENGES_DIR = join(ROOT, 'challenges');
export const REFERENCE_DIR = join(ROOT, 'reference');
const RUNNER_PATH = join(ROOT, 'runtime', 'runner.py');

const CHAPTER_DIR_RE = /^(\d{2})-[a-z0-9]+(-[a-z0-9]+)*$/;

const read = (path: string) => readFileSync(path, 'utf-8');
const readToml = (path: string) => parseToml(read(path)) as Record<string, any>;
const subdirs = (path: string) =>
  existsSync(path)
    ? readdirSync(path)
        .filter((name: string) => !name.startsWith('.') && !name.startsWith('_') && statSync(join(path, name)).isDirectory())
        .sort()
    : [];

export function chapterNumber(chapterSlug: string): number {
  return Number(chapterSlug.slice(0, 2));
}

/** Следит за папкой в режиме разработки и перезагружает коллекцию при изменениях. */
function watch(context: LoaderContext, dir: string, reload: () => Promise<void>) {
  if (!context.watcher) return;
  context.watcher.add(dir);
  const onChange = (path: string) => {
    if (path.startsWith(dir)) reload();
  };
  context.watcher.on('change', onChange);
  context.watcher.on('add', onChange);
  context.watcher.on('unlink', onChange);
  context.watcher.on('unlinkDir', onChange);
}

export function booksLoader(): Loader {
  return {
    name: 'books-loader',
    load: async (context) => {
      const load = async () => {
        context.store.clear();
        for (const book of subdirs(CHALLENGES_DIR)) {
          const metaPath = join(CHALLENGES_DIR, book, 'book.toml');
          if (!existsSync(metaPath)) continue;
          const data = await context.parseData({ id: book, data: readToml(metaPath) });
          context.store.set({ id: book, data, digest: context.generateDigest(data) });
        }
      };
      await load();
      watch(context, CHALLENGES_DIR, load);
    },
  };
}

export function chaptersLoader(): Loader {
  return {
    name: 'chapters-loader',
    load: async (context) => {
      const load = async () => {
        context.store.clear();
        for (const book of subdirs(CHALLENGES_DIR)) {
          for (const chapter of subdirs(join(CHALLENGES_DIR, book))) {
            const metaPath = join(CHALLENGES_DIR, book, chapter, 'chapter.toml');
            if (!CHAPTER_DIR_RE.test(chapter) || !existsSync(metaPath)) continue;
            const id = `${book}/${chapter}`;
            const raw = { ...readToml(metaPath), book, slug: chapter, number: chapterNumber(chapter) };
            const data = await context.parseData({ id, data: raw });
            context.store.set({ id, data, digest: context.generateDigest(data) });
          }
        }
      };
      await load();
      watch(context, CHALLENGES_DIR, load);
    },
  };
}

export function challengesLoader(): Loader {
  return {
    name: 'challenges-loader',
    load: async (context) => {
      const load = async () => {
        context.store.clear();
        const runner = read(RUNNER_PATH);
        for (const book of subdirs(CHALLENGES_DIR)) {
          const bookPath = join(CHALLENGES_DIR, book);
          if (!existsSync(join(bookPath, 'book.toml'))) continue;
          const bookMeta = readToml(join(bookPath, 'book.toml'));
          for (const chapter of subdirs(bookPath)) {
            const chapterPath = join(bookPath, chapter);
            if (!CHAPTER_DIR_RE.test(chapter) || !existsSync(join(chapterPath, 'chapter.toml'))) continue;
            const chapterMeta = readToml(join(chapterPath, 'chapter.toml'));
            const word = bookMeta.kind === 'topic' ? 'Раздел' : 'Глава'; // так же, как chapter_label в validate.py
            const chapterLabel = `${word} ${chapterNumber(chapter)}. ${chapterMeta.title}`;
            for (const slug of subdirs(chapterPath)) {
              const dir = join(chapterPath, slug);
              if (!existsSync(join(dir, 'meta.toml'))) continue;
              const meta = readToml(join(dir, 'meta.toml'));
              const taskMd = read(join(dir, 'task.md'));
              const isComplexity = meta.type === 'complexity';
              const file = (name: string) => (existsSync(join(dir, name)) ? read(join(dir, name)) : undefined);

              const common = {
                title: meta.title as string,
                id: meta.id as string,
                difficulty: meta.difficulty as Difficulty,
                type: meta.type as ChallengeType,
                bookTitle: bookMeta.title as string,
                chapterLabel,
                slug,
                taskMd,
                tests: file('tests.py') ?? '',
                runner,
              };
              const id = `${book}/${chapter}/${slug}`;
              const raw = {
                ...meta,
                taskId: meta.id,
                book,
                chapter,
                slug,
                starter: file('starter.py'),
                solution: file('solution.py'),
                code: file('code.py'),
                bundle: isComplexity ? undefined : buildBundle({ ...common, code: file('starter.py') ?? '' }),
              };
              delete (raw as Record<string, unknown>).id;
              const data = await context.parseData({ id, data: raw });
              const rendered = await context.renderMarkdown(taskMd);
              context.store.set({ id, data, rendered, digest: context.generateDigest({ ...data, taskMd }) });
            }
          }
        }
      };
      await load();
      watch(context, join(ROOT, 'runtime'), load);
      watch(context, CHALLENGES_DIR, load);
    },
  };
}

export function topicsLoader(): Loader {
  return {
    name: 'reference-topics-loader',
    load: async (context) => {
      const load = async () => {
        context.store.clear();
        for (const topic of subdirs(REFERENCE_DIR)) {
          const metaPath = join(REFERENCE_DIR, topic, 'topic.toml');
          if (!existsSync(metaPath)) continue;
          const data = await context.parseData({ id: topic, data: readToml(metaPath) });
          context.store.set({ id: topic, data, digest: context.generateDigest(data) });
        }
      };
      await load();
      watch(context, REFERENCE_DIR, load);
    },
  };
}
