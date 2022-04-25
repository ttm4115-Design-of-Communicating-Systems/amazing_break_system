<script>
	import axios from "axios";
	import { onMount } from "svelte";
	import async from "async";
	import { io, Manager } from "socket.io-client";
	export let name;

	let res = ""
	async function test_f() {
		axios.get('http://127.0.0.1:5000/')
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
		socket = io("ws://127.0.0.1:5000/ws_test")
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

	let signSocket;
	async function signaling_test(){
		signSocket = io("ws://127.0.0.1:9999")
		signSocket.on("connect", ()=> {
			signSocket.emit("message", JSON.stringify({type: "login", name: "testing"}));
		})
		signSocket.on("message",(event)=>{
			console.log("From server: " + event)
		})
	}
</script>

<main>
	<h1>Hello {name}!</h1>
	<p>Visit the <a href="https://svelte.dev/tutorial">Svelte tutorial</a> to learn how to build Svelte apps.</p>
	<button on:click={test_f}>axios_test</button>
	<button on:click={websocket_test}>start websocket test</button>
	<button on:click={signaling_test}>start signaling test (see console)</button>
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
