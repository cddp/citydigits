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











