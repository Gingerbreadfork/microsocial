<script>
    import { onMount, onDestroy } from "svelte";
    import * as timeago from "timeago.js";

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
        <div class="p-1">
            <div class="bg-gray-100 p-4 rounded-lg shadow-lg border-2">
                <p class="text-gray-600 text-sm">{hostBio}</p>
            </div>
        </div>
    {/if}
    {#if hostPostsLoaded}
        <h2 class="text-2xl pt-4 pb-2">Posts</h2>
        {#each hostPosts as { value, time }}
            <div class="p-1">
                <div class="bg-gray-100 p-4 rounded-lg shadow-lg border-2">
                    <div class="flex">
                        <div class="flex items-center text-xs text-gray-400">
                            <p>{convertTimestamp(time)}</p>
                            <p class="px-1">•</p>
                            <p>
                                {timeago.format(convertTimestamp(time))}
                            </p>
                        </div>
                    </div>
                    <div class="mt-2">
                        <p class="text-gray-600 text-sm">
                            {value}
                        </p>
                    </div>
                </div>
            </div>
        {/each}
    {/if}
</div>
