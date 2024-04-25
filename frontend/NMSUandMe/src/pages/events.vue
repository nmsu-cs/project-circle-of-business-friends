<template>
    <userPortalLayout :profileClicked="goToProfile" :matchesClicked="goToMatches" :eventsClicked="goToEvents"
        :logoutClicked="logout">
        <template #buttons>
            <v-btn @click="goToProfile">Profile</v-btn>
            <v-btn @click="goToMatches">Matches</v-btn>
            <v-btn @click="goToUserPortal">User Portal</v-btn>
            <v-btn @click="logout">Logout</v-btn>
        </template>

        <v-container class="text-center">
            <h1>Welcome to Events</h1>
        </v-container>
        <v-container class="text-center">
            <v-carousel>
                <v-carousel-item v-for="(event, index) in events" :key="index">
                    <v-row align="center" class="fill-height">
                        <v-col cols="12">
                            <v-card class="mx-auto" max-width="500">
                                <v-card-title>
                                    {{ event.host }}
                                </v-card-title>
                                <v-card-text>
                                    <p>{{ event.location }}</p>
                                    <p>{{ event.start_date }}</p>
                                    <p>{{ event.end_date }}</p>
                                    <p>{{ event.desc }}</p>
                                    <p> {{event.url}}</p>
                                </v-card-text>
                                <v-card-actions>
                                    <v-container class="text-center">
                                    </v-container>
                                </v-card-actions>
                            </v-card>
                        </v-col>
                    </v-row>
                </v-carousel-item>
            </v-carousel>
        </v-container>
    </userPortalLayout>
</template>

<script setup>
import userPortalLayout from '@/layouts/userPortalLayout.vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const user_id_temp = ref(null)
const router = useRouter()
const path = "http://localhost:5000/events"

const events = ref(null)

onMounted(() => {
    user_id_temp.value = router.currentRoute.value.query.user_id
    const path_withparameters = `${path}?user_id=${user_id_temp.value}`

    axios.get(path_withparameters)
        .then(response => {
            events.value = response.data.data
            console.log(response.data.data)
        })
        .catch(error => {
            console.log(response.data)
        })
})

const goToProfile = () => {
    const user_id = user_id_temp.value
    router.push({ path: '/profile', query: { user_id }, })
}

const goToMatches = () => {
    const user_id = user_id_temp.value
    router.push({ path: '/matches', query: { user_id }, })
}

const goToUserPortal = () => {
    const id = user_id_temp.value
    router.push({ path: '/user_portal', query: { id }, })
}

const logout = () => {
    // Your logout logic here
}
</script>