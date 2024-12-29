/** @type {import('tailwindcss').Config} */
export default {
  content: ["./src/**/*.{jsx,js,ts,tsx}"],
  theme: {
    extend: {
      backgroundImage: {
        'bg-desktop-dark': "url('/desktop-dark.jpg')",
        'bg-desktop': "url('/desktop.jpg')",
      },
    },
  },
  plugins: [],
};
