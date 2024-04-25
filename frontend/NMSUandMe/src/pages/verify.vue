<template>
    <v-container>
      <v-responsive class="align-center fill-height mx-auto" max-width="900">
        <v-card>
          <v-card-title class="text-h5">Verify Your Email</v-card-title>
          <v-card-text>
            <v-form @submit.prevent="submitVerificationCode">
              <v-text-field
                v-model="verificationCode"
                label="Verification Code"
                :rules="[rules.required]"
                outlined
                required
              ></v-text-field>
              <v-alert v-if="error" type="error" :value="true">
                {{ errorMessage }}
              </v-alert>
              <v-btn type="submit" color="primary">Verify</v-btn>
            </v-form>
          </v-card-text>
        </v-card>
      </v-responsive>
    </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import axios from 'axios';

const verificationCode = ref('');
const error = ref(false);
const errorMessage = ref('');
const userId = ref(null); // to store user id

const rules = {
  required: value => !!value || 'Required.',
};

const router = useRouter();
const route = useRoute();

onMounted(() => {
  userId.value = route.query.user_id; // get user_id from query parameter
});

const submitVerificationCode = async () => {
  const formData = new FormData();
  formData.append('vtoken', verificationCode.value);
  formData.append('user_id', userId.value); // + user_id in request

  try {
    const response = await axios({
      method: 'post',
      url: 'http://localhost:5000/verify',
      data: formData,
      headers: {'Content-Type': 'multipart/form-data' }
    });

    if (response.data.status === 'success') {
      // pass user id as query param to profile route
      router.push({path: '/profile', query: {user_id: userId.value}});
    } else {
      throw new Error(response.data.message);
    }
  } catch (err) {
    error.value = true;
    errorMessage.value = err.message || 'Verification failed, try again.';
  }
};
</script>
