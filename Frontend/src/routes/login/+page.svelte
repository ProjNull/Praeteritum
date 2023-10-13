<div class="flex flex-col md:flex-row h-screen">
	<div class="bg-gray-500 flex-grow relative">
		<img src="/image/bg/login-2x.jpg" class="w-full h-full min-h-0 object-cover" alt="">
		<span class="absolute bottom-1 right-1 text-white">&copy; Pexels</span>
	</div>
	<div class="p-4 pb-20 md:px-20 flex flex-col gap-2 shadow-2xl md:justify-center">
		<img src="" class="mx-auto bg-slate-800 w-20 aspect-square" alt="">
		<h1 class="text-xl text-center">Praeterium</h1>
		<input class="login-input" required type="email" placeholder="Email">
		<input class="login-input" required minlength="8" type="password" placeholder="Password">
		<button class="bg-gray-400 w-full p-2 rounded-xl">Login</button>
		<a href="/register" class="text-gray-800 underline mx-auto">Don't have an account?</a>
	</div>
</div>


<style lang="postcss">
	.login-input {
		@apply bg-gray-200 w-full min-w-[15rem] p-2 duration-500 rounded-xl border-2 transition-colors focus:outline-none valid:bg-green-100 valid:border-green-600
	}
</style>