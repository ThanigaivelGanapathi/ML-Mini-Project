import pandas as pd
import seaborn as sns
from matplotlib import pyplot
from scipy.stats import norm

class Univariate:
    def qualQuan(self,dataset):
        qual = []
        quan = []
        for column in dataset.columns:   
            if(dataset[column].dtypes == "object"):
                qual.append(column)
            else:
                quan.append(column)
        return qual,quan

    def getUnivarateTbl(self,dataset,quan):
        tble = pd.DataFrame(index = ["Mean","Median","Mode","Q1:25%","Q2:50%","Q3:75%","Q4:100%","IQR","1.5Rule","Lesser","Greater","Minimum","Maximum","Skew","Kurtosis","Variance","STD"],columns = quan)
        for column in quan:             
            tble[column]["Mean"] = dataset[column].mean() 
            tble[column]["Median"] = dataset[column].median() 
            tble[column]["Mode"] = dataset[column].mode()[0]
            tble[column]["Q1:25%"]  = dataset.describe()[column]["25%"]
            tble[column]["Q2:50%"]  = dataset.describe()[column]["50%"]
            tble[column]["Q3:75%"]  = dataset.describe()[column]["75%"]
            tble[column]["Q4:100%"]  = dataset.describe()[column]["max"]
            tble[column]["IQR"]  = tble[column]["Q3:75%"] - tble[column]["Q1:25%"]
            tble[column]["1.5Rule"]  = 1.5 * tble[column]["IQR"]
            tble[column]["Lesser"]  = tble[column]["Q1:25%"] - tble[column]["1.5Rule"]
            tble[column]["Greater"]  = tble[column]["Q3:75%"] + tble[column]["1.5Rule"]
            tble[column]["Minimum"] = dataset[column].min()
            tble[column]["Maximum"] = dataset[column].max()
            tble[column]["Skew"] = dataset[column].skew()
            tble[column]["Kurtosis"] = dataset[column].kurtosis()
            tble[column]["Variance"] = dataset[column].var()
            tble[column]["STD"] = dataset[column].std()
            
        return tble   

    def getFrequencyTble(self,dataset,column):
        frequency_tble = pd.DataFrame(columns = ["UniqueValues","Frequency","RelativeFrequency","CummulativeFrequency"])
        frequency_tble["UniqueValues"] = dataset[column].value_counts().index
        frequency_tble["Frequency"] = dataset[column].value_counts().values
        frequency_tble["RelativeFrequency"] = (dataset[column].value_counts().values) / dataset[column].shape[0]
        frequency_tble["CummulativeFrequency"] = frequency_tble["RelativeFrequency"].cumsum()
        return frequency_tble

    def getPdfProbs(self,dataset,startRange,endRange):
        ax = sns.distplot(dataset,kde = True,kde_kws = {'color':'blue'},color = 'green')
        pyplot.axvline(startRange,color= "red")
        pyplot.axvline(endRange,color= "red")
        sample = dataset
        sample_mean = round(sample.mean(),2)
        sample_std = round(sample.std(),2) 
        dist = norm(startRange,endRange)
        values = [value for value in range(startRange,endRange)]
        probs = [dist.pdf(value) for value in values]
        return sample_mean,sample_std,round(sum(probs),2)

    def convert_to_Std_NB(self,dataset):
       values = [value for value in dataset]
       sd_mean = dataset.mean()
       sd_std = dataset.std()
       z_score = [ (j - sd_mean)/sd_std for j in values]
       return z_score
       
        