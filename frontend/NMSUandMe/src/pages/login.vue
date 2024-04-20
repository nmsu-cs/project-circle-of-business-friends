<template>
    <v-container>
    <v-responsive
      class="align-centerfill-height mx-auto"
      max-width="900"
    >

      <v-alert
      v-if="showAlert"
      color="error"
      icon="$error"
      title="Error"
      :text="alertMessage"
      dismissible
      ></v-alert>

      <div class="text-center">
        <h1 class="text-h2 font-weight-bold">Log In</h1>
      </div>

      <div class="py-4" />

      <form @submit.prevent="submit">
        <v-text-field
          v-model="username.value.value"
          :counter="10"
          :error-messages="username.errorMessage.value"
          label="Username"
        ></v-text-field>

        <v-text-field
          :append-inner-icon="eyeIcon"
          :type="inputType"
          v-model="password.value.value"
          :counter="12"
          :error-messages="password.errorMessage.value"
          label="Password"
          @click:append-inner="toggleVis"
        ></v-text-field>

        <v-btn
          class="me-4" type="submit"> submit </v-btn>

        <v-btn @click="handleReset"> clear </v-btn>
      </form>

    </v-responsive>
  </v-container>
    
</template>

<script setup>
  import { ref, computed } from 'vue'
  import { useField, useForm } from 'vee-validate'
  import {useRouter} from 'vue-router'
  import axios from 'axios'

  const router = useRouter()

  const visible = ref(true)
  const showAlert = ref(false)
  const alertMessage = ref('')
  const path = 'http://localhost:5000/login'

  const showErrorMessage = (message) => {
    alertMessage.value = message
    showAlert.value = true
  }

  const toggleVis = () => {visible.value = !visible.value};
  const inputType = computed(() => visible.value ? 'text' : 'password');
  const eyeIcon = computed(() => visible.value ? 'mdi-eye' : 'mdi-eye-off');


  const { handleSubmit, handleReset } = useForm({
    validationSchema: {
      username (value) {
        if(value?.length >= 10) return true
        
        return "Username needs to be at least 10 characters"
      },
      password (value) {
        if (value?.length > 12 && /(?=.*[@#$%^&*!~])/.test(value)) return true

        return 'Password must be at least 12 characters long and contain 1 special character.'
      },
    },
  })
  const username = useField('username')
  const password = useField('password')

  const submit = handleSubmit( async values => {
    try {
        const response = await axios.post(path, values)
        console.log(response.data)
        if(response.data.status === 'success'){
          console.log('User logged in:', response.data.msg)
          const user_id = response.data.user_id
          router.push({path:'/user_portal', query: {user_id},})
        }

        else if(response.data.msg === 'error'){
            console.log('Conflict found:', response.data.msg)
            showErrorMessage(response.data.msg)
        }
        else{
          console.log('Failed to validate user:', response.data.msg)
          showErrorMessage(response.data.msg)
        }
      }

      catch (error){
        console.error('Error verifying user:', error.message)
        showErrorMessage(response.data.msg)
      }
  })
</script>