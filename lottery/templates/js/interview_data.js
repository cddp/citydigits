
var Models = function(){
	/* basically builds a sort of database with a set of tables
	*/
    var models = {};
	var models.collectObjs = function(modelSet, subModel){
		/* creates tables from arrays contained in objects.
		* assumes that all objects have an id propertie
		* and that arrays are arrays of objects.
		*/
		var things = {}
		for (i=0; i<modelSet.length; i++){
			var model = modelSet[i];
			if (model[submodel] instanceof Array){
				for (j=0; j<model[submodel].length, j++){
					var item = model[submodel][j];
					things[item.id] = item;
				}
			} else { // is a single object
				var item = model[submodel];
				things[item.id] = item;
			}
		}
		return arr;
	};
    var models.interviews = {{interviews}};
	var models.questions = {{questions}};
	var models.photos = models.collectObjs(models.interviews, 'photos');
	var models.audios = models.collectObjs(models.interviews, 'audios');
    var models.locations = models.collectObjs(models.interviews, 'location');
    var models.quotes = models.collectObjs(models.audios, 'quotes');
}

var models = Models();


