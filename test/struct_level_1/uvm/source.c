
#include <stdlib.h>

typedef struct {
	int n;
	double *arr;
	double coeff;
} mainstruct_t;

#define N 10000

int main() {
	mainstruct_t *main_p;

	main_p = (mainstruct_t*) malloc(sizeof(mainstruct_t));

	main_p->n = N;

	main_p->arr = (double*) malloc(sizeof(double) * main_p->n);

	#pragma acc parallel loop
	for(int i=0;i<main_p->n;i++) {
		main_p->arr[i] = i;
	}

	return main_p->arr[0]*main_p->arr[N-1] != 0;
}
