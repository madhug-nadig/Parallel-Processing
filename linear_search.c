#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "omp.h"

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

int linearSearch(int* A, int n, int tos){
	
	int foundat = -1;

	#pragma omp parallel for
	for(int iter =0; iter< n; iter++){
		if(A[iter] == tos)
			foundat = iter+1;
	}
	return foundat;
}