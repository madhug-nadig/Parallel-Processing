#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "omp.h"

/*
OpenMP implementation example
Details of implementation/tutorial can be found here: http://madhugnadig.com/articles/parallel-processing/2017/02/25/parallel-computing-in-c-using-openMP.html
*/

clock_t t;
double cpu_time_used;

int linearSearch(int* A, int n, int tos);

int main(){

	int number, iter =0, find;
	int* Arr;

	Arr = (int *)malloc( number * sizeof(int));

	scanf("%d", &number);

	for(; iter<number; iter++){
		scanf("%d", &Arr[iter]);
	}
    
	scanf("%d", &find);
	printf("\nTo find: %d\n", find);

    t = clock();
	int indexx = linearSearch(Arr, number, find);
    t = clock()-t;
	
	if(indexx == -1){
		printf("Not found");
	}
	else
		printf("Found at %d\n", indexx);

	cpu_time_used = ((double)t)/CLOCKS_PER_SEC;

	printf("\nTime taken for search: %f", cpu_time_used);
	return 0;

}

// Linear serach beigns here
int linearSearch(int* A, int n, int tos){
	
	int foundat = -1;

	//Simple OpenMP for loop in parallel
	#pragma omp parallel for
	for(int iter =0; iter< n; iter++){
		if(A[iter] == tos)
			// DO not return since it will result in an invalid branch.
			foundat = iter+1;
	}
	// Return the index finally, after each and every element has been checked.
	return foundat;
}

