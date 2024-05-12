// src/routes/+page.server.ts
import { redirect } from '@sveltejs/kit'
import type { PageServerLoad } from './$types'

export const load: PageServerLoad = async ({ url, locals: { supabase } }) => {
  const { data: session } = await supabase.auth.getSession();

  console.log(new Date().toLocaleString(), 'src/routes/+page.server.ts: ServerLoad called', session);  // Log when action is called
  // if the user is already logged in return them to the account page
  if (session) {
    console.log(new Date().toLocaleString(), 'src/routes/+page.server.ts: Redirect to /account');  // Log when action is called
    // throw redirect(303, '/account')
  } else {
    console.log(new Date().toLocaleString(), 'src/routes/+page.server.ts: Redirect to /login');  // Log when action is called
    throw redirect(303, '/login')
  }

  console.log(new Date().toLocaleString(), 'src/routes/+page.server.ts: ServerLoad return');  // Log when action is called
  return { url: url.origin }
}
