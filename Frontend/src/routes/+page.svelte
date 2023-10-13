<script>
	import apiHandler from "$lib/apiHandler";
	const api = new apiHandler();
	let reponse = {};
	(async () => {
		reponse = await api.uniFetch("/ping/")
		console.log(reponse);
	})()
</script>

<h1>Welcome to SvelteKit</h1>
<p>Visit <a href="https://kit.svelte.dev">kit.svelte.dev</a> {reponse}</p>
