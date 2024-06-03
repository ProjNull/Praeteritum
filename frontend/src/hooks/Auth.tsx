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
  } else {
    const token = localStorage.getItem("token");
    if (token) {
      if (!(await verifyTokenValditity(token))) {
        localStorage.removeItem("token");
        setTimeout(() => {
          window.location.href = "/api/v1/kinde/login";
        }, 1000);
        return;
      }
    } else {
      setTimeout(() => {
        window.location.href = "/api/v1/kinde/login";
      }, 1000);
      return;
    }
  }
  if (window.location.pathname === "/") {
    setTimeout(() => {
      window.location.href = "/home";
    }, 2000);
  }
}

export { resolveAuthenticationToken };
