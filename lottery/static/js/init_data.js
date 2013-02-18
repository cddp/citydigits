/* initialize data and models
 *
 * models.js framework should be loaded before this.
 */

var models = Models(); // initialize the models global
// we also now have an ajaxQueue

$(document).ready(function(){

// add objects
models.addTable('interview', interviewObjects);
models.tables.interview.domContainers = $('#contents');
models.addTable('photo', photoJsons) // maybe prepopulated from server.
models.addTable('audio', audioJsons); // prepopulated from server
models.addTable('quote', quoteJsons); // these refer to audio files
models.addTable('question', questionJsons); // prepopulated from server

});
