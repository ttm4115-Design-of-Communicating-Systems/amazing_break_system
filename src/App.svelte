<script>
	import axios from "axios";
	import { onMount } from "svelte";
	import async from "async";
	import { io, Manager } from "socket.io-client";
	import url from './url'
	import Home from "./Components/Home.svelte"
	import Office from "./Components/Office.svelte"
	export let backend;

	let status = "standby"


</script>
  
{#if $url.hash === '' || $url.hash === '#/'}
	<Home backend={backend} status={status}/>
{:else if $url.hash === '#/office'}
	<Office backend={backend} status={status}/>
{:else}
	<h1>404</h1>
{/if}
