
$('.addphoto').click(function(e){
	var interview_id = $(this).parents('.interview').attr('id');
	// add a photo
	views.addInterviewPhoto(interview_id);
});

$('.delete-photo').click(function(e){
	// there is no delete photo button
	var photo_id = $(this).parents('.interview-photo-wrapper').attr('id');
	// delete the photo
	views.deletePhoto(photo_id);
});

$('.edit-description').click(function(e){
	// check and make sure it's not already being edited
	if ($(this).find('input')){
		  
		// change it into an edit field
		$(this).removeClass('edit-description');
		var current_value = $(this).html().trim();
		var input = $('<input class="interview-description-input" type="text" name="interview-description" placeholder=" Name, Retailer or Player, Place">');
		input.val(current_value);
		$(this).html(input);
		input.focus();

	}
	
});
// add or edit quote
// this needs to allow for changes to the existing quotes, for edits.
$('.answer-quote-input').change(function(e){
	var val = $(this).val();
	if ($(this).hasClass('new')){
		var audio_id = $(this).parent('.audio').attr('id');
		// add a quote
		views.addQuote(audio_id, quoteText);
	} else {
		var quote_id = $(this).attr('id');
		// edit the quote
		views.editQuote(quote_id, quoteText);
	}
});


$('.quote-delete').click(function(e){
	var quote_id = $(this).parents('.answer-quote').attr('id');
	// delete the quote
	views.deleteQuote(quote_id);
});

$('.record-button').click(function(e){
	var interview_id = $(this).parents('.interview').attr("id");
	var question_id = $(this).parents('.questionblock').attr("id");
	// add audio to question
	views.addAudioAnswer(interview_id, question_id);
});

$('.audio-delete').click(function(e){
	var audio_id = $(this).parents('.answer_audio').attr('id');
	// delete audio
	views.deleteAudio(audio_id);
});





