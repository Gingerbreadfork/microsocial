<script>
    import "./lib/TailwindCSS.svelte";
    import ManageFriends from "./components/ManageFriends.svelte";
    import Feed from "./components/Feed.svelte";
    import Profile from "./components/Profile.svelte";
    import Settings from "./components/Preferences.svelte";
    import { onMount } from "svelte";

    let currentComponent = "Feed";

    onMount(async () => {
        // Navbar Toggle
        document.addEventListener("DOMContentLoaded", function () {
            // Get all "navbar-burger" elements
            var $navbarBurgers = Array.prototype.slice.call(
                document.querySelectorAll(".navbar-burger"),
                0
            );

            // Check if there are any navbar burgers
            if ($navbarBurgers.length > 0) {
                // Add a click event on each of them
                $navbarBurgers.forEach(function ($el) {
                    $el.addEventListener("click", function () {
                        // Get the "main-nav" element
                        var $target = document.getElementById("main-nav");

                        // Toggle the class on "main-nav"
                        $target.classList.toggle("hidden");
                    });
                });
            }
        });
    });

    function toggleBurger() {
        var $target = document.getElementById("main-nav");
        $target.classList.toggle("hidden");
    }
</script>

<div class="border-b border-gray-900 bg-black py-2 px-2">
    <div class="container mx-auto">
        <nav class="flex items-center justify-between flex-wrap">
            <div class="flex items-center flex-no-shrink text-white mr-6">
                <svg
                    class="h-8 w-8 mr-2 text-purple-500"
                    fill="currentColor"
                    viewBox="0 0 20 20"
                    xmlns="http://www.w3.org/2000/svg"
                    ><path
                        fill-rule="evenodd"
                        d="M9.504 1.132a1 1 0 01.992 0l1.75 1a1 1 0 11-.992 1.736L10 3.152l-1.254.716a1 1 0 11-.992-1.736l1.75-1zM5.618 4.504a1 1 0 01-.372 1.364L5.016 6l.23.132a1 1 0 11-.992 1.736L4 7.723V8a1 1 0 01-2 0V6a.996.996 0 01.52-.878l1.734-.99a1 1 0 011.364.372zm8.764 0a1 1 0 011.364-.372l1.733.99A1.002 1.002 0 0118 6v2a1 1 0 11-2 0v-.277l-.254.145a1 1 0 11-.992-1.736l.23-.132-.23-.132a1 1 0 01-.372-1.364zm-7 4a1 1 0 011.364-.372L10 8.848l1.254-.716a1 1 0 11.992 1.736L11 10.58V12a1 1 0 11-2 0v-1.42l-1.246-.712a1 1 0 01-.372-1.364zM3 11a1 1 0 011 1v1.42l1.246.712a1 1 0 11-.992 1.736l-1.75-1A1 1 0 012 14v-2a1 1 0 011-1zm14 0a1 1 0 011 1v2a1 1 0 01-.504.868l-1.75 1a1 1 0 11-.992-1.736L16 13.42V12a1 1 0 011-1zm-9.618 5.504a1 1 0 011.364-.372l.254.145V16a1 1 0 112 0v.277l.254-.145a1 1 0 11.992 1.736l-1.735.992a.995.995 0 01-1.022 0l-1.735-.992a1 1 0 01-.372-1.364z"
                        clip-rule="evenodd"
                    /></svg
                >
                <span class="font-semibold text-xl tracking-tight"
                    >Microsocial</span
                >
            </div>
            <div class="block sm:hidden">
                <button
                    class="navbar-burger flex items-center px-3 py-2 border rounded text-white border-white hover:text-white hover:border-white focus:outline-none"
                >
                    <svg
                        class="fill-current h-3 w-3"
                        viewBox="0 0 20 20"
                        xmlns="http://www.w3.org/2000/svg"
                        ><title>Microsocial</title><path
                            d="M0 3h20v2H0V3zm0 6h20v2H0V9zm0 6h20v2H0v-2z"
                        /></svg
                    >
                </button>
            </div>
            <div
                id="main-nav"
                class="w-full gap-4 flex-grow sm:flex items-center sm:w-auto hidden"
            >
                <div class="text-sm sm:flex-grow text-white" />
                {#if currentComponent != "Feed"}
                    <button
                        on:click={() => {
                            toggleBurger();
                            currentComponent = "Feed";
                        }}
                        class="font-medium text-gray-200 hover:text-white flex pt-2 sm:pt-0 m-auto focus:outline-none"
                        ><svg
                            class="w-6 h-6"
                            fill="currentColor"
                            viewBox="0 0 20 20"
                            xmlns="http://www.w3.org/2000/svg"
                            ><path
                                d="M7 3a1 1 0 000 2h6a1 1 0 100-2H7zM4 7a1 1 0 011-1h10a1 1 0 110 2H5a1 1 0 01-1-1zM2 11a2 2 0 012-2h12a2 2 0 012 2v4a2 2 0 01-2 2H4a2 2 0 01-2-2v-4z"
                            /></svg
                        ><span class="text-white sm:hidden ml-2">Live Feed</span
                        ></button
                    >
                {:else}
                    <button
                        on:click={() => {
                            toggleBurger();
                            currentComponent = "Feed";
                        }}
                        class="font-medium text-indigo-500 hover:text-indigo-400 flex pt-2 sm:pt-0 m-auto focus:outline-none"
                        ><svg
                            class="w-6 h-6"
                            fill="currentColor"
                            viewBox="0 0 20 20"
                            xmlns="http://www.w3.org/2000/svg"
                            ><path
                                d="M7 3a1 1 0 000 2h6a1 1 0 100-2H7zM4 7a1 1 0 011-1h10a1 1 0 110 2H5a1 1 0 01-1-1zM2 11a2 2 0 012-2h12a2 2 0 012 2v4a2 2 0 01-2 2H4a2 2 0 01-2-2v-4z"
                            /></svg
                        ><span class="text-white sm:hidden ml-2">Live Feed</span
                        ></button
                    >
                {/if}
                {#if currentComponent != "Profile"}
                    <button
                        on:click={() => {
                            toggleBurger();
                            currentComponent = "Profile";
                        }}
                        class="font-medium text-gray-200 hover:text-white flex pt-2 sm:pt-0 m-auto focus:outline-none"
                        ><svg
                            class="w-6 h-6"
                            fill="currentColor"
                            viewBox="0 0 20 20"
                            xmlns="http://www.w3.org/2000/svg"
                            ><path
                                fill-rule="evenodd"
                                d="M10 2a1 1 0 00-1 1v1a1 1 0 002 0V3a1 1 0 00-1-1zM4 4h3a3 3 0 006 0h3a2 2 0 012 2v9a2 2 0 01-2 2H4a2 2 0 01-2-2V6a2 2 0 012-2zm2.5 7a1.5 1.5 0 100-3 1.5 1.5 0 000 3zm2.45 4a2.5 2.5 0 10-4.9 0h4.9zM12 9a1 1 0 100 2h3a1 1 0 100-2h-3zm-1 4a1 1 0 011-1h2a1 1 0 110 2h-2a1 1 0 01-1-1z"
                                clip-rule="evenodd"
                            /></svg
                        ><span class="text-white sm:hidden ml-2">Profile</span
                        ></button
                    >
                {:else}
                    <button
                        on:click={() => {
                            toggleBurger();
                            currentComponent = "Profile";
                        }}
                        class="font-medium text-indigo-500 hover:text-indigo-400 flex pt-2 sm:pt-0 m-auto focus:outline-none"
                        ><svg
                            class="w-6 h-6"
                            fill="currentColor"
                            viewBox="0 0 20 20"
                            xmlns="http://www.w3.org/2000/svg"
                            ><path
                                fill-rule="evenodd"
                                d="M10 2a1 1 0 00-1 1v1a1 1 0 002 0V3a1 1 0 00-1-1zM4 4h3a3 3 0 006 0h3a2 2 0 012 2v9a2 2 0 01-2 2H4a2 2 0 01-2-2V6a2 2 0 012-2zm2.5 7a1.5 1.5 0 100-3 1.5 1.5 0 000 3zm2.45 4a2.5 2.5 0 10-4.9 0h4.9zM12 9a1 1 0 100 2h3a1 1 0 100-2h-3zm-1 4a1 1 0 011-1h2a1 1 0 110 2h-2a1 1 0 01-1-1z"
                                clip-rule="evenodd"
                            /></svg
                        ><span class="text-white sm:hidden ml-2">Profile</span
                        ></button
                    >
                {/if}
                {#if currentComponent != "Friends"}
                    <button
                        on:click={() => {
                            toggleBurger();
                            currentComponent = "Friends";
                        }}
                        class="font-medium text-gray-200 hover:text-white flex pt-2 sm:pt-0 m-auto focus:outline-none"
                        ><svg
                            class="w-6 h-6"
                            fill="currentColor"
                            viewBox="0 0 20 20"
                            xmlns="http://www.w3.org/2000/svg"
                            ><path
                                d="M13 6a3 3 0 11-6 0 3 3 0 016 0zM18 8a2 2 0 11-4 0 2 2 0 014 0zM14 15a4 4 0 00-8 0v3h8v-3zM6 8a2 2 0 11-4 0 2 2 0 014 0zM16 18v-3a5.972 5.972 0 00-.75-2.906A3.005 3.005 0 0119 15v3h-3zM4.75 12.094A5.973 5.973 0 004 15v3H1v-3a3 3 0 013.75-2.906z"
                            /></svg
                        ><span class="text-white sm:hidden ml-2">Friends</span
                        ></button
                    >{:else}
                    <button
                        on:click={() => {
                            toggleBurger();
                            currentComponent = "Friends";
                        }}
                        class="font-medium text-indigo-500 hover:text-indigo-400 flex pt-2 sm:pt-0 m-auto focus:outline-none"
                        ><svg
                            class="w-6 h-6"
                            fill="currentColor"
                            viewBox="0 0 20 20"
                            xmlns="http://www.w3.org/2000/svg"
                            ><path
                                d="M13 6a3 3 0 11-6 0 3 3 0 016 0zM18 8a2 2 0 11-4 0 2 2 0 014 0zM14 15a4 4 0 00-8 0v3h8v-3zM6 8a2 2 0 11-4 0 2 2 0 014 0zM16 18v-3a5.972 5.972 0 00-.75-2.906A3.005 3.005 0 0119 15v3h-3zM4.75 12.094A5.973 5.973 0 004 15v3H1v-3a3 3 0 013.75-2.906z"
                            /></svg
                        ><span class="text-white sm:hidden ml-2">Friends</span
                        ></button
                    >
                {/if}
                {#if currentComponent != "Settings"}
                    <button
                        on:click={() => {
                            toggleBurger();
                            currentComponent = "Settings";
                        }}
                        class="font-medium text-gray-200 hover:text-white flex pt-2 sm:pt-0 m-auto focus:outline-none"
                        ><svg
                            class="w-6 h-6"
                            fill="currentColor"
                            viewBox="0 0 20 20"
                            xmlns="http://www.w3.org/2000/svg"
                            ><path
                                fill-rule="evenodd"
                                d="M11.49 3.17c-.38-1.56-2.6-1.56-2.98 0a1.532 1.532 0 01-2.286.948c-1.372-.836-2.942.734-2.106 2.106.54.886.061 2.042-.947 2.287-1.561.379-1.561 2.6 0 2.978a1.532 1.532 0 01.947 2.287c-.836 1.372.734 2.942 2.106 2.106a1.532 1.532 0 012.287.947c.379 1.561 2.6 1.561 2.978 0a1.533 1.533 0 012.287-.947c1.372.836 2.942-.734 2.106-2.106a1.533 1.533 0 01.947-2.287c1.561-.379 1.561-2.6 0-2.978a1.532 1.532 0 01-.947-2.287c.836-1.372-.734-2.942-2.106-2.106a1.532 1.532 0 01-2.287-.947zM10 13a3 3 0 100-6 3 3 0 000 6z"
                                clip-rule="evenodd"
                            />
                        </svg><span class="text-white sm:hidden ml-2"
                            >Settings</span
                        ></button
                    >
                {:else}
                    <button
                        on:click={() => {
                            toggleBurger();
                            currentComponent = "Settings";
                        }}
                        class="font-medium text-indigo-500 hover:text-indigo-400 flex pt-2 sm:pt-0 m-auto focus:outline-none"
                        ><svg
                            class="w-6 h-6"
                            fill="currentColor"
                            viewBox="0 0 20 20"
                            xmlns="http://www.w3.org/2000/svg"
                            ><path
                                fill-rule="evenodd"
                                d="M11.49 3.17c-.38-1.56-2.6-1.56-2.98 0a1.532 1.532 0 01-2.286.948c-1.372-.836-2.942.734-2.106 2.106.54.886.061 2.042-.947 2.287-1.561.379-1.561 2.6 0 2.978a1.532 1.532 0 01.947 2.287c-.836 1.372.734 2.942 2.106 2.106a1.532 1.532 0 012.287.947c.379 1.561 2.6 1.561 2.978 0a1.533 1.533 0 012.287-.947c1.372.836 2.942-.734 2.106-2.106a1.533 1.533 0 01.947-2.287c1.561-.379 1.561-2.6 0-2.978a1.532 1.532 0 01-.947-2.287c.836-1.372-.734-2.942-2.106-2.106a1.532 1.532 0 01-2.287-.947zM10 13a3 3 0 100-6 3 3 0 000 6z"
                                clip-rule="evenodd"
                            />
                        </svg><span class="text-white sm:hidden ml-2"
                            >Settings</span
                        ></button
                    >
                {/if}
            </div>
        </nav>
    </div>
</div>

<div class="p-2">
    {#if currentComponent == "Friends"}
        <ManageFriends />
    {:else if currentComponent == "Settings"}
        <Settings />
    {:else if currentComponent == "Feed"}
        <Feed />
    {:else if currentComponent == "Profile"}
        <Profile />
    {/if}
</div>
