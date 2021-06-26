<script>
    import "../lib/TailwindCSS.svelte";
    import { onMount, onDestroy } from "svelte";

    let hostAccessKey = "";
    let manageFriendKey;
    let addFriendKey;
    let addFriendBridge;
    let friendFeedLoaded = false;
    let friendListResp;
    let friendListLoaded = false;
    let myKeyLoaded = false;
    let hostUsername;
    let myNameLoaded;
    let manageFriendName;
    let anyPending = false;

    onMount(async () => {
        getMyKey();
        getMyName();
    });

    onDestroy(async () => {});

    const getMyKey = async () => {
        var myKeyReq = await fetch("my-key");
        var myKeyResp = await myKeyReq.json();
        hostAccessKey = myKeyResp.key;
        myKeyLoaded = true;
        getFriends();
    };

    const getMyName = async () => {
        var myNameReq = await fetch("my-name");
        var myNameResp = await myNameReq.json();
        hostUsername = myNameResp.name;
        myNameLoaded = true;
    };

    const getFriendName = async (bridge) => {
        var friendURL = "https://" + bridge + ".deta.dev/my-name";
        var friendNameReq = await fetch(friendURL);
        var friendNameResp = await friendNameReq.json();
        return friendNameResp.name;
    };

    const removeFriend = async (key) => {
        var friendToDelete = {
            key: key,
            access_key: hostAccessKey,
        };

        var removeResp = await fetch("remove-friend", {
            method: "DELETE",
            headers: {
                Accept: "application/json",
                "Content-Type": "application/json",
            },
            body: JSON.stringify(friendToDelete),
        });

        var removeResult = await removeResp.json();
        getFriends();
    };

    const getFriends = async () => {
        var listReq = await fetch(
            "friend-list?" +
                new URLSearchParams({
                    access_key: hostAccessKey,
                    pending: "true",
                })
        );
        friendListResp = await listReq.json();

        friendListResp.forEach((friend) => {
            if (friend.type == "pending_friend") {
                anyPending = true;
            } else {
                anyPending = false;
            }
        });

        friendListLoaded = true;
    };

    const sendFriendRequest = async (bridge) => {
        var friendReqContent = {
            access_key: hostAccessKey,
            name: hostUsername,
            bridge: window.location.hostname.split(".")[0],
            public_key: hostAccessKey,
        };

        var friendReqURL = "https://" + bridge + ".deta.dev/add";
        var friendReqResp = await fetch(friendReqURL, {
            method: "POST",
            headers: {
                Accept: "application/json",
                "Content-Type": "application/json",
            },
            body: JSON.stringify(friendReqContent),
        });

        var friendResult = await friendReqResp.json();
        getFriends();
    };
</script>

<div class="container mx-auto sm:p-10">
    <div
        class="border border-gray-300 p-2 bg-gray-200 shadow-lg rounded-lg md:w-1/2 lg:w-1/3 w-full flex m-auto"
    >
        <div class="border border-gray-300 p-2 rounded w-full">
            <div class="flex border rounded bg-gray-300 items-center p-2 ">
                <svg
                    class="mr-2"
                    width="24"
                    height="24"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                    xmlns="http://www.w3.org/2000/svg"
                    ><path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1"
                    /></svg
                >
                <input
                    bind:value={addFriendBridge}
                    type="text"
                    placeholder="Bridge"
                    class="bg-gray-300 w-full focus:outline-none text-gray-700"
                />
            </div>
        </div>

        <button
            on:click={() => {
                sendFriendRequest(addFriendBridge);
            }}
            class="m-2 p-2 border bg-green-500 text-white rounded-3xl focus:outline-none"
            ><svg
                class="w-6 h-6"
                fill="currentColor"
                viewBox="0 0 20 20"
                xmlns="http://www.w3.org/2000/svg"
                ><path
                    d="M8 9a3 3 0 100-6 3 3 0 000 6zM8 11a6 6 0 016 6H2a6 6 0 016-6zM16 7a1 1 0 10-2 0v1h-1a1 1 0 100 2h1v1a1 1 0 102 0v-1h1a1 1 0 100-2h-1V7z"
                /></svg
            ></button
        >
    </div>

    {#if friendListLoaded}
        <h2 class="text-2xl pt-4 pb-2">Friends</h2>
        <table
            class="rounded-t-lg rounded-b-lg w-full mx-auto bg-gray-200 text-gray-800"
        >
            <tr class="text-left border-b-2 border-gray-300">
                <th class="px-4 py-3">Name</th>
                <th class="px-4 py-3">Bridge</th>
                <th class="px-4 py-3">Key</th>
                <th class="px-4 py-3">Actions</th>
            </tr>
            {#each friendListResp as { bridge, name, key, type }}
                {#if type != "pending_friend"}
                    <tr class="bg-gray-100 border-b border-gray-200">
                        <td class="px-4 py-3">{name}</td>
                        <td class="px-4 py-3">{bridge}</td>
                        <td class="px-4 py-3 text-red-500">{key}</td>
                        <td class="px-4 py-3">
                            <button
                                class="outline-none"
                                on:click={() => {
                                    removeFriend(key);
                                }}
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
                            <button
                                class="outline-none"
                                on:click={() => {
                                    console.log(bridge);
                                }}
                                ><svg
                                    class="w-6 h-6"
                                    fill="currentColor"
                                    viewBox="0 0 20 20"
                                    xmlns="http://www.w3.org/2000/svg"
                                    ><path
                                        fill-rule="evenodd"
                                        d="M10 18a8 8 0 100-16 8 8 0 000 16zM7 9H5v2h2V9zm8 0h-2v2h2V9zM9 9h2v2H9V9z"
                                        clip-rule="evenodd"
                                    /></svg
                                ></button
                            >
                        </td>
                    </tr>
                {/if}
            {/each}
            <tr class="bg-gray-400 border-b border-gray-200" />
            <br />
            <td />
        </table>

        {#if anyPending == true}
            <h2 class="text-2xl pt-4 pb-2">Friend Requests</h2>
            <table
                class="rounded-t-lg rounded-b-lg w-full mx-auto bg-gray-200 text-gray-800"
            >
                <tr class="text-left border-b-2 border-gray-300">
                    <th class="px-4 py-3">Name</th>
                    <th class="px-4 py-3">Bridge</th>
                    <th class="px-4 py-3">Key</th>
                    <th class="px-4 py-3">Actions</th>
                </tr>
                {#each friendListResp as { bridge, name, key, type }}
                    {#if type == "pending_friend"}
                        <tr class="bg-gray-100 border-b border-gray-200">
                            <td class="px-4 py-3">{name}</td>
                            <td class="px-4 py-3">{bridge}</td>
                            <td class="px-4 py-3 text-red-500">{key}</td>
                            <td class="px-4 py-3">
                                <button
                                    class="outline-none"
                                    on:click={() => {
                                        sendFriendRequest(bridge);
                                    }}
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
                                <button
                                    class="outline-none"
                                    on:click={() => {
                                        removeFriend(key);
                                    }}
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
                                <button
                                    class="outline-none"
                                    on:click={() => {
                                        console.log(bridge);
                                    }}
                                    ><svg
                                        class="w-6 h-6"
                                        fill="currentColor"
                                        viewBox="0 0 20 20"
                                        xmlns="http://www.w3.org/2000/svg"
                                        ><path
                                            fill-rule="evenodd"
                                            d="M10 18a8 8 0 100-16 8 8 0 000 16zM7 9H5v2h2V9zm8 0h-2v2h2V9zM9 9h2v2H9V9z"
                                            clip-rule="evenodd"
                                        /></svg
                                    ></button
                                >
                            </td>
                        </tr>
                    {/if}
                {/each}
                <tr class="bg-gray-400 border-b border-gray-200" />
                <br />
                <td />
            </table>
        {/if}
    {/if}
</div>
