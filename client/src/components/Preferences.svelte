<script>
    import { onMount, onDestroy } from "svelte";

    let hostAccessKey = "";
    let hostUsername = "";
    let newAccessKey;
    let newUsername;
    let hostBio;
    let hostProfileLoaded;
    let updatedUsername = false;
    let updatedBio = false;
    let initialBio;

    let devBridge = "";

    if (window.location.hostname == "localhost") {
        devBridge = "https://41034m.deta.dev/";
    }

    onMount(async () => {
        getMyProfile();
    });

    onDestroy(async () => {});

    const getMyProfile = async () => {
        var hostProfileReq = await fetch(`${devBridge}public/profile`);
        var hostProfileResp = await hostProfileReq.json();
        hostUsername = hostProfileResp.username;
        hostBio = hostProfileResp.bio;
        hostProfileLoaded = true;
        newUsername = hostUsername;
        initialBio = hostBio;
    };

    const changeName = async (name) => {
        updatedUsername = false;

        if (name.length > 20) {
            alert(
                `Requested Username too Long. 20 characters max, current ${name.length}!`
            );
            return;
        }

        var changeNameResp = await fetch(`${devBridge}edit`, {
            method: "PUT",
            headers: {
                Accept: "application/json",
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                content: name,
                item: "username",
            }),
        });

        var changeKeyResult = await changeNameResp.json();
        getMyProfile();
        updatedUsername = true;
    };

    const changeBio = async () => {
        updatedBio = false;

        if (hostBio.length > 5000) {
            alert(
                `Updated bio too Long. 5000 characters max, current ${hostBio.length}!`
            );
            return;
        }

        var changeBioResp = await fetch(`${devBridge}edit`, {
            method: "PUT",
            headers: {
                Accept: "application/json",
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                content: hostBio,
                item: "bio",
            }),
        });

        var changeBioResult = await changeBioResp.json();
        getMyProfile();
        updatedBio = true;
    };

    const purgePosts = async () => {
        var purgePostsReq = await fetch(`${devBridge}purge/posts`);
        var purgePostsResp = await purgePostsReq.json();
    };

    const purgeCache = async () => {
        var purgeCacheReq = await fetch(`${devBridge}purge/cache`);
        var purgeCacheResp = await purgeCacheReq.json();
    };
</script>

<div class="container w-full mx-auto sm:p-10 md:w-2/3 lg:w-1/2 xl:w-1/2">
    {#if hostProfileLoaded}
        <div
            class="grid grid-cols-1 gap-2 p-2 bg-gray-200 border border-gray-300 rounded-lg shadow-lg dark:bg-truegray-800 dark:border-truegray-900"
        >
            <div class="flex">
                <svg
                    class="inline-block w-6 h-6 mb-1 ml-2 mr-2 text-gray-700 dark:text-truegray-300"
                    fill="currentColor"
                    viewBox="0 0 20 20"
                    xmlns="http://www.w3.org/2000/svg"
                    ><path
                        fill-rule="evenodd"
                        d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-6-3a2 2 0 11-4 0 2 2 0 014 0zm-2 4a5 5 0 00-4.546 2.916A5.986 5.986 0 0010 16a5.986 5.986 0 004.546-2.084A5 5 0 0010 11z"
                        clip-rule="evenodd"
                    /></svg
                > <span> Change Username </span>
            </div>
            <div
                class="grid p-2 border border-gray-300 rounded dark:border-truegray-700 dark:bg-truegray-800"
            >
                <div
                    class="flex items-center p-2 bg-white border rounded dark:border-truegray-700 dark:bg-truegray-900"
                >
                    <input
                        bind:value={newUsername}
                        type="text"
                        class="w-full text-gray-700 focus:outline-none dark:bg-truegray-900 dark:text-truegray-300"
                    />
                </div>
            </div>

            <div class="flex mt-2 mb-2">
                {#if updatedUsername}
                    <div class="flex flex-row mt-3">
                        <div class="px-2">
                            <svg
                                width="24"
                                height="24"
                                viewBox="0 0 1792 1792"
                                fill="#44C997"
                                xmlns="http://www.w3.org/2000/svg"
                            >
                                <path
                                    d="M1299 813l-422 422q-19 19-45 19t-45-19l-294-294q-19-19-19-45t19-45l102-102q19-19 45-19t45 19l147 147 275-275q19-19 45-19t45 19l102 102q19 19 19 45t-19 45zm141 83q0-148-73-273t-198-198-273-73-273 73-198 198-73 273 73 273 198 198 273 73 273-73 198-198 73-273zm224 0q0 209-103 385.5t-279.5 279.5-385.5 103-385.5-103-279.5-279.5-103-385.5 103-385.5 279.5-279.5 385.5-103 385.5 103 279.5 279.5 103 385.5z"
                                />
                            </svg>
                        </div>

                        <span>Username Updated!</span>
                    </div>
                {/if}
                {#if hostUsername !== newUsername}
                    <button
                        title="Save Updated Username"
                        on:click={() => {
                            changeName(newUsername);
                            newUsername = "";
                        }}
                        class="p-2 ml-auto text-white bg-blue-500 border hover:bg-blue-400 rounded-3xl focus:outline-none"
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
                {/if}
            </div>
        </div>

        <div
            class="p-2 mt-2 bg-gray-200 border border-gray-300 rounded-lg shadow-lg dark:border-truegray-900 dark:bg-truegray-800"
        >
            <svg
                class="inline-block w-6 h-6 mb-1 ml-2 mr-2 text-gray-700 dark:text-truegray-300"
                fill="currentColor"
                viewBox="0 0 20 20"
                xmlns="http://www.w3.org/2000/svg"
                ><path
                    fill-rule="evenodd"
                    d="M10 2a1 1 0 00-1 1v1a1 1 0 002 0V3a1 1 0 00-1-1zM4 4h3a3 3 0 006 0h3a2 2 0 012 2v9a2 2 0 01-2 2H4a2 2 0 01-2-2V6a2 2 0 012-2zm2.5 7a1.5 1.5 0 100-3 1.5 1.5 0 000 3zm2.45 4a2.5 2.5 0 10-4.9 0h4.9zM12 9a1 1 0 100 2h3a1 1 0 100-2h-3zm-1 4a1 1 0 011-1h2a1 1 0 110 2h-2a1 1 0 01-1-1z"
                    clip-rule="evenodd"
                /></svg
            >
            <span> Edit Bio </span>
            <div
                class="p-2 pb-0 border border-gray-300 rounded-xl dark:border-truegray-700"
            >
                <textarea
                    bind:value={hostBio}
                    class="w-full p-2 text-gray-700 border rounded-lg focus:outline-none dark:bg-truegray-900 dark:text-truegray-300 dark:border-truegray-700"
                    rows="5"
                />
            </div>
            <div class="flex mt-2 mb-2">
                {#if updatedBio}
                    <div class="flex flex-row mt-3">
                        <div class="px-2">
                            <svg
                                width="24"
                                height="24"
                                viewBox="0 0 1792 1792"
                                fill="#44C997"
                                xmlns="http://www.w3.org/2000/svg"
                            >
                                <path
                                    d="M1299 813l-422 422q-19 19-45 19t-45-19l-294-294q-19-19-19-45t19-45l102-102q19-19 45-19t45 19l147 147 275-275q19-19 45-19t45 19l102 102q19 19 19 45t-19 45zm141 83q0-148-73-273t-198-198-273-73-273 73-198 198-73 273 73 273 198 198 273 73 273-73 198-198 73-273zm224 0q0 209-103 385.5t-279.5 279.5-385.5 103-385.5-103-279.5-279.5-103-385.5 103-385.5 279.5-279.5 385.5-103 385.5 103 279.5 279.5 103 385.5z"
                                />
                            </svg>
                        </div>

                        <span>Bio Updated</span>
                    </div>
                {/if}
                {#if hostBio !== initialBio}
                    <button
                        title="Save Updated Bio"
                        on:click={changeBio}
                        class="p-2 mt-2 ml-auto text-white bg-blue-500 border hover:bg-blue-400 rounded-3xl focus:outline-none"
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
                    >{/if}
            </div>
        </div>
        <div
            class="mb-4 mt-4 p-2 bg-gray-200 border border-gray-300 rounded-lg shadow-lg dark:border-truegray-900 dark:bg-truegray-800"
        >
            <div class="pb-2">
                <svg
                    class="w-6 h-6 inline-block ml-1 text-gray-700 dark:text-truegray-300"
                    fill="currentColor"
                    viewBox="0 0 20 20"
                    xmlns="http://www.w3.org/2000/svg"
                    ><path
                        fill-rule="evenodd"
                        d="M11.49 3.17c-.38-1.56-2.6-1.56-2.98 0a1.532 1.532 0 01-2.286.948c-1.372-.836-2.942.734-2.106 2.106.54.886.061 2.042-.947 2.287-1.561.379-1.561 2.6 0 2.978a1.532 1.532 0 01.947 2.287c-.836 1.372.734 2.942 2.106 2.106a1.532 1.532 0 012.287.947c.379 1.561 2.6 1.561 2.978 0a1.533 1.533 0 012.287-.947c1.372.836 2.942-.734 2.106-2.106a1.533 1.533 0 01.947-2.287c1.561-.379 1.561-2.6 0-2.978a1.532 1.532 0 01-.947-2.287c.836-1.372-.734-2.942-2.106-2.106a1.532 1.532 0 01-2.287-.947zM10 13a3 3 0 100-6 3 3 0 000 6z"
                        clip-rule="evenodd"
                    /></svg
                >
                <span>Advanced</span><br />
            </div>
            <div
                class="p-2 pb-2 border border-gray-300 rounded-xl dark:border-truegray-700"
            >
                <button
                    on:click={() => {
                        if (
                            confirm(
                                "Are you sure? Deleting your posts can't be undone & this will delete ALL your posts!"
                            )
                        ) {
                            purgePosts();
                        }
                    }}
                    class="m-2 border-2 focus:outline-none border-red-600 rounded-lg px-3 py-2 bg-red-500 text-white cursor-pointer hover:bg-red-600 hover:text-red-200"
                >
                    Delete All Posts
                </button>
                <button
                    on:click={() => {
                        if (
                            confirm(
                                "The cache we be rebuilt the next time the feed is refreshed, are you sure you want to clear the cache?"
                            )
                        ) {
                            purgeCache();
                        }
                    }}
                    class="m-2 border-2 focus:outline-none border-amber-600 rounded-lg px-3 py-2 bg-amber-500 text-white cursor-pointer hover:bg-amber-600 hover:text-amber-200"
                >
                    Purge Feed Cache
                </button>
            </div>
        </div>
    {/if}
</div>
