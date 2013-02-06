
AjaxQueue = function(timeout) {

    var que = {}; // this object

    var requests = [];

    que.t = timeout || 1000;
    que.tid = null;

    que.add = function (request) {
        // adds a request to the ajax queue
        requests.push(request);
    };

    que.remove = function (request) {
        if ($.inArray(request, requests) > -1) {
            requests.splice( $.inArray(request, requests), 1);
        }
    };

    que.run = function() {
        if (requests.length) {
            // if there are any requests
            // get the completion success attribute of the request
            var onComplete = requests[0].complete;

            requests[0].complete = function () {
                if (typeof onComplete === 'function') {
                    // call it
                    onComplete();
                }
                // pop off the first item
                requests.shift();
                // run more
                que.run();
            };

            $.ajax(requests[0]);
        } else {
            que.tid = setTimeout( function(){ que.run(); }, que.t);
        }
    };

    que.stop = function () {
        requests = [];
        clearTimeout(que.tid);
    };

    return que;
};



