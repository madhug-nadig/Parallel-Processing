	function compute(){
		if (window.Worker) { // Check if the Browser supports the Worker api.
			// Requires script name as input
			var worker = new Worker("task.js");

			worker.postMessage([0.554,2]); // Sending message as an array to the worker
			console.log('Message posted to worker');

			worker.onmessage = function(e) {
				console.log(e.data);
				document.getElementById("result").innerHTML = e.data;
				console.log('Message received from worker');
			};
		}
	}
	