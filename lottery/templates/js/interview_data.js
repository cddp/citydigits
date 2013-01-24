
var Models = function(){
	/* basically builds a sort of database with a set of tables
	*/
    var models = {};
	models.collectObjs = function(modelSet, subModel){
		/* creates tables from arrays contained in objects.
		* assumes that all objects have an id propertie
		* and that arrays are arrays of objects.
		*/
		var things = {};
		var item;
		for (i=0; i<modelSet.length; i++){
			var model = modelSet[i];
			if (model[subModel]){
				if (model[subModel] instanceof Array){
					for (j=0; j<model[subModel].length; j++){
						item = model[subModel][j];
						things[item.id] = item;
					}
				} else { // is a single object
					item = model[subModel];
					things[item.id] = item;
				}
			}
		}
		return things;
	};
	{% if interviewJsons and questionJsons %}
    models.interviews = {{interviewJsons}};
	models.questions = {{questionJsons}};
	models.photos = models.collectObjs(models.interviews, 'photos');
	models.audios = models.collectObjs(models.interviews, 'audios');
    models.locations = models.collectObjs(models.interviews, 'location');
    models.quotes = models.collectObjs(models.audios, 'quotes');
	{% endif %}
}

var models = Models();


