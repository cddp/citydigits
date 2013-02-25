/* module for extending javascript 'classes' to suit the particulars of the
 * lottery app.
 */


/*
// an example of extending a model
*/

var Interview = function (model) {
    model.toGeoJson = function () {
        var gj = {};
        var point = model.data.point;
        delete model.data.point;
        gj.properties = model.data;
        gj.geometry = {
            type:"Point",
            coordinates:[ point['lng'], point['lat'] ],
        };
        gj.id = model.id;
        gj.type = 'Feature';
        return gj;
    };

    return model
}

function flatten (items) {
    for (var i=0; i<items.length; i++){
        items[i] = items[i].flat();
    }
    return items;
}

function interviewContext (uuid) {
    // get the correct interview
    var interview = models.table.interview.getBy("uuid", uuid).flat();
    console.log("got an interview object");
    console.log(interview);
    // get all its photos
    interview.photos = flatten(interview.getChildren("photo"));
    // get all the questions
    var questions = models.table.question.items;
    // for each question:
    for (var i=0; i<questions.length; i++){
        var question = questions[i];
        // get the notes and
        // find the ones for this interview
        var notes = interview.getChildrenFromList(question.getRelated("note"));
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
    }
    return {
        "interview": interview,
        "questions":flatten(questions),
    };
}









