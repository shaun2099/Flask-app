const app = Vue.createApp({
	// template: '<h2>I am template</h2>'
	data() {
		return {
			title: 'The Final Empire',
			author: 'Brandon',
			age: 34,
			url: 'http://www.google.com.sg'
		}
	},
	methods: {
		changeTitle() {
			this.title = "Title"
		},
		handleEvent(e) {
			console.log(e)
		}
	}
})

app.mount('#app')