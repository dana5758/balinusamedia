import { defineConfig } from "astro/config";
import sitemap from "@astrojs/sitemap";

export default defineConfig({
    site: "https://balinusamedia.com",

    integrations: [
        sitemap()
    ],

    devToolbar: {
        enabled: false
    },

    build: {
        sourcemap: false
    }
});