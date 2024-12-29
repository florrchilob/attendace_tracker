/** @type {import('tailwindcss').Config} */
export default {
  content: ["./src/**/*.{jsx,js,ts,tsx}"],
  theme: {
    extend: {
      backgroundImage: {
        'bg-desktop-dark': "url('/desktop-dark.jpg')",
        'bg-desktop': "url('/desktop.jpg')",
      },
      colors: {
        primary: "#4CAF50",
        greenConvined: "#8DF9B0",
        lavanderConvined: "#8D91F7",
        turquiseConvined: "#8DF7F6",
        limeConvined: "#AEF78E",
        pinkConvined: "#F28DF7",
        orangeConvined: "#F7AF8D",
        redConvinedStronger: "#FF7373",
        yellowConvined: "#F7F78D"
      },
    },
  },
  plugins: [],
};
