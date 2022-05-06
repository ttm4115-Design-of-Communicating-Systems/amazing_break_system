<script>
  export let stop_working
</script>
  
  
<span>
  <div class="timer">
    <h2>You should be working now ;) </h2>
    <br/>
    <br/>
    <button on:click={stop_working}>Stop working</button>
        <!-- TODO: remove this (should be handeled backend)-->
    <!-- <button on:click={meeting_notify}>Meeting notify</button>  -->
  </div>
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