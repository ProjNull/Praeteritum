import createKindeClient, { KindeClient } from "@kinde-oss/kinde-auth-pkce-js";

async function syncState(kinde: KindeClient) {
  const resp = await fetch("/api/v1/kinde/token", {
    headers: {
      Authorization: `Bearer ${await kinde.getToken()}`,
    },
  });
  if (resp.status != 200 || resp.redirected) {
    window.location.href = "/api/v1/kinde/login";
    return;
  } else {
    const json = await resp.json();
    localStorage.setItem("token", json.token);
  }
}

async function verifyTokenValidity() {
  const resp = await fetch("/api/v1/kinde/token", {
    headers: {
      Authorization: `Bearer ${localStorage.getItem("token") ?? ""}`,
    },
  });
  return resp.status == 200 && !resp.redirected;
}

const authenticate = async (redirect_to_home: boolean = true) => {
  const kinde = await createKindeClient({
    client_id: "df28cfcf901448078400d1445f769a11",
    domain: "https://hyscript7-praedev.eu.kinde.com",
    redirect_uri: window.location.origin + "/",
    audience: "127.0.0.1",
  });
  if (await kinde.isAuthenticated()) {
    if (localStorage.getItem("token") == null || !verifyTokenValidity()) {
      await syncState(kinde);
    }
    if (redirect_to_home) {
      setTimeout(() => (window.location.href = "/home"), 1000);
    }
    return;
  }
  await kinde.login();
};

export default authenticate;
