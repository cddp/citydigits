/* setup call backs
 *
 *
 */


// test the tap on map
var theMap = $('#map');
Tap.enableTap(theMap);

theMap.on('tap', function(e){
    console.log('tapped!');
    console.log(e);
});




var mh = 26;
var mw = 26;
var sh = 10;
var sw = 4;

function markerMouse(e){
        var x = e.offsetX - 11;
        var y = e.offsetY - (mh + sh);
        e.data.g.attr('transform', 'translate('+x+', '+y+')');
}

function addInterviewAndMarker(e) {
            // get the new location
            var x = e.offsetX;
            var y = e.offsetY;
            var point = new MM.Point(x, y);
            // convert the point to geographic coordinates
            var geopoint = map.pointLocation(point);
            // make the new interview
            var obj = {}; 
            obj.point = {
                'lng':geopoint['lon'],
                'lat':geopoint['lat'],
            };
            console.log(obj);
            var interview = Interview(models.tables.interview.addOrEdit(obj));
            geoJson = interview.toGeoJson();
            interviewGeoJsons.push(geoJson);
            var layer = map.getLayer('interviews');
            layer.data(interviewGeoJsons);
            layer.draw();
            finishAddingInterview(e.data.control, e.data.contents);
}

function finishAddingInterview(control, contents){
        $('body').off('mousemove', '#contents', markerMouse);
        $('body').off('click', '#contents', addInterviewAndMarker);
        $('.new_marker').remove();
        control.removeClass('addingpoint');
        control.addClass('addpoint');
        control.html(contents);
}

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
});


// for adding points
$('.user_controls').on('click', '.addpoint', {}, function(e){
    var control = $('.addpoint');
    var svg = $('.add_marker').clone();
    control.removeClass('addpoint');
    control.addClass('addingpoint');
    var contents = control.html();
    control.html('Select the location for the interview');
    svg.insertAfter($('#map'));
    svg.attr('class', 'new_marker');
    svg.attr('width', $('#map').innerWidth());
    // I don't know why I need to subtract 11 pixels here, but I 
    // couldn't find the cause
    svg.attr('height', $('#map').innerHeight() - 11);
    svg.css('position', 'relative');
    // attach svg to mouse
    var g = svg.find('g');
    // as the mouse moves follow it with the svg marker
    $('body').on('mousemove', '#contents', {'g':g}, markerMouse);
    $('body').on('click', '#contents', {
                        'g':g,
                        'control':control,
                        'contents':contents,
                    }, addInterviewAndMarker);
});

// for the photo thing, get make a new photo
$('.interview-column').on('click', '.addphoto', function(e){
    var thisNode = $(this);
    thisNode.removeClass('addphoto');
    thisNode.addClass('addingphoto');
    // save things
    var contents = thisNode.html();
    var h = thisNode.height();
    var w = thisNode.width(); 
    // set it to blank
    thisNode.html('');
    // append a snapshot button
    var button = $('<div class="camera button">Take Photo</div>');
    var videoBit = $('<video id="video" width="'+w+'" height="'+h+'" autoplay="" ></video>');
    // replace everything with a canvas
    var canvasBit = $('<canvas id="canvas" width="'+w+'" height="'+h+'"></canvas>');
    thisNode.append(videoBit);
    thisNode.append(canvasBit);
    thisNode.append(button);

    // this may need to chance for different browsers
    navigator.webkitGetUserMedia({'video':true}, function (stream) {
        console.log("getting user media");
        console.log(navigator.webkitGetUserMedia);
        console.log(stream);
        var objectURL = window.webkitURL.createObjectURL(stream);
        console.log("made a URL:");
        console.log(objectURL);
        video.src = objectURL;
        video.play();
        console.log("Told the video to play");
        console.log(video);
    }, function (error) {
        thisNode.html(contents);
    });
});

// set up photo snapshot listener
$('.interview-column').on('click', '.camera.button', function(e){
    var video = $('video');
    var canvas = $('canvas');
    var width = canvas.width();
    var height = canvas.height();
    var context = canvas[0].getContext('2d');
    context.drawImage(video[0], 0, 0);
    var imgUrl = canvas[0].toDataURL('image/jpg');
    // get the corresponding interview
    var classes = $('.interview.text').prop('class').split(' ');
    for (var i=0; i<classes.length; i++ ) {
        klass = classes[i];
        if (klass.indexOf('rid') !== -1) {
            var remote_id = parseInt(klass.split('rid')[1]);
            // this is the id
            console.log(remote_id);
            // no interviews are loaded locally, so this doesn't work
            var interview = models.tables.interview.getBy('remote_id', remote_id );
            // create base for photo object
            var obj = {
                interview: interview.data.uuid,
                url: imgUrl,
            };
            // save photo object to client data
            var photo = models.tables.photo.addOrEdit(obj);
            console.log(photo);
        }
    }
    
});

function closeQuoteInput (inputItem, uuid) {
    // just close things up
    var value = inputItem.val();
    var par = inputItem.parent('.quote');
    var other = par.find('.quote-text');
    if (other.length < 1) {
        // there was no other
        var other = $('<span class="quote-text"></span>');
        other.attr('uuid', uuid);
        other.insertBefore(inputItem);
    } else {
        other.show();
    }
    other.html(value);
    inputItem.remove();
}

$('.interview-column').on('keyup','input.answer-quote-input', function(e){
    // is this an existing quote?
    // either way save it
    var value = $(this).val();
    var par = $(this).parent('.quote');
    var uuid = par.attr('uuid');
    var audio = par.parent().prev();
    var audio_uuid = audio.attr('uuid');
    var obj = {
        'text':value,
        'uuid':uuid,
        'audio': audio_uuid,
    }
    // was the key the return key?
    if (e.keyCode == 13){
        // they hit return
        closeQuoteInput( $(this), uuid);
    }

}).on('blur', 'input.answer-quote-input', function(e){
    // if it's not empty
    var value = $(this).val();
    if (value !== "") {
        // if we lose focus, make it not a input
        // do the same as the return key
        closeQuoteInput( $(this));
    }
});

// the quote editing listener
$('.interview-column').on('click','.quote-text', function(e){
    // turn it into an input
    var value = $(this).html();
    var input = $('input.answer-quote-input').first().clone();
    input.val(value);
    input.attr('uuid', $(this).attr('uuid') );
    input.insertAfter($(this));
    $(this).hide();
    console.log('clicked on an existing quote');
});

}); // end of document ready
