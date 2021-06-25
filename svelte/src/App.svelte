<script>
    import ManageFriends from "./components/ManageFriends.svelte";
    import Feed from "./components/Feed.svelte";
    import Profile from "./components/Profile.svelte";
    import Settings from "./components/Preferences.svelte";

    let currentComponent = "Home";
</script>

<nav
    class="flex text-center sm:flex-row sm:text-left sm:justify-between p-2 bg-gray-800 shadow sm:items-baseline w-full"
>
    <div class="flex text-purple-100 mb-2 sm:mb-0">
        <button
            on:click={() => {
                currentComponent = "Home";
            }}
            class="text-2xl pr-2 focus:outline-none">Microsocial</button
        >
        <span
            ><svg
                class="w-6 h-6"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
                xmlns="http://www.w3.org/2000/svg"
                ><path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"
                /></svg
            ></span
        >
    </div>
    <div class="flex items-end">
        <button
            class="pl-2 pr-2 text-indigo-500 hover:text-indigo-400 focus:outline-none"
            on:click={() => {
                currentComponent = "Profile";
            }}>Profile</button
        >
        <button
            class="pl-2 pr-2 text-indigo-500 hover:text-indigo-400 focus:outline-none"
            on:click={() => {
                currentComponent = "Friends";
            }}>Friends</button
        ><button
            class="pl-2 pr-2 text-indigo-500 hover:text-indigo-400 focus:outline-none"
            on:click={() => {
                currentComponent = "Feed";
            }}>Feed</button
        ><button
            class="pl-2 pr-2 text-indigo-500 hover:text-indigo-400 focus:outline-none"
            on:click={() => {
                currentComponent = "Settings";
            }}>Settings</button
        >
    </div>
</nav>

{#if currentComponent == "Friends"}
    <ManageFriends />
{:else if currentComponent == "Settings"}
    <Settings />
{:else if currentComponent == "Feed"}
    <Feed />
{:else if currentComponent == "Profile"}
    <Profile />
{:else if currentComponent == "Home"}
    <div class="container mx-auto sm:p-10">
        <p class="text-xl">Welcome, use the Nav to look around!</p>
    </div>
{/if}
