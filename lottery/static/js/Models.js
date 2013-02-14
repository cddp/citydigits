/* a framework for handling client-side data for the city digits lottery
 * application.
 */

makeRandomUUID = function () {
    // this generates a UUID compliant with the RFC 4122 standard 
    // code is copied from http://stackoverflow.com/a/2117523/399726
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
        var r = Math.random()*16|0, v = c == 'x' ? r : (r&0x3|0x8);
        return v.toString(16);
    });
}

ModelInstance = function (table, id, obj) {
    /* ModelInstances are meant to be created by ModelTables
     * they are assigned an id upon creation, and they take an object literal
     * argument as their base data. The properties of the object literal are
     * merged with the ModelInstance.
     */
    console.log(obj);
    this.table = table; // points to the ModelTable for this object
    this.id = id; // set the local id
    // set the data as a property
    this.data = obj;
    // this is a flag that indicates if this should be synced
    this.is_dirty = false;
    if (obj.id) { // it's from the server
        console.log('adding remote id');
        // we are using both remote and uuids
        // it's redundant but it makes for nicer html
        this.data.remote_id = obj.id;
        // get all existing dom elements and assign the new id
        $('.rid' + obj.id + '.' + this.table.name).addClass('.id' + id);
    } else { // we're making a new thing locally
        // give it a uuid
        this.data.uuid = makeRandomUUID();
        // sync it with the database
        var request = this.buildAjaxRequest(function (response) {
            // set the remote_id to confirm it's presence 
            // in the remote database
            this.remote_id = response.id;
        });
    }
    // set properties
    this.selector = '.id' + id + '.' + this.table.name; // example: ".id3.interview"
};

ModelInstance.prototype = {
    // default properties and methods for ModelInstances
    id: null, // for storing this object's place in the table, a unique identifier
    // remote_id is used for syncing
    remote_id: null, // store it's identifier in a remote database
    data: null, // the data row object is stored here
    table: null, // the ModelTable this belongs to
    selector: null, // selector can be used to select html representations of this 
    // we won't actually delete things, we'll use is_deleted to filter them
    is_deleted: false,
    is_dirty: false,

    // get the dom elements that are associated with this object
    getDomElements: function (selector) {
        // returns the html pieces that represent this object
        // optional selector to filter further
        if (selector) {
            return $(this.selector).filter(selector);
        } else {
            return $(this.selector);
        }
    },

    getRelated: function (modelName) {
        // locally, foreign keys will be designated by UUIDs
        // We can assume this is okay here, because locally we won't do any
        // complicated lookups or joins. All lookups should be simple and
        // relation lookups are explicitly called by this method.
        var table = this.owner.tables[modelName];
        if (table) {
            // gets the UUID stored under the modelname
            var otherUUID = this.data[modelName];
            return table.getBy('uuid', otherUUID);
        }
        return null;
    },

    getChildren: function (modelName) {
        // this allows reverse foreign key lookups
        var table = this.owner.tables[modelName];
        if (table) {
            // find all the objects in modelname table
            // that have an attribute of this thing's table 
            // with a value of this thing's uuid
            return table.findMatching(this.table.name, this.uuid);
        }
        
        return [];
    },

    // generate an ajax request for this object.
    // This should maybe be called upon object creation.
    buildAjaxRequest: function (callback) {
        // callback is a function to call upon success of the ajax request
        // there is only one api method, and it is an add/edit
        // `deletion` is an edit to an existing thing, not an actual deletion
        var root = '/lottery/api/' + this.table.name + '/';
        // include remote id and deleted in the data
        var obj = this.data;
        obj.client_id = this.id;
        obj.is_deleted = this.is_deleted;
        return {
            type:'POST',
            url:'/lottery/api/' + this.table.name + '/',
            params: obj, // send this ModelInstance (is that smart?)
            success: callback, // set the response handler
        };
    },

    sync: function (queue) {
        var self = this;
        var request = this.buildAjaxRequest(function (response) {
            // set the remote_id to confirm it's presence 
            // in the remote database
            self.remote_id = response.id;
        });
        // not yet implemented
        queue.add(request);
    },
};

ModelTable = function (owner, name, items) {
    // for a set of objects
    // this.items must be declared here, otherwise it'd be a class attribute
    this.items = [];
    this.name = name; // example "interview"
    this.owner = owner; // owner is a Models object
    // build up items
    // an optional list of html pieces that contain lists of elements
    // in these containers would be searched in order to obtain html
    // representations of objects.
    // domContainers should be a jQuery selection
    this.domContainers = $('.container-' + name);
    for (var i=0; i<items.length; i++){
        this.add( items[i] )
    }
};

ModelTable.prototype = {
    // ModelTable methods and default properties

    owner:null,
    name:null,
    domContainers:null,

    // methods
    add: function (obj) {
        // add an object to this model table
        // get the next id for this object
        var id = this.items.length;
        // convert it to a model instance
        var model = new ModelInstance(this, id, obj);
        // then add it
        this.items[model.id] = model;
        return model;
    },
    
    edit: function (obj) {
        // use the input object's id to update the existing object instance
        this.items[obj.id] = obj;
    },

    getBy: function (key, value) {
        // grab an item from the table based on an attribute value
        for (var i = 0; i < this.items.length; i++) {
            var item = this.items[i];
            if (!item.is_deleted) { // make sure it hasn't been deleted
                if (item.data[key] == value) {
                    return item;
                }
            }
        }
        return null;
    },

    findMatching: function (key, value) {
        // get all items in this table whose key matches value
        var matches = [];
        for (var i = 0; i < this.items.length; i++) {
            var item = this.items[i];
            if (!item.is_deleted) { // make sure it hasn't been deleted
                if (item.data[key] == value) {
                    matches.push(item);
                }
            }
        }
        return matches;
    },

    getDomElements: function () {
        // gets all the html representing all the items in this table
        return this.domContainers.find('.' + this.name);
    },

    remove: function (objId) {
        // mark this item as deleted
        this.items[objId].is_deleted = true;
        // get dom objects and remove them.
        this.domContainers.find('.id' + objId + '.' + this.name).remove();
    },

    listen: function ( preselector, events, selector, handler, data ) {
        // uses jQuery's ".on()" to delegate events.
        // will 'this' in the handler refer to the ModelTable or the thing
        // clicked?
        if (preselector) {
            this.domContainers.filter(preselector).on(events, selector, data, handler);
        } else {
            this.domContainers.on(events, selector, data, handler);
        }
        return this;
    },

}

Models = function () {
    var models = {};
    models.tables = {};

    ajaxQueue = AjaxQueue();
    ajaxQueue.run();

    models.sync = function () {
        // search for unsynced items and sync them
        for (modelname in tables) {
            var table = models.tables[modelname];
            for (var i=0; i<table.items.length; i++){
                if (table.items[i].remote_id == null||table.items[i].is_dirty) {
                    table.items[i].sync(ajaxQueue);
                }
            }
        }
    };

    models.addTable = function (name, items) {
        models.tables[name] = new ModelTable(models, name, items);
    };
    return models;
};




