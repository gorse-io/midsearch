<template>
    <v-container>
        <v-row>
            <v-col cols="12">
                <v-expansion-panels>
                    <v-expansion-panel v-for="[index, conversation] in conversations.entries()">
                        <v-expansion-panel-title>
                            {{ conversation.question }}
                            <template v-slot:actions>
                                <v-icon v-if="conversation.helpful === true" color="teal" icon="mdi-check">
                                </v-icon>
                                <v-icon v-else-if="conversation.helpful === false" color="error" icon="mdi-close">
                                </v-icon>
                                <v-icon v-else-if="conversation.helpful === null" color="warning" icon="mdi-radiobox-blank">
                                </v-icon>
                            </template>
                        </v-expansion-panel-title>
                        <v-expansion-panel-text>
                            <v-row>
                                <v-col>
                                    <article class="markdown-body" v-html="conversation.answer"></article>
                                </v-col>
                            </v-row>
                            <v-row>
                                <v-col>
                                    <v-btn prepend-icon="mdi-check" color="teal" size="small" variant="text"
                                        @click="accept(index)">
                                        Accept
                                    </v-btn>
                                    <v-btn prepend-icon="mdi-close" color="error" size="small" variant="text"
                                        @click="reject(index)">
                                        Reject
                                    </v-btn>
                                    <v-btn prepend-icon="mdi-delete" color="warning" size="small" variant="text"
                                        @click="remove(conversation.id)">
                                        Delete
                                    </v-btn>
                                    <v-btn prepend-icon="mdi-content-copy" color="primary" size="small" variant="text"
                                        @click="copyToClipBoard(conversation.question)">
                                        Copy Question
                                    </v-btn>
                                    <v-dialog v-model="dialog" width="auto">
                                        <template v-slot:activator="{ props }">
                                            <v-btn prepend-icon="mdi-message-arrow-right-outline" color="primary"
                                                size="small" variant="text" v-bind="props">
                                                View Context
                                            </v-btn>
                                        </template>
                                        <v-card>
                                            <v-card-text>
                                                <article class="markdown-body" v-html="conversation.prompt"></article>
                                            </v-card-text>
                                            <v-card-actions>
                                                <v-btn color="primary" block @click="dialog = false">Close Dialog</v-btn>
                                            </v-card-actions>
                                        </v-card>
                                    </v-dialog>
                                </v-col>
                            </v-row>
                        </v-expansion-panel-text>
                    </v-expansion-panel>
                </v-expansion-panels>
            </v-col>
        </v-row>
        <v-row class="justify-center">
            <v-pagination v-model="page_num" :length="page_count" rounded="circle"></v-pagination>
        </v-row>
    </v-container>
</template>

<script>
import axios from 'axios';

export default {
    name: "History",
    data() {
        return {
            conversations: [],
            dialog: false,
            page_count: 0,
            page_num: 1,
        }
    },
    mounted() {
        axios.get('/api/conversations/count/')
            .then(response => {
                this.page_count = Math.ceil(response.data / 20);
            })
            .catch(error => {
                console.log(error)
            })
        this.loadPage();
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
        remove: function (id) {
            axios.delete('/api/conversation/' + id)
                .then(response => {
                    this.loadPage();
                })
                .catch(error => {
                    console.log(error)
                })
        },
        loadPage: function () {
            axios.get('/api/conversations/', {
                params: {
                    n: 20,
                    offset: (this.page_num - 1) * 20,
                }
            })
                .then(response => {
                    this.conversations = response.data
                })
                .catch(error => {
                    console.log(error)
                })
        },
        copyToClipBoard(text) {
            navigator.clipboard.writeText(text);
        },
    }
}
</script>
