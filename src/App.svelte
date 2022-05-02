<script>
	import axios from "axios";
	import { onMount } from "svelte";
	import async from "async";
	import { io, Manager } from "socket.io-client";
	import url from './url'
	import Home from "./Components/Home.svelte"
	import Office from "./Components/Office.svelte"
	import Meeting from "./Components/Meeting.svelte"
	import { v4 as uuidv4 } from 'uuid';
	export let backend;
	export let signalingBackend;
	export let name;

	let status = "standby"
	let uid = uuidv4();

</script>

{#if $url.hash === '' || $url.hash === '#/'}
	<Home backend={backend} status={status}/>
	<Meeting uid={uid} signalingBackend={signalingBackend}/>
{:else if $url.hash === '#/office'}
	<Office backend={backend} status={status}/>
{:else}
	<h1>404</h1>
{/if}

<style>
	main{
		text-align: center;
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
