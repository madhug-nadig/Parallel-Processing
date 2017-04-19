	function compute(){
		if (window.Worker) { // Check if the Browser supports the Worker api.
			// Requires script name as input
			var worker = new Worker("three-hump-camel-function.js");

			worker.postMessage([0.554,2]); // Sending message as an array to the worker
			console.log('Message posted to worker');

			worker.onmessage = function(e) {
				console.log(e.data);
				document.getElementById("result").innerHTML = e.data;
				console.log('Message received from worker');
			};
		}
	}

	array= []
	for(i =12800; i > 0; i--){
		array.push(Math.round(Math.random()*1000));
	}

	a = performance.now();
	bothsort();
	b = performance.now();
	document.getElementById("time").innerHTML = b-a;

	a = performance.now();
	mergeSort(array);
	quickSort(array, 0, array.length-1);
	b = performance.now();
	console.log(b-a)
	document.getElementById("time2").innerHTML = b-a;

	
	function bothsort(){
		if (window.Worker) { // Check if the Browser supports the Worker api.
			// Requires script name as input
			var worker = new Worker("mergesort.js");
			var worker_2 = new Worker("quicksort.js");

			
			worker.postMessage(array); // Sending message as an array to the worker
			worker_2.postMessage(array); // Sending message as an array to the worker

			worker.onmessage = function(e) {
				console.log(e.data);
				document.getElementById("result").innerHTML = e.data;
				console.log('MergeSort Message received from worker');
			};
			worker_2.onmessage = function(e) {
				console.log(e.data);
				document.getElementById("result_2").innerHTML = e.data;
				console.log('QUickSort Message received from worker');
			};
		}
	}


	function mergeSort(arr){

	    if (arr.length < 2)
	        return arr;
	 
	    var middle = parseInt(arr.length / 2);
	    var left   = arr.slice(0, middle);
	    var right  = arr.slice(middle, arr.length);
	 
	    return merge(mergeSort(left), mergeSort(right));
	}
	 
	function merge(left, right){
	    var result = [];
	 
	    while (left.length && right.length) {
	        if (left[0] <= right[0]) {
	            result.push(left.shift());
	        } else {
	            result.push(right.shift());
	        }
	    }
	 
	    while (left.length)
	        result.push(left.shift());
	 
	    while (right.length)
	        result.push(right.shift());
	 
	    return result;
	}
	 


	function swap(items, firstIndex, secondIndex){
	    var temp = items[firstIndex];
	    items[firstIndex] = items[secondIndex];
	    items[secondIndex] = temp;
	}

	function partition(items, left, right) {

	    var pivot   = items[Math.floor((right + left) / 2)],
	        i       = left,
	        j       = right;


	    while (i <= j) {

	        while (items[i] < pivot) {
	            i++;
	        }

	        while (items[j] > pivot) {
	            j--;
	        }

	        if (i <= j) {
	            swap(items, i, j);
	            i++;
	            j--;
	        }
	    }

	    return i;
	}

	function quickSort(items, left, right) {

	    var index;

	    if (items.length > 1) {

	        index = partition(items, left, right);

	        if (left < index - 1) {
	            quickSort(items, left, index - 1);
	        }

	        if (index < right) {
	            quickSort(items, index, right);
	        }

	    }

	    return items;
	}
