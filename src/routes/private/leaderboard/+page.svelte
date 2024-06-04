<!-- src/routes/private/leaderboard/+page.svelte -->
<script lang="ts">
	import { enhance, applyAction } from '$app/forms';
	import type { SubmitFunction } from '@sveltejs/kit';
	import { invalidate } from '$app/navigation';

	export let data;
	export let form;

  let submitForm: HTMLFormElement

	let { participants, partylookup, resultsReady, avatar_url, username } = data;
	$: ({ participants, partylookup, resultsReady, avatar_url, username } = data);
	let loading = false;
	// Ensure participants is always an array
	participants = participants || [];

	let constituencies: string | any[] = [];
  let calculatedParticipants: string | any[] = [];  

	// Sort participants alphabetically by username
	participants.sort((a, b) => a.username.localeCompare(b.username));

	function formatDate(dateString: string) {
		const date = new Date(dateString);
		const options: Intl.DateTimeFormatOptions = {
			weekday: 'short',
			year: 'numeric',
			month: 'long',
			day: 'numeric'
		};
		return date.toLocaleDateString(undefined, options);
	}

	const handleViewPredictions: SubmitFunction = () => {
		loading = true;
		return async ({ result }) => {
      console.debug(new Date().toLocaleString(), 'src/routes/private/leaderboard/+page.svelte: handleViewPredictions(): Called');  // Log when action is called
			if (result.type === 'success') {
				constituencies = result.data?.constituencies || [];
        calculatedParticipants = result.data?.participants || [];
        console.debug(new Date().toLocaleString(), 'src/routes/private/leaderboard/+page.svelte: handleViewPredictions(): Results');  // Log when action is called
				invalidate(''); // Invalidate the current page
			}
      applyAction(result);
			loading = false;
      console.debug(new Date().toLocaleString(), 'src/routes/private/leaderboard/+page.svelte: handleViewPredictions(): Return');  // Log when action is called
		};
	};
</script>

<div class="relative isolate max-w-7xl px-6 pt-4 lg:px-8">
	<div class="absolute inset-x-0 transform-gpu overflow-hidden blur-3xl" aria-hidden="true">
		<div
			class="relative left-[calc(50%-11rem)] aspect-[1155/678] w-[36.125rem] -translate-x-1/2 rotate-[30deg] bg-gradient-to-tr from-[#ff80b5] to-[#9089fc] opacity-30 sm:left-[calc(50%-30rem)] sm:w-[72.1875rem]"
			style="clip-path: polygon(74.1% 44.1%, 100% 61.6%, 97.5% 26.9%, 85.5% 0.1%, 80.7% 2%, 72.5% 32.5%, 60.2% 62.4%, 52.4% 68.1%, 47.5% 58.3%, 45.2% 34.5%, 27.5% 76.7%, 0.1% 64.9%, 17.9% 100%, 27.6% 76.8%, 76.1% 97.7%, 74.1% 44.1%)"
		></div>
	</div>
	<div class="mx-auto max-w-2xl py-32 sm:py-12 lg:py-20">
		<div class="hidden sm:mb-8 sm:flex sm:justify-center">
			{#if resultsReady === false}
      <div class="relative rounded-full px-3 py-1 text-sm leading-6 text-gray-600 ring-1 ring-gray-900/10 hover:ring-gray-900/20">
        Winners will be announced on 4<sup>th</sup> Jun.
      </div>
			{:else}
			<div class="relative rounded-full px-3 py-1 text-sm leading-6 text-gray-600 ring-1 ring-gray-900/10 hover:ring-gray-900/20">
        🎉 LIVE: Counting in progress. The scores are updated at 12PM 4Jun!
        <!-- 🎉 The scores got updated! -->
      </div>
			{/if}
		</div>
		<div class="text-center">
			<img class="inline-block h-16 w-16 rounded-full ring-2 ring-white" src={avatar_url} alt="" />
			<h1 class="text-4xl font-bold tracking-tight text-gray-900 sm:text-6xl">Hello {username}!</h1>
			<p class="mt-6 text-lg leading-8 text-gray-600">
        {#if resultsReady === false}
				🕒 Stay tuned, scores will be updated after announcing election results!
        {:else}
        <!-- 🎉 The wait is over, the election results are in – <i>check your scores now</i>! -->
        🚧 The election counting in progress – <i>check your scores now</i>!
        {/if}        
			</p>
			<div class="mt-10 flex items-center justify-center gap-x-6">
        {#if resultsReady !== false}
				<form class="z-40" method="post" action="?/scorecard" use:enhance={handleViewPredictions} bind:this={submitForm}>
					<div>
						<input type="submit" class="rounded-md bg-indigo-600 px-3.5 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600" disabled={loading} value={loading ? 'Loading...' : 'Show scores'} />
					</div>
				</form>
        <a href="/private/predict" class="z-40 text-sm font-semibold leading-6 text-gray-900"
					>View your prediction <span aria-hidden="true">→</span></a
				>
        {:else}
        <a href="/private/predict" class="z-40 rounded-md bg-indigo-600 px-3.5 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
        >Submit your prediction <span aria-hidden="true">→</span></a>
        {/if}
			</div>
      <!-- {#if form?.success}<p class="text-green-600 px-6">Successfully saved!</p>{/if} -->
      {#if form?.error}<p class="text-xs text-red-600 px-6">{form.error}</p>{/if}
		</div>
	</div>
	<div
		class="absolute inset-x-0 top-[calc(100%-13rem)] -z-10 transform-gpu overflow-hidden blur-3xl sm:top-[calc(100%-30rem)]"
		aria-hidden="true"
	>
		<div
			class="relative left-[calc(50%+3rem)] aspect-[1155/678] w-[36.125rem] -translate-x-1/2 bg-gradient-to-tr from-[#ff80b5] to-[#9089fc] opacity-30 sm:left-[calc(50%+36rem)] sm:w-[72.1875rem]"
			style="clip-path: polygon(74.1% 44.1%, 100% 61.6%, 97.5% 26.9%, 85.5% 0.1%, 80.7% 2%, 72.5% 32.5%, 60.2% 62.4%, 52.4% 68.1%, 47.5% 58.3%, 45.2% 34.5%, 27.5% 76.7%, 0.1% 64.9%, 17.9% 100%, 27.6% 76.8%, 76.1% 97.7%, 74.1% 44.1%)"
		></div>
	</div>

	{#if calculatedParticipants.length > 0}
    <!-- Final score & winner -->
    <div class="flex flex-wrap place-content-center min-w-full gap-8 p-2">
      <ul role="list" class="divide-y divide-gray-100 rounded-lg p-4 shadow-md">
        {#each calculatedParticipants as participant, i}
          <li class="flex justify-between gap-x-6 py-5">
            <div class="flex min-w-0 gap-x-4">
              <img
                class="h-12 w-12 flex-none rounded-full bg-gray-50"
                src={participant.avatar_url}
                alt={participant.username}
              />
              <div class="min-w-0 flex-auto">
                <p class="text-sm font-semibold leading-6 text-gray-900">{participant.username}</p>
                <p class="mt-1 truncate text-xs leading-5 text-gray-500">
                  #{i+1}
                  {#if (i === 0)}
                  <span class="inline-flex items-center rounded-md bg-blue-50 px-2 py-1 text-xs font-medium text-blue-700 ring-1 ring-inset ring-blue-700/10">🏆</span>
                  {/if}
                </p>
              </div>
            </div>
            <div class="shrink-0 sm:flex sm:flex-col sm:items-end">
              <p class="text-sm font-semibold leading-6 text-indigo-600">{participant.total_points}</p>
              <p class="mt-1 text-xs leading-5 text-gray-500">Points</p>
            </div>
          </li>
        {/each}
      </ul>
    </div>
  {:else if (participants.length > 0) && (resultsReady === false)}
    <!-- Submission -->
    <div class="flex flex-wrap place-content-center gap-8 p-2">
      <ul role="list" class="divide-y divide-gray-100 rounded-lg p-4 shadow-md">
        {#each participants as participant}
          <li class="flex justify-between gap-x-6 py-5">
            <div class="flex min-w-0 gap-x-4">
              <img
                class="h-12 w-12 flex-none rounded-full bg-gray-50"
                src={participant.avatar_url}
                alt={participant.username}
              />
              <div class="min-w-0 flex-auto">
                <p class="text-sm font-semibold leading-6 text-gray-900">{participant.username}</p>
                <p class="shrink-0 sm:flex sm:flex-col sm:items-end mt-1 text-xs leading-5">✔️Submitted</p>
              </div>
            </div>
            <div class="hidden shrink-0 sm:flex sm:flex-col sm:items-end">
              <p class="text-sm font-semibold leading-6 text-indigo-600">🕒 Stay tuned...</p>
              <p class="mt-1 text-xs leading-5 text-gray-500">
                On <time datetime={participant.submitted_at}
                  >{formatDate(participant.submitted_at)}</time
                >
              </p>
            </div>
          </li>
        {/each}
      </ul>
    </div>  
  {/if}

  {#if constituencies.length > 0}
  <div class="max-w-full mx-auto p-6">
    <h1 class="p-8 text-2xl font-bold tracking-tight text-gray-900 sm:text-3xl">Detailed scorecard</h1>
    <div class="flex flex-wrap gap-8 p-2">
        {#each constituencies as constituency}
          <!-- Constituency -->
          <div class="flex shadow rounded-lg p-4 max-w-fill place-content-center">
            <div class="flex flex-col space-y-3">
              <p class="px-6 py-4 font-bold text-center">{constituency.constituency_name}</p>
              <!-- Winning candidate -->
              <div class="flex flex-row items-center p-4 space-x-3 space-y-3">
                <!-- Winner Details -->
                <div class="flex flex-row place-content-center gap-2">
                  <!-- Canidate image -->
                  <img class="inline-block h-32 rounded-full ring-2 ring-white" src="{partylookup?.[constituency.elected_member].photo_url}" alt="{constituency.elected_member}">                  
                  <!-- Details  -->
                  <div class="flex flex-col gap-2">
                    <div class="text-left">
                      <p class="font-semibold text-gray-900">{constituency.elected_member}</p>
                      <img class="inline-block h-6 rounded-full ring-2 ring-white" src="/images/party/{constituency.elected_party}.webp" alt="{constituency.elected_party}">
                    </div>
                    <div class="text-left">
                      <p class="font-semibold text-gray-600">Party:</p>
                      <p class="text-gray-600">{constituency.elected_party}</p>                      
                    </div>
                    <div class="text-left">
                      <p class="font-semibold text-gray-600">Vote Share:</p>
                      <p class="text-gray-600">{constituency.vote_share_percentage}%</p>                      
                    </div>
                    
                    <div class="text-left">
                      <p class="font-semibold text-gray-600">Winning votes:</p>
                      <p class="text-gray-600">{constituency.margin}</p>
                    </div>
                  </div>
                </div>            
              </div>
              <!-- Prediction by participants -->
              <div class="flex flex-col flex-wrap p-4 space-y-3">                
                <div class="flex flex-row items-baseline gap-8">
                  <!-- Correct predictions -->
                  <div class="flex flex-col gap-2 items-left">
                    <p class="font-semibold text-left">✅Correct</p>
                    {#each constituency.predictions as prediction}
                    {#if prediction.candidate_name === constituency.elected_member}
                    <div class="flex flex-row gap-2 items-center">
                      <img class="h-8 w-8 rounded-full bg-gray-50" src="{prediction.avatar_url}" alt="{prediction.username}" />
                      <p class="text-sm font-semibold leading-6 text-gray-900">{prediction.username}</p>
                      <p class="text-xs leading-5 text-gray-500">{prediction.points ? prediction.points : '-'}</p>
                      <p class="text-xs leading-5 text-gray-500">{prediction.vote_share ? `${prediction.vote_share}%` : '-'}</p>
                      <p class="text-xs leading-5 text-gray-500">{prediction.winning_margin ? prediction.winning_margin : '-'}</p>
                    </div>
                    {/if}
                    {/each}
                  </div>
                  <!-- Wrong predictions -->
                  <div class="flex flex-col gap-2 items-left">
                    <p class="font-semibold text-left">❌ Wrong</p>
                    {#each constituency.predictions as prediction}
                    {#if prediction.candidate_name !== constituency.elected_member}
                    <div class="flex flex-row gap-2 items-center">
                      <img class="h-8 w-8 rounded-full bg-gray-50" src="{prediction.avatar_url}" alt="{prediction.username}" />
                      <p class="text-sm font-semibold leading-6 text-gray-900">{prediction.username}</p>
                      <!-- <p class="text-xs leading-5 text-gray-500">{prediction.vote_share}%</p> -->
                      <!-- <p class="text-xs leading-5 text-gray-500">{prediction.winning_margin}</p> -->
                    </div>
                    {/if}
                    {/each}
                  </div>
                </div>                
              </div>
            </div>            
          </div>
        {/each}
    </div>
  </div>
  {/if}
</div>
