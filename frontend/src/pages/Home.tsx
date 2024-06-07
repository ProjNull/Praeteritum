import { createComputed, createSignal, For, type Component } from "solid-js";
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

interface Organization {
  group_id: number;
  name: string;
}

interface CreateOrganizationProps {
  callbackFunc: () => void;
}

const CreateOrganization: Component<CreateOrganizationProps> = ({
  callbackFunc,
}) => {
  const [name, setName] = createSignal("");

  const handleSubmit = async (e: Event) => {
    e.preventDefault();
    const body = { name: name() };
    const response = await fetch("/api/v1/groups/create_group", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token()}`,
      },
      body: JSON.stringify(body),
    });
    if (response.status != 200 || response.redirected) {
      throw new Error("Error creating organization");
    }
    setName("");
    await callbackFunc();
  };

  return (
    <div class="card bg-base-100 shadow-xl">
      <form onSubmit={handleSubmit}>
        <div class="card-body">
          <h2 class="card-title">Create new organization</h2>
          <div class="form-control">
            <input
              type="text"
              placeholder="Organization name"
              value={name()}
              onInput={(e) => setName((e.target as HTMLInputElement).value)}
              class="input input-bordered w-full"
            />
          </div>
          <div class="card-actions justify-end">
            <button type="submit" class="btn btn-primary">
              Create
            </button>
          </div>
        </div>
      </form>
    </div>
  );
};

const RetroGroup: Component<RetroGroupProps> = (props) => {
  return (
    <div class="bg-base-300 m-2 p-2 rounded-lg">
      <h2 class="text-2xl">{props.title}</h2>
      <ul class="list-none flex flex-row flex-wrap gap-2">
        {props.retros.map((retro) => (
          <li>
            <div class="card w-96 bg-base-100 shadow-xl">
              <div class="card-body">
                <h2 class="card-title">{retro.name}</h2>
                <div
                  class={
                    "badge " +
                    (retro.is_public ? "badge-success" : "badge-error")
                  }
                >
                  {retro.is_public ? "Public" : "Private"}
                </div>
                <p>{retro.desc}</p>
                <div class="card-actions justify-end">
                  <button
                    class="btn btn-primary"
                    onclick={() => {
                      window.location.href = `/retro/${retro.retro_id}`;
                    }}
                  >
                    Open
                  </button>
                </div>
              </div>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
};

async function fetchGroups(
  setterOrgList: (orgs: Organization[]) => void,
  setterCurrentOrgId: (id: number) => void
) {
  const res = await fetch("/api/v1/groups/get_groups", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token()}`,
    },
  });
  if (res.ok) {
    const data = await res.json();
    setterOrgList(data);
    setterCurrentOrgId(data[0].group_id);
  }
}

const Home: Component = () => {
  const [organizations, setOrganizations] = createSignal<Organization[]>([]);
  const [currentOrganizationId, setCurrentOrganizationId] = createSignal(1);
  const [retrosInOrg, setRetrosInOrg] = createSignal<Retro[]>([]);
  // TODO: If the user has no organizations, force open a create dialogue. It's easier than handling the errors.
  createComputed(async () => {
    fetchGroups(setOrganizations, setCurrentOrganizationId);
  });
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
              <h2>Organizations</h2>
            </div>
            <div class="flex flex-col gap-2">
              <For each={organizations()}>
                {(organization) => (
                  <div class="card bg-base-100 shadow-xl">
                    <div class="card-body">
                      <h2 class="card-title">{organization.name}</h2>
                      <div
                        class={
                          "badge " +
                          (organization.group_id === currentOrganizationId()
                            ? "badge-success"
                            : "badge-error")
                        }
                      >
                        <button
                          onClick={() =>
                            setCurrentOrganizationId(organization.group_id)
                          }
                        >
                          {organization.group_id === currentOrganizationId()
                            ? "Current"
                            : "Click here to switch"}
                        </button>
                      </div>
                      <div>
                        <button class="btn btn-ghost hover:bg-error btn-circle" onClick={async () => {
                          await fetch("/api/v1/groups/leave_group", {
                            method: "POST",
                            headers: {
                              "Content-Type": "application/json",
                              Authorization: `Bearer ${token()}`,
                            },
                            body: JSON.stringify({
                              group_id: organization.group_id,
                            }),
                          })
                          await fetchGroups(setOrganizations, setCurrentOrganizationId);
                          }}>
                          <svg
                            xmlns="http://www.w3.org/2000/svg"
                            fill="none"
                            viewBox="0 0 24 24"
                            stroke-width="1.5"
                            stroke="currentColor"
                            class="size-6"
                          >
                            <path
                              stroke-linecap="round"
                              stroke-linejoin="round"
                              d="M8.25 9V5.25A2.25 2.25 0 0 1 10.5 3h6a2.25 2.25 0 0 1 2.25 2.25v13.5A2.25 2.25 0 0 1 16.5 21h-6a2.25 2.25 0 0 1-2.25-2.25V15M12 9l3 3m0 0-3 3m3-3H2.25"
                            />
                          </svg>
                        </button>
                      </div>
                    </div>
                  </div>
                )}
              </For>
              <CreateOrganization
                callbackFunc={async () =>
                  fetchGroups(setOrganizations, setCurrentOrganizationId)
                }
              />
            </div>
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
