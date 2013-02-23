
AjaxQueue = function(timeout) {
    console.log('Instantiating Ajax Queue');

    var que = {}; // this object

    que.requests = [];

    que.t = timeout || 1000;
    que.timeoutId = null;

    que.state = 'stopped';
    que.stateChangeCallback = null;
    que.changeState = function (state) {
        que.state = state;
        // if there's a status change call back
        if (que.stateChangeCallback !== null ) {
            que.stateChangeCallback(que);
        }
    };

    que.add = function (request) {
        // adds a request to the ajax queue
        que.requests.push(request);
        console.log('adding a request to the queue.');
    };

    que.remove = function (request) {
        if ($.inArray(request, que.requests) > -1) {
            que.requests.splice( $.inArray(request, que.requests), 1);
        }
    };

    que.run = function() {
        if (que.requests.length) {
            que.changeState('sending');
            console.log('There are this many requests in the queue:');
            console.log(que.requests.length);
            // if there are any requests
            // get the success attribute of the request
            var request = que.requests.shift();
            console.log('Just shifted the queue, now there are', que.requests.length);
            var done = request.success;
            // pop off the first item
            console.log('about to call $.ajax');
            $.ajax(request);
            console.log('just called $.ajax');
            console.log('about to call run() again');
            que.run();
            console.log('just called run() again');
            // run more

        } else {
            // check for the thing is empty callback
            if (que.state !== 'empty'){
                que.changeState('empty');
            }
            que.timeoutId = setTimeout( function(){ que.run(); }, que.t);
        }
    };

    que.stop = function () {
        que.requests = [];
        clearTimeout(que.timeoutId);
        que.changeState('stopped');
    };

    return que;
};



