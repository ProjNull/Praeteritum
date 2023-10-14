<script>
	import Table from "../table.svelte";
	import Cookies from "js-cookie";
	import { page } from '$app/stores';
	import { goto } from "$app/navigation";
	import Qustion from "../qustion.svelte";

	import Answ from "../answ.svelte";
	
	import APIHandler from "$lib/apiHandler";

	const api = new APIHandler();
	(async () => {
		if (Cookies.get("token")) {
			api.setToken(Cookies.get("token"))
		} else {
			goto("/login")
		}
	})()


	let qustion = 0
	let qustions = [{
		cols: []
	}];

	(async () => {
		qustions = await api.getQuestions($page.params.id)
		qustions = qustions
	})()

	let feeds = []

	const fetchFeed = async () => {
		console.log("hi");
		const odata = await api.fetchFeedbacks(qustion)
		feeds = odata.feedbacks
	}
	

	const sendFeed = async (data) => {
		console.log("hi");
		await api.sendFeedback(data.detail.text, data.detail.col, qustion)
		await fetchFeed()
	}
	

</script>
<span class="w-full fixed bottom-0 text-center pointer-events-none" style="bottom: 0; opacity: 0.2;">id: {$page.params.id}</span>


<Qustion title="Cool TItle" on:reload={fetchFeed}>
	{#each qustions[0].cols as col, index}
		<Table title={col} qid={index.toString()} on:send={sendFeed}>
			{#each feeds.filter((s) => s.col == col) as feed, index}
				<Answ text={feed.content}>
					
				</Answ>
			{/each}
		</Table>
	{/each}
</Qustion>