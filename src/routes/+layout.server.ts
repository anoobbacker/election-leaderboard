// src/routes/+layout.server.ts
import type { LayoutServerLoad } from './$types'

export const load = (async ({ locals: { supabase, safeGetSession } }) => {
  console.log(new Date().toLocaleString(), 'src/routes/+layout.server.ts: ServerLoad called');  // Log when action is called
  const { session, user } = await safeGetSession()
  let avatar_url = ''
  if (user) {
    const { data: profile, error: profileError } = await supabase
    .from('profiles')
    .select(`username, avatar_url`)
    .eq('id', user.id)
    .single()

    if (profileError) {
      console.error(new Date().toLocaleString(), 'src/routes/+layout.server.ts: Failed to load profile ', profileError);  // Log when action is called
      return {
        session,
        avatar_url: ''
      };
    }
    avatar_url = profile.avatar_url
    console.log(new Date().toLocaleString(), 'src/routes/+layout.server.ts: ServerLoad return. Set avatar url = ', avatar_url);  // Log when action is called
  }

  return {
    session,
    avatar_url
  }
}) satisfies LayoutServerLoad