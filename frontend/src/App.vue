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
            <v-text-field v-model="query" append-icon="mdi-magnify" variant="filled" label="Search" type="text"
              @click:append="search"></v-text-field>
          </v-col>
        </v-row>
        <v-row v-for="document in documents">
          <v-col>
            <v-card :text="document.page_content"></v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
import axios from 'axios';

export default {
  name: 'App',
  data() {
    return {
      query: '',
      documents: [],
      version: '',
      items: [
        { title: 'Search', icon: 'mdi-magnify', link: '/' },
      ]
    }
  },
  methods: {
    search() {
      if (this.query === '') {
        this.documents = [];
        return;
      }
      axios.get('/api/search/', {
        params: {
          query: this.query
        }
      }).then((response) => {
        this.documents = response.data;
      }).catch((error) => {
        console.log(error);
      });
    }
  }
}
</script>
