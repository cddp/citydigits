/*
For the moment, this will rely on one of three javascript libraries
jwerty, moustrap, or kibo.
I want this to be able to connect views, similar to a url configuration file,
but it needs to take the current context into account, and to work like a graph
with nodes and edges, in order to walk between views.

django deals with this by passing arguments (the request) into the view
function that allows the function to get access to the context.

I need to be able to pass arguments to the view functions that provide context

How might this be used later for ajax functions or the "choose your own
adventure" style of navigation?

A graph of options might be best as something stored in a database-like object.
I could do a simple key/value store in order to handle that sort of connection.

Can I inherit my view functions from another function, that processes and gives
access to a context?

What kinds of things do I want in the context?
	url
	window
	data
	event
	thing that was clicked (this)

events = {
action0:{
        context0: handlerA,
        context1: handlerB,
        context2: handlerC,
    },
action1
action2
action3
}

function handlerA ( context ){
}
*/

events = {
	'arrow_up': goTowardsGrid,
	'arrow_down': goTowardsMap,
	'arrow_right': nextInterview,
	'arrow_left': prevInterview,
	'space': nextInterview,
}



