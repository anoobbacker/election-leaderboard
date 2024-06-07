<!-- src/routes/private/+layout.svelte -->
<script lang="ts">
  import { page } from '$app/stores';
	import type { LayoutData } from './$types';

	export let data: LayoutData;

	let { avatar_url, username } = data
	$: ({ avatar_url, username } = data)

  export let currentPath: string = '';
  $: currentPath = $page.url.pathname;
  
  console.debug(new Date().toLocaleString(), 'src/routes/private/+layout.svelte:', currentPath, $page.url.pathname);  // Log when action is called
  let isDropdownOpen = false;  // State to control the visibility of the mobile dropdown
  let isMenuOpen = false;  // State to control the visibility of the mobile menu
  
  function toggleDropdown() {
    isDropdownOpen = !isDropdownOpen;
  }

  function toggleMenu() {
    isMenuOpen = !isMenuOpen;
  }

</script>

<nav class="bg-gray-800 z-50">
  <div class="mx-auto max-w-7xl px-2 sm:px-6 lg:px-8">
    <div class="relative flex h-16 items-center justify-between">
      <div class="absolute inset-y-0 left-0 flex items-center sm:hidden">
        <!-- Mobile menu button-->
        <button type="button" class="relative inline-flex items-center justify-center rounded-md p-2 text-gray-400 hover:bg-gray-700 hover:text-white focus:outline-none focus:ring-2 focus:ring-inset focus:ring-white" aria-controls="mobile-menu" aria-expanded="{!isMenuOpen}" on:click={toggleMenu}>
          <span class="absolute -inset-0.5"></span>
          <span class="sr-only">Open main menu</span>
          <!--
            Icon when menu is closed.

            Menu open: "hidden", Menu closed: "block"
          -->
          <svg class="{ (isMenuOpen === false)? 'block' : 'hidden'} h-6 w-6" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" aria-hidden="true" >
            <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5" />
          </svg>
          <!--
            Icon when menu is open.

            Menu open: "block", Menu closed: "hidden"
          -->
          <svg class="{ (isMenuOpen === true)? 'block' : 'hidden'} h-6 w-6" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" aria-hidden="true">
            <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>      
      <div class="flex flex-1 items-center justify-center sm:items-stretch sm:justify-start">
        <div class="flex flex-shrink-0 items-center">
          <img class="h-8 w-auto" src="/images/logo/kotas.webp" alt="Kotas">
        </div>
				<div class="hidden sm:ml-6 sm:block">
          <div class="flex space-x-4">
             <!-- Current: "bg-gray-900 text-white", Default: "text-gray-300 hover:bg-gray-700 hover:text-white" -->
            <a 
              href="/private" 
              class="{currentPath === '/private' ? 'bg-gray-900 text-white rounded-md px-3 py-2 text-sm font-medium': 'text-gray-300 hover:bg-gray-700 hover:text-white rounded-md px-3 py-2 text-sm font-medium'}"
              aria-current={currentPath === '/private' ? 'page' : false}>
              Home
            </a>
            <a href="/private/candidate" class="{currentPath === '/private/candidate' ? 'bg-gray-900 text-white rounded-md px-3 py-2 text-sm font-medium': 'text-gray-300 hover:bg-gray-700 hover:text-white rounded-md px-3 py-2 text-sm font-medium'}"
            aria-current={currentPath === '/private/candidate' ? 'page' : false}>Candidate</a>
            <a href="/private/predict" class="{currentPath === '/private/predict' ? 'bg-gray-900 text-white rounded-md px-3 py-2 text-sm font-medium': 'text-gray-300 hover:bg-gray-700 hover:text-white rounded-md px-3 py-2 text-sm font-medium'}"
            aria-current={currentPath === '/private/predict' ? 'page' : false}>Predict</a>
            <a href="/private/leaderboard" class="{currentPath === '/private/leaderboard' ? 'bg-gray-900 text-white rounded-md px-3 py-2 text-sm font-medium': 'text-gray-300 hover:bg-gray-700 hover:text-white rounded-md px-3 py-2 text-sm font-medium'}"
            aria-current={currentPath === '/private/leaderboard' ? 'page' : false}>Leaderboard</a>
            <a href="/private/results" class="{currentPath === '/private/results' ? 'bg-gray-900 text-white rounded-md px-3 py-2 text-sm font-medium': 'text-gray-300 hover:bg-gray-700 hover:text-white rounded-md px-3 py-2 text-sm font-medium'}"
            aria-current={currentPath === '/private/results' ? 'page' : false}>Results</a>
          </div>
        </div>
      </div>
      <div class="absolute inset-y-0 right-0 flex items-center pr-2 sm:static sm:inset-auto sm:ml-6 sm:pr-0">
        <!-- Profile dropdown -->
        <div class="relative ml-3">
          <div>
            <button type="button" class="relative flex rounded-full bg-gray-800 text-sm focus:outline-none focus:ring-2 focus:ring-white focus:ring-offset-2 focus:ring-offset-gray-800" id="user-menu-button" aria-expanded="{isDropdownOpen}" aria-haspopup="true" on:click={toggleDropdown}>
              <span class="absolute -inset-1.5"></span>
              <span class="sr-only">Open user menu</span>
              <img class="h-8 w-8 mr-4 rounded-full" src="{data.avatar_url}" alt="">
            </button>
          </div>
          <div class="absolute right-0 z-10 mt-2 w-48 origin-top-right rounded-md bg-white py-1 shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none" role="menu" aria-orientation="vertical" aria-labelledby="user-menu-button" tabindex="-1" class:hidden={!isDropdownOpen}>
            <a href="/private/account" class="block px-4 py-2 text-sm text-gray-700" role="menuitem" tabindex="-1" id="user-menu-item-0">Your Profile</a>
            <a href="/private/account" class="block px-4 py-2 text-sm text-gray-700" role="menuitem" tabindex="-1" id="user-menu-item-1">Sign out</a>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Mobile menu, show/hide based on menu state. -->
  <div class="sm:hidden" id="mobile-menu" class:!block={isMenuOpen} class:hidden={!isMenuOpen}>
    <div class="space-y-1 px-2 pb-3 pt-2">
      <!-- Current: "bg-gray-900 text-white", Default: "text-gray-300 hover:bg-gray-700 hover:text-white" -->
      <a href="/private" class="{currentPath === '/private' ? 'bg-gray-900 text-white block rounded-md px-3 py-2 text-base font-medium' : 'text-gray-300 hover:bg-gray-700 hover:text-white block rounded-md px-3 py-2 text-base font-medium'}" aria-current={currentPath === '/private' ? 'page' : false}>Home</a>
      <a href="/private/candidate" class="{currentPath === '/private/candidate' ? 'bg-gray-900 text-white block rounded-md px-3 py-2 text-base font-medium' : 'text-gray-300 hover:bg-gray-700 hover:text-white block rounded-md px-3 py-2 text-base font-medium'}" aria-current={currentPath === '/private/candidate' ? 'page' : false}>Candidate</a>
      <a href="/private/predict" class="{currentPath === '/private/predict' ? 'bg-gray-900 text-white block rounded-md px-3 py-2 text-base font-medium' : 'text-gray-300 hover:bg-gray-700 hover:text-white block rounded-md px-3 py-2 text-base font-medium'}" aria-current={currentPath === '/private/predict' ? 'page' : false}>Predict</a>
      <a href="/private/leaderboard" class="{currentPath === '/private/leaderboard' ? 'bg-gray-900 text-white block rounded-md px-3 py-2 text-base font-medium' : 'text-gray-300 hover:bg-gray-700 hover:text-white block rounded-md px-3 py-2 text-base font-medium'}" aria-current={currentPath === '/private/leaderboard' ? 'page' : false}>Leaderboard</a>
      <a href="/private/results" class="{currentPath === '/private/results' ? 'bg-gray-900 text-white block rounded-md px-3 py-2 text-base font-medium' : 'text-gray-300 hover:bg-gray-700 hover:text-white block rounded-md px-3 py-2 text-base font-medium'}" aria-current={currentPath === '/private/results' ? 'page' : false}>Results</a>
    </div>
  </div>
</nav>


<div class="bg-white">
  <div class="mx-auto max-w-7xl">
      <slot />    
  </div>
</div>