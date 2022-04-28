<script>
	import axios from "axios";
	import { onMount } from "svelte";
	import async from "async";
	import { io, Manager } from "socket.io-client";
    import Settings from "./Settings.svelte"
    import Working from "./Working.svelte"
	export let backend;
    export let status

    let websocket_qa = []
	let socket;

    //TODO: save in local storage
    let wt = 25 //work time
    let bt = 10 //break time

    async function start_working(){
		socket = io(`ws://${backend}/ws_test`) //TODO: update backend adress
		socket.on("connect", ()=> {
			socket.emit("message", {data: {wt: wt, bt:bt}})
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

</script>

<main>
    {#if status == "setup"}
	    <Settings backend={backend} start_working={start_working} wt={wt} bt={bt}/>
    {:else if status=="working"}
        <Working wt={wt} bt={bt}/>
    {/if}
</main>

