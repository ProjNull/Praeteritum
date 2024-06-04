import { createEffect, createSignal } from "solid-js";

const [getTheme, setThemeSignal] = createSignal(
  localStorage.getItem("theme") ?? ""
);

function setTheme(theme: string) {
  localStorage.setItem("theme", theme);
  setThemeSignal(theme);
}

function clearTheme() {
  localStorage.removeItem("theme");
  setThemeSignal("");
}

createEffect(() => {
  const root = document.querySelector("html");
  if (!root) return;
  if (getTheme() == "") {
    root.removeAttribute("data-theme");
    return;
  }
  root.setAttribute("data-theme", getTheme());
});

export { getTheme, setTheme, clearTheme };
