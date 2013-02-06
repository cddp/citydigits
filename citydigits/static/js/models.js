
var ModelInstance = function(table, obj){
	// for each individual object
	obj.table = table; // points to the ModelTable for this object
	obj.selector = '.id'+obj.id+'.'+obj.table.className; // example: ".id3.interview"

	obj.getDomElements = function(selector){
		// returns the html pieces that represent this object
		// optional selector to filter further
		if (selector){
			return $(obj.selector).filter(selector);
		} else {
			return $(obj.selector);
		}
	};

	obj.remoteSync = function(url, callback){
		// does an ajax call to a remore server, using the input url
		// the object sends itself as the post data
		// the url is intended to be an add-or-edit api
		// 'deleting' is equivalent to editing
		// the callback is called with the response upon completion
	};

	return obj;
}

var ModelTable = function(name, className, items, domContainers){
	// for a set of objects
	var modelTable = {};
	modelTable.name = name; // example "interviews"
	modelTable.className = className; // example "interview"
	// set items
	modelTable.items = {};
	// build up items
	// an optional list of html pieces that contain lists of elements
	// in these containers would be searched in order to obtain html
	// representations of objects.
	// domContainers should be a jQuery selection
	modelTable.domContainers = domContainers;

	modelTable.deletedItems = []; // because we won't actually delete things

	// methods
	modelTable.add = function(obj){
		// add an object to this model table
		// check to see if it is a model instance
		if (obj.hasOwnProperty('table')){
			// add the item using it's id
			modelTable.items[obj.id] = obj;
		} else {
			// convert it to a model instance
			var model = ModelInstance(modelTable, obj);
			// then add it
			modelTable.items[model.id] = model;
	};
	
	

	modelTable.edit = function(obj){
		// use the input object's id to update the existing object instance
		modelTable.items[obj.id] = obj;
	};

	modelTable.getBy = function(key, value){
		// grab an item from the table based on an attribute value
		for (var i = 0; i < modelTable.items.length; i++){
			var item = modelTable.items[i];
			if (item[key] == value){
				return item;
			}
		}
		return null;
	};

	modelTable.getDomElements = function(){
		// gets all the html representing all the items in this table
		return modelTable.domContainers.find('.'+modelTable.className);
	}

	modelTable.remove = function(objId){
		// move this item to the deleted list
		var obj = modelTable.items[objId];
		// get dom objects and remove them.
		modelTable.domContainers.find('.id'+objId+'.'+obj.className).remove();
	};

	modelTable.listen = function( preselector, events, selector, handler, data ){
		// uses jQuery's ".on()" to delegate events.
		if (preselector){
			modelTable.domContainers.filter(preselector).on(events, selector, data, handler);
		} else {
			modelTable.domContainers.on(events, selector, data, handler);
		}
	};

	return modelTable
}

var Models = function( data ){
	// data should be a json object of the form:
	//		{
	//		 "model1":{
	//			"className": "name",
	//			"domContainers": [],
	//			"items": [ item, item, ...],
	//			},
	//		 "model2":{
	//			"className": "name",
	//			"domContainers": [],
	//			"items": [ item, item, ...],
	//			},
	//		 ...
	//		}
	var models = {};

	return models;
}


