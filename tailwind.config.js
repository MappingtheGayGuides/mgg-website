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
      }
    },
  },
  plugins: [
    require("daisyUI"),
    require("@tailwindcss/typography")
  ],
  daisyUI: {
    themes: [
      "light", 
      "dark",
      {
        "mgg-modern": {
          "primary": "#2A6F97",
          "primary-content": "#ffffff",
          "secondary": "#FF6B6B",
          "secondary-content": "#ffffff", 
          "accent": "#FFB347",
          "accent-content": "#ffffff",
          "neutral": "#2D3748",
          "neutral-content": "#ffffff",
          "base-100": "#F5F7FA",
          "base-200": "#E2E8F0",
          "base-300": "#CBD5E0",
          "base-content": "#2D3748",
          "info": "#3182CE",
          "success": "#38A169",
          "warning": "#D69E2E",
          "error": "#E53E3E",
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
