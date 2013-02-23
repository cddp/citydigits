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
    tap.fireTaps = function (jq, subselector) {
        // set the touchstart listener
        jq.on('touchstart mousedown', subselector, function (e) {
            var cachedX = e.pageX;
            var cachedY = e.pageY;
            tap.touching = true;
            tap.lastTouchEvent = e;
            setTimeout(function(){
                var currX = tap.lastTouchEvent.pageX;
                var currY = tap.lastTouchEvent.pageY;
                var movedX = (Math.abs(cachedX - currX) > 1);
                var movedY = (Math.abs(cachedY - currY) > 1);
                var stillTouching = tap.touching;
                // if the touching has ended within 200 ms, 
                // and is in the same place, fire the tap
                if ( !stillTouching && !movedX && !movedY ) {
                    var target = $(e.currentTarget);
                    // fire the tap event
                    target.trigger('tap');
                }
            }, 200);
        });
        // set the touchend listener
        jq.on('touchend mouseup', subselector, function (e) {
            tap.touching = false;
            tap.lastTouchEvent = e;
        });
        return jq;
    };

    return tap;

}());
