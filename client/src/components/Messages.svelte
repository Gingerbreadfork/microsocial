<script>
    import { onMount, onDestroy } from "svelte";
    import * as timeago from "timeago.js";
    import anchorme from "anchorme";

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
        getFriends();
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
            `${devBridge}friend-list?check_name=False&pending=False`
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

        if (anchorme.validate.url(newMessage)) {
            createLinkPost();
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

    const createLinkPost = async () => {
        if (
            newMessage.startsWith("http://") ||
            newMessage.startsWith("https://")
        ) {
        } else {
            newMessage = "https://" + newMessage;
        }

        if (
            newMessage.endsWith(".gif") ||
            newMessage.endsWith(".jpg") ||
            newMessage.endsWith(".png")
        ) {
            var postedPost = `<a href="${newMessage}"><img src="${newMessage}"></a>`;
        } else {
            var metaFetch = await fetch(
                devBridge + "metatags?link=" + newMessage
            );
            var metaTags = await metaFetch.json();
            var titleLink = metaTags.title.link(newMessage);
            var description;

            if (metaTags.image != "None") {
                var image = `<a href="${newMessage}"><img src="${metaTags.image}"></a>`;
            } else {
                var image = " ";
            }

            if (metaTags.description != "None") {
                description = metaTags.description;
            } else {
                description = " ";
            }

            var postedPost = `<b>${titleLink}</b><br><br>${image}<br>${description}`;
        }

        // Only required for Dev - TODO: Remove Jank
        if (window.location.hostname == "localhost") {
            var postBridge = "41034m.deta.dev";
        } else {
            var postBridge = hostBridge;
        }

        if (!postedPost) {
            var postedPost = newMessage;
        }

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

    const destroyChat = async () => {
        if (confirm("Are you sure you want to destroy the chat?")) {
            var clearProfileReq = await fetch(
                `${devBridge}public/messages/clear?key=${currentKey}`
            );
            var clearProfileResp = await clearProfileReq.json();
        }
    };

    const lazyCheck = setInterval(getFriends, 2000);
</script>

<div class="container w-full p-2 mx-auto sm:p-10 md:w-2/3 lg:w-1/2 xl:w-1/2">
    {#if friendListLoaded && friends.length == 0}
        <div
            class="flex items-center justify-center p-8 mt-10 bg-gray-200 shadow-md hover:shodow-lg rounded-2xl dark:bg-truegray-800"
        >
            <div class="flex items-center">
                <svg
                    class="w-20 h-20 text-purple-700 animate-pulse"
                    fill="currentColor"
                    viewBox="0 0 20 20"
                    xmlns="http://www.w3.org/2000/svg"
                    ><path
                        fill-rule="evenodd"
                        d="M9.504 1.132a1 1 0 01.992 0l1.75 1a1 1 0 11-.992 1.736L10 3.152l-1.254.716a1 1 0 11-.992-1.736l1.75-1zM5.618 4.504a1 1 0 01-.372 1.364L5.016 6l.23.132a1 1 0 11-.992 1.736L4 7.723V8a1 1 0 01-2 0V6a.996.996 0 01.52-.878l1.734-.99a1 1 0 011.364.372zm8.764 0a1 1 0 011.364-.372l1.733.99A1.002 1.002 0 0118 6v2a1 1 0 11-2 0v-.277l-.254.145a1 1 0 11-.992-1.736l.23-.132-.23-.132a1 1 0 01-.372-1.364zm-7 4a1 1 0 011.364-.372L10 8.848l1.254-.716a1 1 0 11.992 1.736L11 10.58V12a1 1 0 11-2 0v-1.42l-1.246-.712a1 1 0 01-.372-1.364zM3 11a1 1 0 011 1v1.42l1.246.712a1 1 0 11-.992 1.736l-1.75-1A1 1 0 012 14v-2a1 1 0 011-1zm14 0a1 1 0 011 1v2a1 1 0 01-.504.868l-1.75 1a1 1 0 11-.992-1.736L16 13.42V12a1 1 0 011-1zm-9.618 5.504a1 1 0 011.364-.372l.254.145V16a1 1 0 112 0v.277l.254-.145a1 1 0 11.992 1.736l-1.735.992a.995.995 0 01-1.022 0l-1.735-.992a1 1 0 01-.372-1.364z"
                        clip-rule="evenodd"
                    /></svg
                >
            </div>
            <div class="flex flex-col ml-3">
                <div class="font-medium leading-none">
                    You Don't Have Any Friends Just Yet!
                </div>
                <p
                    class="mt-1 text-sm leading-none text-gray-600 dark:text-truegray-300"
                >
                    Head to the "Manage Friends" tab to add a friend. You may
                    also be seeing this message if you have encountered a
                    network issue.
                </p>
            </div>
        </div>
    {/if}

    {#if friendListLoaded && friends.length > 0 && viewingMessages == ""}
        <h2 class="pb-6 text-2xl text-center">
            <svg
                class="inline w-8 h-8"
                fill="currentColor"
                viewBox="0 0 20 20"
                xmlns="http://www.w3.org/2000/svg"
                ><path
                    d="M2 5a2 2 0 012-2h7a2 2 0 012 2v4a2 2 0 01-2 2H9l-3 3v-3H4a2 2 0 01-2-2V5z"
                /><path
                    d="M15 7v2a4 4 0 01-4 4H9.828l-1.766 1.767c.28.149.599.233.938.233h2l3 3v-3h2a2 2 0 002-2V9a2 2 0 00-2-2h-1z"
                /></svg
            >
            Direct Messages
        </h2>
    {/if}

    {#if viewingMessages == ""}
        {#each friends as { name, bridge, key, messages }}
            <button
                on:click={() => {
                    viewingMessages = bridge;
                    currentKey = key;
                }}
                class="flex w-full mb-2 text-indigo-600 bg-gray-200 rounded shadow hover:bg-gray-100 focus:outline-none dark:text-truegray-300 dark:bg-truegray-800 dark:hover:bg-truegray-700"
            >
                <div class="w-1/3 p-2 dark:text-indigo-500">
                    {name}
                </div>

                <div class="self-center p-2 text-gray-500 title">
                    <svg
                        class="inline w-6 h-6 mb-1"
                        fill="currentColor"
                        viewBox="0 0 20 20"
                        xmlns="http://www.w3.org/2000/svg"
                        ><path
                            fill-rule="evenodd"
                            d="M12.586 4.586a2 2 0 112.828 2.828l-3 3a2 2 0 01-2.828 0 1 1 0 00-1.414 1.414 4 4 0 005.656 0l3-3a4 4 0 00-5.656-5.656l-1.5 1.5a1 1 0 101.414 1.414l1.5-1.5zm-5 5a2 2 0 012.828 0 1 1 0 101.414-1.414 4 4 0 00-5.656 0l-3 3a4 4 0 105.656 5.656l1.5-1.5a1 1 0 10-1.414-1.414l-1.5 1.5a2 2 0 11-2.828-2.828l3-3z"
                            clip-rule="evenodd"
                        /></svg
                    >
                    {bridge}
                </div>
                <div class="self-center p-2 ml-auto mr-2 text-gray-500 title">
                    <svg
                        class="inline w-6 h-6"
                        fill="currentColor"
                        viewBox="0 0 20 20"
                        xmlns="http://www.w3.org/2000/svg"
                        ><path
                            fill-rule="evenodd"
                            d="M18 10c0 3.866-3.582 7-8 7a8.841 8.841 0 01-4.083-.98L2 17l1.338-3.123C2.493 12.767 2 11.434 2 10c0-3.866 3.582-7 8-7s8 3.134 8 7zM7 9H5v2h2V9zm8 0h-2v2h2V9zM9 9h2v2H9V9z"
                            clip-rule="evenodd"
                        /></svg
                    >
                    {messages.length}
                </div>
            </button>
        {/each}
    {/if}

    {#if viewingMessages != ""}
        <div
            class="p-2 mb-2 bg-gray-100 border-2 border-gray-200 rounded shadow-md dark:bg-truegray-800 dark:border-truegray-900"
        >
            <textarea
                placeholder="Something to say?..."
                bind:value={newMessage}
                class="w-full p-1 border rounded shadow focus:outline-none dark:bg-truegray-900 dark:border-truegray-800 dark:text-gray-300"
                rows="3"
            />
            <div class="flex">
                <div class="mt-2 mb-2">
                    <button
                        class="p-2 text-white bg-pink-700 border hover:bg-pink-600 rounded-3xl focus:outline-none dark:border-pink-600 dark:bg-pink-900 dark:hover:bg-pink-600"
                        title="Go Back"
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
                <div class="mt-2 mb-2 ml-auto">
                    <button
                        title="Delete Chat"
                        on:click={() => {
                            destroyChat();
                        }}
                        class="p-2 text-white bg-yellow-500 border hover:bg-yellow-400 rounded-3xl focus:outline-none dark:border-yellow-600 dark:bg-yellow-700 dark:hover:bg-yellow-600"
                        ><svg
                            class="w-6 h-6"
                            fill="currentColor"
                            viewBox="0 0 20 20"
                            xmlns="http://www.w3.org/2000/svg"
                            ><path
                                fill-rule="evenodd"
                                d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z"
                                clip-rule="evenodd"
                            /></svg
                        ></button
                    >
                </div>
                <div class="mt-2 mb-2 ml-auto">
                    {#if newMessage}
                        <button
                            title="Send Message"
                            on:click={() => {
                                createPost();
                            }}
                            class="p-2 text-white bg-blue-500 border hover:bg-blue-400 rounded-3xl focus:outline-none dark:bg-truegray-700 dark:hover:bg-truegray-600 dark:border-truegray-600"
                            ><svg
                                class="w-6 h-6"
                                fill="currentColor"
                                viewBox="0 0 20 20"
                                xmlns="http://www.w3.org/2000/svg"
                                ><path
                                    fill-rule="evenodd"
                                    d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                                    clip-rule="evenodd"
                                /></svg
                            ></button
                        >{:else}
                        <button
                            title="Send Message"
                            on:click={() => {
                                alert("Nothing to send...");
                            }}
                            class="p-2 text-white bg-gray-300 border rounded-3xl focus:outline-none dark:bg-truegray-900 dark:border-truegray-700"
                            ><svg
                                class="w-6 h-6 dark:text-truegray-600"
                                fill="currentColor"
                                viewBox="0 0 20 20"
                                xmlns="http://www.w3.org/2000/svg"
                                ><path
                                    fill-rule="evenodd"
                                    d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                                    clip-rule="evenodd"
                                /></svg
                            ></button
                        >
                    {/if}
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
                            class="p-4 mb-2 bg-gray-100 border-2 rounded-lg shadow-lg dark:bg-truegray-800 dark:border-truegray-900"
                        >
                            {#if response == false}
                                <p class="font-medium text-indigo-600">
                                    {name}
                                </p>
                            {:else}
                                <p class="font-medium text-purple-600">
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
                                <p
                                    class="text-sm text-gray-600 dark:text-truegray-300"
                                >
                                    {@html anchorme(message)}
                                </p>
                            </div>
                        </div>
                    {/each}
                {/if}
            {/if}
        {/each}
    {/if}
</div>
