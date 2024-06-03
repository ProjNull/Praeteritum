import { createSignal, Show, type Component } from "solid-js";
import logo from "../assets/logo.png";

function getToken() {
  return localStorage.getItem("token") ?? null;
}

function tokenIsSet() {
  return getToken() != null;
}

const Unauthorized: Component = () => {
  return (
    <div>
      <div>You are not authenticated.</div>
      <div>
        Click{" "}
        <a
          onclick={() => (window.location.href = "/api/v1/kinde/login")}
          class=""
        >
          here
        </a>{" "}
        to login <i>(direct API link)</i>
      </div>
    </div>
  );
};

const TokenCodeBlock: Component = () => {
  return <p class="max-w-[50vw] min-w-[50vw] font-mono bg-base-300 break-words">{getToken()}</p>;
};

const TokenView: Component = () => {
  const [actionConfirm, setActionConfirm] = createSignal(false);
  return (
    <div class="bg-base-300 p-3 rounded-lg">
      <Show when={!actionConfirm()} fallback={<TokenCodeBlock />}>
        <div class="text-center">
          <div class="text-3xl text-red-500">
            You are about to do something dangerous
          </div>
          <div>
            If you are sure you want to display your token, click the button
            below
          </div>
          <button
            class="btn btn-outline border-red-500 text-red-500 hover:bg-red-700 hover:border-red-700 hover:text-base-100"
            onclick={() => setActionConfirm(true)}
          >
            Display Token
          </button>
        </div>
      </Show>
    </div>
  );
};

const TokenDisplay: Component = () => {
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
        <Show when={tokenIsSet()} fallback={<Unauthorized />}>
          <TokenView />
        </Show>
      </div>
      <div class="text-base-500 italic">Made by {"{NULL}"}</div>
    </div>
  );
};

export default TokenDisplay;
