// src/routes/+layout.server.ts
import type { LayoutServerLoad } from './$types'

export const load = (async ({ locals: { supabase, safeGetSession } }) => {
  console.log('===Server load function called===');
  const { session, user } = await safeGetSession()
  let avatar_url = ''
  if (user) {
    const { data: profile, error: profileError } = await supabase
    .from('profiles')
    .select(`username, avatar_url`)
    .eq('id', user.id)
    .single()

    if (profileError) {
      console.error('Failed to load data:', profileError);
      return {
        session,
        avatar_url: ''
      };
    }
    avatar_url = profile.avatar_url
    console.log(new Date().toLocaleString(), 'Set avatar url:', avatar_url);  // Log when called
  }

  return {
    session,
    avatar_url
  }
}) satisfies LayoutServerLoad