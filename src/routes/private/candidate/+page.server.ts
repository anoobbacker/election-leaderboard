// /src/routes/private/candidate/+page.server.ts

import type { PageServerLoad } from './$types'

interface CandidatePartyLookup {
  [key: string]: {party: string, photo_url: string};  // Define an index signature
}

export const load: PageServerLoad = async ({ depends, locals: { supabase, session } }) => {
  depends('supabase:db:kerala_election_2024');
  depends('supabase:db:candidate_party_mapping');

  // Fetching election data if needed for other parts of your page
  const { data: electionData, error: electionError } = await supabase
    .from('kerala_election_2024')
    .select()
    .order("id");

  // Fetch candidate and party information
  const { data: candidatePartyData, error: candidatePartyError } = await supabase
    .from('candidate_party_mapping')
    .select('candidate_name, party, photo_url');

  if (electionError || candidatePartyError) {
    console.error('Failed to load data:', electionError || candidatePartyError);
    return {};
  }

  // Transform data into a lookup object
  const candidatePartyLookup:CandidatePartyLookup = {};
  candidatePartyData.forEach(({ candidate_name, party, photo_url }) => {
    candidatePartyLookup[candidate_name] = {party, photo_url};
  });

  return { session, electionData, candidatePartyLookup }
}