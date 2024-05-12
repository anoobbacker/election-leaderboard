// src/routes/login/+page.server.ts
import { fail, redirect } from '@sveltejs/kit'
import type { Actions, PageServerLoad } from './$types'

export const actions: Actions = {
  login: async ({ request, locals: { supabase } }) => {
    console.log(new Date().toLocaleString(), 'src/routes/login/+page.server.ts: Login action called');  // Log when action is called
    
    const formData = await request.formData()
    const email = formData.get('email') as string
    const password = formData.get('password') as string

    if (!email) {
      console.error(new Date().toLocaleString(), 'src/routes/login/+page.server.ts: Login action missing email!');  // Log when action is called
			return fail(400, { email, missing: true });
		}

    if (!password) {
      console.error(new Date().toLocaleString(), 'src/routes/login/+page.server.ts: Login action missing password!');  // Log when action is called
			return fail(400, { password, missing: true });
		}
    
    console.log(new Date().toLocaleString(), 'src/routes/login/+page.server.ts: Login form data received:', email);

    const { error: err } = await supabase.auth.signInWithPassword({ 
      email: email,
      password: password,
    })

    if (err) {
      console.log(new Date().toLocaleString(), 'src/routes/login/+page.server.ts: Login action signIn error.', 'Error = ', err.message);  // Log when action is called
      return fail(500, {email, incorrect: true});
    }
    
    console.log(new Date().toLocaleString(), 'src/routes/login/+page.server.ts: Login action return successfully');  // Log when action is called    
    return redirect(303, '/private')
  },
}
