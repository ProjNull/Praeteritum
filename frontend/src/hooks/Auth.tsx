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
        alert("wtf");
        return;
      }
    }
  } else {
    const token = localStorage.getItem("token");
    if (token) {
      if (!(await verifyTokenValditity(token))) {
        localStorage.removeItem("token");
        window.location.href = "/api/v1/kinde/login";
        return;
      }
    } else {
      window.location.href = "/api/v1/kinde/login";
      return;
    }
  }
  if (window.location.href === "/") {
    window.location.href = "/home";
  }
}

export { resolveAuthenticationToken };
