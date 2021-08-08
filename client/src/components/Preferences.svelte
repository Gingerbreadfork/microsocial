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

    let devBridge = "";

    if (window.location.hostname == "localhost") {
        devBridge = "https://41034m.deta.dev/";
    }

    onMount(async () => {
        getMyProfile();
    });

    onDestroy(async () => {});

    const getMyProfile = async () => {
        var hostProfileReq = await fetch(devBridge + "public/profile");
        var hostProfileResp = await hostProfileReq.json();
        hostUsername = hostProfileResp.username;
        hostBio = hostProfileResp.bio;
        hostProfileLoaded = true;
    };

    const changeName = async (name) => {
        updatedUsername = false;

        if (name.length > 20) {
            alert(
                `Requested Username too Long. 20 characters max, current ${name.length}!`
            );
            return;
        }

        var changeNameResp = await fetch(devBridge + "edit", {
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
        var changeBioResp = await fetch(devBridge + "edit", {
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
</script>

<div class="container mx-auto sm:p-10 w-full md:w-2/3 lg:w-1/2 xl:w-1/2">
    {#if hostProfileLoaded}
        <div
            class="border border-gray-300 p-2 grid grid-cols-1 gap-2 bg-gray-200 shadow-lg rounded-lg"
        >
            <div class="flex">
                <svg
                    class="w-6 h-6 mb-1 ml-2 mr-2 inline-block text-gray-700"
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
            <div class="grid border border-gray-300 p-2 rounded">
                <div class="flex border rounded bg-gray-300 items-center p-2 ">
                    <input
                        bind:value={newUsername}
                        type="text"
                        placeholder={hostUsername}
                        class="bg-gray-300 w-full focus:outline-none text-gray-700"
                    />
                </div>
            </div>

            <div class="flex mb-2 mt-2">
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

                        <span class="font-semibold">Username Updated!</span>
                    </div>
                {/if}
                <button
                    on:click={() => {
                        changeName(newUsername);
                        newUsername = "";
                    }}
                    class="ml-auto p-2 border bg-blue-500 hover:bg-blue-400 rounded-3xl text-white focus:outline-none"
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

        <div
            class="border border-gray-300 p-2 bg-gray-200 shadow-lg rounded-lg mt-2"
        >
            <svg
                class="w-6 h-6 inline-block mb-1 ml-2 mr-2 text-gray-700"
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
            <div class="border border-gray-300 rounded-xl p-2 pb-0">
                <textarea
                    bind:value={hostBio}
                    class="w-full text-gray-700 border rounded-lg focus:outline-none p-1"
                    rows="5"
                />
            </div>
            <div class="flex mb-2 mt-2">
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

                        <span class="font-semibold">Bio Updated</span>
                    </div>
                {/if}
                <button
                    on:click={changeBio}
                    class="ml-auto p-2 border bg-blue-500 hover:bg-blue-400 rounded-3xl text-white focus:outline-none"
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
    {/if}
</div>
