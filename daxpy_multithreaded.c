#include <stdio.h>
#include <stdlib.h>
#include <omp.h>

// Multi-threaded DAXPY kernel
// y = a * x + y
void daxpy(int N, double a, double *x, double *y) {
    // Parallelize the loop with OpenMP
    #pragma omp parallel for
    for (int i = 0; i < N; i++) {
        y[i] = a * x[i] + y[i];  // Each thread handles different indices
    }
}

int main() {
    int N = 1000000;  // Array size
    double a = 2.5;   // Scalar multiplier

    // Allocate arrays
    double *x = (double*) malloc(N * sizeof(double));
    double *y = (double*) malloc(N * sizeof(double));

    if (x == NULL || y == NULL) {
        fprintf(stderr, "Memory allocation failed!\n");
        return 1;
    }

    // Initialize arrays
    for (int i = 0; i < N; i++) {
        x[i] = i * 0.1;
        y[i] = i * 0.2;
    }

    // Optional: set number of threads
    omp_set_num_threads(8);  // Change this to your desired number of cores

    // Run multi-threaded DAXPY
    daxpy(N, a, x, y);

    // Verify results: print first 10 elements
    printf("First 10 results:\n");
    for (int i = 0; i < 10; i++) {
        printf("y[%d] = %f\n", i, y[i]);
    }

    // Clean up
    free(x);
    free(y);

    return 0;
}
