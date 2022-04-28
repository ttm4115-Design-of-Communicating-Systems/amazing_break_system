<script>
	import axios from "axios";
	import { onMount } from "svelte";
	import async from "async";
	import { io, Manager } from "socket.io-client";
	export let backend;
	export let start_working

	let res = ""
	async function test_f() {
		axios.get(`http://${backend}/`)
				.then(function (response) {
					res += response.data.mutch
					console.log("resp: ", response.data);
				})
				.catch(function (error) {
					console.log(error);
				});
	}
	let websocket_qa = []
	let socket;
	async function websocket_test(){
		socket = io(`ws://${backend}/ws_test`)
		socket.on("connect", ()=> {
			socket.emit("message", {data: "ping"})
			websocket_qa.push("ping")
			websocket_qa = websocket_qa
		})
		socket.on("message",(event)=>{
			let resp_obj = JSON.parse(event)
			websocket_qa.push(resp_obj.data);
			websocket_qa = websocket_qa;
			(async () => {
				await new Promise(resolve => setTimeout(resolve, 500));
				socket.emit("message", {data: "ping"});
				websocket_qa.push("ping");
				websocket_qa = websocket_qa;
			})()
		})
	}

	export let wt  //work time
	export let bt  //break time
	let previousWt = wt
	let previousBt = bt

	const wtvalidator = (node, value) => {
		return {
			update(value) {
				wt = value === null || wt < node.min ? previousWt : parseInt(value)
				previousWt = value
			}
		}
	}

	const btvalidator = (node, value) => {
		return {
			update(value) {
				bt = value === null || bt < node.min ? previousBt : parseInt(value)
				previousBt = value
			}
		}
	}

</script>

<main>
	<h1>Amazing break system</h1>

	Work time: <input type="number" use:wtvalidator={wt} bind:value={wt} min=1> <br/>
	Break time: <input type="number" use:btvalidator={bt} bind:value={bt} min=1> <br/>

	<br/>
	<button on:click={start_working}>Start working</button>
	<br/><br/>
	
	<button on:click={test_f}>axios_test</button>
	<button on:click={websocket_test}>start websocket test</button>
	<h3>server answer: {res}</h3>

	<h2>web socket qa log: {websocket_qa}</h2>
</main>

<style>
	main {
		text-align: center;
		padding: 1em;
		max-width: 240px;
		margin: 0 auto;
	}
	h2{
		word-wrap: break-word;
		width: 100%;
	}

	h3{
		word-wrap: break-word;
		width: 100%;
	}
	h1 {
		color: #5bc0de;
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