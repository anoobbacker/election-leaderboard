// src/routes/+layout.ts
import { PUBLIC_SUPABASE_ANON_KEY, PUBLIC_SUPABASE_URL } from '$env/static/public'
import type { LayoutLoad } from './$types'
import { createBrowserClient, isBrowser, parse } from '@supabase/ssr'

export const load = (async ({ fetch, data, depends }) => {
  depends('supabase:auth')

  console.log(new Date().toLocaleString(), 'src/routes/+layout.ts: Universal load called');  // Log when action is called
  const supabase = createBrowserClient(PUBLIC_SUPABASE_URL, PUBLIC_SUPABASE_ANON_KEY, {
    global: {
      fetch,
    },
    cookies: {
      get(key) {
        if (!isBrowser()) {
          return JSON.stringify(data.ssession)
        }

        const cookie = parse(document.cookie)
        return cookie[key]
      },
    },
  })

  let avatar_url = data.avatar_url
  /**
   * It's fine to use `getSession` here, because on the client, `getSession` is
   * safe, and on the server, it reads `session` from the `LayoutData`, which
   * safely checked the session using `safeGetSession`.
   */
  const {
    data: { session },
  } = await supabase.auth.getSession()

  console.log(new Date().toLocaleString(), 'src/routes/+layout.ts: Universal load return');  // Log when action is called
  return { supabase, session, avatar_url }
}) satisfies LayoutLoad