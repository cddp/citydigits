
AjaxQueue = function(timeout) {
    console.log('Instantiating Ajax Queue');

    var que = {}; // this object

    var requests = [];

    que.t = timeout || 1000;
    que.tid = null;

    que.add = function (request) {
        // adds a request to the ajax queue
        requests.push(request);
        console.log('adding a request to the queue.');
    };

    que.remove = function (request) {
        if ($.inArray(request, requests) > -1) {
            requests.splice( $.inArray(request, requests), 1);
        }
    };

    que.run = function() {
        if (requests.length) {
            console.log('There are this many requests in the queue:');
            console.log(requests.length);
            // if there are any requests
            // get the success attribute of the request
            var request = requests.shift();
            console.log('Just shifted the queue, now there are', requests.length);
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
            que.tid = setTimeout( function(){ que.run(); }, que.t);
        }
    };

    que.stop = function () {
        requests = [];
        clearTimeout(que.tid);
    };

    return que;
};



