<!-- src/routes/+page.svelte -->
<script lang="ts">
	import { enhance, applyAction} from '$app/forms';
	import { invalidateAll, goto } from '$app/navigation';
	import type { SubmitFunction } from '@sveltejs/kit';

	export let form

	let loginForm: HTMLFormElement
	let loading = false
	let email: string = ''

	const handleSubmit: SubmitFunction = () => {
		loading = true
		return async ( {result} ) => {
			if ( result.type === 'success' ) {
				// rerun all `load` functions, following the successful update
				await invalidateAll();
			}
			applyAction(result);
			loading = false
		}
	}
</script>

<div class="flex min-h-full flex-col justify-center px-6 py-12 lg:px-8">
  <div class="sm:mx-auto sm:w-full sm:max-w-sm">
    <img class="mx-auto h-10 w-auto" src="https://tailwindui.com/img/logos/mark.svg?color=indigo&shade=600" alt="Kotas">
		<h2 class="mt-10 text-center font-semibold text-indigo-600">Kerala Election 2024</h2>
    <h2 class="mt-10 text-center text-2xl font-bold leading-9 tracking-tight text-gray-900">Sign in to your account</h2>
  </div>

  <div class="mt-10 sm:mx-auto sm:w-full sm:max-w-sm">
    <form 
			class="space-y-6" 
			action="?/login"
			use:enhance={handleSubmit}
			method="POST"
			bind:this={loginForm}>
      <div>
        <label for="email" class="block text-sm font-medium leading-6 text-gray-900">Email address</label>
        <div class="mt-2">
          <input id="email" name="email" type="email" autocomplete="email" required class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6" value={email}>
        </div>
      </div>

			<div>
        <div class="flex items-center justify-between">
          <label for="password" class="block text-sm font-medium leading-6 text-gray-900">Password</label>
        </div>
        <div class="mt-2">
          <input id="password" name="password" type="password" autocomplete="current-password" required class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6">
        </div>
      </div>

      <div>
        <input type="submit" class="flex w-full justify-center rounded-md bg-indigo-600 px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600" value={loading ? 'Signing in...' : 'Sign in'} />
				{#if form?.missing}<p class="text-red-600">The email and password field is required!</p>{/if}
				{#if form?.incorrect}<p class="text-red-600">Error: Invalid credentials!</p>{/if}
      </div>
    </form>
  </div>
</div>