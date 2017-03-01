import timeit



benchmark_results = {}

#res = timeit.Timer('download_input_serial()','from run import download_input_serial').timeit(number=1)
#benchmark_results['download_input_serial'] = res



#res = timeit.Timer('download_input_mp()','from run import download_input_mp').timeit(number=1)
#benchmark_results['download_input_parallel'] = res

res = timeit.Timer('download_solution_serial()','from run import download_solution_serial').timeit(number=1)
benchmark_results['download_solution_serial'] = res

res = timeit.Timer('download_solution_mp()','from run import download_solution_mp').timeit(number=1)
benchmark_results['download_solution_parallel'] = res


print benchmark_results 
