
#include <stdlib.h>

#define N 10000

int main() {
	double *p;

	p = (double*) malloc(sizeof(double) * N);
	double prag = 1.0;

	#pragma pointerchain declare(p{double*:restrictconst}, prag{double})

	#pragma pointerchain region begin
	#pragma acc parallel loop copy(prag,p[0:N])
	for(int i=0;i<N;i++) {
		p[i] = i * prag;
	}
	#pragma pointerchain region end

	return p[0]*p[N-1] != 0;
}

