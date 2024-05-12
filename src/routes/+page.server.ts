// src/routes/+page.server.ts
import { redirect } from '@sveltejs/kit'
import type { PageServerLoad } from './$types'

export const load: PageServerLoad = async ({ url, locals: { supabase, safeGetSession} }) => {
  // const { session } = await safeGetSession()
  const { data: session, error: err } = await supabase.auth.getSession()

  console.log(new Date().toLocaleString(), 'src/routes/+page.server.ts: ServerLoad called', session, err);  // Log when action is called
  // if the user is already logged in return them to the account page
  if (!session.session) {
    console.log(new Date().toLocaleString(), 'src/routes/+page.server.ts: Redirect to /login', err);  // Log when action is called
    throw redirect(303, '/login')
  }

  console.log(new Date().toLocaleString(), 'src/routes/+page.server.ts: ServerLoad return', url.origin);  // Log when action is called
  return { url: url.origin }
}
