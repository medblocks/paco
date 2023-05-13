import { sveltekit } from '@sveltejs/kit/vite';
import { build, defineConfig } from 'vite';
import UnoCSS from 'unocss/vite'


export default defineConfig({
	plugins: [
		UnoCSS(),
		sveltekit()
	],
	build: {
		sourcemap: true
	}
});