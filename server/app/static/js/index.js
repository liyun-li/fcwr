$('#waitlist').ready(() => {
	const socket = io.connect('http://' + document.domain + ':' + location.port);
	socket.on('connect', () => {
		socket.emit('get_queue', {});
	});
	socket.on('waitlist', data => {
		if ('queue' in data && data.queue > 0) {
			$('#waitlist').text(`#${data.queue}`);
		}
	});
});

$('#reload').click(() => location.reload());

$('#rematch').ready(() => {
	$('#rematch').click(() => {
		axios.get('/rematch').then(response => {
			if (response.status === 200) {
				// request successful, refresh
				location.reload();
			}
		});
	});
});

$('#gender-preference').ready(() => {
	let gender = '';
	let preference = '';

	const set_preference = () => {
		if (gender && preference) {
			axios.post('/set_preference', {
				gender,
				preference
			}).then(response => {
				if (response.status === 200) {
					// Yay, refresh
					location.reload();
				} else if (response.status === 403) {
					// Uh oh something went wrong
					alert(response.data);
				} else {
					// You shouldn't be here
					alert(response.data || 'Error. Please try again later');
				}
			});
		} else {
			alert('ERROR: You must select a gender and a preference');
		}
	}

	$('#gender-f').click(() => {
		gender = 'F';
		$('#gender-m').addClass('d-none');
	});

	$('#gender-m').click(() => {
		gender = 'M';
		$('#gender-f').addClass('d-none');
	});

	$('#preference-m').click(() => {
		preference = 'M';
		$('#preference-f').addClass('d-none');
	});

	$('#preference-f').click(() => {
		preference = 'F';
		$('#preference-m').addClass('d-none');
	});

	$('#set-preference').click(set_preference);
	$('#reset-preference').click(() => {
		gender = '';
		preference = '';
		$('#preference-f').removeClass('d-none');
		$('#preference-m').removeClass('d-none');
		$('#gender-f').removeClass('d-none');
		$('#gender-m').removeClass('d-none');
	});
});
