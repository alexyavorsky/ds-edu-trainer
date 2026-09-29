// @ts-check
import mdx from '@astrojs/mdx';
import { defineConfig } from 'astro/config';

export default defineConfig({
  integrations: [mdx()],
  trailingSlash: 'ignore',
  markdown: {
    shikiConfig: { theme: 'vitesse-dark', wrap: false },
  },
});
