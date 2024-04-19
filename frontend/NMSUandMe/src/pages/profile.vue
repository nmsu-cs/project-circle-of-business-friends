<template>
  <v-container class="fill-height">
      <v-responsive
        class="align-centerfill-height mx-auto"
        max-width="900"
      >
  
        <div class="text-center">
          <h1 class="text-h2 font-weight-bold">Profile</h1>
        </div>
  
  
        <v-form @submit.prevent="submitProfile">
        <v-text-field
          v-model="profile.age"
          label="Age"
          type="number"
          outlined
          readonly
        ></v-text-field>

        <v-text-field
          v-model="profile.gender"
          label="Gender"
          outlined
        ></v-text-field>

        <v-select
          v-model="profile.major"
          :items="majors"
          label="College Major"
          outlined
          chips
          attach
        ></v-select>

        <v-select
          v-model="profile.education_level"
          :items="ed_levels"
          label="Education Level"
          outlined
          chips
          attach
        ></v-select>

        <v-select
          v-model="profile.career_interest"
          :items="occupations"
          label="Career Interest"
          outlined
          chips
          attach
        ></v-select>

        <v-select
          v-model="selectedInterests"
          :items="interests"
          label="Interests"
          multiple
          chips
          attach
          outlined
        ></v-select>

        <v-btn color="primary" type="submit">Save</v-btn>
        </v-form>
  
      </v-responsive>
    </v-container>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import {useRouter} from 'vue-router'
  import axios from 'axios'

  const router = useRouter()
  const path = "http://localhost:5000/profile"
  const user_id = ref(null)

  const profile = ref({
    age: '',
    gender: '',
    major: '',
    education_level: '',
    career_interest: '',
    interests: {}
  })
  const selectedInterests = ref([])

  const interests = ['football', 'basketball', 'soccer', 'art', 'music', 'food', 'bar-hopping', 'partying', 'dinner-ing?']
  const majors = ['majorA', 'majorB', 'majorC', 'majorD', 'majorE', 'majorF']
  const occupations = ['occA', 'occB', 'occC', 'occD', 'occE', 'occF']
  const ed_levels = ['Freshman', 'Sophomore', 'Junior', 'Senior']

  
  onMounted(() => {
    user_id.value = router.currentRoute.value.query.user_id

    const path_withparameters = `${path}?user_id=${user_id.value}`
    axios.get(path_withparameters)
      .then(response => {
        console.log("User_id passed successfully:", response.data)
        if (response.data.status === 'success'){
          const profile_data = response.data.data

          profile.value = {
          age: profile_data.age || '',
          gender: profile_data.gender || '',
          major: profile_data.major || '',
          education_level: profile_data.education_level || '',
          career_interest: profile_data.career_interest || '',
          interests: profile_data.interests || []
          }
          selectedInterests.value = profile_data.interests || []
        }
        else {
          console.log("Failed to fetch profile:", response.data.msg)
        }
      })
      .catch(error => {
        console.log("Error sending user_id:", error.message)
      })
  })
  
  const submitProfile = async () => {
    
    const data = {
      ...profile.value,
      interests: selectedInterests.value,
      user_id: user_id.value
    }

    try {
      const response = await axios.post(path, data)
      console.log(response.data.msg)
      const id = user_id.value
      router.push({path:'/user_portal', query: {id},})

    }

    catch (error) {
      console.error('Failed to submit profile', error.message)
    }
  }

  

  </script>