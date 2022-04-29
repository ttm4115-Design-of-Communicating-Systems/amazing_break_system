<script>
    export let dont_pause
    export let accept_meeting
</script>



<div>
    <h2> You are schedueled for a break! </h2>
    Do you wish to take a social break or keep working one more round? <br/><br/>
    <button on:click={dont_pause}>Keep working</button>
    <button on:click={accept_meeting}>BREAK-TIME!</button> 
</div>


<style>
	div {
		text-align: center;
		padding: 1em;
		max-width: 400px;
		margin: 0 auto;
	}
	h2{
		word-wrap: break-word;
		width: 100%;
	}

</style>