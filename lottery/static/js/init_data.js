/* initialize data and models
 *
 * models.js framework should be loaded before this.
 */



function loadQuestions(){
    // have base questions
    var questions_en = [
    "How many NY Lotto tickets do you sell each week?",
    "What kinds of numbers do people pick?",
    "Do you play the lottery? Why or why not?",
    "Are there lottery regulars who buy tickets here?",
    "How many tickets do people usually buy?",
    "How much of the money (or what percentage of the money) that the store brings in for lottery tickets does the store get to keep?",
            ];
    var questions_es = [
    "Cuanto billetes vende usted cada semana?",
    "Que tipos de numeros elige la genta?",
    "Juega usted la loteria? Por que o por que no?",
    "Hay gente que suele venir aqui para jugar?",
    "Cuanto billetes suele comprar la gente?",
    "Que porcentaje de las ventas sobra para la tienda?"
            ];
    for (var i=0;i<questions_en.length;i++){
        var q = {};
        q.en = questions_en[i];
        q.es = questions_es[i];
        var m = models.tables.question.addOrEdit(q);
    }
}
function hasGetUserMedia() {
  // Note: Opera is unprefixed.
  return !!(navigator.getUserMedia || navigator.webkitGetUserMedia ||
            navigator.mozGetUserMedia || navigator.msGetUserMedia);
}

function addPhoto(e){
    console.log(hasGetUserMedia());
    var onFailSoHard = function(e) {
        console.log('Reeeejected!', e);
      };

  // Not showing vendor prefixes.
  navigator.webkitGetUserMedia({video: true, audio: true}, function(localMediaStream) {
    var video = document.querySelector('video');
    video.src = window.URL.createObjectURL(localMediaStream);

    video.onloadedmetadata = function(e) {
      // Ready to go. Do some stuff.
    };
  }, onFailSoHard);
}

function addAudio(e){
}

var models = Models(); // initialize the models global

$(document).ready(function(){

// add objects
models.addTable('interview', interviewObjects);
models.tables.interview.domContainers = $('#contents');
models.addTable('photo', []); // maybe prepopulated from server.
models.addTable('audio', []); // prepopulated from server
models.addTable('quote', []); // these refer to audio files
models.addTable('question', []); // prepopulated from server



loadQuestions();
// addPhoto();





});
