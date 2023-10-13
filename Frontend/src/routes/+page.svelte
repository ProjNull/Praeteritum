<script>
	import apiHandler from "$lib/apiHandler";
	const api = new apiHandler();
	let reponse = {};
	(async () => {
		reponse = await api.uniFetch("/ping/")
		console.log(reponse);
	})()


</script>

<div class="loading">
	<div class="w-12 h-12 border-black border-4 border-l-transparent rounded-[50%]  box-border"></div>
</div>


<style lang="postcss">
	.loading div {
		animation: loading 2s cubic-bezier(.62,.28,.41,.77) infinite;
		position: fixed;
		top: 50%;
		left: 50%;
		opacity: 1;
	}
	@keyframes loading {
		0% {
			transform: translate(-50%,-53%) rotate(0turn);

		}
		100% {
			transform: translate(-50%,-50%) rotate(5turn);
		}
	}
	.loading.hide {
		opacity: 0;
	}
</style>