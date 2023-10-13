<script>
	import "../app.css";
</script>

<slot />

<style>
	@import url('https://fonts.googleapis.com/css2?family=Oswald:wght@200;300;400;500;600;700&display=swap');

	:global(h1.project-name) {
		font-family: 'Oswald', sans-serif;
		font-weight: 800;
	}
</style>