from stats_help import *


#def printLatexRows():



def generateTabellData(column):
    columns = ['language','user_id',column]
    dataframe = get_all_data(columns)
    dataframe = dataframe.loc[dataframe[column] != '-']
    dataframe = dataframe.apply(pandas.to_numeric, errors='ignore')
    shadowMin = 0
    shadowMed = 0
    shadowMean = 0
    shadowMax = 0
    shadowSum = 0
    for language,groupedFrame in dataframe.groupby('language'):
        print groupedFrame.loc[groupedFrame[column]<5]
        #minVal = groupedFrame[column].min()
        #medianVal = groupedFrame[column].median()
        #meanVal = groupedFrame[column].mean()
        #maxVal = groupedFrame[column].max()
        #sumVal = groupedFrame[column].sum()
        #shadowMin += minVal
        #shadowMax += maxVal
        #shadowSum += sumVal
        #shadowMean+= meanVal
        #shadowMed += medianVal
        #print language + ' & '+ str(minVal) + ' & '+ str(int(medianVal)) + ' & '+ "%.2f" % meanVal + ' & '+str(maxVal) + ' & '+ str(sumVal) +  ' \\\\'
    #print ' & '+ str(shadowMin) + ' & '+  str(int(shadowMed)) + ' & '+ "%.2f" %  shadowMean + ' & '+str(shadowMax) + ' & '+ str(shadowSum)  +  ' \\\\'


generateTabellData('cloc')
