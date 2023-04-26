<template>
	<v-container>
		<v-row>
			<v-col cols="12">
				<v-text-field v-model="message" append-icon="mdi-send" variant="filled" label="Chat" type="text"
					@click:append="send"></v-text-field>
			</v-col>
		</v-row>
		<v-row>
			<v-col v-if="waiting">
				<v-progress-linear indeterminate color="yellow-darken-2"></v-progress-linear>
			</v-col>
			<v-col v-if="reply">
				<v-card>
					<v-card-text class="markdown-body" v-html="reply"></v-card-text>
				</v-card>
			</v-col>
		</v-row>
	</v-container>
</template>

<script>
import axios from 'axios';

export default {
	name: "Chat",
	data() {
		return {
			message: "",
			reply: "",
			waiting: false
		};
	},
	methods: {
		send() {
			if (this.message === "") {
				this.reply = '';
				return;
			}
			this.reply = '';
			this.waiting = true;
			axios.get("/api/chat/", {
				params: {
					message: this.message
				}
			}).then((response) => {
				this.reply = response.data;
				this.waiting = false;
			}).catch((error) => {
				console.log(error);
			});
		}
	},
}
</script>
