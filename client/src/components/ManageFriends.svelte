<script>
    import { onMount, onDestroy } from "svelte";
    import * as timeago from "timeago.js";
    import anchorme from "anchorme";

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
    let pendingFriendCount = 0;
    let viewingFriendsPosts = false;
    let viewingPosts;
    let howDoYouConnect = false;
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
        var myKeyReq = await fetch(`${devBridge}my-key`);
        var myKeyResp = await myKeyReq.json();
        hostAccessKey = myKeyResp.key;
        myKeyLoaded = true;
        getFriends();
    };

    const getMyName = async () => {
        var myNameReq = await fetch(`${devBridge}public/profile`);
        var myNameResp = await myNameReq.json();
        hostUsername = myNameResp.username;
        myNameLoaded = true;
    };

    const removeFriend = async (key) => {
        var friendToDelete = {
            key: key,
            access_key: hostAccessKey,
        };

        var removeResp = await fetch(`${devBridge}remove-friend`, {
            method: "DELETE",
            headers: {
                Accept: "application/json",
                "Content-Type": "application/json",
            },
            body: JSON.stringify(friendToDelete),
        });

        var removeResult = await removeResp.json();
        getFriends();
        purgeCache();
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
                pendingFriendCount++;
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
        // Lazy URL Trimming

        var friendReqContent = {
            access_key: hostAccessKey,
            name: hostUsername,
            bridge: hostBridge,
            public_key: hostAccessKey,
        };

        var friendReqURL = `https://${bridge
            .replace("https://", "")
            .replace("/", "")}/public/request`;
        var friendReqResp = await fetch(friendReqURL, {
            method: "POST",
            headers: {
                Accept: "application/json",
                "Content-Type": "application/json",
            },
            body: JSON.stringify(friendReqContent),
        });

        var friendResult = await friendReqResp.json();
        addFriendBridge = "";
        getFriends();
    };

    const acceptFriendRequest = async (bridge, key, name) => {
        var friendReqContent = {
            name: name,
            bridge: bridge,
            public_key: key,
        };

        var friendReqURL = `${devBridge}accept`;
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
        addFriendBridge = "";
        friendListLoaded = false;
        anyPending = false;
        getFriends();
    };

    const getFriendProfile = async (bridge) => {
        var friendURL = `https://${bridge}/public/profile`;
        var friendProfileReq = await fetch(friendURL);
        var friendProfileResp = await friendProfileReq.json();
        viewingProfile = friendProfileResp;
        viewingFriendProfile = true;
    };

    const getFriendPosts = async (bridge) => {
        if (hostBridge != "localhost") {
            var friendURL = `https://${hostBridge}/friend-posts?bridge=${bridge}`;
        } else {
            var friendURL = devBridge + "friend-posts?bridge=" + bridge;
        }

        var friendPostsReq = await fetch(friendURL);
        var friendPostsResp = await friendPostsReq.json();
        viewingPosts = friendPostsResp;
        viewingFriendsPosts = true;
    };

    function convertTimestamp(timestamp) {
        var dateObject = new Date(timestamp * 1000);
        var readableDate = dateObject.toLocaleString();
        return readableDate;
    }

    const purgeCache = async () => {
        var purgeCacheReq = await fetch(`${devBridge}purge/cache`);
        var purgeCacheResp = await purgeCacheReq.json();
    };

    // Intervals
    const checkFriends = setInterval(getFriends, 5000);
</script>

<div class="container w-full mx-auto sm:p-10 md:w-2/3 lg:w-1/2 xl:w-1/2">
    {#if viewingFriendProfile == false}
        <div
            class="flex w-full p-2 m-auto bg-gray-200 border border-gray-300 rounded-lg shadow-lg md:w-3/4 dark:bg-truegray-800 dark:border-truegray-900"
        >
            <div
                class="w-full p-2 border border-gray-300 rounded dark:border-truegray-600"
            >
                <div
                    class="flex items-center p-2 bg-gray-300 border rounded dark:bg-truegray-900 dark:border-truegray-800"
                >
                    <svg
                        class="mr-2 dark:text-truegray-200"
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
                        placeholder="Microsocial Server URL"
                        class="w-full text-gray-700 bg-gray-300 focus:outline-none dark:bg-truegray-900 dark:text-truegray-300"
                    />
                </div>
            </div>
            {#if addFriendBridge}
                <button
                    title="Add Friend"
                    on:click={async () => {
                        sendFriendRequest(addFriendBridge);
                        alert("Friend Request Sent! (If Valid)");
                    }}
                    class="p-2 m-2 ml-4 text-white bg-green-500 border hover:bg-green-400 rounded-3xl focus:outline-none"
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
            {:else}
                <button
                    title="Add Friend"
                    on:click={async () => {
                        alert(
                            "You need to enter a valid Microsocial server URL"
                        );
                    }}
                    class="p-2 m-2 ml-4 text-white bg-truegray-500 border hover:bg-truegray-400 rounded-3xl focus:outline-none"
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
            {/if}
        </div>
        <div class="flex ">
            <div class="m-auto">
                <button
                    on:click={() => {
                        howDoYouConnect = !howDoYouConnect;
                    }}
                    class="text-xs underline text-sky-700 focus:outline-none"
                    >How does this work?</button
                >
            </div>
        </div>
        {#if howDoYouConnect == true}
            <div
                class="p-4 mb-4 mt-4 bg-gray-100 border-2 rounded-lg shadow-lg dark:bg-truegray-800 dark:border-truegray-900"
            >
                <p class="text-sm p-2 md:p-0">
                    To connect with friends simply enter the URL that points to
                    their Microsocial deployment in the form above, if they
                    accept your request you'll get one back so don't forget to
                    come back and accept it! Your Microsocial server URL is <span
                        class="text-green-800 dark:text-amber-400"
                        >{hostBridge}</span
                    > share it with your friends so they can connect with you. Friends
                    and any pending requests will be displayed below where you can
                    manage them and do things like view their profiles.
                </p>
            </div>
        {/if}

        {#if friendListLoaded}
            {#if actualFriendCount > 0}
                <h2 class="pt-4 pb-2 text-2xl">Friends</h2>

                {#each friendListResp as { bridge, name, key, category }}
                    {#if category != "pending_friend"}
                        <div
                            class="flex w-full mb-2 text-gray-600 bg-gray-200 rounded shadow dark:bg-truegray-800 dark:text-gray-300"
                        >
                            <div class="self-center w-full p-2">
                                <div class="flex">
                                    <div>{name}</div>
                                </div>

                                <div class="-mt-1 text-xs text-gray-400 title">
                                    {bridge}
                                </div>
                            </div>
                            <div class="self-center p-2 sec w-2/8">
                                <div class="flex text-xs font-light">
                                    <button
                                        title="Remove Friend"
                                        class="p-2 mr-1 rounded shadow cursor-pointer hover:bg-red-100 dark:hover:bg-red-500 focus:outline-none"
                                        on:click={() => {
                                            if (
                                                confirm(
                                                    `Are you sure you want to remove ${name} as a friend?`
                                                )
                                            ) {
                                                removeFriend(key);
                                            }
                                        }}
                                    >
                                        <svg
                                            class="w-6 h-6"
                                            fill="currentColor"
                                            viewBox="0 0 20 20"
                                            xmlns="http://www.w3.org/2000/svg"
                                            ><path
                                                fill-rule="evenodd"
                                                d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z"
                                                clip-rule="evenodd"
                                            /></svg
                                        >
                                    </button>
                                    <button
                                        title="View Profile"
                                        class="p-2 mr-1 rounded shadow cursor-pointer hover:bg-indigo-100 dark:hover:bg-indigo-500 focus:outline-none"
                                        on:click={() => {
                                            viewingName = name;
                                            getFriendProfile(bridge);
                                            getFriendPosts(bridge);
                                        }}
                                    >
                                        <svg
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
                                        >
                                    </button>
                                </div>
                            </div>
                        </div>
                    {/if}
                {/each}
            {/if}

            {#if anyPending == true}
                {#if pendingFriendCount > 0}
                    <h2 class="pt-4 pb-2 text-2xl">Requests</h2>
                {/if}
                {#each friendListResp as { bridge, name, key, category }}
                    {#if category == "pending_friend"}
                        <div
                            class="flex w-full mb-2 text-gray-600 bg-gray-200 rounded shadow dark:bg-truegray-800 dark:text-gray-300"
                        >
                            <div class="self-center w-full p-2">
                                <div class="flex">
                                    <div>{name}</div>
                                </div>

                                <div class="-mt-1 text-xs text-gray-400 title">
                                    {bridge}
                                </div>
                            </div>
                            <div class="self-center p-2 sec w-2/8">
                                <div class="flex text-xs font-light">
                                    <button
                                        title="Accept Friend Request"
                                        class="p-2 mr-1 rounded shadow cursor-pointer hover:bg-green-100 focus:outline-none dark:hover:bg-green-500"
                                        on:click={() => {
                                            acceptFriendRequest(
                                                bridge,
                                                key,
                                                name
                                            );
                                            --pendingFriendCount;
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
                                        >
                                    </button>
                                    <button
                                        title="Decline Friend Request"
                                        class="p-2 mr-1 rounded shadow cursor-pointer hover:bg-red-100 focus:outline-none dark:hover:bg-red-500"
                                        on:click={() => {
                                            removeFriend(key);
                                            --pendingFriendCount;
                                        }}
                                        ><svg
                                            class="w-6 h-6"
                                            fill="currentColor"
                                            viewBox="0 0 20 20"
                                            xmlns="http://www.w3.org/2000/svg"
                                            ><path
                                                fill-rule="evenodd"
                                                d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                                                clip-rule="evenodd"
                                            /></svg
                                        >
                                    </button>
                                </div>
                            </div>
                        </div>
                    {/if}
                {/each}
            {/if}
        {/if}
    {:else}
        <button
            title="Go back"
            class="text-xl text-indigo-500 focus:outline-none hover:text-indigo-400"
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
        <h2 class="pb-2 text-2xl">{viewingProfile.username}'s Profile</h2>
        <div class="p-1">
            <div
                class="p-4 bg-gray-200 border-2 rounded-lg shadow-lg dark:bg-truegray-800 dark:border-truegray-900"
            >
                <p class="text-sm text-gray-600 dark:text-truegray-300">
                    {viewingProfile.bio}
                </p>
            </div>
        </div>
        {#if viewingFriendsPosts}
            <h2 class="pt-4 pb-2 text-2xl">Posts</h2>
            {#each viewingPosts as { value, time }}
                <div class="p-1">
                    <div
                        class="p-4 bg-gray-200 border-2 rounded-lg shadow-lg dark:bg-truegray-800 dark:border-truegray-900"
                    >
                        <div class="flex">
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
                        <div class="mt-2">
                            <p
                                class="text-sm text-gray-600 dark:text-truegray-300"
                            >
                                {@html anchorme(value)}
                            </p>
                        </div>
                    </div>
                </div>
            {/each}
        {/if}
    {/if}
</div>
