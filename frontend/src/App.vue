<template>
  <v-app>
    <v-navigation-drawer app permanent>
      <v-list density="compact" nav>
        <v-list-item v-for="item in items" :key="item.title" :prepend-icon="item.icon" :title="item.title"></v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-app-bar app color="primary" dark>
    </v-app-bar>

    <v-main>
      <v-container>
        <v-row>
          <v-col cols="12">
            <v-text-field v-model="message" append-icon="mdi-magnify" variant="filled" label="Search" type="text"
              @click:append="search"></v-text-field>
          </v-col>
        </v-row>
        <v-row v-for="result in results" :key="result">
          <v-col>
            <v-card :text="result"></v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      query: '',
      results: [],
      version: '',
      items: [
        { title: 'Search', icon: 'mdi-magnify', link: '/' },
      ]
    }
  },
  methods: {
    search() {
      this.results = ['A','C'];
    }
  }
}
</script>
