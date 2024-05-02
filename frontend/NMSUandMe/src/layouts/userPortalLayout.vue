<template>
    <v-app>
      <v-app-bar app>
        <v-toolbar-title>NMSU&Me</v-toolbar-title>
        <v-spacer></v-spacer>
        <slot name="buttons"></slot>
      </v-app-bar>
      <v-main>
        <slot></slot>
      </v-main>
    </v-app>
  </template>
  
  <script setup>
import { defineProps } from 'vue'

const props = defineProps({
  profileClicked: Function,
  matchesClicked: Function,
  logoutClicked: Function,
  userPortalClicked: Function,
  eventsClicked: Function,
})
</script>
  
  <style>
  /* Add your layout styles here */
  </style>
  