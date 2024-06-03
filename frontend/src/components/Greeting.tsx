import { createSignal, type Component } from "solid-js";
import { fullname, email } from "../hooks/User";

function getPreference() {
  return (sessionStorage.getItem("showGreeting") ?? "true") === "true";
}

function setPreference() {
  return sessionStorage.setItem("showGreeting", "false");
}

const Greeting: Component = () => {
  const [visible, setVisible] = createSignal(getPreference());
  return (
    <div
      class={
        (visible() ? "" : "hidden ") +
        "min-w-full p-2 rounded-lg bg-base-200 text-center break-words relative"
      }
    >
      <div class="absolute top-0 right-0 z-2 p-2 m-2">
        <button
          class="btn btn-ghost btn-circle"
          onclick={() => {
            setVisible(false);
            setPreference();
          }}
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            stroke-width={1.5}
            stroke="currentColor"
            class="size-6"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              d="M6 18 18 6M6 6l12 12"
            />
          </svg>
        </button>
      </div>
      <h1 class="text-3xl mt-2">Hello {fullname()}!</h1>
      <p class="text-2xl">Welcome to Praeteritum.</p>
      <p>
        Your email address is <span class="code">{email()}</span>
      </p>
    </div>
  );
};

export default Greeting;
