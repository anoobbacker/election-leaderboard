import { fail, redirect } from '@sveltejs/kit'
import type { Actions, PageServerLoad } from './$types'

interface CandidatePartyLookup {
  [key: string]: string;  // Define an index signature
}

interface CandidatePredictionLookup {
  [key: string]: {candidate_name: string, vote_share: string, winning_margin: string};  // Define an index signature
}

export const load: PageServerLoad = async ({ locals: { supabase, safeGetSession } }) => {
  const { session } = await safeGetSession()

  if (!session) {
    throw redirect(303, '/')
  }

  // Fetching election data if needed for other parts of your page
  const { data: electionData, error: electionError } = await supabase
    .from('kerala_election_2024')
    .select();

  // Fetch candidate and party information
  const { data: candidatePartyData, error: candidatePartyError } = await supabase
    .from('candidate_party_mapping')
    .select('candidate_name, party');
  
  // Fetch previous predictions
  const { data: candidatePrediction, error: candidatePredictionError } = await supabase
    .from('election_prediction_2024')
    .select('constituency, candidate_name, vote_share, winning_margin')
    .eq('participant_id', session.user.id);

  if (electionError || candidatePartyError || candidatePredictionError) {
    console.error('Failed to load data:', electionError || candidatePartyError || candidatePredictionError);
    return {};
  }

  // Transform data into a lookup object
  const candidatePartyLookup:CandidatePartyLookup = {};
  candidatePartyData.forEach(({ candidate_name, party }) => {
    candidatePartyLookup[candidate_name] = party;
  });

  const candidatePredictionLookup:CandidatePredictionLookup = {}
  candidatePrediction.forEach(({ constituency, candidate_name, vote_share, winning_margin }) => {
    candidatePredictionLookup[constituency] = {candidate_name, vote_share, winning_margin};
  });

  return { electionData, candidatePartyLookup, candidatePredictionLookup}
}

export const actions: Actions = {
  update: async ({ request, locals: { supabase, safeGetSession } }) => {
    console.log(new Date().toLocaleString(), 'Update action called');  // Log when action is called

    const formData = await request.formData()
    const formDataEntries = Array.from(formData.entries());
    const constituencies = new Set();

    console.log(new Date().toLocaleString(), 'Form data received:', Object.fromEntries(formData));

    // Extract constituency names from form keys
    formDataEntries.forEach(([key, _]) => {
      const result = key.match(/^(.+?)-.+$/);
      if (result) {
        constituencies.add(result[1]);
      }
    });

    console.log(new Date().toLocaleString(), 'Processed form constituencies:', constituencies);

    // const { session } = await safeGetSession()
    const uuid = (await supabase.auth.getUser())?.data?.user?.id;

    // Prepare and insert data for each constituency
    for (const constituency of constituencies) {
      const candidate = formData.get(`${constituency}-candidate`);
      const voteShare = formData.get(`${constituency}-winnervoteshare`);
      const winningMargin = formData.get(`${constituency}-winningvotes`);

      console.log(new Date().toLocaleString(), 'Candidate:', candidate, 'Votes Share:', voteShare, 'Votes:', winningMargin);

      const { data, error } = await supabase
        .from('election_prediction_2024')
        .upsert({
          participant_id: uuid,
          constituency: constituency,
          candidate_name: candidate,
          vote_share: voteShare ? voteShare : '40',
          winning_margin: winningMargin ? winningMargin : '1000'
        }).select();

        if (error) {
          return fail(500, {constituency: constituency, message: 'Failed to save data'})
        }
    }

    console.log(new Date().toLocaleString(), 'Update action return');  // Log when action is called
    return {};
  },
}
