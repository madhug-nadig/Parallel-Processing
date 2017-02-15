#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "omp.h"

clock_t t, end;
double cpu_time_used;


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
	
	verify(Arr, number);

	printf("\nTime taken for sort: %f", cpu_time_used);
	return 0;

}

void selectionSort(int* A, int n){
	
	for(int startpos =0; startpos < n; startpos++){
		int minpos = startpos;
		#pragma omp parallel for
		for(int i=startpos +1; i< n; ++i){
			if(A[i] < A[minpos]){
				minpos = i;
			}
		}

		swap(&A[startpos], &A[minpos]);
	}
}


void verify(int* A, int n){
	int failcount = 0;
	for(int iter = 0; iter < n-1; iter++){
		if(A[iter] > A[iter+1]){
			//printf("\nSort fail\n");
			failcount++;
			//printf("%d and %d", A[iter], A[iter+1]);
		}
		//printf("\nSort success\n");
	}
	printf("\nFail count: %d\n", failcount);

}

void swap(int* a, int* b){
	int temp = *a;
	*a = *b;
	*b = temp;
}

