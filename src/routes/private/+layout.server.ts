// src/routes/private/+layout.server.ts
import type { LayoutServerLoad } from './$types'

export const load: LayoutServerLoad = async ({ locals: { supabase, session } }) => {
  console.debug(new Date().toLocaleString(), 'src/routes/private/+layout.server.ts: ServerLoad called');  // Log when action is called
  const uuid = session?.user.id

  let avatar_url = ''
  console.debug(new Date().toLocaleString(), 'src/routes/private/+layout.server.ts: ServerLoad ', JSON.stringify(session).replace(/\r/g, ''), uuid);  // Log when action is called
  if (uuid) {
    const { data: profile, error: profileError } = await supabase
    .from('profiles')
    .select(`username, avatar_url`)
    .eq('id', uuid)
    .single()

    if (profileError) {
      console.error(new Date().toLocaleString(), 'src/routes/private/+layout.server.ts: Failed to load profile ', profileError);  // Log when action is called
      return {
        avatar_url: ''
      };
    }
    avatar_url = profile.avatar_url
  } else {
    console.error(new Date().toLocaleString(), 'src/routes/private/+layout.server.ts: ServerLoad No session or  user');  // Log when action is called  
  }

  console.debug(new Date().toLocaleString(), 'src/routes/private/+layout.server.ts: ServerLoad return. Avatar url = ', avatar_url);  // Log when action is called
  return {
    avatar_url
  }
}