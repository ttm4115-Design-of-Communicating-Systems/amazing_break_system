<script>
	import { onMount } from "svelte";
	import Countdown from 'svelte-countdown/src/index.js'
    import dayjs from 'dayjs'
    export let wt
    export let stop_working
    export let meeting_notify //TODO: remove this (should be handeled backend)

    let from = dayjs().add(wt, 'minute')

</script>
  
  
<span>
	<Countdown from={from.format("YYYY-MM-DD HH:mm:ss")} dateFormat="YYYY-MM-DD H:m:s" zone="Europe/Amsterdam" let:remaining>
		<div class="timer">
			{#if remaining.done === false}
                <h2>You should be working now ;) </h2>
				<span>{remaining.minutes} minutes</span>
				<span>{remaining.seconds} seconds</span>
                <br/>
                <br/>
                <button on:click={stop_working}>Stop working</button>
                    <!-- TODO: remove this (should be handeled backend)-->
                <button on:click={meeting_notify}>Meeting notify</button> 
			{:else}
				<h2>A break is coming up!</h2>
			{/if}
		</div>
	</Countdown>
</span>


<style>
	span {
		text-align: center;
		padding: 1em;
		max-width: 240px;
		margin: 0 auto;
	}
	h2{
		word-wrap: break-word;
		width: 100%;
	}

</style>