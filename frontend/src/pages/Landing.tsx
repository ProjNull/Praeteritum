import type { Component } from "solid-js";
import logo from "../assets/logo.png";

const LoadingScreen: Component = () => {
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
