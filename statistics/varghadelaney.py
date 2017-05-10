import scipy.stats
import numpy
from stats_help import *

def VarghaDelaney(ax, ay):
    #ax, ay = numpy.array(x), numpy.array(y)
    Uy, p = scipy.stats.mannwhitneyu(ax, ay)
    nx, ny = ax.size, ay.size
    Ux = nx*ny - Uy
    # rank sum for x
    Rx = Ux + (nx*(nx+1)/2.0)
    # rank sum for y
    Ry = Uy + (ny*(ny+1)/2.0)
    A_xy = (float(Rx)/nx - (nx+1)/2.0)/(1.0*ny)
    return A_xy

def compareTraits(column):
    columns = ['language',column]
    languages = ['Java','Python','C++','C','C#']
    dataframe = get_all_data(columns)
    del dataframe['problem_id']
    dict_of_results = {}
    for i in range (0,5):
        for j in range (i+1,5):
            language_two = dataframe.loc[dataframe['language'] == languages[j]]
            language_two = filter_dummyvalues(data = language_two ,error_column = column)
            language_one = dataframe.loc[dataframe['language'] == languages[i]]
            language_one = filter_dummyvalues(data = language_one ,error_column = column)
            ax = language_one[column].values
            ay = language_two[column].values
            dict_of_results[(languages[i],languages[j])] = VarghaDelaney(ax, ay)
    print dict_of_results



compareTraits("cloc")
