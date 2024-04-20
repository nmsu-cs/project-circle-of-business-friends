<template>
  <v-container class="fill-height">
    <v-responsive
      class="align-centerfill-height mx-auto"
      max-width="900"
    >

      <div class="text-center">
        <div class="text-body-2 font-weight-light mb-n1">Welcome to</div>

        <h1 class="text-h2 font-weight-bold">NMSUandMe</h1>
      </div>

      <div class="text-center">
        <v-btn @click="goToSignUp">Sign Up</v-btn>
        <v-btn class="ml-4" @click="goToLogin">Login</v-btn>
      </div>


      <div class="py-4" />

    </v-responsive>
  </v-container>
</template>

<script setup>
  import {useRouter} from 'vue-router'
  const router = useRouter()

  const goToSignUp = () =>{
    router.push('/signup')
  }
  const goToLogin = () =>{
    router.push('/login')
  }
</script>
