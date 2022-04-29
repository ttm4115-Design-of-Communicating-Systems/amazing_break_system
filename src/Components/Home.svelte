<script>
	import axios from "axios";
	import { onMount } from "svelte";
	import async from "async";
	import { io, Manager } from "socket.io-client";
    import Settings from "./Settings.svelte"
    import Working from "./Working.svelte"
    import MeetingNotify from "./MeetingNotify.svelte"
    import Meeting from "./Meeting.svelte"
	export let backend;
    export let status

    let websocket_qa = []
	let socket;

    //TODO: save in local storage
    let wt = 25 //work time
    let bt = 10 //break time

    async function start_working(){
        status="user_working"
		socket = io(`ws://${backend}/ws_test`) //TODO: update backend adress
		socket.on("connect", ()=> {
			socket.emit("message", {data: {status: "click_start_timer", wt: wt, bt:bt}})
			websocket_qa.push("ping")
			websocket_qa = websocket_qa
		})
		socket.on("message",(event)=>{
			let resp_obj = JSON.parse(event)
            console.log(resp_obj.data)

            //TODO: fix backend to send these (or equivalent) messages
            if(resp_obj.data.status && resp_obj.data.status == "meeting_notify"){
                meeting_notify()
            }
            if(resp_obj.data.status && resp_obj.data.status == "back_to_work"){
                back_to_work()
            }
		})
        socket.on('close', () => console.log('disconnected'));
	}

    async function stop_working(){
        status="standby"
        socket.emit("message", {data: {status: "click_abort"}});
    }

    async function dont_pause(){
        status="user_working"
        socket.emit("message", {data: {status: "dont_pause"}});
    }

    async function meeting_notify(){
        status="meeting_notify"
    }

    async function accept_meeting(){
        console.log("meeting")
        status="meeting"
        socket.emit("message", {data: {status: "accept_meeting"}}); 
    }

    async function back_to_work(){
        status="user_working"
    }

</script>

<main>
    {#if status == "standby"}
        <nav>
            <a href="#/">Home</a>
            <a href="#/office">Office</a>
        </nav>
	    <Settings backend={backend} start_working={start_working} wt={wt} bt={bt}/>
    {:else if status=="user_working"}
        <Working wt={wt} stop_working={stop_working} meeting_notify={meeting_notify}/>
    {:else if status =="meeting_notify"}
        <MeetingNotify dont_pause={dont_pause} accept_meeting={accept_meeting}/>
    {:else if status == "meeting"}
        <Meeting/>
    {/if}
</main>

