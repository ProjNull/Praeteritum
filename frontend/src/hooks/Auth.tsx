import { createSignal } from "solid-js";

const [authenticated, setAuthenticated] = createSignal(false);
const [token, setToken] = createSignal("");
const [ready, setReady] = createSignal(false);

async function verifyTokenValditity(token: string): Promise<boolean> {
  const resp = await fetch("/api/v1/kinde/token", {
    headers: {
      Authorization: `Bearer ${token ?? ""}`,
    },
  });
  return resp.status == 200 && !resp.redirected;
}

async function resolveAuthenticationToken() {
  if (window.location.search.includes("token=")) {
    const token = new URLSearchParams(window.location.search).get("token");
    if (token) {
      localStorage.setItem("token", token);
      if (!(await verifyTokenValditity(token))) {
        alert("An unexpected error has occurred. Please re-login.");
        return;
      }
    }
    setToken(token ?? "");
    setAuthenticated(true);
  } else {
    const token = localStorage.getItem("token");
    if (token) {
      if (!(await verifyTokenValditity(token))) {
        localStorage.removeItem("token");
        if (window.location.pathname === "/token") {
          setTimeout(() => {
            setReady(true);
          }, 500);
          return;
        }
        setTimeout(() => {
          window.location.href = "/api/v1/kinde/login";
        }, 1000);
        return;
      }
    } else {
      if (window.location.pathname === "/token") {
        setTimeout(() => {
          setReady(true);
        }, 500);
        return;
      }
      setTimeout(() => {
        window.location.href = "/api/v1/kinde/login";
      }, 1000);
      return;
    }
    setToken(token);
  }
  setAuthenticated(true);
  setTimeout(() => {
    setReady(true);
    if (window.location.pathname === "/") {
      window.location.href = "/home";
    }
  }, 500);
}

export { resolveAuthenticationToken, ready, authenticated, token };
