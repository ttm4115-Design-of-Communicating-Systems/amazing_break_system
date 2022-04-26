<script>
	import axios from "axios";
	import { onMount } from "svelte";
	import async from "async";
	import { io, Manager } from "socket.io-client";
	import { v4 as uuidv4 } from 'uuid';
	export let name;


	let localVideo = null;
	let remoteVideo = null;
	let res = ""
	let uid = uuidv4();
	let pc;
	let remoteId = '';
	let signSocket;
	let localStream;
	let websocket_qa = []
	let socket;

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

	async function setup_signaling(){
		try {
			localStream = await navigator.mediaDevices.getUserMedia({audio: true, video: true});
			localVideo.srcObject = localStream;
			localVideo.play();
		} catch (e) {
			console.log(e)
		}
		signSocket = io("ws://127.0.0.1:9999")
		signSocket.on("connect", async ()=> {
			signSocket.emit("message", JSON.stringify({type: "login", name: uid}));
		})
		signSocket.on("message",(event)=>{
			console.log("From server: " + event)
			let data = JSON.parse(event)
			switch (data.type) {
				case 'login':
					if (data.success) {
						createPeerConnection();
					}
					break;
				case 'offer':
					handleOffer(data);
					break;
				case 'answer':
					handleAnswer(data);
					break;
				case 'candidate':
					handleCandidate(data);
					break;

				default:
				console.log('unhandled', data);
				break;
			}
		})

	}

	function sendMsg(message) {
		message.name = remoteId;
		signSocket.emit("message", JSON.stringify(message));
	}

	async function signaling_test(){
		const offer = await pc.createOffer();
		sendMsg({type: "offer", offer: offer, });
		await pc.setLocalDescription(offer);
	}

	function createPeerConnection() {
		pc = new RTCPeerConnection();
		pc.onicecandidate = e => {
			const message = {
				type: 'candidate',
				candidate: null,
			};
			if (e.candidate) {
				message.candidate = e.candidate
				sendMsg(message)
			}
		};
		pc.ontrack = e => remoteVideo.srcObject = e.streams[0];
		localStream.getTracks().forEach(track => pc.addTrack(track, localStream));
	}

	async function handleOffer(offer) {
		remoteId = offer.name;
		await pc.setRemoteDescription(offer.offer);

		const answer = await pc.createAnswer();
		sendMsg({type: 'answer', answer: answer});
		await pc.setLocalDescription(answer);
		remoteVideo.play();
	}

	async function handleAnswer(answer) {
		if (!pc) {
			console.error('no peerconnection');
			return;
		}
		await pc.setRemoteDescription(answer.answer);
		remoteVideo.play();
	}

	async function handleCandidate(candidate) {
		if (!pc) {
			console.error('no peerconnection');
			return;
		}
		if (!candidate.candidate) {
			await pc.addIceCandidate(null);
		} else {
			await pc.addIceCandidate(candidate.candidate);
		}
	}

	setup_signaling();
</script>

<main>
	<h1>Hello {name}!</h1>
	<p>Visit the <a href="https://svelte.dev/tutorial">Svelte tutorial</a> to learn how to build Svelte apps.</p>
	<button on:click={test_f}>axios_test</button>
	<button on:click={websocket_test}>start websocket test</button>
	<h3>server answer: {res}</h3>
	<h2>web socket qa log: {websocket_qa}</h2>
	<h1> video test </h1>
	<h3>UUID: {uid}</h3>
	<button on:click={signaling_test}>start signaling test</button>
	<input bind:value={remoteId} placeholder="enter remote id">
	<div>
		<video bind:this={localVideo} />
		<video bind:this={remoteVideo} />
	</div>
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
	video {
		border: solid 2px black;
	}
</style>
