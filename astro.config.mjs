import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://petfoodlab.it.com',
  integrations: [tailwind(), sitemap()],
  output: 'static',
  markdown: {
    shikiConfig: {
      theme: 'github-light',
    },
    // 启用目录生成
    remarkPlugins: [],
  },
});
