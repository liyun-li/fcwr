$('#waitlist').ready(() => {
	// get /tutorial and display to #waitlist
	axios.get('/tutorial').then(response => {
		const data = response.data;
		$('#waitlist').text(data);
	});
});


$(document).ready(function() {
	var self_gender;
	var prefer_gender;

	[$("#self-female"),$("#self-male"),$("#prefer-male"),$("#prefer-female")].forEach(function(elem){
		elem.css("opacity",".5");
	});

	$("#self-female").on('click',function(){
		$("#self-female").css("opacity","1");
		$("#self-male").css("opacity",".5");
		self_gender = "F";
	});
	$("#self-male").on('click',function(){
		$("#self-male").css("opacity","1");
		$("#self-female").css("opacity",".5");
		self_gender = "M";
	});
	$("#prefer-male").on('click',function(){
		$("#prefer-male").css("opacity","1");
		$("#prefer-female").css("opacity",".5");
		prefer_gender = "M";
	});
	$("#prefer-female").on('click',function(){
		$("#prefer-male").css("opacity",".5");
		$("#prefer-female").css("opacity","1");
		prefer_gender = "F";
	});

	$("#submit-btn").on('click',function(){
		if(prefer_gender && self_gender){
			$.ajax({
				type: "POST",
				url: "/setSexAndInterest",
				data:{
					sex:self_gender,
					interest:prefer_gender,
				},
				success:function(res){
					alert("success");
				},
				error:function(err){
					alert("err set sex" + err);
				},
	    	});
		}else{
			alert("you must select your gender and interest");
		}
	});
});