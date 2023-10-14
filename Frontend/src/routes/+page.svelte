<script>
	import { browser } from "$app/environment";
	import Cookies from "js-cookie";
	import { goto } from "$app/navigation";
	import apiHandler from "$lib/apiHandler";
	import Board from "./board.svelte";
	const api = new apiHandler();
	let reponse = {};
	(async () => {
		reponse = await api.uniFetch("/ping/")
		console.log(reponse);
	})()

	let isLoggedIn = false

	if (Cookies.get("token")) {
		isLoggedIn = true
	} else {
		goto("/login")
	}
</script>

<div class="loading {isLoggedIn ? 'hide': ''}">
	<div class="w-12 h-12 border-black border-4 border-l-transparent rounded-[50%]  box-border"></div>
</div>

<div class="bg-slate-200 w-[98vw] max-w-[50rem] mx-auto mt-[10%] p-2 rounded-xl">
	<div class="mx-auto w-20 bg-gray-400 rounded-full aspect-square -mt-10">

	</div>

	<div class="text-center font-bold text-xl">
		Hello someone!
	</div>

	<h2>Avalible tribus boards</h2>
	<div class="flex flex-col gap-2">
		<Board>
			<span slot="title">Someone</span>
			<span slot="by">user</span>
		</Board>

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
	}
</style>