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
    let postOptions = false;
    let postOptionSelector;
    let reactToPost = false;
    let reactingPost;

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
        // Only required for Dev - TODO: Remove Jank
        if (window.location.hostname == "localhost") {
            var postBridge = "41034m.deta.dev";
        } else {
            var postBridge = hostBridge;
        }

        var postedPost = newPost;
        newPost = "";
        refreshingFeed = true;
        var contentToPost = {
            access_key: hostAccessKey,
            value: postedPost,
            bridge: postBridge,
        };

        var postResp = await fetch(devBridge + "create-post", {
            method: "POST",
            headers: {
                Accept: "application/json",
                "Content-Type": "application/json",
            },
            body: JSON.stringify(contentToPost),
        });

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

    const editPost = async (key, updatedContent) => {
        var contentToEdit = {
            item: "post",
            delete: false,
            key: key,
            content: updatedContent,
        };

        var editResp = await fetch(devBridge + "edit", {
            method: "PUT",
            headers: {
                Accept: "application/json",
                "Content-Type": "application/json",
            },
            body: JSON.stringify(contentToEdit),
        });

        getFeed();
    };

    const deletePost = async (key) => {
        var contentToDelete = {
            item: "post",
            delete: true,
            key: key,
        };

        var deleteResp = await fetch(devBridge + "edit", {
            method: "PUT",
            headers: {
                Accept: "application/json",
                "Content-Type": "application/json",
            },
            body: JSON.stringify(contentToDelete),
        });

        getFeed();
    };

    const reactPost = async (key, reacted, bridge) => {
        var reactionToPost = {
            postkey: key,
            emoji: reacted,
        };

        var reactResp = await fetch("https://" + bridge + "/public/react", {
            method: "POST",
            headers: {
                Accept: "application/json",
                "Content-Type": "application/json",
            },
            body: JSON.stringify(reactionToPost),
        });
        getFeed();
        notifyFriends();
    };

    const reactionList = ["❤️", "🔥", "😊", "😂", "👍"];

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
            {#each friendFeedPosts as { name, value, time, edited, key, reactions, bridge }}
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
                            {#if name == hostUsername}
                                <button
                                    class="ml-auto focus:outline-none"
                                    on:click={() => {
                                        if (postOptionSelector == key) {
                                            postOptions = !postOptions;
                                        } else {
                                            postOptions = true;
                                        }
                                        postOptionSelector = key;

                                        if (reactingPost == key) {
                                            reactToPost = !reactToPost;
                                        } else {
                                            reactToPost = true;
                                        }
                                        reactingPost = key;
                                    }}
                                >
                                    <svg
                                        class="w-6 h-6 text-gray-300"
                                        fill="currentColor"
                                        viewBox="0 0 20 20"
                                        xmlns="http://www.w3.org/2000/svg"
                                        ><path
                                            d="M10 6a2 2 0 110-4 2 2 0 010 4zM10 12a2 2 0 110-4 2 2 0 010 4zM10 18a2 2 0 110-4 2 2 0 010 4z"
                                        /></svg
                                    >
                                </button>
                            {:else}
                                <button
                                    class="ml-auto focus:outline-none"
                                    on:click={() => {
                                        if (reactingPost == key) {
                                            reactToPost = !reactToPost;
                                        } else {
                                            reactToPost = true;
                                        }
                                        reactingPost = key;
                                    }}
                                >
                                    <svg
                                        class="w-6 h-6 text-gray-300"
                                        fill="currentColor"
                                        viewBox="0 0 20 20"
                                        xmlns="http://www.w3.org/2000/svg"
                                        ><path
                                            d="M10 6a2 2 0 110-4 2 2 0 010 4zM10 12a2 2 0 110-4 2 2 0 010 4zM10 18a2 2 0 110-4 2 2 0 010 4z"
                                        /></svg
                                    >
                                </button>
                            {/if}
                        </div>
                        <div class="mt-2">
                            <p
                                class="text-gray-600 text-sm sm:text-base line-clamp-3 break-words"
                            >
                                {value}
                            </p>
                            <div class="flex">
                                {#if edited == true}
                                    <div
                                        class="flex items-center mr-4 focus:outline-none"
                                    >
                                        <i class="mr-2">
                                            <svg
                                                xmlns="http://www.w3.org/2000/svg"
                                                class="text-blue-300 w-4 h-4"
                                                fill="none"
                                                viewBox="0 0 24 24"
                                                stroke="currentColor"
                                            >
                                                <path
                                                    stroke-linecap="round"
                                                    stroke-linejoin="round"
                                                    stroke-width="2"
                                                    d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"
                                                />
                                            </svg>
                                        </i>
                                        <p class="mt-1 text-blue-300 text-sm">
                                            Edited
                                        </p>
                                    </div>
                                {/if}
                                {#if name == hostUsername && postOptions == true && postOptionSelector == key}
                                    <button
                                        on:click={async () => {
                                            var updatedContent = prompt(
                                                "Edit Post",
                                                value
                                            );
                                            if (updatedContent) {
                                                editPost(key, updatedContent);
                                                postOptions = false;
                                                reactToPost = false;
                                            }
                                        }}
                                        class="flex items-center mr-4 focus:outline-none hover:text-yellow-500 text-yellow-400"
                                    >
                                        <svg
                                            xmlns="http://www.w3.org/2000/svg"
                                            class="w-4 h-4 mr-2"
                                            fill="none"
                                            viewBox="0 0 24 24"
                                            stroke="currentColor"
                                        >
                                            <path
                                                stroke-linecap="round"
                                                stroke-linejoin="round"
                                                stroke-width="2"
                                                d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z"
                                            />
                                        </svg>

                                        <span class="mt-1  text-sm">
                                            Edit
                                        </span>
                                    </button>

                                    <button
                                        on:click={async () => {
                                            if (
                                                confirm(
                                                    "Are you sure you want to delete this post?"
                                                )
                                            ) {
                                                deletePost(key);
                                                postOptions = false;
                                                reactToPost = false;
                                            }
                                        }}
                                        class="flex items-center mr-4 focus:outline-none hover:text-red-400 text-red-300"
                                    >
                                        <svg
                                            xmlns="http://www.w3.org/2000/svg"
                                            class="w-4 h-4 mr-2"
                                            fill="none"
                                            viewBox="0 0 24 24"
                                            stroke="currentColor"
                                        >
                                            <path
                                                stroke-linecap="round"
                                                stroke-linejoin="round"
                                                stroke-width="2"
                                                d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z"
                                            />
                                        </svg>

                                        <span
                                            class="mt-1 text-sm focus:outline-none"
                                        >
                                            Delete
                                        </span>
                                    </button>
                                {/if}
                                <div class="flex ml-auto">
                                    {#if reactToPost == true && reactingPost == key}
                                        <div class="flex justify-end">
                                            {#each reactionList as displayedReaction}
                                                <button
                                                    class="focus:outline-none"
                                                    on:click={async () => {
                                                        postOptions = false;
                                                        var reacted =
                                                            displayedReaction;
                                                        reactToPost = false;
                                                        reactPost(
                                                            key,
                                                            reacted,
                                                            bridge
                                                        );
                                                    }}
                                                    >{displayedReaction}</button
                                                >
                                            {/each}
                                        </div>
                                    {/if}
                                </div>
                            </div>
                            {#if reactions.length != 0}
                                <div
                                    class="flex justify-center m-auto -mb-3 rounded-2xl bg-gray-200 border border-gray-300 flex-shrink w-min pl-2 pr-2"
                                >
                                    {#each reactions as reaction}
                                        <span class=""> {reaction}</span>
                                    {/each}
                                </div>
                            {/if}
                        </div>
                    </div>
                </div>
            {/each}
        {/if}
    </div>
</div>
