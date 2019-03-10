$('#waitlist').ready(() => {
	const setDatetime = () => {
		const d = new Date();
		const display = d.toLocaleTimeString();
		$('#waitlist').text(display);
		console.log(display);
	};

	const timer = setInterval(setDatetime, 1000);
});
