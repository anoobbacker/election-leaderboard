import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';
import basicSsl from '@vitejs/plugin-basic-ssl'

export default defineConfig({
	server: {
		https: {
			key: './certs/private.key',
			cert: './certs/certificate.crt',
		},
		proxy: {},
	},
	plugins: [basicSsl(), sveltekit()]
});
