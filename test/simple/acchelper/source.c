
#include <stdlib.h>

#define N 10000

int main() {
	double *arr;

	arr = (double*) malloc(sizeof(double) * N);

	#pragma pointerchain declare(arr{double*:restrictconst})

	#pragma pointerchain region begin
	#pragma acc parallel loop copy(arr[0:N])
	for(int i=0;i<N;i++) {
		arr[i] = i;
	}
	#pragma pointerchain region end

	return arr[0]*arr[N-1] != 0;
}

