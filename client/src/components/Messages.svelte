<script>
    import { onMount, onDestroy } from "svelte";
    import * as timeago from "timeago.js";

    let hostAccessKey = "";
    let friendListResp;
    let friendListLoaded = false;
    let hostBridge = window.location.hostname;
    let friends = [];
    let viewingMessages = "";
    let newMessage = "";
    let currentKey;
    let hostUsername = "";

    let devBridge = "";

    if (hostBridge == "localhost") {
        devBridge = "https://41034m.deta.dev/";
    }

    const getMyProfile = async () => {
        var hostProfileReq = await fetch(devBridge + "public/profile");
        var hostProfileResp = await hostProfileReq.json();
        hostUsername = hostProfileResp.username;
    };

    onMount(async () => {
        friendListLoaded = false;
        viewingMessages == "";
        getMyProfile();
    });

    onDestroy(async () => {
        clearInterval(lazyCheck);
        friendListLoaded = false;
        friends = [];
    });

    function convertTimestamp(timestamp) {
        var dateObject = new Date(timestamp * 1000);
        var readableDate = dateObject.toLocaleString();
        return readableDate;
    }

    const getFriends = async () => {
        var listReq = await fetch(
            devBridge +
                "friend-list?" +
                new URLSearchParams({
                    access_key: hostAccessKey,
                    pending: "true",
                })
        );
        friendListResp = await listReq.json();

        friends = [];
        friendListResp.forEach((friend) => {
            if (friend.category == "friend") {
                friend.messages = friend.messages.reverse();
                friends.push(friend);
            }
        });

        friends = friends;
        friendListLoaded = true;
    };

    const createPost = async () => {
        if (newMessage.length > 2500) {
            alert(
                `Message too long! ${newMessage.length} characters, max accepted is 2500`
            );
            return;
        }

        var postedPost = newMessage;
        newMessage = "";

        var contentToPost = {
            key: currentKey,
            content: postedPost,
        };

        var postResp = await fetch(devBridge + "messages/respond", {
            method: "POST",
            headers: {
                Accept: "application/json",
                "Content-Type": "application/json",
            },
            body: JSON.stringify(contentToPost),
        });
    };

    const lazyCheck = setInterval(getFriends, 1000);
</script>

<div class="container mx-auto sm:p-10 w-full md:w-2/3 lg:w-1/2 xl:w-1/2">
    {#if !friendListLoaded}
        <svg
            class="m-auto animate-spin text-purple-800 w-20 h-20"
            fill="currentColor"
            viewBox="0 0 20 20"
            xmlns="http://www.w3.org/2000/svg"
            ><path
                fill-rule="evenodd"
                d="M11.49 3.17c-.38-1.56-2.6-1.56-2.98 0a1.532 1.532 0 01-2.286.948c-1.372-.836-2.942.734-2.106 2.106.54.886.061 2.042-.947 2.287-1.561.379-1.561 2.6 0 2.978a1.532 1.532 0 01.947 2.287c-.836 1.372.734 2.942 2.106 2.106a1.532 1.532 0 012.287.947c.379 1.561 2.6 1.561 2.978 0a1.533 1.533 0 012.287-.947c1.372.836 2.942-.734 2.106-2.106a1.533 1.533 0 01.947-2.287c1.561-.379 1.561-2.6 0-2.978a1.532 1.532 0 01-.947-2.287c.836-1.372-.734-2.942-2.106-2.106a1.532 1.532 0 01-2.287-.947zM10 13a3 3 0 100-6 3 3 0 000 6z"
                clip-rule="evenodd"
            /></svg
        >
    {/if}

    {#if viewingMessages == ""}
        {#each friends as { name, bridge, key }}
            <button
                on:click={() => {
                    viewingMessages = bridge;
                    currentKey = key;
                }}
                class="flex rounded shadow w-full text-gray-600 mb-2 bg-gray-100 hover:bg-purple-100"
            >
                <div class="self-center p-2 w-1/2">
                    {name}
                </div>

                <div class="title text-xs text-gray-400 self-center p-2">
                    {bridge}
                </div>
            </button>
        {/each}
    {/if}

    {#if viewingMessages != ""}
        <div
            class="shadow-md border-2 border-gray-200 rounded p-2 mb-2 bg-gray-100"
        >
            <textarea
                bind:value={newMessage}
                class="shadow rounded border p-1 focus:outline-none w-full"
                rows="3"
            />
            <div class="flex">
                <div class="mb-2 mt-2">
                    <button
                        class="p-2 border bg-pink-700 hover:bg-pink-600 rounded-3xl text-white focus:outline-none"
                        on:click={() => {
                            viewingMessages = "";
                        }}
                        ><svg
                            class="w-6 h-6"
                            fill="currentColor"
                            viewBox="0 0 20 20"
                            xmlns="http://www.w3.org/2000/svg"
                            ><path
                                fill-rule="evenodd"
                                d="M15.707 15.707a1 1 0 01-1.414 0l-5-5a1 1 0 010-1.414l5-5a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 010 1.414zm-6 0a1 1 0 01-1.414 0l-5-5a1 1 0 010-1.414l5-5a1 1 0 011.414 1.414L5.414 10l4.293 4.293a1 1 0 010 1.414z"
                                clip-rule="evenodd"
                            /></svg
                        ></button
                    >
                </div>
                <div class="mb-2 mt-2 ml-auto">
                    <button
                        on:click={() => {
                            console.log("TODO: createLinkPost");
                        }}
                        class="p-2 border bg-blue-500 hover:bg-blue-400 rounded-3xl text-white focus:outline-none"
                        ><svg
                            class="w-6 h-6"
                            fill="currentColor"
                            viewBox="0 0 20 20"
                            xmlns="http://www.w3.org/2000/svg"
                            ><path
                                fill-rule="evenodd"
                                d="M12.586 4.586a2 2 0 112.828 2.828l-3 3a2 2 0 01-2.828 0 1 1 0 00-1.414 1.414 4 4 0 005.656 0l3-3a4 4 0 00-5.656-5.656l-1.5 1.5a1 1 0 101.414 1.414l1.5-1.5zm-5 5a2 2 0 012.828 0 1 1 0 101.414-1.414 4 4 0 00-5.656 0l-3 3a4 4 0 105.656 5.656l1.5-1.5a1 1 0 10-1.414-1.414l-1.5 1.5a2 2 0 11-2.828-2.828l3-3z"
                                clip-rule="evenodd"
                            /></svg
                        ></button
                    >
                </div>

                <div class="ml-auto mb-2 mt-2">
                    <button
                        on:click={() => {
                            createPost();
                        }}
                        class="p-2 border bg-blue-500 hover:bg-blue-400 rounded-3xl text-white focus:outline-none"
                        ><svg
                            class="w-6 h-6"
                            fill="currentColor"
                            viewBox="0 0 20 20"
                            xmlns="http://www.w3.org/2000/svg"
                            ><path
                                fill-rule="evenodd"
                                d="M18 5v8a2 2 0 01-2 2h-5l-5 4v-4H4a2 2 0 01-2-2V5a2 2 0 012-2h12a2 2 0 012 2zM7 8H5v2h2V8zm2 0h2v2H9V8zm6 0h-2v2h2V8z"
                                clip-rule="evenodd"
                            /></svg
                        ></button
                    >
                </div>
            </div>
        </div>
    {/if}

    {#if friendListLoaded}
        {#each friends as { name, messages, bridge }}
            {#if viewingMessages == bridge}
                {#if messages.length > 0}
                    {#each messages as { timestamp, message, response }}
                        <div
                            class="bg-gray-100 p-4 rounded-lg shadow-lg border-2 mb-2"
                        >
                            {#if response == false}
                                <p class="text-indigo-600 font-medium">
                                    {name}
                                </p>
                            {:else}
                                <p class="text-purple-600 font-medium">
                                    {hostUsername}
                                </p>
                            {/if}
                            <div class="flex">
                                <div
                                    class="flex items-center text-sm text-gray-400"
                                >
                                    <p>{convertTimestamp(timestamp)}</p>
                                    <p class="px-1">•</p>
                                    <p>
                                        {timeago.format(
                                            convertTimestamp(timestamp)
                                        )}
                                    </p>
                                </div>
                            </div>
                            <div class="mt-2">
                                <p class="text-gray-600 text-sm">
                                    {@html message}
                                </p>
                            </div>
                        </div>
                    {/each}
                {/if}
            {/if}
        {/each}
    {/if}
</div>
