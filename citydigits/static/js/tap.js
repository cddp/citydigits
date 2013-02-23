// This file is meant to create a touch tap event listener that can be used for
// firing callbacks.
//
// The thing I select needs to listen to touch events
// specifically touch start and touch end
// this requires jQuery

var Tap = (function(){
    tap = {};
    tap.touching = false;
    tap.lastTouchEvent = null;
    tap.enableTap = function (jq, subselector) {
        // set the touchstart listener
        jq.on('touchstart mousedown', subselector, function (e) {
            console.log('moused down');
            var cachedX = e.pageX;
            var cachedY = e.pageY;
            console.log( 'x:', cachedX, 'y:', cachedY);
            tap.touching = true;
            console.log('set touching to true');
            tap.lastTouchEvent = e;
            setTimeout(function(){
                console.log('timeout done');
                var currX = tap.lastTouchEvent.pageX;
                var currY = tap.lastTouchEvent.pageY;
                console.log('checking coords');
                console.log( 'x:', currX, 'y:', currY);
                var movedX = (Math.abs(cachedX - currX) > 1);
                var movedY = (Math.abs(cachedY - currY) > 1);
                console.log( 'moved? x:', movedX, 'y:', movedY);
                var stillTouching = tap.touching;
                console.log('still touching?:', stillTouching);
                // if the touching has ended within 200 ms, 
                // and is in the same place, fire the tap
                if ( !stillTouching && !movedX && !movedY ) {
                    var target = $(e.currentTarget);
                    console.log('triggering tap on:', target);
                    // fire the tap event
                    target.trigger('tap');
                }
            }, 200);
        });
        // set the touchend listener
        jq.on('touchend mouseup', subselector, function (e) {
            console.log('mouseup');
            console.log('set touching to false');
            tap.touching = false;
            tap.lastTouchEvent = e;
        });
        return jq;
    };

    return tap;

}());
