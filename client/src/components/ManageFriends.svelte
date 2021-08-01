<script>
    import { onMount, onDestroy } from "svelte";

    let hostAccessKey = "";
    let addFriendBridge;
    let friendListResp;
    let friendListLoaded = false;
    let myKeyLoaded = false;
    let hostUsername;
    let myNameLoaded;
    let anyPending = false;
    let viewingFriendProfile = false;
    let viewingProfile;
    let viewingName;
    let actualFriendCount = 0;
    let viewingFriendsPosts = false;
    let viewingPosts;
    let hostBridge = window.location.hostname;

    let devBridge = "";

    if (hostBridge == "localhost") {
        devBridge = "https://41034m.deta.dev/";
    }

    onMount(async () => {
        getMyKey();
        getMyName();
    });

    onDestroy(async () => {
        clearInterval(checkFriends);
    });

    const getMyKey = async () => {
        var myKeyReq = await fetch(devBridge + "my-key");
        var myKeyResp = await myKeyReq.json();
        hostAccessKey = myKeyResp.key;
        myKeyLoaded = true;
        getFriends();
    };

    const getMyName = async () => {
        var myNameReq = await fetch(devBridge + "public/profile");
        var myNameResp = await myNameReq.json();
        hostUsername = myNameResp.username;
        myNameLoaded = true;
    };

    const getFriendName = async (bridge) => {
        var friendURL = "https://" + bridge + "/public/profile";
        var friendNameReq = await fetch(friendURL);
        var friendNameResp = await friendNameReq.json();
        return friendNameResp.username;
    };

    const removeFriend = async (key) => {
        var friendToDelete = {
            key: key,
            access_key: hostAccessKey,
        };

        var removeResp = await fetch(devBridge + "remove-friend", {
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
            devBridge +
                "friend-list?" +
                new URLSearchParams({
                    access_key: hostAccessKey,
                    pending: "true",
                })
        );
        friendListResp = await listReq.json();
        actualFriendCount = 0;
        friendListResp.forEach((friend) => {
            if (friend.category == "pending_friend") {
                anyPending = true;
            } else {
                if (friend.category == "friend") {
                    actualFriendCount++;
                }
            }
        });

        friendListLoaded = true;
    };

    const sendFriendRequest = async (bridge) => {
        var friendReqContent = {
            access_key: hostAccessKey,
            name: hostUsername,
            bridge: hostBridge,
            public_key: hostAccessKey,
        };

        var friendReqURL = "https://" + bridge + "/public/request";
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

    const acceptFriendRequest = async (bridge, key, name) => {
        var friendReqContent = {
            name: name,
            bridge: bridge,
            public_key: key,
        };

        var friendReqURL = devBridge + "accept";
        var friendReqResp = await fetch(friendReqURL, {
            method: "POST",
            headers: {
                Accept: "application/json",
                "Content-Type": "application/json",
            },
            body: JSON.stringify(friendReqContent),
        });

        var friendResult = await friendReqResp.json();
        sendFriendRequest(bridge);
        getFriends();
    };

    const getFriendProfile = async (bridge) => {
        var friendURL = "https://" + bridge + "/public/profile";
        var friendProfileReq = await fetch(friendURL);
        var friendProfileResp = await friendProfileReq.json();
        viewingProfile = friendProfileResp;
        viewingFriendProfile = true;
    };

    const getFriendPosts = async () => {
        if (hostBridge != "localhost") {
            var friendURL =
                "https://" +
                hostBridge +
                "/friend-posts?access_key=" +
                hostAccessKey +
                "&name=" +
                viewingName;
        } else {
            devBridge +
                "friend-posts?access_key=" +
                hostAccessKey +
                "&name=" +
                viewingName;
        }
        var friendPostsReq = await fetch(friendURL);
        var friendPostsResp = await friendPostsReq.json();
        viewingPosts = friendPostsResp.posts;
        viewingFriendsPosts = true;
    };

    function convertTimestamp(timestamp) {
        var dateObject = new Date(timestamp * 1000);
        var readableDate = dateObject.toLocaleString();
        return readableDate;
    }

    const checkFriends = setInterval(getFriends, 5000);
</script>

<div class="container mx-auto sm:p-10">
    {#if viewingFriendProfile == false}
        <div
            class="border border-gray-300 p-2 bg-gray-200 shadow-lg rounded-lg lg:w-1/2 w-full flex m-auto"
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
                on:click={async () => {
                    sendFriendRequest(addFriendBridge);
                }}
                class="m-2 p-2 border bg-green-500 hover:bg-green-400 text-white rounded-3xl focus:outline-none"
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
            {#if actualFriendCount > 0}
                <h2 class="text-2xl pt-4 pb-2">Friends</h2>
                <table
                    class="rounded-t-lg rounded-b-lg w-full mx-auto bg-gray-200 text-gray-800"
                >
                    <tr class="text-left border-b-2 border-gray-300">
                        <th class="px-4 py-3">Name</th>
                        <th class="px-4 py-3">Bridge</th>
                        <th class="px-4 py-3">Actions</th>
                    </tr>
                    {#each friendListResp as { bridge, name, key, category }}
                        {#if category != "pending_friend"}
                            <tr class="bg-gray-100 border-b border-gray-200">
                                <td class="px-4 py-3">{name}</td>
                                <td class="px-4 py-3">{bridge}</td>
                                <td class="px-4 py-3">
                                    <button
                                        class="focus:outline-none hover:text-red-500"
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
                                        class="focus:outline-none hover:text-indigo-500"
                                        on:click={() => {
                                            viewingName = name;
                                            getFriendProfile(bridge);
                                            getFriendPosts();
                                        }}
                                        ><svg
                                            class="w-6 h-6"
                                            fill="currentColor"
                                            viewBox="0 0 20 20"
                                            xmlns="http://www.w3.org/2000/svg"
                                            ><path
                                                d="M10 12a2 2 0 100-4 2 2 0 000 4z"
                                            /><path
                                                fill-rule="evenodd"
                                                d="M.458 10C1.732 5.943 5.522 3 10 3s8.268 2.943 9.542 7c-1.274 4.057-5.064 7-9.542 7S1.732 14.057.458 10zM14 10a4 4 0 11-8 0 4 4 0 018 0z"
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

            {#if anyPending == true}
                <h2 class="text-2xl pt-4 pb-2">Requests</h2>
                <table
                    class="rounded-t-lg rounded-b-lg w-full mx-auto bg-gray-200 text-gray-800"
                >
                    <tr class="text-left border-b-2 border-gray-300">
                        <th class="px-4 py-3">Name</th>
                        <th class="px-4 py-3">Bridge</th>
                        <th class="px-4 py-3">Actions</th>
                    </tr>
                    {#each friendListResp as { bridge, name, key, category }}
                        {#if category == "pending_friend"}
                            <tr class="bg-gray-100 border-b border-gray-200">
                                <td class="px-4 py-3">{name}</td>
                                <td class="px-4 py-3">{bridge}</td>
                                <td class="px-4 py-3">
                                    <button
                                        class="focus:outline-none hover:text-green-500"
                                        on:click={() => {
                                            acceptFriendRequest(
                                                bridge,
                                                key,
                                                name
                                            );
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
                                        class="focus:outline-none hover:text-red-500"
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
                                        class="focus:outline-none hover:text-indigo-500"
                                        on:click={() => {
                                            viewingName = name;
                                            getFriendProfile(bridge);
                                            getFriendPosts();
                                        }}
                                        ><svg
                                            class="w-6 h-6"
                                            fill="currentColor"
                                            viewBox="0 0 20 20"
                                            xmlns="http://www.w3.org/2000/svg"
                                            ><path
                                                d="M10 12a2 2 0 100-4 2 2 0 000 4z"
                                            /><path
                                                fill-rule="evenodd"
                                                d="M.458 10C1.732 5.943 5.522 3 10 3s8.268 2.943 9.542 7c-1.274 4.057-5.064 7-9.542 7S1.732 14.057.458 10zM14 10a4 4 0 11-8 0 4 4 0 018 0z"
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
    {:else}
        <button
            class="focus:outline-none text-xl text-indigo-500 hover:text-indigo-400"
            on:click={() => {
                viewingFriendProfile = false;
            }}
            ><svg
                class="w-8 h-8"
                fill="currentColor"
                viewBox="0 0 20 20"
                xmlns="http://www.w3.org/2000/svg"
                ><path
                    fill-rule="evenodd"
                    d="M10 18a8 8 0 100-16 8 8 0 000 16zm.707-10.293a1 1 0 00-1.414-1.414l-3 3a1 1 0 000 1.414l3 3a1 1 0 001.414-1.414L9.414 11H13a1 1 0 100-2H9.414l1.293-1.293z"
                    clip-rule="evenodd"
                /></svg
            ></button
        >
        <h2 class="text-2xl pb-2">{viewingProfile.username}'s Profile</h2>
        <div
            class="border border-gray-300 p-2 grid grid-cols-1 gap-2 bg-gray-200 shadow-lg rounded-lg"
        >
            <p class="break-words">{viewingProfile.bio}</p>
        </div>
        {#if viewingFriendsPosts}
            <h2 class="text-2xl pt-4 pb-2">Posts</h2>
            {#each viewingPosts as { value, time }}
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
    {/if}
</div>
