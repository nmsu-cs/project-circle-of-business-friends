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
        <h1 class="text-h2 font-weight-bold">Sign Up</h1>
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
          v-model="email.value.value"
          :error-messages="email.errorMessage.value"
          label="E-mail"
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

        <v-text-field
          v-model="firstName.value.value"
          :counter="2"
          :error-messages="firstName.errorMessage.value"
          label="First Name"
        ></v-text-field>

        <v-text-field
          v-model="lastName.value.value"
          :counter="2"
          :error-messages="lastName.errorMessage.value"
          label="Last Name"
        ></v-text-field>

        <v-text-field
          v-model="dob.value.value"
          :error-messages="dob.errorMessage.value"
          label="Date of Birth"
          outlined
          type="date"
        >
        </v-text-field>

        <v-checkbox
          v-model="checkbox.value.value"
          :error-messages="checkbox.errorMessage.value"
          label="T&C"
          type="checkbox"
          value="1"
        ></v-checkbox>

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
  const path = 'http://localhost:5000/signup'

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
      email (value) {
        if (/^[a-z0-9.-]+@nmsu.edu$/i.test(value)) return true

        return 'Must be a valid e-mail.'
      },
      firstName (value) {
        if (value?.length >= 2) return true

        return 'Name needs to be at least 2 characters.'
      },
      lastName (value) {
        if (value?.length >= 2) return true

        return 'Name needs to be at least 2 characters.'
      },
      dob (value) {

        if (value)
        {
          const dateRegex = /^\d{4}-\d{2}-\d{2}$/
          const [year, month, day] = value.split('-').map(Number)

          if (year > 1940) {
            if (dateRegex.test(value)){
            return true
            }
          }
          else{
            return 'DOB is invalid'
          }
        }
        
        return 'DOB is required'
      },
      checkbox (value) {
        if (value === '1') return true

        return 'Must be checked.'
      },
    },
  })
  const username = useField('username')
  const password = useField('password')
  const email = useField('email')
  const firstName = useField('firstName')
  const lastName = useField('lastName')
  const dob = useField('dob')
  const checkbox = useField('checkbox')

  const submit = handleSubmit( async values => {
    try {
        const response = await axios.post(path, values)
        console.log(response.data)
        if(response.data.status === 'success'){
          console.log('User added:', response.data.msg)
          const user_id = response.data.user_id
          router.push({path:'/profile', query: {user_id},})
        }

        else if(response.data.msg === 'error'){
            console.log('Conflict found:', response.data.msg)
            showErrorMessage(response.data.msg)
        }
        else{
          console.log('Failed to add user:', response.data.msg)
          showErrorMessage(response.data.msg)
        }
      }

      catch (error){
        console.error('Error adding user:', error.message)
        showErrorMessage(response.data.msg)
      }
  })
</script>