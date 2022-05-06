<script>
	import async from "async";
	import axios from "axios";
	import { io, Manager } from "socket.io-client";

	export let fromHome

	let localVideo = null;
	let remoteVideo = null;
	let res = ""
	let pc;
	let remoteId = '';
	let signSocket;
	let localStream;
	let websocket_qa = []
	let socket;

	export let uid;
	export let signalingBackend;

	async function setup_signaling(){
		try {
			localStream = await navigator.mediaDevices.getUserMedia({audio: true, video: true});
			localVideo.srcObject = localStream;
			localVideo.play();
		} catch (e) {
			alert("no webcam dectected")
			console.log(e)
		}
		signSocket = io(`ws://${signalingBackend}`)
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
				case 'leave':
					hangup();
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
		remoteId = answer.name;
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

	async function hangup() {
		if (pc) {
			pc.close();
			pc = null;
		}
		createPeerConnection()
	};

	function send_hangup() {
		console.log("Hangup", remoteId);
		signSocket.emit("message", JSON.stringify({type: "leave", name: remoteId}));
		hangup();
	}

	setup_signaling();
</script>
<main>
	{#if fromHome}
		<h1> Break </h1>
		<button on:click={signaling_test}>join meeting</button>
	{:else}
		<h3>UUID: {uid}</h3>
	{/if}
	<div>
		<video bind:this={localVideo} />
		<video bind:this={remoteVideo} />
	</div>
	{#if fromHome}
		<button on:click={send_hangup}>leave meeting</button>
	{/if}
</main>

<style>
	main{
		text-align: center;
	}
	h3{
		word-wrap: break-word;
		width: 100%;
	}
	h1 {
		color: green;
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
