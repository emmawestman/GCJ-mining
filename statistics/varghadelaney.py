import scipy.stats
import numpy
from stats_help import *

def VarghaDelaney(ax, ay):
    #ax, ay = numpy.array(x), numpy.array(y)
    Uy, p = scipy.stats.mannwhitneyu(ax, ay, alternative = 'two_sided')
    nx, ny = ax.size, ay.size
    Ux = nx*ny - Uy
    # rank sum for x
    Rx = Ux + (nx*(nx+1)/2.0)
    # rank sum for y
    Ry = Uy + (ny*(ny+1)/2.0)
    A_xy = (float(Rx)/nx - (nx+1)/2.0)/(1.0*ny)
    return A_xy



def compareTraits(dataframe,column):
    languages = ['Java','Python','C++','C','C#']
    dict_of_results = {}
    for i in range (0,5):
        for j in range (0,5):
            if(i!= j):
                language_two = dataframe.loc[dataframe['language'] == languages[j]]
                #language_two = filter_dummyvalues(data = language_two ,error_column = column)
                language_one = dataframe.loc[dataframe['language'] == languages[i]]
                #language_one = filter_dummyvalues(data = language_one ,error_column = column)
                ax = language_one[column].values
                ay = language_two[column].values
                A_xy = VarghaDelaney(ay, ax)
                print "VarghaDelaney " +  "language " + languages[i] + ", language " + languages[j] + " "+ str(A_xy)
    return dict_of_results

def compareRanks():
    rank_user_data = get_rank_user()
    rank_user_data = rank_user_data.apply(pandas.to_numeric, errors='ignore')
    language_two = rank_user_data.loc[rank_user_data['language'] == 'Java']
    print "Java",language_two
    #language_two = filter_dummyvalues(data = language_two ,error_column = column)
    language_one = rank_user_data.loc[rank_user_data['language'] == 'C++']
    print "C++",language_one
    x = language_one['rank'].values
    y = language_two['rank'].values
    print "VD rankcomp C++,Java",VarghaDelaney(ax = x, ay = y)
    print "VD rankcomp Java,C++",VarghaDelaney(ax = y, ay = x)


compareRanks()
