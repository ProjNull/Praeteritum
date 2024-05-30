import type { Component } from "solid-js";
import logo from "../assets/logo.png";

import createKindeClient from "@kinde-oss/kinde-auth-pkce-js";

const login = async () => {
  const kinde = await createKindeClient({
    client_id: "df28cfcf901448078400d1445f769a11",
    domain: "https://hyscript7-praedev.eu.kinde.com",
    redirect_uri: window.location.origin + "/",
    audience: "127.0.0.1"
  });
  if (await kinde.isAuthenticated()) {
    console.log(await kinde.getToken());
    if (localStorage.getItem("token") == null) {
      const resp = await fetch("/api/v1/kinde/token", {
        headers: {
          Authorization: `Bearer ${await kinde.getToken()}`,
        },
      })
      if (resp.status != 200 || resp.redirected) {
        window.location.href = "/api/v1/kinde/login";
        return;
      } else {
        console.log(resp);
        const json = await resp.json();
        localStorage.setItem("token", json.token);
      }
    }
    setTimeout(() => (window.location.href = "/home"), 1000);
    return;
  }
  await kinde.login();
};

const LoadingScreen: Component = () => {
  login();
  return (
    <div class="flex flex-col items-center justify-center min-h-[100vh]">
      <div class="flex flex-col items-center gap-2">
        <div>
          <img
            src={logo}
            alt="Praeteritum Logo"
            class="mx-auto"
            width="150vw"
            height="auto"
          />
        </div>
        <h1 class="text-3xl">Praeteritum</h1>
        <div>
          <span class="loading loading-infinity w-20"></span>
        </div>
      </div>
      <div class="text-base-500 italic">Made by {"{NULL}"}</div>
    </div>
  );
};

export default LoadingScreen;
