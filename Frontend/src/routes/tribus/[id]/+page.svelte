<script>
	import Table from "../table.svelte";
	import { page } from '$app/stores';
	
</script>
<div class="sticky top-0">
	<a href="/">Back</a>
</div>
<span class="w-full fixed bottom-0 text-center pointer-events-none" style="bottom: 0; opacity: 0.2;">id: {$page.params.id}</span>
<div class="flex justify-center gap-2 items-center w-screen h-screen overflow-x-auto overflow-y-auto">
	<Table>

	</Table>
	<Table>

	</Table>
	<Table>

	</Table>
	<Table>

	</Table>
</div>