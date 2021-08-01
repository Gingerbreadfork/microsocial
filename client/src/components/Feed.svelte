<script>
    import { onMount, onDestroy } from "svelte";
    import * as timeago from "timeago.js";

    let hostAccessKey = "";
    let newPost;
    let friendFeedLoaded = false;
    let friendFeedPosts;
    let friendListResp;
    let friendListLoaded = false;
    let myKeyLoaded = false;
    let notifications;
    let hostBridge = window.location.hostname;
    let devBridge = "";
    let notifyBridge;
    let refreshingFeed = false;
    let hostUsername;

    if (hostBridge == "localhost") {
        devBridge = "https://41034m.deta.dev/";
    }

    onMount(async () => {
        getMyKey();
        quickFeed();
        getFriends();
        getMyName();
    });

    onDestroy(async () => {
        clearInterval(getNotifications);
    });

    const getMyName = async () => {
        var myNameReq = await fetch(devBridge + "public/profile");
        var myNameResp = await myNameReq.json();
        hostUsername = myNameResp.username;
    };

    const getMyKey = async () => {
        var myKeyReq = await fetch(devBridge + "my-key?");
        var myKeyResp = await myKeyReq.json();
        hostAccessKey = myKeyResp.key;
        myKeyLoaded = true;
    };

    const createPost = async () => {
        var postedPost = newPost;
        newPost = "";
        refreshingFeed = true;
        var contentToPost = {
            access_key: hostAccessKey,
            value: postedPost,
        };

        var postResp = await fetch(devBridge + "create-post", {
            method: "POST",
            headers: {
                Accept: "application/json",
                "Content-Type": "application/json",
            },
            body: JSON.stringify(contentToPost),
        });
        //var postResult = await postResp.json();
        await getFeed();
        await notifyFriends();
    };

    const getFeed = async () => {
        refreshingFeed = true;
        var FeedReq = await fetch(
            devBridge +
                "feed?" +
                new URLSearchParams({
                    access_key: hostAccessKey,
                    cache: "true",
                })
        );
        friendFeedPosts = await FeedReq.json();
        friendFeedLoaded = true;
        refreshingFeed = false;
    };

    const quickFeed = async () => {
        var FeedReq = await fetch(
            devBridge +
                "feed?" +
                new URLSearchParams({
                    access_key: hostAccessKey,
                    cached: "true",
                })
        );
        friendFeedPosts = await FeedReq.json();
        friendFeedLoaded = true;
    };

    const notifyFriends = async () => {
        friendListResp.forEach(async (friend) => {
            // Only required for Dev - TODO: Remove Jank
            if (window.location.hostname == "localhost") {
                notifyBridge = "41034m.deta.dev";
            } else {
                notifyBridge = hostBridge;
            }

            var contentToPost = {
                key: hostAccessKey,
                bridge: notifyBridge,
            };
            var friendNotifURL = "https://" + friend.bridge + "/public/notify";
            var notifyResp = await fetch(friendNotifURL, {
                method: "POST",
                headers: {
                    Accept: "application/json",
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(contentToPost),
            });
        });
    };

    const getFriends = async () => {
        var listReq = await fetch(
            devBridge +
                "friend-list?" +
                new URLSearchParams({
                    access_key: hostAccessKey,
                })
        );
        friendListResp = await listReq.json();
        friendListLoaded = true;
    };

    function convertTimestamp(timestamp) {
        var dateObject = new Date(timestamp * 1000);
        var readableDate = dateObject.toLocaleString();
        return readableDate;
    }

    const clearNotifications = async () => {
        await fetch(
            devBridge +
                "notifications?" +
                new URLSearchParams({
                    clear: "True",
                })
        );
    };

    const checkNotifications = async () => {
        if (friendFeedLoaded && friendListLoaded) {
            var notificationsReq = await fetch(devBridge + "notifications?");
            notifications = await notificationsReq.json();
            if (notifications.notifications !== "No Notifications") {
                getFeed();
                clearNotifications();
            }
        }
    };

    // Intervals
    const getNotifications = setInterval(checkNotifications, 500);
</script>

<div class="container mx-auto sm:p-10">
    <div
        class="shadow-md border-2 border-gray-200 rounded p-2 mb-2 bg-gray-100"
    >
        <textarea
            bind:value={newPost}
            class="shadow rounded border p-1 focus:outline-none w-full"
            rows="5"
        />

        <div class="flex justify-end mb-2 mt-2">
            <button
                on:click={createPost}
                class="p-3 border bg-blue-500 rounded-3xl text-white focus:outline-none"
                ><svg
                    class="w-6 h-6"
                    fill="currentColor"
                    viewBox="0 0 20 20"
                    xmlns="http://www.w3.org/2000/svg"
                    ><path
                        fill-rule="evenodd"
                        d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                        clip-rule="evenodd"
                    /></svg
                ></button
            >
        </div>
    </div>

    <div class="pt-2">
        {#if friendFeedLoaded}
            {#if refreshingFeed}
                <div
                    class="text-center flex justify-center align-middle text-gray-600"
                >
                    <svg
                        class="animate-bounce w-6 h-6 m-2"
                        fill="currentColor"
                        viewBox="0 0 20 20"
                        xmlns="http://www.w3.org/2000/svg"
                        ><path
                            fill-rule="evenodd"
                            d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-11a1 1 0 10-2 0v3.586L7.707 9.293a1 1 0 00-1.414 1.414l3 3a1 1 0 001.414 0l3-3a1 1 0 00-1.414-1.414L11 10.586V7z"
                            clip-rule="evenodd"
                        /></svg
                    >
                </div>
            {/if}
            {#each friendFeedPosts as { name, value, time }}
                <div class="p-1">
                    <div class="bg-gray-100 p-4 rounded-lg shadow-lg border-2">
                        <div class="flex">
                            <div>
                                {#if name == hostUsername}
                                    <p class="text-purple-600 font-medium">
                                        {name}

                                        <svg
                                            class="w-4 h-4 inline-block mb-1 text-green-400 opacity-25"
                                            fill="currentColor"
                                            viewBox="0 0 20 20"
                                            xmlns="http://www.w3.org/2000/svg"
                                            ><path
                                                fill-rule="evenodd"
                                                d="M6.267 3.455a3.066 3.066 0 001.745-.723 3.066 3.066 0 013.976 0 3.066 3.066 0 001.745.723 3.066 3.066 0 012.812 2.812c.051.643.304 1.254.723 1.745a3.066 3.066 0 010 3.976 3.066 3.066 0 00-.723 1.745 3.066 3.066 0 01-2.812 2.812 3.066 3.066 0 00-1.745.723 3.066 3.066 0 01-3.976 0 3.066 3.066 0 00-1.745-.723 3.066 3.066 0 01-2.812-2.812 3.066 3.066 0 00-.723-1.745 3.066 3.066 0 010-3.976 3.066 3.066 0 00.723-1.745 3.066 3.066 0 012.812-2.812zm7.44 5.252a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                                                clip-rule="evenodd"
                                            /></svg
                                        >
                                    </p>
                                {:else}
                                    <p class="text-indigo-600 font-medium">
                                        {name}
                                    </p>
                                {/if}

                                <div
                                    class="flex items-center text-xs text-gray-400"
                                >
                                    <p>{convertTimestamp(time)}</p>
                                    <p class="px-1">•</p>
                                    <p>
                                        {timeago.format(convertTimestamp(time))}
                                    </p>
                                </div>
                            </div>
                        </div>
                        <div class="mt-2">
                            <p
                                class="text-gray-600 text-sm sm:text-base line-clamp-3 break-words"
                            >
                                {value}
                            </p>
                        </div>
                    </div>
                </div>
            {/each}
        {/if}
    </div>
</div>
