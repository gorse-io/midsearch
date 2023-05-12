<template>
    <v-container>
        <v-row class="justify-center">
            <v-card width="500px">
                <v-card-text>
                    <v-form>
                        <v-text-field v-model="username" label="Username" required></v-text-field>
                        <v-text-field v-model="password" label="Password" required type="password"></v-text-field>
                    </v-form>
                    <v-alert v-if="message" color="error" :text="message"></v-alert>
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
            password: '',
            message: ''
        }
    },
    methods: {
        login() {
            if (this.username === '') {
                this.message = 'Username is required';
                return;
            }
            if (this.password === '') {
                this.message = 'Password is required';
                return;
            }
            var formData = new FormData();
            formData.append('username', this.username);
            formData.append('password', this.password);
            axios.post('/api/login/', formData).then(() => {
                this.$router.push('/');
            }).catch((error) => {
                this.message = error.response.data;
            })
        }
    }
}
</script>