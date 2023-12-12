#include "mex.h"
#include "cec15_test_func.h"

/* The gateway function */
void mexFunction( int nlhs, mxArray *plhs[],
        int nrhs, const mxArray *prhs[])
{
    double *inMatrix;               /* 1xN input matrix */
    mwSize ncols;                   /* size of matrix */
    double fx;
    int n;
    int func_num;
    int run;
    char* dirname, *filenameprefix;
    
    char * command = mxArrayToString(prhs[0]);
    
    
    if (command[0]=='e'){
        
        /* check for proper number of arguments */
        if(nrhs!=3) {
            mexErrMsgTxt("please call as cec15problems(''eval'', x, func_num)\n");
        }
        n=(int)mxGetNumberOfElements(prhs[1]);
        
        if (n!=10 && n!=30)
        {
            mexErrMsgTxt("Only 10D and 30D problems are defined in the competition.\n");
        }
        
        
        inMatrix=(double *)mxGetPr(prhs[1]);
        func_num = (int)mxGetScalar(prhs[2]);
        
        if (func_num<1 || func_num>15)
        {
            mexErrMsgTxt("Only 15 problems are defined in the competition. func_num \\in [1,15].\n");
        }
        
        
        cec15_test_func(inMatrix, &fx,n, 1, func_num);
        
        
        /* create the output matrix */
        plhs[0] = mxCreateDoubleScalar(fx);
        return;
    }
    #ifndef NO_RECORDING
    else if (command[0]=='r') {
        
        
        
        if(nrhs!=2) {
            mexErrMsgTxt("please call as cec15problems(''runnumber'', run)\n");
        }
        n=(int)mxGetNumberOfElements(prhs[1]);
        
        if (n!=1)
        {
            mexErrMsgTxt("Use scalar to set number of current run.\n");
        }
        
        
        run = (int)mxGetScalar(prhs[1]);
        
        if (run<1)
        {
            mexErrMsgTxt("Run number should be greater than 0.\n");
        }
        
        
        //     cec15_test_func(inMatrix, &fx,n, 1, func_num);
        set_number_of_run(run);
        return;
    } else if (command[0]=='o') {
        
        
        /* check for proper number of arguments */
        if(nrhs!=3) {
            mexErrMsgTxt("please call as cec15problems(''output'', dirname, filename_prefix)\n");
        }
        
        dirname = mxArrayToString(prhs[1]);
        filenameprefix = mxArrayToString(prhs[2]);
        
        
        //cec15_test_func(inMatrix, &fx,n, 1, func_num);
        write_result_statistics_to_file(dirname, filenameprefix);
        return;
    }
    #endif //NO_RECORDING
    else {
        
        mexPrintf("Usage: 1. cec15problems(''eval'', x, func_num)  -- evaluate func_num\n");
        #ifndef NO_RECORDING
        mexPrintf("       2. cec15problems(''runnumber'', run) -- set number of run.\n");
        mexPrintf("       3. cec15problems(''output'', dirname, filename_prefix)-- write output files.\n");
        #endif //NO_RECORDING
        mexPrintf(" Please check Readme.txt for detail information.\n");
    }
    
}