import { createSignal, For, type Component } from "solid-js";
import Navbar from "../components/Navbar";

interface Group {
    group_id: string;
    name: string;
}
interface Retro {
    retro_id: number;
    group_id: number;
    user_id: string;
    name: string;
    desc: string;
    columns: string;
    display_type: number;
    stage: number;
    is_active: boolean;
    is_public: boolean;
}

interface Member {
    user_id: string;
    name: string;
}

interface Action {
    action_id: string;
    name: string;
}

interface Team {
    team_id: string;
    name: string;
}

const [group, setGroup] = createSignal({} as Group);
const [retros, setRetros] = createSignal([] as Retro[]);
const [members, setMembers] = createSignal([] as Member[]);
const [actions, setActions] = createSignal([] as Action[]);
const [teams, setTeams] = createSignal([] as Team[]);

const Home: Component = () => {
  return (
    <div>
        <Navbar/>
        <main>
            <div class="lg:mx-10 mx-5 mt-10 bg-base-200">
                <div class="bg-base-300 font-bold px-5 py-4 text-xl">
                    <p>Group Name</p>
                </div>
                <div class="grid lg:grid-cols-2 grid-cols-1 gap-4 p-8">
                    <div class="bg-base-100 p-3 overflow-hidden">
                        <p class="font-bold text-lg">Retrospectives</p>
                        <hr class="my-2"/>
                        <table class="w-full text-left border-collapse border border-base-300">
                            <thead class="bg-base-200">
                                <tr class="border border-base-300">
                                    <th>Name</th>
                                    <th>Author</th>
                                    <th>Description</th>
                                    <th>Active/Ended</th>
                                    <th>public/private</th>
                                    <th>stage</th>
                                </tr>
                            </thead>
                            <tbody>
                                <For each={retros()}>{
                                    (retro) =>
                                    <tr class="bg-base-200">
                                        <td class="text-nowrap  align-top"><a href={"/retro/"+retro.retro_id}>{retro.name}</a></td>
                                        <td class="text-nowrap  align-top">{"by "+retro.user_id}</td>
                                        <td>{retro.desc}</td>
                                        <td>{retro.is_active ? "active":"ended"}</td>
                                        <td>{retro.is_public ? "public":"private"}</td>
                                        <td>{retro.stage}</td>
                                    </tr>
                                }</For>
                            </tbody>
                        </table>
                    </div>
                    <div class="bg-base-100 p-3">
                        <p class="font-bold text-lg">Members</p>
                        <hr class="my-2"/>
                        <table class="w-full text-left border-collapse border border-base-300">
                            <thead class="bg-base-200">
                                <tr class="border border-base-300">
                                    <th>Name</th>
                                </tr>
                            </thead>
                            <tbody>
                                <For each={members()}>{
                                    (member) =>
                                    <tr class="bg-base-200">
                                        <td>{member.name}</td>
                                    </tr>
                                }</For>
                            </tbody>
                        </table>
                    </div>
                    <div class="bg-base-100 p-3">
                        <p class="font-bold text-lg">Actions</p>
                        <hr class="my-2"/>
                        <table class="w-full text-left border-collapse border border-base-300">
                            <thead class="bg-base-200">
                                <tr class="border border-base-300">
                                    <th>Name</th>
                                </tr>
                            </thead>
                            <tbody>
                                <For each={actions()}>{
                                    (action) =>
                                    <tr class="bg-base-200">
                                        <td>{action.name}</td>
                                    </tr>
                                }</For>
                            </tbody>
                        </table>
                    </div>
                    <div class="bg-base-100 p-3">
                        <p class="font-bold text-lg">Teams</p>
                        <hr class="my-2"/>
                        <table class="w-full text-left border-collapse border border-base-300">
                            <thead class="bg-base-200">
                                <tr class="border border-base-300">
                                    <th>Name</th>
                                </tr>
                            </thead>
                            <tbody>
                                <For each={teams()}>{
                                    (team) =>
                                    <tr class="bg-base-200">
                                        <td>{team.name}</td>
                                    </tr>
                                }</For>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </main>
    </div>
  );
};

export default Home;
