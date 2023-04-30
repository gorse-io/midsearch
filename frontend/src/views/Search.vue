<template>
    <v-container>
        <v-row>
            <v-col cols="12">
                <v-text-field v-model="query" append-icon="mdi-magnify" variant="filled" label="Search" type="text"
                    @click:append="search"></v-text-field>
            </v-col>
        </v-row>
        <v-row v-for="document in documents">
            <v-col>
                <v-card>
                    <v-card-item>
                        <v-chip-group>
                            <v-chip>
                                <v-icon start icon="mdi-alpha-a"></v-icon>
                                {{ document.token_count }}
                            </v-chip>
                            <v-chip>
                                <v-icon start icon="mdi-sort-reverse-variant"></v-icon>
                                {{ document.score }}
                            </v-chip>
                        </v-chip-group>
                    </v-card-item>
                    <v-card-text class="markdown-body" v-html="document.page_content"></v-card-text>
                </v-card>
            </v-col>
        </v-row>
    </v-container>
</template>

<script>
import axios from 'axios';

export default {
    name: "Search",
    data() {
        return {
            query: "",
            documents: [],
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
}
</script>
