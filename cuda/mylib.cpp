#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <dlfcn.h>
#include <cuda_runtime.h>
#include <time.h>

clock_t startTime, endTime;

void checkLog(){
    FILE* file = fopen("info.txt","a");
    float ms;
    ms = (float)(endTime-startTime)/CLOCKS_PER_SEC;
    fprintf (file, "%f\n", ms);
    fclose(file);
}


cudaError_t cudaMallocHost(void** h_cc, size_t count)
{
cudaError_t (*lcudaMallocHost) ( void**, size_t) = (cudaError_t (*) ( void**, size_t ))dlsym(RTLD_NEXT, "cudaMallocHost");
    startTime = clock();
    printf("cudaMallocHost hooked\n");
    return lcudaMallocHost( h_cc, count );
}



cudaError_t cudaMalloc(void** devPtr, size_t count)
{
cudaError_t (*lcudaMalloc) ( void**, size_t) = (cudaError_t (*) ( void**, size_t ))dlsym(RTLD_NEXT, "cudaMalloc");
    printf("cudaMalloc hooked\n");
    return lcudaMalloc( devPtr, count );
}

cudaError_t cudaMemcpy ( void* dst, const void* src, size_t count, cudaMemcpyKind kind )
{
cudaError_t (*lcudaMemcpy) ( void*, const void*, size_t, cudaMemcpyKind) = (cudaError_t (*) ( void* , const void* , size_t , cudaMemcpyKind  ))dlsym(RTLD_NEXT, "cudaMemcpy");
    printf("cudaMemcpy hooked\n");
    return lcudaMemcpy( dst, src, count, kind );
}

cudaError_t cudaFree ( void* devPtr )
{
cudaError_t (*lcudaFree) ( void*) = (cudaError_t (*) ( void*))dlsym(RTLD_NEXT, "cudaFree");
    printf("cudaFree hooked\n");
    return lcudaFree( devPtr );
}


cudaError_t cudaEventSynchronize ( cudaEvent_t event )
{
cudaError_t (*lcudaEventSynchronize) (cudaEvent_t) = (cudaError_t (*) ( cudaEvent_t))dlsym(RTLD_NEXT, "cudaEventSynchronize");
    endTime = clock();
    checkLog();
    return lcudaEventSynchronize( event );
}
