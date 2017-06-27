from stats_help import *
from box_plots import get_data_frame


#def printLatexRows():



def generateTabellData(column):
    #columns = ['language','user_id',column]
    dataframe = get_data_frame(column)
    #dataframe = dataframe.loc[dataframe[column] != '-']
    dataframe = dataframe.apply(pandas.to_numeric, errors='ignore')
    shadowMin = []
    shadowMed = []
    shadowMean = 0
    shadowMax = []
    shadowSum = 0
    for language,groupedFrame in dataframe.groupby('language'):
        #print groupedFrame.loc[groupedFrame[column]<5]
        minVal = groupedFrame['new_col'].min()
        medianVal = groupedFrame['new_col'].median()
        meanVal = groupedFrame['new_col'].mean()
        maxVal = groupedFrame['new_col'].max()
        sumVal = groupedFrame['new_col'].sum()
        shadowMin.append(minVal)
        shadowMax.append(maxVal)
        shadowSum += sumVal
        shadowMean += meanVal
        shadowMed.append(medianVal)
        print language + ' & '+ str(minVal) + ' & '+ str(float(medianVal)) + ' & '+ "%.2f" % meanVal + ' & '+str(maxVal) + ' & '+ str(sumVal) +  ' \\\\'
    shadowMed.sort()
    print '\\midrule'
    print 'Overall & '+ str(min(shadowMin)) + ' & '+  str(shadowMed[2]) + ' & '+ "%.2f" %  (shadowMean/5.0) + ' & '+str(max(shadowMax)) + ' & '+ str(shadowSum)  +  ' \\\\'
 
def all_tabels():
    fetures = ['cloc', 'max_RAM', 'exe_size', 'user_time', 'wall_clock']
    for f in fetures:
        generateTabellData(f)
        print ''


all_tabels()

