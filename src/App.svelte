<script>
	import axios from "axios";

	export let name;

	let res = "Answer goes here"
	async function test_f() {
		axios.get('http://127.0.0.1:5000/test')
				.then(function (response) {
					res = response.data.mutch
					console.log("resp: ", response.data);
				})
				.catch(function (error) {
					console.log(error);
				});
	}
</script>

<main>
	<h1>Hello {name}!</h1>
	<p>Visit the <a href="https://svelte.dev/tutorial">Svelte tutorial</a> to learn how to build Svelte apps.</p>
	<button on:click={test_f}>axios_test</button>
	<h3>server answer: {res}</h3>
</main>

<style>
	main {
		text-align: center;
		padding: 1em;
		max-width: 240px;
		margin: 0 auto;
	}

	h1 {
		color: #ff3e00;
		text-transform: uppercase;
		font-size: 4em;
		font-weight: 100;
	}

	@media (min-width: 640px) {
		main {
			max-width: none;
		}
	}
</style>