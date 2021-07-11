<script>
    import { onMount, onDestroy } from "svelte";

    let hostAccessKey = "";
    let newPost;
    let friendFeedLoaded = false;
    let friendFeedPosts;
    let friendListResp;
    let friendListLoaded = false;
    let myKeyLoaded = false;
    let notifications;
    let hostBridge = window.location.hostname.split(".")[0];

    onMount(async () => {
        getMyKey();
    });

    onDestroy(async () => {
        clearInterval(getNotifications);
    });

    const getMyKey = async () => {
        var myKeyReq = await fetch("my-key?");
        var myKeyResp = await myKeyReq.json();
        hostAccessKey = myKeyResp.key;
        myKeyLoaded = true;
        getFeed();
        getFriends();
    };

    const createPost = async () => {
        var contentToPost = {
            access_key: hostAccessKey,
            value: newPost,
        };

        var postResp = await fetch("create-post", {
            method: "POST",
            headers: {
                Accept: "application/json",
                "Content-Type": "application/json",
            },
            body: JSON.stringify(contentToPost),
        });
        var postResult = await postResp.json();
        newPost = "";
        notifyFriends();
        getFeed();
    };

    const getFeed = async () => {
        var FeedReq = await fetch(
            "feed?" +
                new URLSearchParams({
                    access_key: hostAccessKey,
                })
        );
        friendFeedPosts = await FeedReq.json();
        friendFeedLoaded = true;
    };

    const notifyFriends = async () => {
        friendListResp.forEach(async (friend) => {
            var contentToPost = {
                key: hostAccessKey,
                bridge: hostBridge,
            };
            var friendNotifURL =
                "https://" + friend.bridge + ".deta.dev/notify";
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
            "notifications?" +
                new URLSearchParams({
                    clear: "True",
                })
        );
    };

    const checkNotifications = async () => {
        if (friendFeedLoaded && friendListLoaded) {
            var notificationsReq = await fetch("notifications?");
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
    <h2 class="text-2xl pt-4 pb-2">Create Post</h2>
    <div class="border border-gray-300 p-2 bg-gray-200 shadow-lg rounded-lg">
        <div class="border border-gray-300 rounded-xl p-2 pb-0">
            <textarea
                bind:value={newPost}
                class="w-full text-gray-700 border rounded-lg focus:outline-none"
                rows="5"
            />
        </div>
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
            <h2 class="text-2xl pt-4 pb-2">Friend Feed</h2>

            {#each friendFeedPosts as { name, value, time }}
                <div
                    class="bg-gray-200 p-2 mb-4 h-auto rounded-2xl shadow-lg flex flex-col sm:flex-row gap-5 border border-gray-300"
                >
                    <div class="flex sm:flex-1 flex-col gap-2 p-1">
                        <div class="grid grid-cols-2">
                            <h3 class="font-semibold  text-gray-600">{name}</h3>
                            <p class="flex justify-end text-gray-400">
                                {convertTimestamp(time)}
                            </p>
                        </div>
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
</div>
