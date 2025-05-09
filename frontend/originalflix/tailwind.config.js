/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
    "./index.html",
  ],
  theme: {
    colors: {
      'background': '#f5f5f4',
      'light': '#fafaf9',
      'dark': '#292524',
      'gray': '#a8a29d',
      'pink': '#f86363',
      'orange': '#da9030',
      'portfolio-bg': '#252525',
      'coffee-bg': '#ffdd04'
    },
    extend: {},
  },
  plugins: [],
}

