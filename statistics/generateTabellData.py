from stats_help import *


#def printLatexRows():



def generateTabellData(column):
    columns = ['language','user_id',column]
    dataframe = get_all_data(columns)
    dataframe = dataframe.loc[dataframe[column] != '-']
    dataframe = dataframe.apply(pandas.to_numeric, errors='ignore')
    shadowMin = []
    shadowMed = []
    shadowMean = 0
    shadowMax = []
    shadowSum = 0
    for language,groupedFrame in dataframe.groupby('language'):
        #print groupedFrame.loc[groupedFrame[column]<5]
        minVal = groupedFrame[column].min()
        medianVal = groupedFrame[column].median()
        meanVal = groupedFrame[column].mean()
        maxVal = groupedFrame[column].max()
        sumVal = groupedFrame[column].sum()
        shadowMin.append(minVal)
        shadowMax.append(maxVal)
        shadowSum += sumVal
        shadowMean += meanVal
        shadowMed.append(medianVal)
        print language + ' & '+ str(minVal) + ' & '+ str(int(medianVal)) + ' & '+ "%.2f" % meanVal + ' & '+str(maxVal) + ' & '+ str(sumVal) +  ' \\\\'
    shadowMed.sort()
    print '\\midrule'
    print 'Overall & '+ str(min(shadowMin)) + ' & '+  str(shadowMed[2]) + ' & '+ "%.2f" %  (shadowMean/5.0) + ' & '+str(max(shadowMax)) + ' & '+ str(shadowSum)  +  ' \\\\'

generateTabellData('cloc')  

