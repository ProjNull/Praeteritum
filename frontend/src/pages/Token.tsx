import { createSignal, Show, type Component } from "solid-js";
import logo from "../assets/logo.png";

function getToken() {
  return localStorage.getItem("token") ?? null;
}

function tokenIsSet() {
  return getToken() != null;
}

const TokenDisplay: Component = () => {
  const [actionConfirm, setActionConfirm] = createSignal(false);
  return (
    <div class="flex flex-col items-center justify-center min-h-[100vh] gap-2">
      <div class="flex flex-col items-center gap-4">
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
        <div class="bg-base-300 p-4 rounded-xl">
          <Show
            when={tokenIsSet()}
            fallback={
              <div class="text-center gap-2">
                <div class="text-3xl text-red-500">You are not logged in!</div>
                <p>Please click the button below to refresh your token</p>
                <div>
                  <button
                    class="btn btn-outline"
                    onClick={() => {
                      window.location.href = "/api/v1/kinde/login";
                    }}
                  >
                    Refresh
                  </button>
                </div>
              </div>
            }
          >
            <Show
              when={!actionConfirm()}
              fallback={
                <p class="max-w-[50vw] min-w-[50vw] font-mono bg-base-300 break-words">
                  {getToken()}
                </p>
              }
            >
              <div class="text-center gap-2">
                <p class="text-3xl text-red-500">
                  You are about to do something dangerous
                </p>
                <p>
                  Are you sure you want to display your token?
                  <br />
                  If a malicious actor or a third party is able to access your
                  token,
                  <br />
                  they can use it to login as you and perform actions on your
                  account.
                </p>
                <div class="mt-2">
                  <button
                    class="btn btn-outline border-red-500 text-red-500 hover:bg-red-700 hover:border-red-700 hover:text-base-100"
                    onclick={() => setActionConfirm(true)}
                  >
                    Display Token
                  </button>
                </div>
              </div>
            </Show>
          </Show>
          <Show when={actionConfirm()} fallback={<></>}>
            <div class="text-center mt-2">
              <button
                class="btn btn-outline border-slate-500 text-slate-500 hover:bg-slate-700 hover:border-slate-700 hover:text-base-100"
                onclick={() => setActionConfirm(false)}
              >
                Hide Token
              </button>
            </div>
          </Show>
        </div>
      </div>
      <div class="text-base-500 italic">Made by {"{NULL}"}</div>
    </div>
  );
};

export default TokenDisplay;
