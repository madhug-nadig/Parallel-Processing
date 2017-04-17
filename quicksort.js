	onmessage = function(e) {
		console.log("Message received from main script.");

		// Implementing three hump camel function

		var arr = e.data;
		console.log(arr);
		result = quickSort(arr, 0, arr.length - 1);
		postMessage(result);
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


	// first call
