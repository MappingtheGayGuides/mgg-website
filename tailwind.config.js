/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
    "./static/**/*.js",
    "./static/**/*.css"
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Gothic A1', 'Outfit', 'Inter', 'system-ui', 'sans-serif'],
        serif: ['Georgia', 'serif']
      },
      fontWeight: {
        'bold': '700',
      }
    },
  },
  plugins: [
    require("daisyui"),
    require("@tailwindcss/typography")
  ],
  daisyUI: {
    themes: [
      "light", 
      "dark",
      {
        "mgg-vibrant": {
          "primary": "#6B46C1",
          "primary-content": "#ffffff",
          "secondary": "#E67E22",
          "secondary-content": "#ffffff", 
          "accent": "#2563EB",
          "accent-content": "#ffffff",
          "neutral": "#374151",
          "neutral-content": "#ffffff",
          "base-100": "#f8fafc",
          "base-200": "#e2e8f0",
          "base-300": "#cbd5e1",
          "base-content": "#1e293b",
          "info": "#2563EB",
          "success": "#10B981",
          "warning": "#F59E0B",
          "error": "#DC2626",
        }
      }
    ],
    darkTheme: "dark",
    base: true,
    styled: true,
    utils: true,
    prefix: "",
    logs: true,
    themeRoot: ":root"
  }
}
