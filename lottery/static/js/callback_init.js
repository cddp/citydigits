/* setup call backs
 *
 *
 */

$(document).ready(function(){
// for the description, change the description of the interview
models.tables.interview.listen(null, 'input', '.edit-description input',
    function(e){
        // get the id of this interview
        var id=0;
        // get the new description value
        var value = $(this).val();
        // get the interview
        var interview = models.tables.interview.items[id];
        // set the desciption to this value
        interview.data.description = value;
        // mark the interview as dirty for updates
        interview.is_dirty = true;
        console.log(interview);
});



// for the photo thing, get make a new photo
$('.addphoto').click(function(e){
    var thisNode = $(this);
    // save things
    var contents = thisNode.html();
    var h = thisNode.height();
    var w = thisNode.width(); 
    // set it to blank
    thisNode.html('');
    // append a snapshot button
    var button = $('<div class="camera button">Take Photo</div>');
    var videoBit = $('<video id="video" width="'+w+'" height="'+h+'" autoplay="" ></video>');
    thisNode.append(button);
    thisNode.append(videoBit);
    // replace everything with a canvas
    var canvasBit = $('<canvas id="canvas" width="'+w+'" height="'+h+'"></canvas>');
    thisNode.append(canvasBit);
    var canvas = document.getElementById("canvas");
    var video = document.getElementById("video");
    var context = canvas.getContext("2d");
    navigator.webkitGetUserMedia({'video':true}, function (stream) {
        console.log(stream);
        var objectURL = window.webkitURL.createObjectURL(stream);
        video.src = objectURL;
        video.play();
    }, function (error) {
        thisNode.html(contents);
    });
});

}); // end of document ready
