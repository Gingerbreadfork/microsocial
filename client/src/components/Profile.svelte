<script>
    import { onMount, onDestroy } from "svelte";
    import * as timeago from "timeago.js";
    import anchorme from "anchorme";

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

<div class="container w-full mx-auto sm:p-10 md:w-2/3 lg:w-1/2 xl:w-1/2">
    {#if hostUsername != ""}
        <h2 class="pt-4 pb-2 text-2xl">{hostUsername}'s Profile</h2>
    {/if}
    {#if hostProfileLoaded}
        <div class="p-1">
            <div class="p-4 bg-gray-100 border-2 rounded-lg shadow-lg">
                <p class="text-sm text-gray-600">{hostBio}</p>
            </div>
        </div>
    {/if}
    {#if hostPostsLoaded}
        <h2 class="pt-4 pb-2 text-2xl">Posts</h2>
        {#each hostPosts as { value, time }}
            <div class="p-1">
                <div
                    class="p-2 bg-gray-200 border-2 border-gray-300 rounded-lg shadow-lg"
                >
                    <div class="flex">
                        <div class="flex items-center text-sm text-gray-400">
                            <p>{convertTimestamp(time)}</p>
                            <p class="px-1">•</p>
                            <p>
                                {timeago.format(convertTimestamp(time))}
                            </p>
                        </div>
                    </div>
                    <div class="mt-2">
                        <p class="text-sm text-gray-600">
                            {@html anchorme(value)}
                        </p>
                    </div>
                </div>
            </div>
        {/each}
    {/if}
</div>
