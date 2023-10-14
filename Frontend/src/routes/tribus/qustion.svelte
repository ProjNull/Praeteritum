<script>
	import {IconArrowNarrowLeft,IconRefresh} from '@tabler/icons-svelte'
	import Table from "./table.svelte";
	import Answ from './answ.svelte';

	import { createEventDispatcher } from 'svelte';

	const dispatch = createEventDispatcher();

	export let title = "Example Title"
</script>

<div class="sticky top-0 flex bg-pink-200 rounded-b-xl content-between">
	<a class="hover:bg-pink-400 rounded-xl" href="/"><IconArrowNarrowLeft size={40}/></a>
	<div class="flex-grow justify-center items-center flex">
		<h1 class="text-center text-2xl font-bold">{title}</h1>
	</div>
	<button on:click={() => dispatch('reload')} class="hover:bg-pink-400 rounded-xl"><IconRefresh size={40}/></button>
</div>
<div class="flex justify-center gap-2 items-start flex-wrap mt-2">
	<slot>
		
	</slot>
</div>