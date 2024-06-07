import { createComputed, createSignal, type Component } from "solid-js";
import { A } from "@solidjs/router";
import Navbar from "../components/Navbar";
import Greeting from "../components/Greeting";
import { authenticated, token } from "../hooks/Auth";
import { userid } from "../hooks/User";

interface Retro {
  retro_id: number;
  stage: number;
  is_active: boolean;
  name: string;
  desc: string;
  is_public: boolean;
  group_id: number;
  user_id: string;
  display_type: number;
  columns: string[]
}

interface RetroGroupProps {
  title: string;
  retros: Retro[];
}

const RetroGroup: Component<RetroGroupProps> = (props) => {
  return (
    <div class="bg-base-300 m-2 p-2 rounded-lg">
      <h2 class="text-2xl">{props.title}</h2>
      <ul class="list-none flex flex-row flex-wrap gap-2">
        {props.retros.map((retro) => (
          <li class="border border-white rounded-md p-2">
            <A href={`/retro/${retro.retro_id}`}>
              <div class="flex flex-col">
                <div class="flex flex-row">
                  <div class="inline">
                    <span class="text-lg">{retro.name}</span>{" "}
                    <span class="badge">{"Phase " + retro.stage}</span>{" "}
                  </div>
                  <div>
                    {!retro.is_public ? (
                      <span>
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
                            d="M16.5 10.5V6.75a4.5 4.5 0 1 0-9 0v3.75m-.75 11.25h10.5a2.25 2.25 0 0 0 2.25-2.25v-6.75a2.25 2.25 0 0 0-2.25-2.25H6.75a2.25 2.25 0 0 0-2.25 2.25v6.75a2.25 2.25 0 0 0 2.25 2.25Z"
                          />
                        </svg>
                      </span>
                    ) : (
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
                          d="M13.5 10.5V6.75a4.5 4.5 0 1 1 9 0v3.75M3.75 21.75h10.5a2.25 2.25 0 0 0 2.25-2.25v-6.75a2.25 2.25 0 0 0-2.25-2.25H3.75a2.25 2.25 0 0 0-2.25 2.25v6.75a2.25 2.25 0 0 0 2.25 2.25Z"
                        />
                      </svg>
                    )}
                  </div>
                </div>
                <div>
                  <p>{retro.desc}</p>
                  <p class="italic text-sm">Authored by {retro.user_id}</p>
                </div>
              </div>
            </A>
          </li>
        ))}
      </ul>
    </div >
  );
};

const Home: Component = () => {
  const [currentOrganizationId, setCurrentOrganizationId] = createSignal(1);
  const [retrosInOrg, setRetrosInOrg] = createSignal<Retro[]>([]);
  createComputed(async () => {
    if (!authenticated()) {
      return;
    }
    const res = await fetch("/api/v1/retrospectives/get_all_retros_in_group", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token()}`,
      },
      body: JSON.stringify({
        group_id: currentOrganizationId(),
        filter: {
          is_active: true,
          public_only: false
        }
      }),
    })
    if (res.ok) {
      const data = await res.json();
      setRetrosInOrg(data);
    }
  })
  return (
    <div>
      <Navbar />
      <div class="m-2 p-0">
        <Greeting />
      </div>
      <main>
        <div class="grid grid-rows-12 lg:grid-rows-1 lg:grid-cols-12 gap-2 m-2 bg-base-200 rounded-lg p-2 lg:divide-x-2 divide-base-300">
          <div class="lg:col-span-3 row-span-3 lg:row-span-12">
            <div class="text-center text-xl">
              <h2>...</h2>
            </div>
            <div>...</div>
          </div>
          <div class="lg:col-span-9 row-span-9 lg:row-span-12 flex flex-col p-2 gap-1">
            <div class="text-center text-xl">
              <h2>Retros</h2>
            </div>
            <div>
              <RetroGroup
                title="My Retros"
                retros={retrosInOrg().filter((retro) => retro.user_id === userid())}
              />
              <RetroGroup title="All Retros" retros={retrosInOrg()} />
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default Home;
