<script>
    import "../lib/TailwindCSS.svelte";
    import { onMount, onDestroy } from "svelte";

    let hostAccessKey = "";
    let myKeyLoaded = false;
    let hostUsername = "";
    let myNameLoaded = false;
    let hostBridge = window.location.hostname.split(".")[0];
    let myBioLoaded = false;
    let hostBio = "";

    onMount(async () => {
        getMyKey();
        getMyName();
        getMyBio();
    });

    onDestroy(async () => {});

    const getMyKey = async () => {
        var myKeyReq = await fetch("my-key?");
        var myKeyResp = await myKeyReq.json();
        hostAccessKey = myKeyResp.key;
        myKeyLoaded = true;
    };

    const getMyName = async () => {
        var myNameReq = await fetch("my-name");
        var myNameResp = await myNameReq.json();
        hostUsername = myNameResp.name;
        myNameLoaded = true;
    };

    const getMyBio = async () => {
        var myBioReq = await fetch("bio");
        var myBioResp = await myBioReq.json();
        hostBio = myBioResp;
        myBioLoaded = true;
    };
</script>

<div class="container mx-auto sm:p-10">
    {#if hostUsername != ""}
        <h2 class="text-2xl pt-4 pb-2">{hostUsername}'s Profile</h2>
    {/if}
    <div
        class="border border-gray-300 p-2 grid grid-cols-1 gap-2 bg-gray-200 shadow-lg rounded-lg"
    >
        {#if myKeyLoaded}
            {#if myNameLoaded}
                <p><b>Access Key:</b> {hostAccessKey}</p>
                <p><b>Name:</b> {hostUsername}</p>
                <p><b>Bridge:</b> {hostBridge}</p>
            {/if}
        {/if}
    </div>
    {#if myBioLoaded}
        <h2 class="text-2xl pt-4 pb-2">Bio</h2>
        <div
            class="border border-gray-300 p-2 grid grid-cols-1 gap-2 bg-gray-200 shadow-lg rounded-lg"
        >
            <p>{hostBio}</p>
        </div>
    {/if}
</div>
