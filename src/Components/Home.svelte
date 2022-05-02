<script>
	import axios from "axios";
  import Settings from "./Settings.svelte"
  import Working from "./Working.svelte"
  import MeetingNotify from "./MeetingNotify.svelte"
  import Meeting from "./Meeting.svelte"

  let wt = 0
  let bt = 0

  const URL = "http://127.0.0.1:5000"
  let state = "LOADING"

  async function poll_get_state() {
    setInterval(async () => {
      try {
        const res = await axios.get(`${URL}/state`)
        console.log(res.data)
        state = res.data.state
        wt = parseInt(res.data.wt)
        bt = parseInt(res.data.bt )
      } catch {
        console.error(`POLL FAILED AT ${Date.now()}`)
        state = "NETWORK ISSUES"
      }
    }, 1000);
  }

  async function post_event(msg, wt=null, bt=null) {
    try {
      await axios.post(`${URL}/post`, {
        message: msg,
        wt, bt
      })
    } catch {
      console.error("COULD NOT POST EVENT")
    }
  }

  poll_get_state()
</script>

<main>
  <h1>{state}</h1>

  {#if state == "STANDBY"}
    <nav>
        <a href="#/">Home</a>
        <a href="#/office">Office</a>
    </nav>
    <Settings 
      wt={wt}
      bt={bt}
      start_working={() => post_event('click_start_timer')} 
      update_durations={(wt, bt) => post_event('update_dur', wt, bt)}
    />
  
  {:else if state == "WORKING"}
    <Working 
      stop_working={() => post_event('click_abort')} 
    />
  
  {:else if state == "WAITING"}
    <MeetingNotify 
      dont_pause={() => post_event('dont_pause')} 
      accept_meeting={() => post_event('accept_meeting')}
    />

  {:else if state == "SEARCHING"}
    <p>Looking for pause partner...</p>
    <p>Will time out after 5 seconds</p>

  {:else if state == "MEETING"}
      <Meeting/>
  {/if}
</main>

