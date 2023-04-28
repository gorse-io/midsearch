<template>
    <v-container>
        <v-row>
            <v-col cols="12">
                <v-expansion-panels>
                    <v-expansion-panel v-for="conversation in conversations">
                        <v-expansion-panel-title>
                            {{ conversation.question }}
                        </v-expansion-panel-title>
                        <v-expansion-panel-text>
                            <article class="markdown-body" v-html="conversation.answer"></article>
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
    }
}
</script>
