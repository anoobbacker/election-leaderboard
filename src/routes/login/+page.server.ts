// src/routes/+page.server.ts
import { fail, redirect } from '@sveltejs/kit'
import type { Actions, PageServerLoad } from './$types'

export const load: PageServerLoad = async ({ url, locals: { supabase, safeGetSession} }) => {
  const origin = import.meta.env.VITE_PUBLIC_URL as string
  console.log(new Date().toLocaleString(), 'src/routes/+page.server.ts: Load called', 'URL = ', url.origin, 'Orgin = ', origin);  // Log when action is called
  const { session } = await safeGetSession()
  // if the user is already logged in return them to the account page
  if (session) {
    console.log(new Date().toLocaleString(), 'src/routes/+page.server.ts: Redirect to /predict');  // Log when action is called
    throw redirect(303, '/predict')
  }

  console.log(new Date().toLocaleString(), 'src/routes/+page.server.ts: Load return');  // Log when action is called
  return { url: url.origin }
}

export const actions: Actions = {
  login: async ({ request, locals: { supabase, safeGetSession } }) => {
    const origin = import.meta.env.VITE_PUBLIC_URL as string
    console.log(new Date().toLocaleString(), 'Login action called', "URL = ", origin);  // Log when action is called
    const { session } = await safeGetSession()

    if (session) {
      throw redirect(303, '/predict')
    }
    
    const formData = await request.formData()
    const email = formData.get('email') as string
    
    const redirectTo = origin || formData.get('redirectTo') as string

    console.log(new Date().toLocaleString(), 'Form data received:', Object.fromEntries(formData));

    const { data: data, error: err } = await supabase.auth.signInWithOtp({ 
      email: email,
      options: {
        emailRedirectTo: redirectTo
      } 
    })

    if (err) {
      return { success: false, message: err.message }
    }
    
    return {
      success: true,
      message: 'Check your email for the magic link.'
    }
  },
}
