onmessage = function(e) {
	console.log("Message received from main script.");

	// Implementing three hump camel function

	var x = e.data[0];
	var y = e.data[1];

	var result = (2*x*x) - (1.05*x*x*x*x) + (Math.pow(x,6)/6) + (x*y) + (y*y);

	var workerResult = "Result: " + result;
	console.log("Posting message back to main script.");
	postMessage(workerResult);
}
