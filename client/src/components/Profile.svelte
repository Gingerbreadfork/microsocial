<script>
    import { onMount, onDestroy } from "svelte";

    let hostAccessKey = "";
    let myKeyLoaded = false;
    let hostUsername = "";
    let hostProfileLoaded = false;
    let hostBridge = window.location.hostname;
    let hostBio = "";
    let hostPostsLoaded = false;
    let hostPosts;

    let devBridge = "";

    if (hostBridge == "localhost") {
        devBridge = "https://41034m.deta.dev/";
    }

    onMount(async () => {
        getMyKey();
        getMyProfile();
    });

    onDestroy(async () => {});

    const getMyKey = async () => {
        var myKeyReq = await fetch(devBridge + "my-key?");
        var myKeyResp = await myKeyReq.json();
        hostAccessKey = myKeyResp.key;
        myKeyLoaded = true;
        getHostPosts();
    };

    const getMyProfile = async () => {
        var hostProfileReq = await fetch(devBridge + "public/profile");
        var hostProfileResp = await hostProfileReq.json();
        hostUsername = hostProfileResp.username;
        hostBio = hostProfileResp.bio;
        hostProfileLoaded = true;
    };

    const getHostPosts = async () => {
        var postsURL = devBridge + "public/shared-posts?key=" + hostAccessKey;
        var hostPostsReq = await fetch(postsURL);
        var hostPostsResp = await hostPostsReq.json();
        hostPosts = hostPostsResp;
        hostPostsLoaded = true;
    };

    function convertTimestamp(timestamp) {
        var dateObject = new Date(timestamp * 1000);
        var readableDate = dateObject.toLocaleString();
        return readableDate;
    }
</script>

<div class="container mx-auto sm:p-10">
    {#if hostUsername != ""}
        <h2 class="text-2xl pt-4 pb-2">{hostUsername}'s Profile</h2>
    {/if}
    {#if hostProfileLoaded}
        <div
            class="border border-gray-300 p-2 mb-4 grid grid-cols-1 gap-2 bg-gray-200 shadow-lg rounded-lg"
        >
            <p class="break-words">{hostBio}</p>
        </div>
    {/if}
    {#if hostPostsLoaded}
        <h2 class="text-2xl pt-4 pb-2">Posts</h2>
        {#each hostPosts as { value, time }}
            <div
                class="bg-gray-200 p-2 mb-4 h-auto rounded-2xl shadow-lg flex flex-col sm:flex-row gap-5 border border-gray-300"
            >
                <div class="flex sm:flex-1 flex-col gap-2 p-1">
                    <p class="text-gray-400">
                        {convertTimestamp(time)}
                    </p>
                    <p
                        class="text-gray-500 text-sm sm:text-base line-clamp-3 break-words"
                    >
                        {value}
                    </p>
                </div>
            </div>
        {/each}
    {/if}
</div>
