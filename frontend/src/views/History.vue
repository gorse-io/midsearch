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
                                    <v-btn prepend-icon="mdi-message-arrow-right-outline" color="primary" size="small"
                                        variant="text">
                                        View Prompt
                                    </v-btn>
                                </v-col>
                            </v-row>
                        </v-expansion-panel-text>
                    </v-expansion-panel>
                </v-expansion-panels>
            </v-col>
        </v-row>
    </v-container>
</template>

<script>
import axios from 'axios';

export default {
    name: "History",
    data() {
        return {
            conversations: []
        }
    },
    mounted() {
        axios.get('/api/conversations/')
            .then(response => {
                this.conversations = response.data
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
    }
}
</script>
