/* setup call backs
 *
 *
 */


// test the tap on map
//Tap.fireTaps($('body'), '#contents');

//theMap.on('tap', function(e){
    //if (states.adding_point) {
    //}
//});




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
            console.log("object:", obj.point);
            // adding the object!
            var interview = Interview(models.tables.interview.addOrEdit(obj));

            // adjust the states
            states.selected_interview = interview.data.uuid;
            console.log("interview:", interview);
            console.log("uuid:", interview.data.uuid);

            // updating the layer
            geoJson = interview.toGeoJson();
            interviewGeoJsons.push(geoJson);
            var layer = map.getLayer('interviews');
            layer.data(interviewGeoJsons);
            layer.draw();

            // clean up
            $('body').off('mousemove', '#contents', markerMouse);
            $('body').off('click', '#contents', addInterviewAndMarker);
            $('.new_marker').remove();
            states.adding_point = false;
            e.data.control.removeClass('addingpoint');
            e.data.control.addClass('addpoint');
            e.data.control.html(e.data.contents);

            renderDetail(interview.data.uuid);
              
            // slide out the side panel
            pullOutDetail(geopoint);
}

function pullOutDetail(newcenter){

            var center = map.center();
            var height = $(map.parent).height();

            $('#map').animate({'width': '50%'},
                {
                done: function (){
                      console.log("showing interview");
                    $('.interview.text').show();
                    },
                duration: 500,
                step: function(now, fx){
                    // adjust the dimensions
                    var width = $(map.parent).width();
                    var dimensions = new MM.Point(width, height);
                    map.setSize(dimensions);

                    if (newcenter) {
                        // adjust the map center
                        var percent = Math.abs(now - fx.start)/Math.abs(fx.end - fx.start);
                        var dLat = (center.lat - newcenter.lat) * percent;
                        var dLon = (center.lon - newcenter.lon) * percent;
                        var tempCenter = new MM.Location( center.lat - dLat, center.lon - dLon );
                        map.setCenter( tempCenter );
                    }
                },
            });
}

function sendingLoop(){
    var statusBar = $('.sending');
    if (statusBar.length > 0){
        if (statusBar.html().indexOf('...') != -1){
            statusBar.html( statusBar.html() + '.');
        } else {
            statusBar.html( statusBar.html().replace('...',''));
        }
        setTimeout(sendingLoop, 400);
    }
}

function ajaxStateManager(que){
    if (que.state == 'sending'){
        $('.edit-mode-link').removeClass('edit-mode-link')
            .addClass('sending').html("Saving data ");
        sendingLoop();
    } else if (que.state == 'empty'){
        var statusBar = $('.sending');
        statusBar.removeClass('sending')
            .addClass('empty').html("Changes saved ...");
        statusBar.animate({"opacity":0}, 800,
                function(){
            statusBar.css('opacity', 1)
            statusBar.removeClass('empty')
                .addClass('edit-mode-link')
            .html('Stop editing interviews');
        });
    }
}

function renderDetail (interviewUUID) {
    var context = interviewContext( interviewUUID );
    $.extend(context, mustache_context);
    var textRender = $($.mustache(templates.interview, context, templates));
    textRender.hide();
    $('.interview.text').replaceWith(textRender);
    splitStyles();
}

// click may replace it with a form
// return updates the model and restores any display. May add a form.

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

function interviewContext (uuid) {
    console.log("getting the interview context");
    console.log("uuid:", uuid);
    // get the correct interview
    var interview = models.tables.interview.getBy("uuid", uuid);
    console.log("interview:", interview);
    // get all its photos
    console.log("getting photos");
    var relPhotos = interview.getChildren("photo");
    console.log("uuid:", uuid);
    console.log("photos:",relPhotos);
    interview.photos = flatten(relPhotos);
    if (interview.photos.length > 0) {
        // snap off the first item
        interview.main_photo = interview.photos.shift();
    } else {
        interview.main_photo = false;
    }
    // get all the questions
    var questions = models.tables.question.items;
    // for each question:
    for (var i=0; i<questions.length; i++){
        var question = questions[i];
        // get the notes and
        // find the ones for this interview
        var qnotes = question.getChildren("note");
        console.log('qnotes:',qnotes);
        var notes = interview.getChildrenFromList(qnotes);
        console.log('notes:',notes);
        question.notes = flatten(notes);
        // get the audios
        // find the ones for this interview
        var audios = interview.getChildrenFromList(question.getRelated("audio"));
        // for each audio
        for (var j=0; j<audios.length; j++){
            // get the quotes
            audios[j].quotes = flatten(audios[j].getChildren("quote"));
        }
        question.audios = flatten(audios);
        if (question.audios.length > 0) {
            question.main_audio = question.audios[0];
        } else {
            question.main_audio = false;
        }
    }
    var context = {
        "interview": interview.flat(),
        "questions":flatten(questions),
    };
    return context;
}




function dealWithNote(thing) {
    var isNew = thing.parent().attr('class').indexOf('new') !== -1;
    var interview = $('.interview.text').attr('uuid');
    var question = thing.parents('.question').attr('uuid');
    console.log(question);
    var value = thing.val();
    if (isNew) {
        var obj = {
            text: value,
            interview: interview,
            question: question,
        }
        thing.parent().removeClass('new');
        // update the id
        // update the uuid
    } else {
        var uuid = thing.parent().attr('uuid');
        var obj = models.tables.note.getBy('uuid', uuid);
        obj.data.interview = interview;
        obj.data.question = question;
        obj.data.text = value;
    }
    var note = models.tables.note.addOrEdit(obj, noteUpdateCallback);
    console.log("here's the value", value);
    console.log("grabbed note", note);
    console.log("text changed");
    // update the html
    updated = $($.mustache( templates.note, note.flat(), templates));
    newNote = $($.mustache( templates.note_new, {}, templates))
    thing.parent().replaceWith(updated);
    updated.after(newNote);
    newNote.children('input').focus();
    splitStyles();
}

function noteUpdateCallback(data){
    // this receives data back from the server
    var uuid = data['uuid'];
    var note = models.tables.note.getBy('uuid', uuid);
    // update the uuid of the note object
}

function mapMarkerClickHandler (e) {
    console.log("clicked on a marker");
    var data = $(this).parent().parent()[0].__data__;
    var uuid = data.properties.uuid;
    renderDetail( uuid );
    pullOutDetail();
}

//
//
//
// DOCUMENT READY FUNCTION
//
//
//
$(document).ready(function(){

models.ajaxQueue.stateChangeCallback = ajaxStateManager;

// check if we are on detail page or not
if (!states.detail_open){
    $('.interview.text').hide();
    $('#map').css('width', '100%');
} else {
    $('#map').css('width', '50%');
}

$('#contents').on('keyup','.interview-description-input', function(e){
    // did they press 'return'?
    if (e.keyCode == 13){
        var uuid = $('.interview.text').attr('uuid');
        console.log("here's the uuid:", uuid);
        var value = $(this).val();
        console.log("here's the value:", value);
        var interview = models.tables.interview.getBy('uuid', uuid);
        interview.data.description = value;
        console.log("grabbed interview", interview);
        models.tables.interview.addOrEdit(interview);
        console.log("description changed");
    }
});


// for adding points
$('.user_controls').on('click', '.addpoint', {}, function(e){
    // clear the interview text thing if it's open
    // and reset the map dimensions
    $('#map').css("width", "100%");
    $('.interview.text').css("margin-left", "0").hide();
    var height = $(map.parent).height();
    var width = $(map.parent).width();
    var dimensions = new MM.Point(width, height);
    map.setSize(dimensions);

    var control = $('.addpoint');
    var svg = $('.add_marker').clone();
    control.removeClass('addpoint');
    control.addClass('addingpoint');
    states.adding_point = true;
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
$('#contents').on('click', '.addphoto', function(e){
    console.log('.addphoto clicked');
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
    console.log('canvas appended');

    var userMediaCaller = (function () {
        if (navigator.getUserMedia){
            return navigator.getUserMedia;
        }
        if (navigator.webkitGetUserMedia){
            return navigator.webkitGetUserMedia;
        }
        console.log('no get user media');
    }());
    // alternative on iOS 6: 
    // <input type="file" accept="image/*" capture="camera">
    // <!-- Accept Multiple Images -->
    // <input type="file" accept="image/*" multiple>
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
$('#contents').on('click', '.camera.button', function(e){
    console.log("handling camera button click");
    var video = $('video');
    var canvas = $('canvas');
    var width = canvas.width();
    var height = canvas.height();
    var context = canvas[0].getContext('2d');
    context.drawImage(video[0], 0, 0);
    var imgUrl = canvas[0].toDataURL('image/jpg');
    // get the corresponding interview
    var uuid = $('.interview.text').attr('uuid');
    // create base for photo object
    var obj = {
        interview: uuid,
        url: imgUrl,
    };
    // save photo object to client data
    var photo = models.tables.photo.addOrEdit(obj);
    console.log("added photo locally");
    console.log(photo);
});

$('#contents').on('keyup keydown','input.answer-note-input', function(e){
    //console.log(e);
    if ($(this).val() !== ""){ // do nothing if empty
        if (e.keyCode == 13 && e.type == "keyup"){
            console.log("someone pressed return");
            dealWithNote($(this));
        } else if (e.keyCode == 9 && e.type == "keydown") {
            console.log("someone pressed tab down");
            dealWithNote($(this));
        }
    }
})

// the quote editing listener
$('#contents').on('click','.quote-text', function(e){
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
