<script>
    import "./lib/TailwindCSS.svelte";
    import ManageFriends from "./components/ManageFriends.svelte";
    import Feed from "./components/Feed.svelte";
    import Profile from "./components/Profile.svelte";
    import Settings from "./components/Preferences.svelte";
    import Messages from "./components/Messages.svelte";
    import { onMount } from "svelte";

    let darkMode;
    let currentComponent = "Landing";

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

    if (localStorage.getItem("theme") === "theme-dark") {
        window.document.body.classList.toggle("dark");
        darkMode = true;
    } else {
        window.document.body.classList.toggle("light");
        darkMode = false;
    }
    function setTheme(themeName) {
        localStorage.setItem("theme", themeName);
        document.documentElement.className = themeName;
    }
    function toggleTheme() {
        window.document.body.classList.toggle("dark");
        if (localStorage.getItem("theme") === "theme-dark") {
            setTheme("theme-light");
            darkMode = false;
        } else {
            setTheme("theme-dark");
            darkMode = true;
        }
    }
</script>

<div class="px-2 py-2 cursor-default bg-truegray-900">
    <div class="container mx-auto">
        <nav class="flex flex-wrap items-center justify-between">
            <div
                on:click={() => {
                    currentComponent = "Landing";
                }}
                class="flex items-center mr-6 text-white cursor-pointer flex-no-shrink"
            >
                <svg
                    class="w-8 h-8 mr-2 text-purple-500"
                    fill="currentColor"
                    viewBox="0 0 20 20"
                    xmlns="http://www.w3.org/2000/svg"
                    ><path
                        fill-rule="evenodd"
                        d="M9.504 1.132a1 1 0 01.992 0l1.75 1a1 1 0 11-.992 1.736L10 3.152l-1.254.716a1 1 0 11-.992-1.736l1.75-1zM5.618 4.504a1 1 0 01-.372 1.364L5.016 6l.23.132a1 1 0 11-.992 1.736L4 7.723V8a1 1 0 01-2 0V6a.996.996 0 01.52-.878l1.734-.99a1 1 0 011.364.372zm8.764 0a1 1 0 011.364-.372l1.733.99A1.002 1.002 0 0118 6v2a1 1 0 11-2 0v-.277l-.254.145a1 1 0 11-.992-1.736l.23-.132-.23-.132a1 1 0 01-.372-1.364zm-7 4a1 1 0 011.364-.372L10 8.848l1.254-.716a1 1 0 11.992 1.736L11 10.58V12a1 1 0 11-2 0v-1.42l-1.246-.712a1 1 0 01-.372-1.364zM3 11a1 1 0 011 1v1.42l1.246.712a1 1 0 11-.992 1.736l-1.75-1A1 1 0 012 14v-2a1 1 0 011-1zm14 0a1 1 0 011 1v2a1 1 0 01-.504.868l-1.75 1a1 1 0 11-.992-1.736L16 13.42V12a1 1 0 011-1zm-9.618 5.504a1 1 0 011.364-.372l.254.145V16a1 1 0 112 0v.277l.254-.145a1 1 0 11.992 1.736l-1.735.992a.995.995 0 01-1.022 0l-1.735-.992a1 1 0 01-.372-1.364z"
                        clip-rule="evenodd"
                    /></svg
                >
                <span class="text-xl font-semibold tracking-tight"
                    >Microsocial</span
                >
            </div>

            <div class="block sm:hidden">
                <button
                    class="flex items-center px-3 py-2 text-white border border-white rounded navbar-burger hover:text-white hover:border-white focus:outline-none"
                >
                    <svg
                        class="w-3 h-3 fill-current"
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
                class="items-center flex-grow hidden w-full gap-4 sm:flex sm:w-auto"
            >
                <div class="text-sm text-white sm:flex-grow" />
                {#if currentComponent != "Feed"}
                    <button
                        title="Live Feed"
                        on:click={() => {
                            toggleBurger();
                            currentComponent = "Feed";
                        }}
                        class="flex pt-2 m-auto font-medium text-gray-200 hover:text-white sm:pt-0 focus:outline-none"
                        ><svg
                            class="w-6 h-6"
                            fill="currentColor"
                            viewBox="0 0 20 20"
                            xmlns="http://www.w3.org/2000/svg"
                            ><path
                                d="M7 3a1 1 0 000 2h6a1 1 0 100-2H7zM4 7a1 1 0 011-1h10a1 1 0 110 2H5a1 1 0 01-1-1zM2 11a2 2 0 012-2h12a2 2 0 012 2v4a2 2 0 01-2 2H4a2 2 0 01-2-2v-4z"
                            /></svg
                        ><span class="ml-2 text-white sm:hidden">Live Feed</span
                        ></button
                    >
                {:else}
                    <button
                        title="Live Feed"
                        on:click={() => {
                            toggleBurger();
                            currentComponent = "Feed";
                        }}
                        class="flex pt-2 m-auto font-medium text-indigo-500 hover:text-indigo-400 sm:pt-0 focus:outline-none"
                        ><svg
                            class="w-6 h-6"
                            fill="currentColor"
                            viewBox="0 0 20 20"
                            xmlns="http://www.w3.org/2000/svg"
                            ><path
                                d="M7 3a1 1 0 000 2h6a1 1 0 100-2H7zM4 7a1 1 0 011-1h10a1 1 0 110 2H5a1 1 0 01-1-1zM2 11a2 2 0 012-2h12a2 2 0 012 2v4a2 2 0 01-2 2H4a2 2 0 01-2-2v-4z"
                            /></svg
                        ><span class="ml-2 text-white sm:hidden">Live Feed</span
                        ></button
                    >
                {/if}
                {#if currentComponent != "Messages"}
                    <button
                        title="Direct Messages"
                        on:click={() => {
                            toggleBurger();
                            currentComponent = "Messages";
                        }}
                        class="flex pt-2 m-auto font-medium text-gray-200 hover:text-white sm:pt-0 focus:outline-none"
                        ><svg
                            class="w-6 h-6"
                            fill="currentColor"
                            viewBox="0 0 20 20"
                            xmlns="http://www.w3.org/2000/svg"
                            ><path
                                fill-rule="evenodd"
                                d="M18 10c0 3.866-3.582 7-8 7a8.841 8.841 0 01-4.083-.98L2 17l1.338-3.123C2.493 12.767 2 11.434 2 10c0-3.866 3.582-7 8-7s8 3.134 8 7zM7 9H5v2h2V9zm8 0h-2v2h2V9zM9 9h2v2H9V9z"
                                clip-rule="evenodd"
                            /></svg
                        ><span class="ml-2 text-white sm:hidden">Messages</span
                        ></button
                    >
                {:else}
                    <button
                        title="Direct Messages"
                        on:click={() => {
                            toggleBurger();
                            currentComponent = "Messages";
                        }}
                        class="flex pt-2 m-auto font-medium text-indigo-500 hover:text-indigo-400 sm:pt-0 focus:outline-none"
                    >
                        <svg
                            class="w-6 h-6"
                            fill="currentColor"
                            viewBox="0 0 20 20"
                            xmlns="http://www.w3.org/2000/svg"
                            ><path
                                fill-rule="evenodd"
                                d="M18 10c0 3.866-3.582 7-8 7a8.841 8.841 0 01-4.083-.98L2 17l1.338-3.123C2.493 12.767 2 11.434 2 10c0-3.866 3.582-7 8-7s8 3.134 8 7zM7 9H5v2h2V9zm8 0h-2v2h2V9zM9 9h2v2H9V9z"
                                clip-rule="evenodd"
                            /></svg
                        ><span class="ml-2 text-white sm:hidden">Messages</span
                        ></button
                    >
                {/if}
                {#if currentComponent != "Profile"}
                    <button
                        title="Profile"
                        on:click={() => {
                            toggleBurger();
                            currentComponent = "Profile";
                        }}
                        class="flex pt-2 m-auto font-medium text-gray-200 hover:text-white sm:pt-0 focus:outline-none"
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
                        ><span class="ml-2 text-white sm:hidden">Profile</span
                        ></button
                    >
                {:else}
                    <button
                        title="Profile"
                        on:click={() => {
                            toggleBurger();
                            currentComponent = "Profile";
                        }}
                        class="flex pt-2 m-auto font-medium text-indigo-500 hover:text-indigo-400 sm:pt-0 focus:outline-none"
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
                        ><span class="ml-2 text-white sm:hidden">Profile</span
                        ></button
                    >
                {/if}
                {#if currentComponent != "Friends"}
                    <button
                        title="Manage Friends"
                        on:click={() => {
                            toggleBurger();
                            currentComponent = "Friends";
                        }}
                        class="flex pt-2 m-auto font-medium text-gray-200 hover:text-white sm:pt-0 focus:outline-none"
                        ><svg
                            class="w-6 h-6"
                            fill="currentColor"
                            viewBox="0 0 20 20"
                            xmlns="http://www.w3.org/2000/svg"
                            ><path
                                d="M13 6a3 3 0 11-6 0 3 3 0 016 0zM18 8a2 2 0 11-4 0 2 2 0 014 0zM14 15a4 4 0 00-8 0v3h8v-3zM6 8a2 2 0 11-4 0 2 2 0 014 0zM16 18v-3a5.972 5.972 0 00-.75-2.906A3.005 3.005 0 0119 15v3h-3zM4.75 12.094A5.973 5.973 0 004 15v3H1v-3a3 3 0 013.75-2.906z"
                            /></svg
                        ><span class="ml-2 text-white sm:hidden">Friends</span
                        ></button
                    >{:else}
                    <button
                        title="Manage Friends"
                        on:click={() => {
                            toggleBurger();
                            currentComponent = "Friends";
                        }}
                        class="flex pt-2 m-auto font-medium text-indigo-500 hover:text-indigo-400 sm:pt-0 focus:outline-none"
                        ><svg
                            class="w-6 h-6"
                            fill="currentColor"
                            viewBox="0 0 20 20"
                            xmlns="http://www.w3.org/2000/svg"
                            ><path
                                d="M13 6a3 3 0 11-6 0 3 3 0 016 0zM18 8a2 2 0 11-4 0 2 2 0 014 0zM14 15a4 4 0 00-8 0v3h8v-3zM6 8a2 2 0 11-4 0 2 2 0 014 0zM16 18v-3a5.972 5.972 0 00-.75-2.906A3.005 3.005 0 0119 15v3h-3zM4.75 12.094A5.973 5.973 0 004 15v3H1v-3a3 3 0 013.75-2.906z"
                            /></svg
                        ><span class="ml-2 text-white sm:hidden">Friends</span
                        ></button
                    >
                {/if}
                {#if currentComponent != "Settings"}
                    <button
                        title="Settings"
                        on:click={() => {
                            toggleBurger();
                            currentComponent = "Settings";
                        }}
                        class="flex pt-2 m-auto font-medium text-gray-200 hover:text-white sm:pt-0 focus:outline-none"
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
                        </svg><span class="ml-2 text-white sm:hidden"
                            >Settings</span
                        ></button
                    >
                {:else}
                    <button
                        title="Settings"
                        on:click={() => {
                            toggleBurger();
                            currentComponent = "Settings";
                        }}
                        class="flex pt-2 m-auto font-medium text-indigo-500 hover:text-indigo-400 sm:pt-0 focus:outline-none"
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
                        </svg><span class="ml-2 text-white sm:hidden"
                            >Settings</span
                        ></button
                    >
                {/if}
                {#if darkMode}
                    <button
                        id="darkButton"
                        title="Light Mode"
                        on:click={toggleTheme}
                        class="p-2"
                        ><svg
                            class="w-6 h-6 text-yellow-200"
                            fill="none"
                            stroke="currentColor"
                            viewBox="0 0 24 24"
                            xmlns="http://www.w3.org/2000/svg"
                            ><path
                                stroke-linecap="round"
                                stroke-linejoin="round"
                                stroke-width="2"
                                d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"
                            /></svg
                        ></button
                    >
                {:else}
                    <button
                        id="darkButton"
                        title="Dark Mode"
                        on:click={toggleTheme}
                        class="p-2"
                        ><svg
                            class="w-6 h-6 text-indigo-200"
                            fill="none"
                            stroke="currentColor"
                            viewBox="0 0 24 24"
                            xmlns="http://www.w3.org/2000/svg"
                            ><path
                                stroke-linecap="round"
                                stroke-linejoin="round"
                                stroke-width="2"
                                d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"
                            /></svg
                        ></button
                    >
                {/if}
            </div>
        </nav>
    </div>
</div>

<div
    class="min-h-screen break-words bg-gray-300 dark:bg-truegray-900 dark:text-white"
>
    {#if currentComponent == "Landing"}
        <div
            class="min-h-screen overflow-auto bg-indigo-900 dark:bg-truegray-900"
        >
            <div class="container max-w-6xl px-6 py-20 mx-auto">
                <div
                    class="w-full pb-6 mx-auto text-center md:w-11/12 xl:w-9/12"
                >
                    <h1
                        class="mb-2 text-4xl font-extrabold leading-none tracking-normal text-gray-900 md:text-6xl md:tracking-tight"
                    >
                        <svg
                            class="inline-block w-10 pb-2 text-purple-500 md:w-14 animate-bounce"
                            fill="currentColor"
                            viewBox="0 0 20 20"
                            xmlns="http://www.w3.org/2000/svg"
                            ><path
                                fill-rule="evenodd"
                                d="M9.504 1.132a1 1 0 01.992 0l1.75 1a1 1 0 11-.992 1.736L10 3.152l-1.254.716a1 1 0 11-.992-1.736l1.75-1zM5.618 4.504a1 1 0 01-.372 1.364L5.016 6l.23.132a1 1 0 11-.992 1.736L4 7.723V8a1 1 0 01-2 0V6a.996.996 0 01.52-.878l1.734-.99a1 1 0 011.364.372zm8.764 0a1 1 0 011.364-.372l1.733.99A1.002 1.002 0 0118 6v2a1 1 0 11-2 0v-.277l-.254.145a1 1 0 11-.992-1.736l.23-.132-.23-.132a1 1 0 01-.372-1.364zm-7 4a1 1 0 011.364-.372L10 8.848l1.254-.716a1 1 0 11.992 1.736L11 10.58V12a1 1 0 11-2 0v-1.42l-1.246-.712a1 1 0 01-.372-1.364zM3 11a1 1 0 011 1v1.42l1.246.712a1 1 0 11-.992 1.736l-1.75-1A1 1 0 012 14v-2a1 1 0 011-1zm14 0a1 1 0 011 1v2a1 1 0 01-.504.868l-1.75 1a1 1 0 11-.992-1.736L16 13.42V12a1 1 0 011-1zm-9.618 5.504a1 1 0 011.364-.372l.254.145V16a1 1 0 112 0v.277l.254-.145a1 1 0 11.992 1.736l-1.735.992a.995.995 0 01-1.022 0l-1.735-.992a1 1 0 01-.372-1.364z"
                                clip-rule="evenodd"
                            /></svg
                        >
                        <span
                            class="inline w-full py-2 text-transparent bg-clip-text leading-12 bg-gradient-to-r from-indigo-400 to-purple-700"
                        >
                            Microsocial
                        </span>
                    </h1>
                    <p
                        class="px-0 mb-6 text-sm text-gray-300 md:text-xl lg:px-24"
                    >
                        Your Experimental Peer-to-Peer Social Platform
                    </p>
                </div>

                <div class="relative text-gray-200">
                    <div
                        class="grid gap-1 pb-10 uppercase sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 sm:gap-6"
                    >
                        <div
                            on:click={() => {
                                currentComponent = "Feed";
                            }}
                            class="flex items-center gap-5 px-2 py-2 mt-5 transition bg-indigo-900 rounded-lg shadow-xl cursor-pointer group bg-opacity-40 ring-2 ring-offset-2 ring-offset-indigo-800 ring-indigo-700 hover:bg-indigo-800 dark:hover:bg-indigo-900 hover:bg-opacity-100"
                        >
                            <svg
                                class="w-9"
                                fill="currentColor"
                                viewBox="0 0 20 20"
                                xmlns="http://www.w3.org/2000/svg"
                                ><path
                                    d="M7 3a1 1 0 000 2h6a1 1 0 100-2H7zM4 7a1 1 0 011-1h10a1 1 0 110 2H5a1 1 0 01-1-1zM2 11a2 2 0 012-2h12a2 2 0 012 2v4a2 2 0 01-2 2H4a2 2 0 01-2-2v-4z"
                                /></svg
                            >
                            <div>
                                <span>Live Feed</span>
                                <span class="block text-xs text-indigo-300"
                                    >Post with your friends</span
                                >
                            </div>
                            <div>
                                <i
                                    class="block transition transform -translate-x-1 opacity-0 fa fa-chevron-right group-hover:opacity-100 group-hover:translate-x-0"
                                />
                            </div>
                        </div>

                        <div
                            on:click={() => {
                                currentComponent = "Messages";
                            }}
                            class="flex items-center gap-5 px-2 py-2 mt-5 transition bg-indigo-900 rounded-lg shadow-xl cursor-pointer group bg-opacity-40 ring-2 ring-offset-2 ring-offset-indigo-800 ring-indigo-700 hover:bg-indigo-800 dark:hover:bg-indigo-900 hover:bg-opacity-100"
                        >
                            <svg
                                class="w-9"
                                fill="currentColor"
                                viewBox="0 0 20 20"
                                xmlns="http://www.w3.org/2000/svg"
                                ><path
                                    fill-rule="evenodd"
                                    d="M18 10c0 3.866-3.582 7-8 7a8.841 8.841 0 01-4.083-.98L2 17l1.338-3.123C2.493 12.767 2 11.434 2 10c0-3.866 3.582-7 8-7s8 3.134 8 7zM7 9H5v2h2V9zm8 0h-2v2h2V9zM9 9h2v2H9V9z"
                                    clip-rule="evenodd"
                                /></svg
                            >
                            <div>
                                <span>Messaging</span>
                                <span class="block text-xs text-indigo-300"
                                    >Chat in Private</span
                                >
                            </div>
                            <div>
                                <i
                                    class="block transition transform -translate-x-1 opacity-0 fa fa-chevron-right group-hover:opacity-100 group-hover:translate-x-0"
                                />
                            </div>
                        </div>

                        <div
                            on:click={() => {
                                currentComponent = "Profile";
                            }}
                            class="flex items-center gap-5 px-2 py-2 mt-5 transition bg-indigo-900 rounded-lg shadow-xl cursor-pointer group bg-opacity-40 ring-2 ring-offset-2 ring-offset-indigo-800 ring-indigo-700 hover:bg-indigo-800 dark:hover:bg-indigo-900 hover:bg-opacity-100"
                        >
                            <svg
                                class="w-9"
                                fill="currentColor"
                                viewBox="0 0 20 20"
                                xmlns="http://www.w3.org/2000/svg"
                                ><path
                                    fill-rule="evenodd"
                                    d="M10 2a1 1 0 00-1 1v1a1 1 0 002 0V3a1 1 0 00-1-1zM4 4h3a3 3 0 006 0h3a2 2 0 012 2v9a2 2 0 01-2 2H4a2 2 0 01-2-2V6a2 2 0 012-2zm2.5 7a1.5 1.5 0 100-3 1.5 1.5 0 000 3zm2.45 4a2.5 2.5 0 10-4.9 0h4.9zM12 9a1 1 0 100 2h3a1 1 0 100-2h-3zm-1 4a1 1 0 011-1h2a1 1 0 110 2h-2a1 1 0 01-1-1z"
                                    clip-rule="evenodd"
                                /></svg
                            >
                            <div>
                                <span>Profile</span>
                                <span class="block text-xs text-indigo-300"
                                    >Your posts and bio</span
                                >
                            </div>
                            <div>
                                <i
                                    class="block transition transform -translate-x-1 opacity-0 fa fa-chevron-right group-hover:opacity-100 group-hover:translate-x-0"
                                />
                            </div>
                        </div>

                        <div
                            on:click={() => {
                                currentComponent = "Friends";
                            }}
                            class="flex items-center gap-5 px-2 py-2 mt-5 transition bg-indigo-900 rounded-lg shadow-xl cursor-pointer group bg-opacity-40 ring-2 ring-offset-2 ring-offset-indigo-800 ring-indigo-700 hover:bg-indigo-800 dark:hover:bg-indigo-900 hover:bg-opacity-100"
                        >
                            <svg
                                class="w-9"
                                fill="currentColor"
                                viewBox="0 0 20 20"
                                xmlns="http://www.w3.org/2000/svg"
                                ><path
                                    d="M13 6a3 3 0 11-6 0 3 3 0 016 0zM18 8a2 2 0 11-4 0 2 2 0 014 0zM14 15a4 4 0 00-8 0v3h8v-3zM6 8a2 2 0 11-4 0 2 2 0 014 0zM16 18v-3a5.972 5.972 0 00-.75-2.906A3.005 3.005 0 0119 15v3h-3zM4.75 12.094A5.973 5.973 0 004 15v3H1v-3a3 3 0 013.75-2.906z"
                                /></svg
                            >
                            <div>
                                <span>Manage Friends</span>
                                <span class="block text-xs text-indigo-300"
                                    >Add/Remove Friends</span
                                >
                            </div>
                            <div>
                                <i
                                    class="block transition transform -translate-x-1 opacity-0 fa fa-chevron-right group-hover:opacity-100 group-hover:translate-x-0"
                                />
                            </div>
                        </div>
                    </div>
                </div>
                <div>
                    <div
                        class="flex flex-col p-4 mb-10 text-center text-gray-300 bg-indigo-900 rounded-lg shadow-xl cursor-pointer group bg-opacity-40 ring-2 ring-offset-2 ring-offset-indigo-800 ring-indigo-700"
                    >
                        Request a Connection to this Server Using the Link: <span
                            class="text-purple-400"
                            >{window.location.hostname}</span
                        >
                    </div>
                    <a
                        href="https://microsocial.xyz"
                        class="flex flex-col p-4 text-center bg-indigo-900 rounded-lg shadow-xl cursor-pointer group bg-opacity-40 ring-2 ring-offset-2 ring-offset-indigo-800 ring-indigo-700 hover:bg-indigo-800 dark:hover:bg-indigo-900 hover:bg-opacity-100 md:text-left md:flex-row md:items-center md:justify-between md:p-12"
                    >
                        <div class="text-2xl font-semibold">
                            <div class="text-gray-300">
                                Not Your Microsocial?
                            </div>
                            <div class="text-purple-500">
                                Find out how to get your own in seconds
                            </div>
                        </div>

                        <div class="mt-3 md:mt-0 md:ml-2">
                            <div
                                class="inline-block px-4 py-2 text-lg font-semibold text-white bg-purple-500 rounded-md"
                            >
                                Get Started
                            </div>
                        </div>
                    </a>
                    <div class="py-10 text-center text-gray-200">
                        <a
                            href="https://github.com/Gingerbreadfork/microsocial"
                        >
                            <svg
                                role="img"
                                viewBox="0 0 24 24"
                                xmlns="http://www.w3.org/2000/svg"
                                class="inline w-5 h-5 mb-1 mr-2 text-center text-white fill-current"
                            >
                                <title>GitHub icon</title>
                                <path
                                    d="M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12"
                                />
                            </svg>Microsocial is Free & Open Source Software
                        </a>
                    </div>
                </div>
            </div>
        </div>
    {:else if currentComponent == "Friends"}
        <ManageFriends />
    {:else if currentComponent == "Settings"}
        <Settings />
    {:else if currentComponent == "Feed"}
        <Feed />
    {:else if currentComponent == "Profile"}
        <Profile />
    {:else if currentComponent == "Messages"}
        <Messages />
    {/if}
</div>
