<template>
    <v-container>
        <v-row>
            <v-col cols="12">
                <v-expansion-panels>
                    <v-expansion-panel v-for="[index, document] in documents.entries()">
                        <v-expansion-panel-title>
                            {{ document.id }}
                            <template v-slot:actions>
                                <v-icon color="primary" icon="mdi-language-markdown">
                                </v-icon>
                            </template>
                        </v-expansion-panel-title>
                        <v-expansion-panel-text>
                            <v-row v-for="chunk in document.chunks">
                                <v-col>
                                    <v-card>
                                        <v-card-item>
                                            <v-chip color="primary">
                                                <v-icon start icon="mdi-alpha-a"></v-icon>
                                                {{ chunk.token_count }}
                                            </v-chip>
                                        </v-card-item>
                                        <v-card-text>
                                            <article class="markdown-body" v-html="chunk.content"></article>
                                        </v-card-text>
                                    </v-card>
                                </v-col>
                            </v-row>
                            <v-row>
                                <v-col>
                                    <v-btn prepend-icon="mdi-delete" color="warning" size="small" variant="text">
                                        Delete
                                    </v-btn>
                                </v-col>
                            </v-row>
                        </v-expansion-panel-text>
                    </v-expansion-panel>
                </v-expansion-panels>
            </v-col>
        </v-row>
        <v-row class="justify-center">
            <v-pagination v-model="page_num" :length="page_count" :total-visible="7" rounded="circle"
                @click="pageChange"></v-pagination>
        </v-row>
    </v-container>
</template>

<script>
import axios from 'axios';

export default {
    name: "History",
    data() {
        return {
            documents: [],
            page_count: 0,
            page_num: 1,
        }
    },
    mounted() {
        axios.get('/api/documents/', {
            params: {
                n: 20,
            }
        })
            .then(response => {
                this.documents = response.data
            })
            .catch(error => {
                console.log(error)
            })
        axios.get('/api/documents/count')
            .then(response => {
                this.page_count = Math.ceil(response.data / 20)
            })
            .catch(error => {
                console.log(error)
            })
    },
    methods: {
        accept: function (index) {
            var formData = new FormData();
            formData.set('helpful', true);
            axios.post('/api/conversation/' + this.conversations[index]['id'], formData)
                .then(response => {
                    this.conversations[index]['helpful'] = true
                })
                .catch(error => {
                    console.log(error)
                })
        },
        reject: function (index) {
            var formData = new FormData();
            formData.set('helpful', false);
            axios.post('/api/conversation/' + this.conversations[index]['id'], formData)
                .then(response => {
                    this.conversations[index]['helpful'] = false
                })
                .catch(error => {
                    console.log(error)
                })
        },
        pageChange: function () {
            axios.get('/api/documents/', {
                params: {
                    n: 20,
                    offset: (this.page_num - 1) * 20,
                }
            })
                .then(response => {
                    this.documents = response.data
                })
                .catch(error => {
                    console.log(error)
                })
        }
    }
}
</script>
