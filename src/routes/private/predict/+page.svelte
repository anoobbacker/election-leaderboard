<!-- src/routes/account/+page.svelte -->
<script lang="ts">
	import { enhance } from '$app/forms';
	import type { SubmitFunction } from '@sveltejs/kit';

	export let data

	let { electionData, candidatePartyLookup, candidatePredictionLookup } = data
	$: ({ electionData, candidatePartyLookup, candidatePredictionLookup } = data)

  let electionPredictionForm: HTMLFormElement
	let loading = false

	const handleSubmit: SubmitFunction = () => {
		loading = true
		return async () => {
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
      <div class="overflow-auto">
      <table class="w-full text-sm text-left text-gray-500">
          <thead class="text-xs text-gray-700 uppercase bg-gray-50">
              <tr>
                  <th scope="col" class="px-2 py-3">#</th>
                  <th scope="col" class="px-2 py-3">Constituency</th>
                  <th scope="col" class="px-2 py-3">Candidate</th>
                  <th scope="col" class="px-2 py-3">Vote share (%)</th>
                  <th scope="col" class="px-2 py-3">Winning vote margin</th>
              </tr>
          </thead>
          <tbody>
            {#each electionData as places, i}
              <tr class="border-b">
                <td class="px-2 py-3">{places.id}</td>
                <td class="px-2 py-3 w-min">{places.constituency}</td>
                <td class="px-2 py-3 w-full">                
                  <select class="relative z-10 mt-1 max-h-56 w-full overflow-auto rounded-md py-1 text-base shadow-lg ring-1 ring-gray-300 ring-opacity-5 focus:outline-none sm:text-sm" name="{places.constituency}-candidate" id="{places.constituency}-candidate">
                    <option class="relative w-full text-gray-900 cursor-default select-none py-2 pl-3 pr-4" value="{places.ldf_candidate}" selected={places.ldf_candidate === candidatePredictionLookup?.[places.constituency]?.candidate_name}>
                        <span class="font-normal ml-3 block truncate">{places.ldf_candidate} - {candidatePartyLookup?.[places.ldf_candidate]} </span>
                    </option>
                    <option class="relative w-full text-gray-900 cursor-default select-none py-2 pl-3 pr-4" value="{places.udf_candidate}" selected={places.udf_candidate === candidatePredictionLookup?.[places.constituency]?.candidate_name}>
                      <span class="font-normal ml-3 block truncate">{places.udf_candidate} - {candidatePartyLookup?.[places.udf_candidate]}</span>
                    </option>
                    <option class="relative w-full text-gray-900 cursor-default select-none py-2 pl-3 pr-4" value="{places.nda_candidate}" selected={places.nda_candidate === candidatePredictionLookup?.[places.constituency]?.candidate_name}>
                      <span class="font-normal ml-3 block truncate">{places.nda_candidate} - {candidatePartyLookup?.[places.nda_candidate]}</span>
                    </option>
                    <option class="relative w-full text-gray-900 cursor-default select-none py-2 pl-3 pr-4" value="{places.other1_candidate}">
                      <span class="font-normal ml-3 block truncate">{places.other1_candidate}</span>
                    </option>
                  </select>
                </td>
                <td class="px-6 py-4">
                  <input type="number" name="{places.constituency}-winnervoteshare" id="{places.constituency}-winnervoteshare" class="block w-min rounded-md border-0 py-1.5 pl-2 pr-2 text-gray-900 ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6" placeholder={candidatePredictionLookup?.[places.constituency]?.vote_share ? candidatePredictionLookup[places.constituency]?.vote_share : "60"} min="1" max="100">
                </td>

                <td class="px-6 py-4">
                  <input type="number" name="{places.constituency}-winningvotes" id="{places.constituency}-winningvotes" class="block w-min rounded-md border-0 py-1.5 pl-2 pr-2 text-gray-900 ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6" placeholder={candidatePredictionLookup?.[places.constituency]?.winning_margin ? candidatePredictionLookup[places.constituency]?.winning_margin : "1000"} min="1" max="200000">
                </td>
              </tr>
            {/each}
          </tbody>
        </table>
      </div>
    </div>

    <div>
			<input
				type="submit"
				class="rounded-md bg-indigo-600 m-6 px-3.5 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
				value={loading ? 'Loading...' : 'Update'}
				disabled={loading}
			/>
		</div>
	</form>  
</div>
{:else}
<div class="bg-white py-24 sm:py-32">
  <p>No data available.</p>
</div>
{/if}