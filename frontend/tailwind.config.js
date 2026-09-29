/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primaryBg: "#0B1220",
        secondaryBg: "#111827",
        cardBg: "#172033",
        borderBg: "#263247",
        primaryBlue: "#2563EB",
        secondaryBlue: "#3B82F6",
        success: "#10B981",
        warning: "#F59E0B",
        critical: "#EF4444",
        textPrimary: "#F8FAFC",
        textSecondary: "#94A3B8"
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif']
      }
    },
  },
  plugins: [],
}
