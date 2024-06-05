import { Show, type Component } from "solid-js";
import { setTheme, clearTheme } from "../hooks/Theme";

interface Props {
  setter: (b: boolean) => void;
  getter: () => boolean;
}

const SettingsModal: Component<Props> = ({ setter, getter }) => {
  return (
    <div>
      <Show when={getter()} fallback={<></>}>
        <div class="absolute z-10 top-0 left-0 h-full w-full bg-black backdrop-blur-lg bg-opacity-20">
          <div class="flex flex-col items-center justify-center min-h-[100vh]">
            <div class="card w-96 bg-base-100 shadow-xl">
              <div class="card-body">
                <h2 class="card-title">Application Settings</h2>
                <div class="flex flex-col flex-wrap gap-2">
                  <div class="flex flex-row gap-2 flex-wrap w-full">
                    <button class="btn btn-outline grow" onclick={clearTheme}>Auto</button>
                    <button class="btn btn-outline grow" onclick={() => setTheme("dark")}>Dark</button>
                    <button class="btn btn-outline grow" onclick={() => setTheme("light")}>Light</button>
                  </div>
                  <div class="flex flex-row gap-2 flex-wrap w-full">
                    <button class="btn btn-outline grow" onclick={() => setTheme("night")}>Night</button>
                    <button class="btn btn-outline grow" onclick={() => setTheme("dracula")}>Dracula</button>
                    <button class="btn btn-outline grow" onclick={() => setTheme("forest")}>Forest</button>
                    <button class="btn btn-outline grow" onclick={() => setTheme("coffee")}>Coffee</button>
                  </div>
                  <div class="flex flex-row gap-2 flex-wrap w-full">
                    <button class="btn btn-outline grow" onclick={() => setTheme("lemonade")}>Lemonade</button>
                    <button class="btn btn-outline grow" onclick={() => setTheme("nord")}>Nord</button>
                    <button class="btn btn-outline grow" onclick={() => setTheme("autumn")}>Autumn</button>
                  </div>
                </div>
                <div class="card-actions justify-end">
                  <button class="btn btn-outline" onClick={() => setter(false)}>
                    Close
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </Show>
    </div>
  );
};

export default SettingsModal;
