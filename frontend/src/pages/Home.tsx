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
  columns: string[];
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
          <li>
              <div class="card w-96 bg-base-100 shadow-xl">
                <div class="card-body">
                  <h2 class="card-title">{retro.name}</h2><div class={"badge " + (retro.is_public ? "badge-success" : "badge-error")}>{retro.is_public ? "Public" : "Private"}</div>
                  <p>{retro.desc}</p>
                  <div class="card-actions justify-end">
                    <button class="btn btn-primary" onclick={() => { window.location.href = `/retro/${retro.retro_id}` }}>Open</button>
                  </div>
                </div>
              </div>
          </li>
        ))}
      </ul>
    </div>
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
          public_only: false,
        },
      }),
    });
    if (res.ok) {
      const data = await res.json();
      setRetrosInOrg(data);
    }
  });
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
                retros={retrosInOrg().filter(
                  (retro) => retro.user_id === userid()
                )}
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
