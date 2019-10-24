
#include <stdlib.h>

typedef struct {
	int n2;
	double *arr2;
	double coeff2;	
} mainstruct_lev2_t;

typedef struct {
	int n;
	mainstruct_lev2_t *arr;
	double coeff;
} mainstruct_t;

#define N 10000

int main() {
	mainstruct_t *main_p;

	main_p = (mainstruct_t*) malloc(sizeof(mainstruct_t));
	main_p->arr = (mainstruct_lev2_t*) malloc(sizeof(mainstruct_lev2_t));

	main_p->arr->n2 = N;
	main_p->arr->arr2 = (double*) malloc(sizeof(double) * main_p->arr->n2);

	#pragma pointerchain declare(main_p->arr->n2{int}, main_p->arr->arr2{double*:restrictconst})

	#pragma pointerchain region begin
	#pragma acc parallel loop copy(main_p->arr->arr2[0:main_p->arr->n2]) gang vector
	for(int i=0;i<main_p->arr->n2;i++) {
		main_p->arr->arr2[i] = i;
	}
	#pragma pointerchain region end

	return main_p->arr->arr2[0] * main_p->arr->arr2[N-1] != 0;
}
