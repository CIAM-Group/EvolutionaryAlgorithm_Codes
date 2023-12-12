#ifndef CEC15_TEST_FUNCTIONS_H
#define CEC15_TEST_FUNCTIONS_H


#define INF 1.0e99
#define EPS 1.0e-14
#define E  2.7182818284590452353602874713526625
#define PI 3.1415926535897932384626433832795029


#define MAX_OF_RUNS 20
#define RECORDING_POINTS_NUM 19
#define MAX_FUNCTION_NUMBER  15
#define TIMES_OF_EVAL  50
#define DIMS 2

/*
 * evaluate specific function
 */
void cec15_test_func(double *x, double *f, int nx, int mx,int func_num);

#ifndef NO_RECORDING
/*
 *  Number of run
 */
void set_number_of_run(int run);
/* 
 * output to file
 */
// dir can only like test/resultdir
void write_result_statistics_to_file(char* dir, char * file_prefix);

#endif //NO_RECORDING

#endif //CEC15_TEST_FUNCTIONS_H
