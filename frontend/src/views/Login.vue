<template>
    <v-container>
        <v-row class="justify-center">
            <v-card width="500px">
                <v-card-text>
                    <v-form>
                        <v-text-field v-model="username" label="Username" required></v-text-field>
                        <v-text-field v-model="password" label="Password" required type="password"></v-text-field>
                    </v-form>
                </v-card-text>
                <v-card-actions>
                    <v-btn @click="login" variant="text" color="primary" block>Login</v-btn>
                </v-card-actions>
            </v-card>
        </v-row>
    </v-container>
</template>

<script>
import axios from 'axios';

export default {
    data() {
        return {
            username: '',
            password: ''
        }
    },
    methods: {
        login() {
            axios.post('/api/login/', {
                username: this.username,
                password: this.password
            }).then((response) => {
                this.$store.commit('setToken', response.data.token);
                this.$store.commit('setUsername', this.username);
                this.$router.push('/');
            }).catch((error) => {
                console.log(error);
            })
        }
    }
}
</script>