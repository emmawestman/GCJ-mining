import scipy.stats
import numpy as np
from stats_help import *
import matplotlib.pyplot as plt
from box_plots import get_data_frame


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
    languages = ['Python','Java','C++','C#','C']

    dict_of_results = {}
    res = []
    for i in range (0,5):
        for j in range (i+1,5):
            if(i!= j):
                language_one = dataframe.loc[dataframe['language'] == languages[i]]
                language_two = dataframe.loc[dataframe['language'] == languages[j]]
                ax = language_one['new_col'].values
                ay = language_two['new_col'].values
                A_xy = VarghaDelaney(ax, ay)
                res.append(A_xy)
                print "VarghaDelaney " + column +  "language " + languages[i] + ", language " + languages[j] + " "+ str(A_xy)
    print 'C\# & ' + "%.2f" % res[9] + '\\\\'
    print 'C++ & ' + "%.2f" % res[8] + ' & ' + "%.2f" % res[7] + '\\\\'
    print 'Java & ' + "%.2f" % res[6] + ' & ' + "%.2f" % res[5] + ' & '  + "%.2f" % res[4] + '\\\\'
    print 'Python & ' + "%.2f" % res[3] + ' & ' + "%.2f" % res[2] + ' & ' + "%.2f" % res[1] + ' & ' + "%.2f" % res[0] + '\\\\'
    return dict_of_results

def compareRanks():
    rank_user_data = get_rank_user()
    rank_user_data = rank_user_data.apply(pandas.to_numeric, errors='ignore')
    print compareTraits(rank_user_data,'rank')

def compareCloc():
    columns = ['language','cloc']
    df = get_all_data(columns)
    df['cloc'] = df[['cloc']].astype(str)
    df = df.loc[df['cloc'] != '-']
    df = df.loc[df['cloc'] != '0']
    df = df.apply(pandas.to_numeric, errors='ignore')
    compareTraits(dataframe=df,column = 'cloc')

def compareExe():
    columns = ['language','compiled','exe_size']
    df = get_all_data(columns)
    df['compiled'] = df[['compiled']].astype(str)

    df = df.loc[df['compiled'] == '0']
    del df['compiled']
    df = df.apply(pandas.to_numeric, errors='ignore')
    compareTraits(dataframe = df, column = 'exe_size')

def compareMaxRam():
    columns = ['language','max_RAM']
    df = get_all_data(columns)
    df['max_RAM'] = df[['max_RAM']].astype(str)
    df = df.loc[df['max_RAM'] != '-']
    df = df.apply(pandas.to_numeric, errors='ignore')
    compareTraits(dataframe = df, column = 'max_RAM')

def compareWallClock():
    columns = ['language','wall_clock']
    df = get_all_data(columns)
    df['wall_clock'] = df[['wall_clock']].astype(str)
    df = df.loc[df['wall_clock'] != '-']
    df = df.apply(pandas.to_numeric, errors='ignore')
    compareTraits(dataframe = df, column = 'wall_clock')

def compareUserTime():
    columns = ['language','user_time']
    df = get_all_data(columns)
    df['user_time'] = df[['user_time']].astype(str)
    df = df.loc[df['user_time'] != '-']
    df = df.apply(pandas.to_numeric, errors='ignore')
    compareTraits(dataframe = df, column = 'user_time')
#def compareEx

def languageRoundDist():
    dict_cid_round = get_cid_name_dict('c_id')
    rank_user_data = get_rank_user()
    rank_user_data = rank_user_data.apply(pandas.to_numeric, errors='ignore')
    dict_cid_lang = {}
    for c_id,df in rank_user_data.groupby('c_id'):
        df_size = len(df)
        print "cid", dict_cid_round[c_id]
        for lang,lang_df in df.groupby('language'):

            print lang
            print str(len(lang_df) / float(df_size))


def checkClocExecuted():
    df = get_all_data(['language','cloc','exit_code','user_id'])
    df['exit_code'] = df[['exit_code']].astype(str)
    df['cloc'] = df [['cloc']].astype(str)
    df = df.loc[df['exit_code'] == '0']
    df = df.loc[df['cloc'] != '-']
    df = df.apply(pandas.to_numeric, errors='ignore')
    df = df.loc[df['cloc'] > 15]
    sumAll = 0
    for language,groupedFrame in df.groupby('language'):
        column = 'cloc'
        minVal = groupedFrame[column].min()
        print "min", groupedFrame.loc[[groupedFrame[column].idxmin()]]
        medianVal = groupedFrame[column].median()
        meanVal = groupedFrame[column].mean()
        maxVal = groupedFrame[column].max()
        sumVal = groupedFrame[column].sum()
        sumAll = sumAll +sumVal
        print language + ' & '+ str(minVal) + ' & '+ str(int(medianVal)) + ' & '+ "%.2f" % meanVal + ' & '+str(maxVal) + ' & '+ str(sumVal) +  ' \\\\'
    print "sumall",sumAll
#compareExe()
#compareMaxRam()
#print ''
#compareWallClock()
#print ''
#compareUserTime()

fetures = ['cloc', 'max_RAM', 'exe_size', 'user_time', 'wall_clock']
for f in fetures:
    df = get_data_frame(f)
    print df
    compareTraits(df,f)
    print ''






