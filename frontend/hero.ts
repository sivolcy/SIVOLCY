import { heroui } from "@heroui/react";

export default heroui({
  defaultTheme: "light",
  layout: {
    radius: {
      small: "5px",
      large: "20px",
    },
  },
  themes: {
    dark: {
      colors: {
        primary: "#4465DB",
      },
    },
    light: {
      colors: {
        primary: "#4465DB",
        background: "#ffffff",
        foreground: "#000000",
        content1: "#ffffff",
        content2: "#ffffff",
        content3: "#ffffff",
        content4: "#ffffff",
        default: {
          50: "#ffffff",
          100: "#ffffff",
          200: "#ffffff",
          300: "#ffffff",
          400: "#000000",
          500: "#000000",
          600: "#000000",
          700: "#000000",
          800: "#000000",
          900: "#000000",
          DEFAULT: "#ffffff",
          foreground: "#000000",
        },
      },
    },
  },
});
