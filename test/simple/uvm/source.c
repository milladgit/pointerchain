
#include <stdlib.h>

#define N 10000

int main() {
	double *arr;

	arr = (double*) malloc(sizeof(double) * N);

	#pragma acc parallel loop 
	for(int i=0;i<N;i++) {
		arr[i] = i;
	}

	return arr[0]*arr[N-1] != 0;
}

