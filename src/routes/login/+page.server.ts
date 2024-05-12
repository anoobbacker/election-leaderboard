// src/routes/login/+page.server.ts
import { fail, redirect } from '@sveltejs/kit'
import type { Actions, PageServerLoad } from './$types'

export const load: PageServerLoad = async ({ url, locals: { supabase, safeGetSession} }) => {
  const origin = import.meta.env.VITE_PUBLIC_URL as string
  console.log(new Date().toLocaleString(), 'src/routes/login/+page.server.ts: ServerLoad called', 'URL = ', url.origin, 'Orgin = ', origin);  // Log when action is called
  const { session, user } = await safeGetSession()
  // if the user is already logged in return them to the account page
  if (session) {
    console.log(new Date().toLocaleString(), 'src/routes/login/+page.server.ts: ServerLoad Redirect to /');  // Log when action is called
    throw redirect(303, '/')
  }

  console.log(new Date().toLocaleString(), 'src/routes/login/+page.server.ts: ServerLoad return');  // Log when action is called
  return { url: url.origin }
}

export const actions: Actions = {
  login: async ({ request, locals: { supabase } }) => {
    const origin = import.meta.env.VITE_PUBLIC_URL as string
    console.log(new Date().toLocaleString(), 'src/routes/login/+page.server.ts: Login action called', "URL = ", origin);  // Log when action is called
    
    const formData = await request.formData()
    const email = formData.get('email') as string
    const password = formData.get('password') as string

    if (!email) {
			return fail(400, { email, missing: true });
		}

    if (!password) {
			return fail(400, { password, missing: true });
		}
    
    console.log(new Date().toLocaleString(), 'src/routes/login/+page.server.ts: Login form data received:', email);

    const { data: data, error: err } = await supabase.auth.signInWithPassword({ 
      email: email,
      password: password,
    })

    if (err) {
      console.log(new Date().toLocaleString(), 'src/routes/login/+page.server.ts: Login action return', 'Error = ', err?.message);  // Log when action is called
      return fail(500, {email, incorrect: true});
    }
    
    console.log(new Date().toLocaleString(), 'src/routes/login/+page.server.ts: Login action return successfully');  // Log when action is called    
    return {success: true}
  },
}
