<template>
    <v-app>
        <v-navigation-drawer app permanent v-if="$route.name != 'Login'">
            <v-list density="compact" nav>
                <v-list-item v-for="item in items" :key="item.title" :prepend-icon="item.icon" :title="item.title"
                    :to="item.link"></v-list-item>
            </v-list>
        </v-navigation-drawer>

        <v-app-bar app color="primary" dark>
            <v-spacer></v-spacer>
            <v-btn icon>
                <v-icon>mdi-exit-to-app</v-icon>
            </v-btn>
        </v-app-bar>

        <v-main>
            <router-view></router-view>
        </v-main>
    </v-app>
</template>

<script>
import axios from 'axios';
import router from './router';

export default {
    name: "App",
    data() {
        return {
            query: "",
            documents: [],
            version: "",
            items: [
                { title: "Home", icon: "mdi-home", link: "/" },
                { title: "Chat", icon: "mdi-chat", link: "/chat" },
                { title: "Search", icon: "mdi-magnify", link: "/search" },
                { title: "History", icon: "mdi-history", link: "/history" },
                { title: "Documents", icon: "mdi-file-document-outline", link: "/documents" },
            ]
        };
    },
    methods: {
        search() {
            if (this.query === "") {
                this.documents = [];
                return;
            }
            axios.get("/api/search/", {
                params: {
                    query: this.query
                }
            }).then((response) => {
                this.documents = response.data;
            }).catch((error) => {
                console.log(error);
            });
        }
    },
    components: { router }
}
</script>
