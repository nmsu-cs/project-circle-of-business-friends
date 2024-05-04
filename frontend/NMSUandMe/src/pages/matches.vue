<template>
  <userPortalLayout :userPortalClicked="goToUserPortal" :logoutClicked="logout">
    <template #buttons>
      <v-btn @click="goToUserPortal">User Portal</v-btn>
      <v-btn @click="logout">Logout</v-btn>
    </template>

    <v-container class="text-center">
      <h1>Welcome to Matches</h1>
    </v-container>
    <v-container class="text-center" v-if="matches">
      <v-carousel hide-delimiters v-model="carosul_model">
        <v-carousel-item v-for="(match, index) in matches" :key="index">
          <v-row align="center" class="fill-height">
            <v-col cols="12">
              <v-card class="mx-auto" max-width="500">
                <v-card-title>
                  {{ match[0] }} {{ match[1] }}
                </v-card-title>
                <v-card-text>
                  <p>Score: {{ match[6] }}</p>
                  <p>Major: {{ match[2] }}</p>
                  <p>Year: {{ match[3] }}</p>
                  <p>Career Interest: {{ match[4]}}</p>
                  <p>Interests:</p>
                </v-card-text>
                <v-chip v-for="(interest, index) in match[5]" :key="index" class="ma-1" outlined>
                  {{ interest }}
                </v-chip>
                <v-card-actions>
                  <v-container class="text-center">
                    <v-btn @click="">Confirm</v-btn>
                    <v-btn class="ml-4" @click="">Skip</v-btn>
                  </v-container>
                </v-card-actions>
              </v-card>
            </v-col>
          </v-row>
        </v-carousel-item>
      </v-carousel>
    </v-container>
    <v-container class="text-center" v-else>
      <v-row align="center" justify="center">
        <v-col cols="12">
          <v-progress-circular indeterminate size="64"></v-progress-circular>
        </v-col>
      </v-row>
    </v-container>
    e
  </userPortalLayout>
</template>
  
  <script setup>
  import userPortalLayout from '@/layouts/userPortalLayout.vue'
  import { useRouter } from 'vue-router'
  import axios from 'axios'
  
  const user_id_temp = ref(null)
  const router = useRouter()
  const path = "http://localhost:5000/matches"

  const matches = ref({})
  const carosul_model = ref(0)

  onMounted(() => {
    user_id_temp.value = router.currentRoute.value.query.user_id
    const path_withparameters = `${path}?user_id=${user_id_temp.value}`

    axios.get(path_withparameters)
    .then(response => {
      matches.value = response.data.matches
      console.log(matches.value)
    })
    .catch(error => {
    })
    })
  
  const goToUserPortal = () => {
    const id=user_id_temp.value
    router.push({path:'/user_portal', query: {id},})
  }
  
  const logout = () => {
    router.push('/')
  }
  </script>
  