// src/routes/+layout.ts
import { PUBLIC_SUPABASE_ANON_KEY, PUBLIC_SUPABASE_URL } from '$env/static/public'
import type { LayoutLoad } from './$types'
import { createBrowserClient, createServerClient, combineChunks, isBrowser, parse } from '@supabase/ssr'

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
            const cookie = combineChunks(key, (name) => {
              const cookies = parse(document.cookie)
              return cookies[name]
            })
            console.log(new Date().toLocaleString(), 'src/routes/+layout.ts: createBrowserClient Cookie.', key, ";", cookie);  // Log when action is called
            return cookie;
          },
        }, 
        cookieOptions: {
          sameSite: false,
          httpOnly: false,
          secure: false,
         },
      })
    : createServerClient(PUBLIC_SUPABASE_URL, PUBLIC_SUPABASE_ANON_KEY, {
        global: {
          fetch,
        },
        cookies: {
          get() {
            console.log(new Date().toLocaleString(), 'src/routes/+layout.ts: createServerClient Cookie.',JSON.stringify(data.session));  // Log when action is called
            return JSON.stringify(data.session)
          },
        },
        cookieOptions: {
          sameSite: false,
          httpOnly: false,
          secure: false,
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