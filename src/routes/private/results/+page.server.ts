// /src/routes/private/results/+page.server.ts
import { fail } from '@sveltejs/kit'
import type { Actions, PageServerLoad } from './$types'

interface CandidatePartyLookup {
  [key: string]: {party: string, alliance: string, photo_url: string};  // Define an index signature
}

export const load: PageServerLoad = async ({ depends, locals: { supabase } }) => {
  depends('supabase:db:profiles');
  depends('supabase:db:election_prediction_2024');

  try {
    // Fetch candidate and party information
    const { data: candidatePartyData, error: candidatePartyError } = await supabase
    .from('candidate_party_mapping')
    .select('candidate_name, party, alliance, photo_url');

    if (candidatePartyError) {
      console.error(new Date().toLocaleString(), 'src/routes/private/results/+page.server.ts: Failed to save predictions', candidatePartyError);  // Log when action is called
      return fail(500, { error: `Failed to get profiles ${candidatePartyError.message}` })
    }

    // Fetch actual election results
    const { data: electionResults, error: resultsError } = await supabase
    .from('election_results')
    .select('constituency_name, elected_member, elected_party, local_alliance, vote_share_percentage, margin')
    .eq('year', '2024');

    if (resultsError) throw new Error(resultsError.message);
        
    // Process data to count the wins per alliance
    const allianceSummary: { [key: string]: number } = {}; // Add index signature to allianceSummary object
    electionResults.forEach((result) => {
        const alliance: string = result.local_alliance;
        if (alliance) {
          if (!allianceSummary[alliance]) {
              allianceSummary[alliance] = 0; // Use index signature to assign a value to allianceSummary
          }
          allianceSummary[alliance]++; // Use index signature to increment the value of allianceSummary
        }
    });

    // Process data to count the wins per alliance
    const partySummary: { [key: string]: number } = {}; // Add index signature to allianceSummary object
    electionResults.forEach((result) => {
      const elected_party: string = result.elected_party;
      if (elected_party) {
        if (!partySummary[elected_party]) {
          partySummary[elected_party] = 0; // Use index signature to assign a value to allianceSummary
        }
        partySummary[elected_party]++; // Use index signature to increment the value of allianceSummary
      }
    });

    // Transform data into a lookup object
    const partylookup:CandidatePartyLookup = {};
    candidatePartyData.forEach(({ candidate_name, party, alliance, photo_url }) => {
      partylookup[candidate_name] = {party, alliance, photo_url};
    });

    return {
      success: true,
      partylookup: partylookup,
      allianceSummary,
      partySummary,
      electionResults
    };
  } catch (error) {
    console.error(new Date().toLocaleString(), 'src/routes/private/results/+page.server.ts: Error fetching data', error);  // Log when action is called

    return fail(500, { error: `Failed to get data!` })
  }
}