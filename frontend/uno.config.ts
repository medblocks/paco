// uno.config.ts
import {
  defineConfig,
  presetAttributify, presetTypography, presetUno
} from 'unocss'

export default defineConfig({
  presets: [
    presetAttributify(), // required when using attributify mode
    presetUno(), // required
    presetTypography(),
  ],
})