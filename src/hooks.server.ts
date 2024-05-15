// src/hooks.server.ts
import { PUBLIC_SUPABASE_URL, PUBLIC_SUPABASE_ANON_KEY } from '$env/static/public'
import { createServerClient } from '@supabase/ssr'
import type { Session } from '@supabase/supabase-js'
import { type Handle, redirect } from '@sveltejs/kit'
import { sequence } from '@sveltejs/kit/hooks'


const supabase: Handle = async ({ event, resolve }) => {
  /**
   * Creates a Supabase client specific to this server request.
   *
   * The Supabase client gets the Auth token from the request cookies.
   */
  event.locals.supabase = createServerClient(PUBLIC_SUPABASE_URL, PUBLIC_SUPABASE_ANON_KEY, {
    cookies: {
      get: (key) => event.cookies.get(key),
      /**
       * SvelteKit's cookies API requires `path` to be explicitly set in
       * the cookie options. Setting `path` to `/` replicates previous/
       * standard behavior.
       */
      set: (key, value, options) => {
        console.log(new Date().toLocaleString(), 'src/hooks.server.ts: Set Cookie.',key, value, options);  // Log when action is called
        event.cookies.set(key, value, { ...options, path: '/' })
      },
      remove: (key, options) => {
        console.log(new Date().toLocaleString(), 'src/hooks.server.ts: Remove Cookie.',key, options);  // Log when action is called
        event.cookies.delete(key, { ...options, path: '/' })
      },
    },
   cookieOptions: {
      sameSite: 'none',
      httpOnly: false,
      secure: true,
     },
  })

  /**
   * Unlike `supabase.auth.getSession()`, which returns the session _without_
   * validating the JWT, this function also calls `getUser()` to validate the
   * JWT before returning the session.
   */
  event.locals.safeGetSession = async () => {
    const {
      data: { session },
      error: serr
    } = await event.locals.supabase.auth.getSession()
    if (!session) {
      console.log(new Date().toLocaleString(), 'src/hooks.server.ts: Session null.', serr);  // Log when action is called
      return { session: null, user: null }
    }

    const {
      data: { user },
      error: uerr,
    } = await event.locals.supabase.auth.getUser()
    if (uerr) {
      // JWT validation has failed
      console.log(new Date().toLocaleString(), 'src/hooks.server.ts: JWT validation failed.',uerr);  // Log when action is called
      return { session: null, user: null }
    }

    return { session, user }
  }

  return resolve(event, {
    filterSerializedResponseHeaders(name) {
      /**
       * Supabase libraries use the `content-range` and `x-supabase-api-version`
       * headers, so we need to tell SvelteKit to pass it through.
       */
      return name === 'content-range' || name === 'x-supabase-api-version'
    },
  })
}

const authGuard: Handle = async ({ event, resolve }) => {
  const { session, user } = await event.locals.safeGetSession()
  event.locals.session = session
  event.locals.user = user
  let cookie : string | undefined = event.cookies.get("sb-wsrczwqvtdiuckpnvztv-auth-token")

  if (!event.locals.session && cookie) {
    const session: Session = JSON.parse(cookie);
		const response = await event.locals.supabase.auth.setSession(session);
    console.log(new Date().toLocaleString(), 'src/hooks.server.ts: No session, found cookie!', cookie);  // Log when action is called  
  }

  if (!event.locals.session && event.url.pathname.startsWith('/private')) {    
    console.log(new Date().toLocaleString(), 'src/hooks.server.ts: No session. Redirecting to /login', event.cookies.get("sb-auth"));  // Log when action is called  
    return redirect(303, '/login')
  }

  if (event.locals.session && event.url.pathname === '/login') {
    console.log(new Date().toLocaleString(), 'src/hooks.server.ts: Redirecting to /private');  // Log when action is called  
    return redirect(303, '/private')
  }

  return resolve(event)
}

export const handle: Handle = sequence(supabase, authGuard)