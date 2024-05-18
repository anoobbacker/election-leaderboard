// src/routes/+layout.server.ts
import type { LayoutServerLoad } from './$types'

export const load: LayoutServerLoad = async (event) => {  
  const { session, user } = await event.locals.safeGetSession()

  return {
    session,
    user,
  }
}