<script>
    import Meeting from './Meeting.svelte'
    import * as office_id from "../../backend/id.json"
    import Navbar from "./Navbar.svelte"
</script>

<Navbar/>

<Meeting uid={office_id.id}/>