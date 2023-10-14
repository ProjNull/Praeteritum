<script>
	import NullLogo from "../nullLogo.svelte";
	import APIHandler from "$lib/apiHandler";
	import { goto } from "$app/navigation";
	import Cookies from "js-cookie";
	const api = new APIHandler()
	let proccesing = false
	const login = async (e) => {
		proccesing = true
		const formData = new FormData(e.target);
		
		let out = {"token":undefined}
		try {
			out = await api.login(formData.get("email"),formData.get("pass"))
		} catch (error) {
			proccesing = false
		}
		
		if (out["token"]) {
			Cookies.set('token', out["token"], { expires: 1 })
			goto("/")
		} else {
			alert(`Error\n${out["name"]}\n${out["description"]}`)
		}
		proccesing = false
	}
</script>
<div class="flex flex-col sm:flex-row h-screen">
	<div class="bg-gray-500 flex-grow relative">
		<img src="/image/bg/login-2x.jpg" class="w-full h-full min-h-0 object-cover" alt="">
		<span class="absolute bottom-1 right-1 text-white">&copy; Pexels</span>
	</div>
	<form class="p-4 pb-20 sm:px-20 flex min-w-[25rem] flex-col gap-2 shadow-2xl sm:justify-center relative" on:submit|preventDefault={login}>
		<img src="/image/logo.png" class="mx-auto drop-shadow-xl w-20 aspect-square" alt="">
		<h1 class="project-name text-xl text-center">Praeterium</h1>
		<input disabled={proccesing} class="login-input" name="email" required type="email" placeholder="Email">
		<input disabled={proccesing} class="login-input" name="pass" required minlength="8" type="password" placeholder="Password">
		<input disabled={proccesing} class="bg-gray-200 rounded-xl p-2 hover:bg-gray-300 w-full focus:bg-gray-300" type="submit" value="Login">
		<a href="/register" class="text-gray-800 underline mx-auto">Don't have an account?</a>
		<NullLogo></NullLogo>
	</form>
</div>


<style lang="postcss">
	input:focus {
		@apply outline outline-offset-2 outline-pink-700
	}
	input {
		@apply w-full
	}
	.login-input {
		@apply bg-gray-200 w-full p-2 duration-200 rounded-xl border-2 transition-colors valid:bg-green-100 valid:border-green-600
	}
	.login-input-flex {
		@apply bg-gray-200 w-full flex-1 p-2 duration-500 rounded-xl border-2 transition-colors valid:bg-green-100 valid:border-green-600
	}
	input.validate {
		@apply invalid:bg-red-200 invalid:border-red-700
	}
	input.invalid {
		@apply !bg-red-200 !border-red-700
	}

	input:disabled {
		@apply opacity-50 pointer-events-none
	}
</style>