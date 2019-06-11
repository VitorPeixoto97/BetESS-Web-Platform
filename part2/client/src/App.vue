
<template>
  <v-app>
   <router-view/>
   <notifications group="foo" />
  </v-app>
</template>

<script>
export default {
  name: 'App'
}
</script>