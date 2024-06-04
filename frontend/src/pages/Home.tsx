import {
  createComputed,
  createEffect,
  createSignal,
  Show,
  type Component,
} from "solid-js";
import Navbar from "../components/Navbar";
import Greeting from "../components/Greeting";
import { userid } from "../hooks/User";
import { token } from "../hooks/Auth";

interface Group {
  group_id: number;
  name: string;
}

interface Team {
  group_id: number;
  name: string;
  team_id: number;
}

interface TeamMember {
  user_id: string;
  utt_id: number;
  team_id: number;
  permission_level: number;
}

interface PropsGroups {
  groups: Group[];
}

const Groups: Component<PropsGroups> = (props) => {
  return (
    <div class="flex flex-col gap-2">
      {props.groups.map((group) => (
        <div>
          ({group.group_id}) {group.name}
        </div>
      ))}
    </div>
  );
};

interface PropsTeams {
  teams: Team[];
}

const Teams: Component<PropsTeams> = (props) => {
  const fetchMembers = async (token: string, team_id: number) => {
    const response = await fetch(
      "/api/v1/teams/get_all_team_member_relations",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          team_id: team_id,
        }),
      }
    ).then((response) => response.json());
    return response;
  };
  const [teamMembers, setTeamMembers] = createSignal([] as TeamMember[]);
  createEffect(() => {
    fetchMembers(token(), 1).then((data) => setTeamMembers(data));
  });
  return (
    <div class="flex flex-col gap-2">
      {props.teams.map((team) => (
        <div>
          ({team.group_id}:{team.team_id}) {team.name}
          <div>
            <ul>
              {teamMembers().map((member) => (
                <li>{member.user_id}</li>
              ))}
            </ul>
          </div>
        </div>
      ))}
    </div>
  );
};

const Home: Component = () => {
  const [groupsReady, setGroupsReady] = createSignal(false);

  const [groups, setGroups] = createSignal([] as Group[]);

  const [teamsReady, setTeamsReady] = createSignal(false);

  const [teams, setTeams] = createSignal([] as Team[]);

  const fetchGroups = async (userid: string, token: string) => {
    const response = await fetch("/api/v1/groups/get_groups", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      }
    });
    if (response.status != 200 || response.redirected) {
      return;
    }
    await response.json().then((data) => {
      setGroups(data);
      setGroupsReady(true);
    });
  };

  createComputed(() => {
    fetchGroups(userid(), token());
  });

  const fetchTeams = async (token: string, group_id: number) => {
    const response = await fetch("/api/v1/teams/get_all_teams_in_org", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({
        organization_id: group_id,
      }),
    });
    if (response.status != 200 || response.redirected) {
      return;
    }
    await response.json().then((data) => {
      setTeams(data);
      setTeamsReady(true);
    });
  };

  createComputed(() => {
    if (groups().length <= 0) {
      return;
    }
    const group: Group = groups()[groups().length - 1];
    fetchTeams(token(), group.group_id);
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
            <div>
              <Show when={groupsReady()} fallback={<div>Loading...</div>}>
                <Groups groups={groups()} />
              </Show>
            </div>
          </div>
          <div class="lg:col-span-9 row-span-9 lg:row-span-12 flex flex-col p-2 gap-1">
            <div class="text-center text-xl">
              <h2>Teams</h2>
            </div>
            <div>
              <Show when={teamsReady()} fallback={<div>Loading...</div>}>
                <Teams teams={teams()} />
              </Show>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default Home;
