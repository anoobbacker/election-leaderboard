<!-- src/routes/account/+page.svelte -->
<script lang="ts">
	import { enhance } from '$app/forms';
	import type { SubmitFunction } from '@sveltejs/kit';

	export let data

	let { session, supabase, electionData, candidatePartyLookup } = data
	$: ({ session, supabase, electionData, candidatePartyLookup } = data)

  let electionPrediction: HTMLFormElement
	let loading = false

	const handleSubmit: SubmitFunction = () => {
		loading = true
		return async () => {
			loading = false
		}
	}

	const handleSignOut: SubmitFunction = () => {
		loading = true
		return async ({ update }) => {
			loading = false
			update()
		}
	}
</script>

{#if electionData}
<div class="max-w-full mx-auto p-6 bg-white rounded-lg shadow-md">
  <div class="overflow-auto">
    <table class="w-full text-sm text-left text-gray-500">
        <thead class="text-xs text-gray-700 uppercase bg-gray-50">
            <tr>
                <th scope="col" class="px-3 py-3">#</th>
                <th scope="col" class="px-6 py-3">Constituency</th>
                <th scope="col" class="px-6 py-3">Candidates</th>
            </tr>
        </thead>
        <tbody>
          {#each electionData as places}
            <tr class="bg-white border-b">
              <td class="px-6 py-4">{places.id}</td>
              <td class="px-6 py-4 font-bold text-base">{places.constituency}</td>
              <td class="px-6 py-4">                
                <div class="mt-4 flex items-center space-x-3 text-base">
                  <div class="font-semibold text-gray-900">{places.udf_candidate}</div>
                  <svg viewBox="0 0 2 2" width="3" height="3" aria-hidden="true" class="fill-gray-900">
                    <circle cx="1" cy="1" r="1" />
                  </svg>
                  <div class="text-gray-600">UDF: {candidatePartyLookup?.[places.udf_candidate]}</div>
                </div>
                <div class="mt-4 flex items-center space-x-3 text-base">
                  <div class="font-semibold  text-gray-900">{places.ldf_candidate}</div>
                  <svg viewBox="0 0 2 2" width="3" height="3" aria-hidden="true" class="fill-gray-900">
                    <circle cx="1" cy="1" r="1" />
                  </svg>
                  <div class="text-gray-600">LDF: {candidatePartyLookup?.[places.ldf_candidate]}</div>
                </div>
                <div class="mt-4 flex items-center space-x-3 text-base">
                  <div class="font-semibold text-gray-900">{places.nda_candidate}</div>
                  <svg viewBox="0 0 2 2" width="3" height="3" aria-hidden="true" class="fill-gray-900">
                    <circle cx="1" cy="1" r="1" />
                  </svg>
                  <div class="text-gray-600">NDA: {candidatePartyLookup?.[places.nda_candidate]}</div>
                </div>
              </td>
            </tr>
          {/each}
        </tbody>
      </table>
    </div>
  </div>
{:else}
  <p>No data available.</p>
{/if}