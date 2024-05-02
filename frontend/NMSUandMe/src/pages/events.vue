<template>
    <userPortalLayout :userPortalClicked="goToUserPortal" :logoutClicked="logout">
        <template #buttons>
            <v-btn @click="goToUserPortal">User Portal</v-btn>
            <v-btn @click="logout">Logout</v-btn>
        </template>

        <v-container class="text-center">
            <h1>Welcome to Events</h1>
        </v-container>
        <v-container class="text-center" v-if="events">
            <v-carousel>
                <v-carousel-item v-for="(event, index) in events" :key="index">
                    <v-row align="center" class="fill-height">
                        <v-col cols="12">
                            <v-card class="mx-auto" max-width="500">
                                <v-card-title>
                                    {{ event.title }}
                                </v-card-title>
                                <v-card-text style="height:200px; overflow-y:scroll">
                                    <p>{{ event.host }}</p>

                                    <p>{{ event.location }}</p>
                                    <p>{{ event.start_date }}</p>
                                    <p>{{ event.end_date }}</p>
                                    <div v-if="!event.showFullDescription">
                                        <p>{{ truncateText(event.desc, 100) }}</p>
                                        <v-btn @click="toggleDesc(event)">Read More</v-btn>
                                    </div>
                                    <div v-else>
                                        <p>{{ event.desc }}</p>
                                        <v-btn @click="toggleDesc(event)">Read Less</v-btn>
                                    </div>
                                </v-card-text>
                                <v-card-actions>
                                    <v-container class="text-center">
                                        <v-btn :href="event.url" target="_blank">View Event</v-btn>
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

const truncateText = (text, maxLength) => { 
    if (text.length <= maxLength) { 
        return text;
    }

    return text.slice(0, maxLength) + "..."
}

const toggleDesc = (event) => { 
    event.showFullDescription = !event.showFullDescription
}

onMounted(() => {
    user_id_temp.value = router.currentRoute.value.query.user_id
    const path_withparameters = `${path}?user_id=${user_id_temp.value}`

    axios.get(path_withparameters)
        .then(response => {
            events.value = response.data.data.map(event => ({ 
                ...event,
                showFullDescription: false
            }))
            console.log(response.data.data)
        })
        .catch(error => {
            console.log(response.data)
        })
})

const goToUserPortal = () => {
    const id = user_id_temp.value
    router.push({ path: '/user_portal', query: { id }, })
}

const logout = () => {
    router.push('/')
}
</script>