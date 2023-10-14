<script>
	export let hidden = false
	export let text = ""


	/**
	 * 
	 * @param {string} text
	 */
	function replaceWithRandomCharacters(text) {
            const words = text.split(' ');

            const replacedWords = words.map(word => {
                const randomChars = Array.from({ length: word.length }, () =>
                    String.fromCharCode(Math.floor(Math.random() * (126 - 33)) + 33)
                ).join('');

                return randomChars;
            });

            return replacedWords.join(' ');
        }

</script>

<div class="bg-gray-400 p-2 rounded-xl">
	<h3 class="{hidden ? "blur-sm w-fit rounded-md": ""}">
		{#if hidden}
		{replaceWithRandomCharacters(text)}
		{:else}
		{text}
		{/if}
	</h3>
</div>