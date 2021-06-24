<script>
    import "../lib/TailwindCSS.svelte";
    import { onMount, onDestroy } from "svelte";

    let hostAccessKey = "";
    let myName = "Me";
    let myKeyLoaded = false;

    onMount(async () => {
        getMyKey();
    });

    onDestroy(async () => {});

    const getMyKey = async () => {
        var myKeyReq = await fetch("my-key?");
        var myKeyResp = await myKeyReq.json();
        hostAccessKey = myKeyResp.key;
        myKeyLoaded = true;
    };
</script>

<div class="container mx-auto sm:p-10">
    <h2 class="text-2xl pt-4 pb-2">My Profile</h2>
    <div
        class="border border-gray-300 p-2 grid grid-cols-1 gap-2 bg-gray-200 shadow-lg rounded-lg"
    >
        {#if myKeyLoaded}
            <p><b>Access Key:</b> {hostAccessKey}</p>
        {/if}
        <p><b>Name:</b> {myName} (this is weird but it's fine for now)</p>
    </div>
</div>
