import scipy.stats
import numpy
from stats_help import *
import matplotlib.pyplot as plt


def VarghaDelaney(ax, ay):
    #ax, ay = numpy.array(x), numpy.array(y)
    Uy, p = scipy.stats.mannwhitneyu(ax, ay, alternative = 'two-sided')
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
        for j in range (i+1,5):
            if(i!= j):
                language_two = dataframe.loc[dataframe['language'] == languages[j]]
                #language_two = filter_dummyvalues(data = language_two ,error_column = column)
                language_one = dataframe.loc[dataframe['language'] == languages[i]]
                #language_one = filter_dummyvalues(data = language_one ,error_column = column)
                ax = language_one[column].values
                ay = language_two[column].values
                A_xy = VarghaDelaney(ay, ax)
                print "VarghaDelaney " + column +  "language " + languages[i] + ", language " + languages[j] + " "+ str(A_xy)
    return dict_of_results

def compareRanks():
    rank_user_data = get_rank_user()
    rank_user_data = rank_user_data.apply(pandas.to_numeric, errors='ignore')
    print compareTraits(rank_user_data,'rank')

def compareCloc():
    columns = ['language','cloc']
    df = get_all_data(columns)
    compareTraits(dataframe=df,column = 'cloc')

def compareExe():
    columns = ['language','exit_code','exe_size']
    df = get_all_data(columns)
    #df = filter_exitcode(data = df)
    del df['exit_code']
    print df

def compareSystem():
    columns = ['language','system_time','nbr_file_out']
    df = get_all_data(columns)
    df['system_time'] = df[['system_time']].astype(str)
    df = df.loc[df['system_time'] != '-']
    df = df.apply(pandas.to_numeric, errors='ignore')
    df = df.loc[df['system_time'] > 0]
    df = df.loc[df['nbr_file_out'] > 0]
    #df['nbr_file_out'] = df[['nbr_file_out']].astype(int)
    #print "nroffiles PYTHON",df
    del df['nbr_file_out']
    df.boxplot(by='language', sym='')
    plt.show()

def exit_code_one():
    columns = ['user_id','language','exit_code','run_error_msg']
    df = get_all_data(columns)
    df['exit_code'] = df[['exit_code']].astype(str)
    df = df.loc[df['exit_code'] == '1']
    df = df.loc[df['run_error_msg']== 'File or Dir not found']
    del df['run_error_msg']
    for problem, df_problem in df.groupby('problem_id'):
        print df_problem

def timed_out():
    columns = ['user_id','language','exit_code']
    df = get_all_data(columns)
    df['exit_code'] = df[['exit_code']].astype(str)

    df = df.loc[df['exit_code'] == '-15']
    print df['exit_code'].count()

def exit_code_meaning():
    columns = ['user_id','language','exit_code','run_error_msg']
    df = get_all_data(columns)
    df['exit_code'] = df[['exit_code']].astype(str)
    for language,df_group in df.groupby('language'):
        for exit, df_exit in df_group.groupby('exit_code'):
            print language,exit,df_exit['exit_code'].count()

##THIS ONE TO USE
def filterTimeOutErrors():
    columns = ['user_id','language','exit_code']
    df = get_all_data(columns)
    df['exit_code'] = df[['exit_code']].astype(str)
    df = df.loc[df['exit_code'] == '-15']
    for language,df_group in df.groupby('language'):
        if language == 'Java':
            for problem_id, df_ in df_group.groupby('problem_id'):
                print "numberofcases",df_['exit_code'].count()
                print df_



filterTimeOutErrors()
