/* initialize data and models
 *
 * models.js framework should be loaded before this.
 */

var models = Models(); // initialize the models global
// we also now have an ajaxQueue

$(document).ready(function(){

// add objects
models.addTable('interview', interviewJsons);
models.tables.interview.domContainers = $('#contents');
models.addTable('photo', photoJsons); 
models.addTable('audio', audioJsons); 
models.addTable('quote', quoteJsons); 
models.addTable('note', noteJsons); 
models.addTable('question', questionJsons);

});




