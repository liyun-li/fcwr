$('#waitlist').ready(() => {
	// get /tutorial and display to #waitlist
	axios.get('/tutorial').then(response => {
		const data = response.data;
		$('#waitlist').text(data);
	});
});
