/* module for extending javascript 'classes' to suit the particulars of the
 * lottery app.
 */


/*
// an example of extending a model
*/

var Interview = function (model) {
    model.toGeoJson = function () {
        var gj = {};
        var location = model.data.location;
        delete model.data.location;
        gj.properties = model.data;
        gj.geometry = {
            type:"Point",
            coordinates:[ location['lng'], location['lat'] ],
        };
        gj.id = model.id;
        gj.type = 'Feature';
        return gj;
    };

    return model
}











