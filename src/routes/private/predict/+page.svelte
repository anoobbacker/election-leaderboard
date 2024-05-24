<!-- src/routes/private/predict/+page.svelte -->
<script lang="ts">
	import { enhance, applyAction } from '$app/forms';
	import type { SubmitFunction } from '@sveltejs/kit';
  import { invalidateAll } from '$app/navigation';
  import { onMount } from 'svelte';

  export let form
	export let data

	let { electionData, candidatePartyLookup, candidatePredictionLookup } = data
	$: ({ electionData, candidatePartyLookup, candidatePredictionLookup } = data)

  let electionPredictionForm: HTMLFormElement
	let loading = false
  let successMessage = '';
  let errorMessage = '';

  // Track if any field has changed
  let hasChanged = false;
  interface FormFields {
    candidate: string;
    voteShare: string;
    winningMargin: string;
  }

  interface FormData {
    [constituency: string]: FormFields;
  }

  let initialFormData: FormData = {};
  let formData: FormData = {};

  onMount(() => {
		electionData?.forEach(places => {
      formData[places.constituency] = {
        candidate: candidatePredictionLookup?.[places.constituency]?.candidate_name || '',
        voteShare: candidatePredictionLookup?.[places.constituency]?.vote_share || '',
        winningMargin: candidatePredictionLookup?.[places.constituency]?.winning_margin || ''
      };

      initialFormData[places.constituency] = { ...formData[places.constituency] };
    });
	});

  function handleSelectInputChange(event: Event) {
    const target = event.target as HTMLInputElement;
    const [constituency] = target.name.split('-');
    formData[constituency].candidate = target.value;

    // Check if any field has changed
    hasChanged = Object.keys(formData).some(
      key => JSON.stringify(formData[key]) !== JSON.stringify(initialFormData[key])
    );

    console.log(new Date().toLocaleString(), 'src/routes/predict/+page.svelte: handleInputChange(): ',  'Constituency:', constituency, 'Current:',formData[constituency].candidate, 'New:',target.value, 'hasChanged:',hasChanged);  // Log when action is called
  }

  function handleVoteShareChange(event: Event) {
    const target = event.target as HTMLInputElement;
    const [constituency] = target.name.split('-');
    formData[constituency].voteShare = target.value;

    // Check if any field has changed
    hasChanged = Object.keys(formData).some(
      key => JSON.stringify(formData[key]) !== JSON.stringify(initialFormData[key])
    );

    console.log(new Date().toLocaleString(), 'src/routes/predict/+page.svelte: handleInputChange(): ',  'Constituency:', constituency, 'Current:',formData[constituency].candidate, 'New:',target.value, 'hasChanged:',hasChanged);  // Log when action is called
  }

  function handleWinningMarginChange(event: Event) {
    const target = event.target as HTMLInputElement;
    const [constituency] = target.name.split('-');
    formData[constituency].winningMargin = target.value;

    // Check if any field has changed
    hasChanged = Object.keys(formData).some(
      key => JSON.stringify(formData[key]) !== JSON.stringify(initialFormData[key])
    );

    console.log(new Date().toLocaleString(), 'src/routes/predict/+page.svelte: handleInputChange(): ',  'Constituency:', constituency, 'Current:',formData[constituency].candidate, 'New:',target.value, 'hasChanged:',hasChanged);  // Log when action is called
  }

	const handleSubmit: SubmitFunction = () => {
		loading = true
    successMessage = '';
    errorMessage = '';
		return async ({result}) => {
      if (result.type === 'success') {
        successMessage = 'Predictions saved successfully!';
        invalidateAll();
      } else {
        errorMessage = 'Failed to save predictions';
      }
      applyAction(result);
      loading = false
    }
	}
</script>

{#if electionData && electionData.length > 0}
<div class="border-b border-gray-900/10 pb-12">
	<form
		class="space-y-6"
		method="post"
		action="?/update"
		use:enhance={handleSubmit}
		bind:this={electionPredictionForm}
	>
    <div class="max-w-full mx-auto p-6 bg-white rounded-lg shadow-md">
      <div class="flex flex-wrap gap-8 p-2 place-content-center">
        {#each electionData as places, i}
        <!-- Constituency -->
        <div class="flex bg-white shadow rounded-lg p-4 w-fit place-content-center">
          <div class="flex flex-col space-y-3">
            <p class="px-6 py-4 font-bold text-center">{places.id}. {places.constituency}</p>
            
            <div class="flex flex-row items-center space-x-6 space-y-3">
              <!-- Prediction -->
              <div class="flex flex-col space-y-3">
                <!-- Candidate dropdown -->
                <label id="listbox-label" for="{places.constituency}-candidate" class="block text-sm font-medium leading-6 text-gray-900">Candidate</label>
                <select class="relative z-10 mt-1 max-h-56 w-auto overflow-auto rounded-md py-1 text-base shadow-lg ring-1 ring-gray-300 ring-opacity-5 focus:outline-none sm:text-sm" name="{places.constituency}-candidate" id="{places.constituency}-candidate" aria-expanded="true" aria-labelledby="listbox-label" on:change={handleSelectInputChange}>
                  <option class="relative w-full text-gray-900 cursor-default select-none py-2 pl-3 pr-4" value="{places.ldf_candidate}" selected={places.ldf_candidate === candidatePredictionLookup?.[places.constituency]?.candidate_name}>
                      <span class="font-normal ml-3 block truncate">{places.ldf_candidate} - {candidatePartyLookup?.[places.ldf_candidate].party} </span>
                  </option>
                  <option class="relative w-full text-gray-900 cursor-default select-none py-2 pl-3 pr-4" value="{places.udf_candidate}" selected={places.udf_candidate === candidatePredictionLookup?.[places.constituency]?.candidate_name}>
                    <span class="font-normal ml-3 block truncate">{places.udf_candidate} - {candidatePartyLookup?.[places.udf_candidate].party}</span>
                  </option>
                  <option class="relative w-full text-gray-900 cursor-default select-none py-2 pl-3 pr-4" value="{places.nda_candidate}" selected={places.nda_candidate === candidatePredictionLookup?.[places.constituency]?.candidate_name}>
                    <span class="font-normal ml-3 block truncate">{places.nda_candidate} - {candidatePartyLookup?.[places.nda_candidate].party}</span>
                  </option>
                  <option class="relative w-full text-gray-900 cursor-default select-none py-2 pl-3 pr-4" value="{places.other1_candidate}">
                    <span class="font-normal ml-3 block truncate">{places.other1_candidate}</span>
                  </option>
                </select>

                <!-- Candidates Photos -->
                <div class="flex flex-row space-x-3">
                  <img class="inline-block h-12 rounded-full ring-2 ring-white" src="{candidatePartyLookup?.[places.ldf_candidate].photo_url}" alt="{places.ldf_candidate}" />
                  <img class="inline-block h-12 rounded-full ring-2 ring-white" src="{candidatePartyLookup?.[places.udf_candidate].photo_url}" alt="{places.udf_candidate}" />
                  <img class="inline-block h-12 rounded-full ring-2 ring-white" src="{candidatePartyLookup?.[places.nda_candidate].photo_url}" alt="{places.nda_candidate}" />
                </div>

                <!-- Vote share input -->
                <label for="{places.constituency}-winnervoteshare" class="block leading-6">
                  <p class="text-sm font-medium  text-gray-900">Vote share %</p>
                  <!-- Tooltip content -->
                  <p class="bottom-full mb-2 text-xs text-gray-400">Percentage of total votes they receive compared to the overall votes casted in the election.</p>
                </label>
                <input type="number" name="{places.constituency}-winnervoteshare" id="{places.constituency}-winnervoteshare" class="block w-1/2 rounded-md border-0 py-1.5 pl-2 pr-2 text-gray-900 ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6" placeholder={candidatePredictionLookup?.[places.constituency]?.vote_share ? candidatePredictionLookup[places.constituency]?.vote_share : "40"} min="1" max="100" on:input={handleVoteShareChange}>                            

                <!-- Winning votes input -->
                <label for="{places.constituency}-winningvotes" class="block leading-6">                  
                  <p class="text-sm font-medium  text-gray-900">Winning votes</p>
                  <!-- Tooltip content -->
                  <p class="bottom-full mb-2 text-xs text-gray-400">Difference in the number of votes winner receive compared to the second-place candidate.</p>
                </label>
                <input type="number" name="{places.constituency}-winningvotes" id="{places.constituency}-winningvotes" class="block w-1/2 rounded-md border-0 py-1.5 pl-2 pr-2 text-gray-900 ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6" placeholder={candidatePredictionLookup?.[places.constituency]?.winning_margin ? candidatePredictionLookup[places.constituency]?.winning_margin : "1000"} min="1" max="2000000" on:input={handleWinningMarginChange}>
              </div>
            </div>
          </div>
        </div>
        {/each}
      </div>
    </div>

    <div>
			<input
				type="submit"
				class="{loading || !hasChanged ? 'rounded-md bg-gray-500 m-6 px-3.5 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600' : 'rounded-md bg-indigo-600 m-6 px-3.5 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600'}"
				value={loading ? 'Saving...' : 'Save'}
				disabled={loading || !hasChanged}
			/>
      {#if !hasChanged}<p class="text-xs text-gray-600 px-6">Changing a prediction enables the save button.</p>{/if}
      {#if form?.success}<p class="text-green-600 px-6">{successMessage}</p>{/if}
			{#if form?.error}<p class="text-red-600 px-6">{errorMessage}. Constituency: {form?.constituency}</p>{/if}
		</div>
	</form>  
</div>
{:else}
<div class="bg-white py-24 sm:py-32">
  <p>No data available.</p>
</div>
{/if}