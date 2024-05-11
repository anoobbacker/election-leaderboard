// src/routes/+page.server.ts
import { redirect } from '@sveltejs/kit'
import type { PageServerLoad } from './$types'

export const load: PageServerLoad = async ({ url, locals: { supabase, safeGetSession} }) => {
  const { session } = await safeGetSession()
  // if the user is already logged in return them to the account page
  if (!session) {
    throw redirect(303, '/login')
  }

  return { url: url.origin }
}
