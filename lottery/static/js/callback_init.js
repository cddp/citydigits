/* setup call backs
 *
 *
 */
var description_input = $('<input class="interview-description-input" type="text" name="interview-description" placeholder=" Name, Retailer or Player, Place" >');

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
    // append a snapshot button
    // replace everything with a canvas


});
// for the quote thing, add a new quote
});
