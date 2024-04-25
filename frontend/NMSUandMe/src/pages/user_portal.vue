<template>
  <userPortalLayout :profileClicked="goToProfile" :matchesClicked="goToMatches" :eventsClicked="goToEvents"
    :logoutClicked="logout">
    <template #buttons>
      <v-btn @click="goToProfile">Profile</v-btn>
      <v-btn @click="goToMatches">Matches</v-btn>
      <v-btn @click="goToEvents">Events</v-btn>
      <v-btn @click="logout">Logout</v-btn>
    </template>

    <v-container class="text-center">
      <h1>Welcome to the User Portal</h1>
    </v-container>
    <v-container>
      <v-row justify="start">
        <v-col cols="5">
          <v-card class="mx-auto" max-width="344" hover>
            <v-card-item>
              <v-card-title>
                <p> {{ profile_data.username }}'s Profile</p>
              </v-card-title>
            </v-card-item>

            <v-card-text>
              <p>Name: {{ profile_data.firstName }} {{ profile_data.lastName }}</p>
              <p>Major: {{ profile_data.major }}</p>
              <p>Year: {{ profile_data.ed_level }}</p>
              <p>Career Interest: {{ profile_data.career_interest }}</p>
              <p>Interests:</p>
            </v-card-text>
            <v-chip v-for="(interest, index) in profile_data.interests" :key="index" class="ma-1" outlined>
              {{ interest }}
            </v-chip>
          </v-card>
        </v-col>
      </v-row>
    </v-container>

  </userPortalLayout>
</template>
    
    <script setup>
    import userPortalLayout from '@/layouts/userPortalLayout.vue'
    import { useRouter } from 'vue-router'
    import axios from 'axios'
    
    const id = ref(null)
    const router = useRouter()
    const path = "http://localhost:5000/user_portal"

    const profile_data = ref({})

    onMounted(() => {
      id.value = router.currentRoute.value.query.id
      const path_withparameters = `${path}?user_id=${id.value}`

      axios.get(path_withparameters)
      .then(response => {
        profile_data.value = response.data.data
        console.log(profile_data)
      })
      .catch(error => {
      })
      })
    
    const goToProfile = () => {
      const user_id=id.value
      router.push({path:'/profile', query: {user_id},})
    }
    
    const goToMatches = () => {
      const user_id=id.value
      router.push({path:'/matches', query: {user_id},})
    }

    const goToEvents = () => {
      const user_id = id.value
      router.push({ path: '/events', query: { user_id }, })
    }
    
    const logout = () => {
      router.push('/')
    }
    </script>
    