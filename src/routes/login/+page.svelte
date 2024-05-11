<!-- src/routes/+page.svelte -->
<script lang="ts">
	import { enhance } from '$app/forms';
	import type { ActionResult, SubmitFunction } from '@sveltejs/kit';
	import { Auth } from '@supabase/auth-ui-svelte'
	import { ThemeSupa } from '@supabase/auth-ui-shared'
	import { Result } from 'postcss';

	export let data	

	let loginForm: HTMLFormElement
	let loading = false
	let email: string = ''
	let statusMessage = ''
	let isLoginButtonDisabled = false;

	// Reactively update the disabled state based on statusMessage
  $: isButtonDisabled = statusMessage.includes('Error');

	const handleSubmit: SubmitFunction = () => {
		loading = true
		return async ( {result} ) => {
			if ( result.status ) {
				statusMessage = result.message;
			} else {
				statusMessage = `Error: ${result.message || 'Unknown error'}`;
			}
			loading = false
		}
	}
</script>

<!-- <div class="row flex-center flex">
	<div class="col-6 form-widget">
		<Auth
			supabaseClient={data.supabase}
			view="magic_link"
			redirectTo={`${data.url}/auth/callback`}
			showLinks={false}
			appearance={{ theme: ThemeSupa, style: { input: 'color: #fff' } }}
		/>
	</div>
</div> -->

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
			<input type="hidden" id="redirectTo" name="redirectTo" value="{`${data.url}/auth/callback`}">
      <div>
        <label for="email" class="block text-sm font-medium leading-6 text-gray-900">Email address</label>
        <div class="mt-2">
          <input id="email" name="email" type="email" autocomplete="email" required class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6" value={email}>
        </div>
      </div>

      <div>
        <button type="submit" class="flex w-full justify-center rounded-md bg-indigo-600 px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600" disabled={isButtonDisabled}>Send Magic Link</button>
				{#if statusMessage}
				<p class="text-blue-600">{statusMessage}</p>
				{/if}
      </div>
    </form>
  </div>
</div>