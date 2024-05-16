// src/routes/+layout.ts
import { PUBLIC_SUPABASE_ANON_KEY, PUBLIC_SUPABASE_URL } from '$env/static/public'
import type { LayoutLoad } from './$types'
import { createBrowserClient, createServerClient, isBrowser, parse } from '@supabase/ssr'

export const load: LayoutLoad = async ({ data, depends, fetch }) => {
  /**
   * Declare a dependency so the layout can be invalidated, for example, on
   * session refresh.
   */
  depends('supabase:auth')

  console.log(new Date().toLocaleString(), 'src/routes/+layout.ts: Universal load called');  // Log when action is called
  const supabase = isBrowser()
    ? createBrowserClient(PUBLIC_SUPABASE_URL, PUBLIC_SUPABASE_ANON_KEY, {
        global: {
          fetch,
        },
        cookies: {
          get(key) {
            const cookie = parse(document.cookie)
            return cookie[key]
          },
        }, 
        cookieOptions: {
          sameSite: false,
          httpOnly: false,
         },
      })
    : createServerClient(PUBLIC_SUPABASE_URL, PUBLIC_SUPABASE_ANON_KEY, {
        global: {
          fetch,
        },
        cookies: {
          get() {
            return JSON.stringify(data.session)
          },
        },
        cookieOptions: {
          sameSite: false,
          httpOnly: false,
         },
      })

  /**
   * It's fine to use `getSession` here, because on the client, `getSession` is
   * safe, and on the server, it reads `session` from the `LayoutData`, which
   * safely checked the session using `safeGetSession`.
   */
  const {
    data: { session },
  } = await supabase.auth.getSession()

  const {
    data: { user },
  } = await supabase.auth.getUser()

  console.log(new Date().toLocaleString(), 'src/routes/+layout.ts: Universal load return');  // Log when action is called
  return { session, supabase, user }
}