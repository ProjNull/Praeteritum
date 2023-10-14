<script>
	export let title = ""
	export let qid = "0"
	import { createEventDispatcher } from 'svelte';

	const dispatch = createEventDispatcher();

	let text = "";

	const sendFdb = () => {
		dispatch('send', {
			text: text,
			col: title
		})
	}
</script>

<div class="bg-gray-300 rounded-xl p-5 w-[20rem]">
	<h1>{title}</h1>
	<div class="flex flex-col gap-2">
		<slot>
		</slot>
	</div>
	<form class="mt-2" on:submit|preventDefault={sendFdb}>
		<input bind:value={text} class="bg-gray-400 text-black placeholder:text-gray-500 p-2 rounded-xl" type="text" name="" id="" placeholder="Text">
		<input class="bg-gray-400 text-black placeholder:text-gray-500 p-2 rounded-xl" type="submit" value="Add">
	</form>
</div>