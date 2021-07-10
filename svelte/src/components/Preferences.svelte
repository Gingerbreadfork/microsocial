<script>
    import { onMount, onDestroy } from "svelte";

    let hostAccessKey = "";
    let hostUsername = "";
    let myNameLoaded = false;
    let newAccessKey;
    let newUsername;
    let hostBio;
    let myBioLoaded;

    onMount(async () => {
        getMyName();
        getMyBio();
    });

    onDestroy(async () => {});

    const getMyName = async () => {
        var myNameReq = await fetch("my-name");
        var myNameResp = await myNameReq.json();
        hostUsername = myNameResp.name;
        myNameLoaded = true;
    };

    const changeName = async () => {
        var updateName = {
            new_name: newUsername,
        };

        var changeNameResp = await fetch("change-name", {
            method: "PUT",
            headers: {
                Accept: "application/json",
                "Content-Type": "application/json",
            },
            body: JSON.stringify(updateName),
        });

        var changeKeyResult = await changeNameResp.json();
        getMyName();
    };

    const getMyBio = async () => {
        var myBioReq = await fetch("bio");
        var myBioResp = await myBioReq.json();
        hostBio = myBioResp;
        myBioLoaded = true;
    };

    const changeBio = async () => {
        var updateedBio = {
            bio: hostBio,
        };

        var changeBioResp = await fetch("change-bio", {
            method: "PUT",
            headers: {
                Accept: "application/json",
                "Content-Type": "application/json",
            },
            body: JSON.stringify(updateedBio),
        });

        var changeBioResult = await changeBioResp.json();
        getMyBio();
    };
</script>

<div class="container mx-auto sm:p-10">
    {#if myNameLoaded}
        <h2 class="text-2xl pb-2 pt-2">Change Username</h2>
        <div
            class="border border-gray-300 p-2 grid grid-cols-1 gap-2 bg-gray-200 shadow-lg rounded-lg"
        >
            <p><b>Current Username: </b>{hostUsername}</p>
            <div class="grid border border-gray-300 p-2 rounded">
                <div class="flex border rounded bg-gray-300 items-center p-2 ">
                    <svg
                        class="w-6 h-6 mr-2"
                        fill="currentColor"
                        viewBox="0 0 20 20"
                        xmlns="http://www.w3.org/2000/svg"
                        ><path
                            fill-rule="evenodd"
                            d="M14.243 5.757a6 6 0 10-.986 9.284 1 1 0 111.087 1.678A8 8 0 1118 10a3 3 0 01-4.8 2.401A4 4 0 1114 10a1 1 0 102 0c0-1.537-.586-3.07-1.757-4.243zM12 10a2 2 0 10-4 0 2 2 0 004 0z"
                            clip-rule="evenodd"
                        /></svg
                    >
                    <input
                        bind:value={newUsername}
                        type="text"
                        placeholder="Username"
                        class="bg-gray-300 w-full focus:outline-none text-gray-700"
                    />
                </div>
            </div>
            <div class="flex justify-end mb-2 mt-2">
                <button
                    on:click={changeName}
                    class="p-3 border bg-blue-600 hover:bg-blue-500 rounded-3xl text-white focus:outline-none"
                    ><svg
                        class="w-6 h-6"
                        fill="currentColor"
                        viewBox="0 0 20 20"
                        xmlns="http://www.w3.org/2000/svg"
                        ><path
                            fill-rule="evenodd"
                            d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z"
                            clip-rule="evenodd"
                        /></svg
                    ></button
                >
            </div>
        </div>
    {/if}

    {#if myBioLoaded}
        <h2 class="text-2xl pt-4 pb-2">Edit Bio</h2>
        <div
            class="border border-gray-300 p-2 bg-gray-200 shadow-lg rounded-lg"
        >
            <div class="border border-gray-300 rounded-xl p-2 pb-0">
                <textarea
                    bind:value={hostBio}
                    class="w-full text-gray-700 border rounded-lg focus:outline-none"
                    rows="5"
                />
            </div>
            <div class="flex justify-end mb-2 mt-2">
                <button
                    on:click={changeBio}
                    class="p-3 border bg-purple-600 hover:bg-purple-500 rounded-3xl text-white focus:outline-none"
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
