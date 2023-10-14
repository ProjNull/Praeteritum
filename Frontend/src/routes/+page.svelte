<script>
	import { browser } from "$app/environment";
	import Cookies from "js-cookie";
	import {IconMenu2} from '@tabler/icons-svelte'
	import { goto } from "$app/navigation";
	import apiHandler from "$lib/apiHandler";
	import Board from "./board.svelte";
	const api = new apiHandler();
	let reponse = {};

	let isLoading = false

	let profile = {
		displayName:"Jan Palma",
		email: "user@example.com",
		avatar: "ssssss"
	}
	let boards = [];
	(async () => {
		if (Cookies.get("token")) {
			api.setToken(Cookies.get("token"))
			

			let boardsRaw = await api.fetchBoards(1)
			boardsRaw.boards.forEach(element => {
				boards.push({id:element.id, name: element.name})
			});
			boards = boards
			isLoading = false
		} else {
			goto("/login")
		}
	})()


	const logout = () => {
		Cookies.remove("token")
		document.location.reload()
	}

	let dropmenu = false
</script>

<div class="loading {isLoading ? '': 'hide'}">
	<div class="w-12 h-12 border-black border-4 border-l-transparent rounded-[50%]  box-border"></div>
</div>


<div class="fixed top-2 right-2 z-[999]">
	<button on:click={() => dropmenu = !dropmenu} class="bg-slate-300 aspect-square p-2 w-[48px] h-[48px] rounded-xl	"><IconMenu2 size={32}></IconMenu2></button>
	<div class="bg-slate-300 p-2 mt-2 rounded-lg flex flex-col gap-2 fixed left-2 sm:left-auto sm:absolute right-2 sm:right-0 shadow-xl {dropmenu ? "" : "hidden"}">
		<button on:click={logout} class="bg-slate-400 hover:bg-slate-500 focus:bg-slate-500 p-2 rounded-lg">Logout</button>
		<button class="bg-slate-400 hover:bg-slate-500 focus:bg-slate-500 p-2 rounded-lg">Dashboard</button>
	</div>
</div>

<div class="bg-slate-200 w-[98vw] max-w-[50rem] mx-auto mt-16 sm:mt-[10%] mb-8 p-2 rounded-xl">
	<img class="mx-auto w-20 shadow-xl bg-gray-400 rounded-full aspect-square -mt-10" src="https://www.gravatar.com/avatar/{profile.avatar}?d=identicon&f=y" alt="profile">
	<h1 class="text-center font-bold text-2xl mb-2">
		Hello {profile.displayName}!
	</h1>

	<div class="bg-slate-100 p-2 rounded-xl mt-2">
		<h2 class="text-lg">Name</h2>
		<div class="flex flex-col gap-2">
			{#each boards as boradData}
				<Board>
					<span slot="title">{boradData.name}</span>
					<span slot="by">user</span>
				</Board>
			{/each}
		</div>
	</div>

	<div class="bg-slate-100 p-2 rounded-xl mt-2">
		<h2 class="text-lg">Name</h2>
		<div class="flex flex-col gap-2">
			{#each boards as boradData}
				<Board>
					<span slot="title">{boradData.name}</span>
					<span slot="by">user</span>
				</Board>
			{/each}
			

		</div>
	</div>

</div>

<style lang="postcss">
	.loading {
		position: fixed;
		inset: 0;
		background: #fff;
	}
	.loading div {
		animation: loading 2s cubic-bezier(.62,.28,.41,.77) infinite;
		position: fixed;
		top: 50%;
		left: 50%;
		opacity: 1;
	}
	@keyframes loading {
		0% {
			transform: translate(-50%,-50%) rotate(0turn);

		}
		100% {
			transform: translate(-50%,-50%) rotate(5turn);
		}
	}
	.loading.hide {
		opacity: 0;
		pointer-events: none;
	}
</style>