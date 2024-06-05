import daisyui from "daisyui";
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {},
  },
  plugins: [daisyui],
  daisyui: {
    themes: [
      "light",
      "dark",
      "night",
      "dracula",
      "forest",
      "coffee",
      "lemonade",
      "nord",
      "autumn",
    ],
  },
};
