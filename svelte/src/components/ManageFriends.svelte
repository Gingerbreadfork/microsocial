<script>
    import "../lib/TailwindCSS.svelte";
    import { onMount, onDestroy } from "svelte";

    let hostAccessKey = "";
    let manageFriendName;
    let addFriendKey;
    let addFriendBridge;
    let friendFeedLoaded = false;
    let friendListResp;
    let friendListLoaded = false;
    let myKeyLoaded = false;

    onMount(async () => {
        getMyKey();
    });

    onDestroy(async () => {});

    const getMyKey = async () => {
        var myKeyReq = await fetch("my-key?");
        var myKeyResp = await myKeyReq.json();
        hostAccessKey = myKeyResp.key;
        myKeyLoaded = true;
        getFriends();
    };

    const addFriend = async () => {
        var friendBridge = addFriendBridge;
        var friendKey = addFriendKey;
        var friendName = manageFriendName;

        var friendToPost = {
            name: friendName,
            access_key: hostAccessKey,
            bridge: friendBridge,
            public_key: friendKey,
        };

        var postResp = await fetch("add-friend", {
            method: "POST",
            headers: {
                Accept: "application/json",
                "Content-Type": "application/json",
            },
            body: JSON.stringify(friendToPost),
        });
        var friendResult = await postResp.json();

        addFriendBridge = "";
        addFriendKey = "";
        friendName = "";

        getFriends();
    };

    const removeFriend = async () => {
        var friendToDelete = {
            name: manageFriendName,
            access_key: hostAccessKey,
        };

        var postResp = await fetch("remove-friend", {
            method: "DELETE",
            headers: {
                Accept: "application/json",
                "Content-Type": "application/json",
            },
            body: JSON.stringify(friendToDelete),
        });

        var friendResult = await postResp.json();

        addFriendBridge = "";
        addFriendKey = "";
        manageFriendName = "";

        getFriends();
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
</script>

<div class="container mx-auto sm:p-10">
    <h2 class="text-2xl pb-2 pt-2">Manage Friends</h2>
    <div
        class="border border-gray-300 p-2 grid grid-cols-1 gap-2 bg-gray-200 shadow-lg rounded-lg"
    >
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div
                class="grid grid-cols-2 gap-2 border border-gray-300 p-2 rounded"
            >
                <div class="flex border rounded bg-gray-300 items-center p-2">
                    <svg
                        class="mr-2"
                        xmlns="http://www.w3.org/2000/svg"
                        viewBox="0 0 24 24"
                        width="24"
                        height="24"
                    >
                        <path
                            class="heroicon-ui"
                            d="M12 12a5 5 0 1 1 0-10 5 5 0 0 1 0 10zm0-2a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm9 11a1 1 0 0 1-2 0v-2a3 3 0 0 0-3-3H8a3 3 0 0 0-3 3v2a1 1 0 0 1-2 0v-2a5 5 0 0 1 5-5h8a5 5 0 0 1 5 5v2z"
                        />
                    </svg>
                    <input
                        bind:value={manageFriendName}
                        type="text"
                        placeholder="Name"
                        class="bg-gray-300 w-full focus:outline-none text-gray-700"
                    />
                </div>
                <div class="flex border rounded bg-gray-300 items-center p-2">
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
                            d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z"
                        /></svg
                    >
                    <input
                        bind:value={addFriendKey}
                        type="text"
                        placeholder="Access Key"
                        class="bg-gray-300 w-full focus:outline-none text-gray-700"
                    />
                </div>
            </div>
            <div class="grid border border-gray-300 p-2 rounded">
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
        </div>
        <p class="text-gray-400 flex justify-center text-xs">
            Only a valid name is required to remove a friend<br />
        </p>
        <p class="text-red-500 flex justify-center text-xs">
            Invalid bridges will break things for now!
        </p>
        <div class="grid grid-cols-2">
            <div class="flex justify-start mb-2">
                <button
                    on:click={addFriend}
                    class="p-3 border bg-green-500 text-white rounded-3xl focus:outline-none"
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
            <div class="flex justify-end mb-2">
                <button
                    on:click={removeFriend}
                    class="p-3 border bg-red-500 text-white rounded-3xl focus:outline-none"
                    ><svg
                        class="w-6 h-6"
                        fill="currentColor"
                        viewBox="0 0 20 20"
                        xmlns="http://www.w3.org/2000/svg"
                        ><path
                            d="M11 6a3 3 0 11-6 0 3 3 0 016 0zM14 17a6 6 0 00-12 0h12zM13 8a1 1 0 100 2h4a1 1 0 100-2h-4z"
                        /></svg
                    ></button
                >
            </div>
        </div>
    </div>
    {#if friendListLoaded}
        <h2 class="text-2xl pt-4 pb-2">Friend List</h2>
        <table
            class="rounded-t-lg rounded-b-lg w-full mx-auto bg-gray-200 text-gray-800"
        >
            <tr class="text-left border-b-2 border-gray-300">
                <th class="px-4 py-3">Name</th>
                <th class="px-4 py-3">Bridge</th>
                <th class="px-4 py-3">Key</th>
            </tr>
            {#each friendListResp as { bridge, name, key }}
                <tr class="bg-gray-100 border-b border-gray-200">
                    <td class="px-4 py-3">{name}</td>
                    <td class="px-4 py-3">{bridge}</td>
                    <td class="px-4 py-3 text-red-500">{key}</td>
                </tr>
            {/each}
            <tr class="bg-gray-400 border-b border-gray-200" />
            <br />
            <td />
        </table>
    {/if}
</div>
