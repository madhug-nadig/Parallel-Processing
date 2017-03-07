#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "omp.h"

/*
OpenMP implementation example
Details of implementation/tutorial can be found here: http://madhugnadig.com/articles/parallel-processing/2017/02/25/parallel-computing-in-c-using-openMP.html
*/

clock_t t, end;
double cpu_time_used;

// Structure for enabling reduction on the index of elements
struct Compare { int val; int index; };
// Custom reduction for finding hte index of the max element.
#pragma omp declare reduction(maximum : struct Compare : omp_out = omp_in.val > omp_out.val ? omp_in : omp_out)


void swap(int* a, int* b);
void selectionSort(int* A, int n);
void verify(int* A, int n);

int main(){

	int number, iter =0;
	int* Arr;

	Arr = (int *)malloc( number * sizeof(int));

	scanf("%d", &number);

	for(; iter<number; iter++){
		scanf("%d", &Arr[iter]);
	}
    
    t = clock();
	selectionSort(Arr, number);
    t = clock()-t;
	
	for(int iter=0; iter<number;iter++){
		printf("%d ", Arr[iter]);
	}

	cpu_time_used = ((double)t)/CLOCKS_PER_SEC;
	
	// Verify if the algorithm works as advised
	verify(Arr, number);

	printf("\nTime taken for sort: %f", cpu_time_used);
	return 0;

}

void selectionSort(int* A, int n){
	
	for(int startpos =0; startpos < n; startpos++){
		// Declare the structure required for reduction
		struct Compare max;
        // Initialize the variables
        max.val = A[startpos];
        max.index = startpos;

        // Parallel for loop with custom reduction, at the end of the loop, max will have the max element and its index.
        #pragma omp parallel for reduction(maximum:max)
		for(int i=startpos +1; i< n; ++i){
			if(A[i] > max.val){
				max.val = A[i];
				max.index = i;
			}
		}

		swap(&A[startpos], &A[max.index]);
	}
}

// Verification function
void verify(int* A, int n){
	int failcount = 0;
	for(int iter = 0; iter < n-1; iter++){
		if(A[iter] < A[iter+1]){
			failcount++;
		}
	}
	printf("\nFail count: %d\n", failcount);
}

//Swap function
void swap(int* a, int* b){
	int temp = *a;
	*a = *b;
	*b = temp;
}

