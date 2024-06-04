// /src/routes/private/leaderboard/+page.server.ts
import { fail } from '@sveltejs/kit'
import type { Actions, PageServerLoad } from './$types'

interface CandidatePartyLookup {
  [key: string]: {party: string, photo_url: string};  // Define an index signature
}

export const load: PageServerLoad = async ({ depends, locals: { supabase, session } }) => {
  depends('supabase:db:profiles');
  depends('supabase:db:election_prediction_2024');

  try {
    // Fetch previous predictions
    const { data: predictions, error: predictionsError } = await supabase
      .from('election_prediction_2024')
      .select('participant_id, updated_at');

    if (predictionsError) {
      console.error(new Date().toLocaleString(), 'src/routes/private/leaderboard/+page.server.ts: Failed to save predictions', predictionsError);  // Log when action is called
      return fail(500, { error: `Failed to get predictions ${predictionsError.message}` })
    }

    // Extract unique user IDs
    const userIds = Array.from(new Set(predictions.map(entry => entry.participant_id)));
    const submissionDates = Object.fromEntries(predictions.map(entry => [entry.participant_id, entry.updated_at]));

    const { data: profiles, error: profilesError } = await supabase
      .from('profiles')
      .select(`id, username, avatar_url`)
      .in('id', userIds)

    if (profilesError) {
      console.error(new Date().toLocaleString(), 'src/routes/private/leaderboard/+page.server.ts: Failed to save predictions', profilesError);  // Log when action is called
      return fail(500, { error: `Failed to get profiles ${profilesError.message}` })
    }

    // Fetch candidate and party information
    const { data: candidatePartyData, error: candidatePartyError } = await supabase
    .from('candidate_party_mapping')
    .select('candidate_name, party, photo_url');

    if (candidatePartyError) {
      console.error(new Date().toLocaleString(), 'src/routes/private/leaderboard/+page.server.ts: Failed to save predictions', candidatePartyError);  // Log when action is called
      return fail(500, { error: `Failed to get profiles ${candidatePartyError.message}` })
    }

    // Transform data into a lookup object
    const partylookup:CandidatePartyLookup = {};
    candidatePartyData.forEach(({ candidate_name, party, photo_url }) => {
      partylookup[candidate_name] = {party, photo_url};
    });

    // Merge profiles with submission dates
    const participants = profiles.map(profile => ({
      ...profile,
      submitted_at: submissionDates[profile.id]
    }));

    return {
      participants: participants || [],
      partylookup: partylookup,
    };
  } catch (error) {
    console.error(new Date().toLocaleString(), 'src/routes/private/leaderboard/+page.server.ts: Error fetching data', error);  // Log when action is called

    return fail(500, { error: `Failed to get data!` })
  }
}

export const actions: Actions = {
  scorecard: async ({ locals: { supabase } }) => {
    console.debug(new Date().toLocaleString(), 'src/routes/private/leaderboard/+page.server.ts: showscorecard(): Called');  // Log when action is called

    try {
      // Fetch the participants and their predictions
      const { data: participants, error: participantsError } = await supabase
        .from('profiles')
        .select('id, username, avatar_url');

      if (participantsError) throw new Error(participantsError.message);

      // Fetch predictions for each participant
      const { data: predictions, error: predictionsError } = await supabase
        .from('election_prediction_2024')
        .select('participant_id, constituency, candidate_name, vote_share, winning_margin');

      if (predictionsError) throw new Error(predictionsError.message);

      // Fetch actual election results
      const { data: results, error: resultsError } = await supabase
        .from('election_results')
        .select('constituency_name, elected_member, elected_party, vote_share_percentage, margin')
        .eq('year', '2024');

      if (resultsError) throw new Error(resultsError.message);

      // Constants for point calculation
      const MAX_POINTS_FOR_CORRECT_WINNER = 50;
      const MAX_POINTS_FOR_VOTE_SHARE = 25;
      const MAX_POINTS_FOR_WINNING_MARGIN = 25;

      // Map to store total points for each participant
      const participantPointsMap = new Map();

      // Group predictions and results by constituency
      const constituencies = results.map(result => {
        const constituencyPredictions = predictions
          .filter(prediction => prediction.constituency === result.constituency_name)
          .map(prediction => {
            const participant = participants.find(p => p.id === prediction.participant_id);
            // Calculate points
            let points = 0;
            if (prediction.candidate_name === result.elected_member) {
                points += MAX_POINTS_FOR_CORRECT_WINNER;
              

                if ( (prediction.vote_share !== null) && (result.vote_share_percentage > 0) ) {
                  const maxVoteShareDiff = result.vote_share_percentage; // Maximum possible difference for vote share (percentage)
                  const voteShareDiff = Math.min(Math.abs(result.vote_share_percentage - prediction.vote_share) / maxVoteShareDiff);
                  const voteSharePoints = MAX_POINTS_FOR_VOTE_SHARE * (1 - voteShareDiff);
                  
                  points += voteSharePoints;
                  
                }

                if ( (prediction.winning_margin !== null) && (result.margin > 0) ) {
                  const maxWinningMarginDiff = result.margin; // Maximum possible winning margin
                  const winningMarginDiff = Math.min(Math.abs(result.margin - prediction.winning_margin) / maxWinningMarginDiff, 1);
                  const winningMarginPoints = MAX_POINTS_FOR_WINNING_MARGIN * (1 - winningMarginDiff);
                  
                  points += winningMarginPoints;
                  
                }

                // Round points to the nearest integer
                points = Math.round(points);
                
                // Update total points for the participant
                if (participantPointsMap.has(prediction.participant_id)) {
                  participantPointsMap.set(prediction.participant_id, participantPointsMap.get(prediction.participant_id) + points);
                } else {
                  participantPointsMap.set(prediction.participant_id, points);
                }
            }

            return {
                ...prediction,
                username: participant?.username,
                avatar_url: participant?.avatar_url,
                points: points
            };
          });

        return {
          ...result,
          predictions: constituencyPredictions.sort((a, b) => b.points - a.points),
        };
      });

      // Create a list of participants with total points
      const participantsWithTotalPoints = Array.from(participantPointsMap.entries()).map(([id, total_points]) => {
        const participant = participants.find(p => p.id === id);
        return {
            ...participant,
            total_points
        };
      });

      // Sort participants by total points
      participantsWithTotalPoints.sort((a, b) => b.total_points - a.total_points);

      console.debug(new Date().toLocaleString(), 'src/routes/private/leaderboard/+page.server.ts: showscorecard(): Return');  // Log when action is called
      return {
        success: true,
        constituencies,
        participants: participantsWithTotalPoints
      };
    } catch (error) {
      console.error('Error fetching data:', error);
      return fail(500, { error: `Failed to get leaderboard data! ${error}` })
    }

  },
}