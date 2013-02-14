
function projectGeoToMap(coords){
    // this function projects a pair of geographic coords to 
    // the map window space
    var point = map.locationPoint({lat:coords[1],lon:coords[0]});
    return [point.x, point.y];
}

function geoJsonProject(geoJson){
    // this function takes a geojson point and returns
    // a point in the map window space
    return projectGeoToMap(geoJson.geometry.coordinates);
}

function d3GeoJsonLayer(className){
    /*
    This can be a basic layer that does default actions based on the geoJson
    assigned in layer.data()
    */
    var layer = {}, 
        collection; 
    // setup nodes and parent
    // this node will be appended to the map div by 
    // map.addLayer()
    var div = d3.select(document.body)
        .append("div")
        .attr("class", className);
    var svg = div.append('svg');
    var g = svg.append('g').attr('class', 'geoJsonLayer');

    // name the layer
    layer.name = className;

    layer.parent = div.node();
    layer.map = map;
    // these should be null by default
    layer.customDataFunction = null;
    layer.customDrawFunction = null;

    layer.drawPoints = function(radius){
        layer.features.attr('cy', function(d){ return geoJsonProject(d)[1];})
        .attr('cx', function(d){ return geoJsonProject(d)[0];})
        .attr('r', function(d){ return radius; });
    };
    layer.drawPaths = function(){
        // get d3's path drawing function
        var path = d3.geo.path().projection( projectGeoToMap );
		layer.features.attr("d", function(d){return path(d.geometry);});
    };

    layer.draw = function(){
        // adjust the svg to the layer
        svg.attr("width", layer.map.dimensions.x)
            .attr("height", layer.map.dimensions.y)
            .style("margin-left", "0px")
            .style("margin-top", "0px");
        // if these are points, draw circles
        if (layer.customDrawFunction == null){ // no special drawing function
            if (layer.featureType == 'Point'){
                // default radius is 7
                layer.drawPoints(7);
            } else {
                // but if they are not points, draw paths
                layer.drawPaths();
            }
        } else {
            layer.customDrawFunction(layer.features);
        }
    }; // end draw method

    layer.data = function(geoJsonOrFeatures){
        /* this method takes a geoJson or a list of geoJson features
           and resets layer.features and calculates bounds
        */
        if (geoJsonOrFeatures instanceof Array){
            // this ensures that it can take both a collection
            // and a list of features.
            collection = {"type":"FeatureCollection",
                "features":geoJsonOrFeatures};
            } else {
                collection = geoJsonOrFeatures;
        }
        // get the geometry type from the first feature
        layer.featureType = collection.features[0].geometry.type;
        if (layer.featureType == 'Point'){ // if we have points
            // bounds are [[left, bottom],[right,top]]
            layer.bounds = [
                [
                   d3.min(collection.features, function(f){
                       return f.geometry.coordinates[0]; }),
                   d3.min(collection.features, function(f){
                       return f.geometry.coordinates[1]; }),
                       ],
                [
                   d3.max(collection.features, function(f){
                       return f.geometry.coordinates[0]; }),
                   d3.max(collection.features, function(f){
                       return f.geometry.coordinates[1]; }),
                      ]
                      ]; // end point bounds
        } else { // if we have polygons or linestrings
            layer.bounds = d3.geo.bounds(collection);
        }
        // d3 setup
        if (layer.customDataFunction == null){ // no special drawing function
            // draw in the default way
            if (layer.featureType == 'Point'){ // if we have points
                layer.features = g.selectAll("circle")
                    .data(collection.features)
                    .enter()
                    .append("circle"); 
            } else { // if we have polygons or linestrings
                layer.bounds = d3.geo.bounds(collection);
                layer.features = g.selectAll("path")
                    .data(collection.features)
                    .enter()
                    .append("path");
            } // end feature setup
            return layer;
        } else { // there is a custom data function
            console.log( collection );
            return layer.features = layer.customDataFunction( g, collection);
        }
    }; // end of .data() method

    layer.extent = function() {
        // This method was called in the mapbox example, but doesn't seem to
        // do anything
        var ext = new MM.Extent(
                new MM.Location(layer.bounds[0][1], layer.bounds[0][0]),
                new MM.Location(layer.bounds[1][1], layer.bounds[1][0])
                );
    };
    layer.customDraw = function( drawFunction ){
        /* this method allows for setting a custom draw function
           the draw function must take the svg g element, and the geoJson
           collection for this layer
        */
        layer.customDrawFunction = drawFunction;
    };
    layer.customData = function( dataFunction ){
        /* this method allows for setting a custom data function
           the data function must take the svg g element, and the geoJson
           collection for this layer
           as an argument and must return a d3 selection
        */
        layer.customDataFunction = dataFunction;
    };
    layer.on = function(eventname, listener){
        /* this assigns a event listener to each of the features in this item
           and uses the eventname as the trigger.
       */
        layer.features.on(eventname, listener);
        return layer;
    }
    return layer;
}





