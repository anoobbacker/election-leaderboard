import { fail, redirect } from '@sveltejs/kit'
import type { Actions, PageServerLoad } from './$types'

export const load: PageServerLoad = async ({ locals: { supabase, safeGetSession } }) => {
  // const { session } = await safeGetSession()
  const user = (await supabase.auth.getUser())?.data?.user;

  if (!user) {
    throw redirect(303, '/login')
  }

  const { data: profile } = await supabase
    .from('profiles')
    .select(`username, full_name, website, avatar_url`)
    .eq('id', user.id)
    .single()

  return { profile }
}

export const actions: Actions = {
  update: async ({ request, locals: { supabase, safeGetSession } }) => {
    const formData = await request.formData()
    const fullName = formData.get('fullName') as string
    const username = formData.get('username') as string
    const website = formData.get('website') as string
    const avatarUrl = formData.get('avatarUrl') as string

    // const { session } = await safeGetSession()
    const uuid = (await supabase.auth.getUser())?.data?.user?.id;

    const { error } = await supabase.from('profiles').upsert({
      id: uuid,
      full_name: fullName,
      username,
      website,
      avatar_url: avatarUrl,
      updated_at: new Date(),
    })

    if (error) {
      return fail(500, {
        fullName,
        username,
        website,
        avatarUrl,
      })
    }

    return {
      fullName,
      username,
      website,
      avatarUrl,
    }
  },
  signout: async ({ locals: { supabase, safeGetSession } }) => {
    const { session } = await safeGetSession()
    if (session) {
      await supabase.auth.signOut()
      throw redirect(303, '/')
    }
  },
}
