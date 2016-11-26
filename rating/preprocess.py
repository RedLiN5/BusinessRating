#!/usr/bin/python


import pandas as pd
import numpy as np
import sys
from statistics import mode
import random
import re
import csv
reload(sys)

class Preprocessing1(object):

    def __init__(self, file, target, sep = ',', header = 0, index_col = 0):
        self.file = file
        self.target = target
        self.sep = sep
        self.header = header
        self.index_col = index_col


    def ReadData(self):
        data = pd.read_table(self.file, sep = self.sep, header = self.header,
                             index_col = self.index_col)
        self.raw = data.copy()


    def checktype(self, temp):
        if pd.isnull(temp) == True:
            return 'SB'
        try:
            float(temp)
            return True
        except ValueError:
            return False


    def Split_Mixing(self, df):
        l = df.shape[0]
        sign0 = 0
        sign = 0
        smlist = []
        sms = []
        mlist = []
        ms = []
        mc = []
        smc = []
        count = 0
        scount = 0
        nac = 0
        for j in range(0,df.shape[1]):
            if df.iloc[:,j].dtype == 'object':
                for i in map(self.checktype, df.iloc[:,j]):
                    if i == True:
                        sign0 = 1
                        count = count + 1

                    elif i == False:
                        sign = 1
                        scount = scount + 1
                    else:
                        nac = nac +1

            if sign0+sign == 2 and count/float(count+scount) > 0.1 and count/float(count+scount) <= 0.9 :
                smlist += [j]
                if count/float(count+scount) > 0.5:
                    sms += ['Num']
                    smc += [count]
                else:
                    sms += ['Str']
                    smc += [scount]

            elif sign0+sign == 2:
                mlist += [j]
                if count/float(count+scount) > 0.5:
                    ms += ['Num']
                    mc += [count]
                else:
                    ms += ['Str']
                    mc += [scount]

            sign = 0
            sign0 = 0
            count = 0
            scount = 0
            nac = 0

        dict = {'SM':smlist, 'SMT':sms, 'SMC':smc, 'M':mlist, 'MT':ms, 'MC':mc}
        return dict


    def Search_m_bug(self, df, bdict):
        bug = []
        bugs = []
        sssc = 0
        for i in range(0,len(bdict['M'])):

            col = bdict['M'][i]

            if bdict['MT'][i] == 'Num':
                clist = list(map(self.checktype,df.iloc[:,col]))
                for k in range(0,len(clist)):
                    if clist[k] == False:
                        ic = self.is_currency(df.iloc[k,col])
                        ip = self.is_percantage(df.iloc[k,col])
                        if ic == 1 or ic == 2:
                            df.iloc[k,col] = self.sp_currency(df.iloc[k,col], ic)
                        elif ip == 1:
                            df.iloc[k,col] = self.sp_percentage(df.iloc[k,col], ip)
                        else:
                            bug += [k]

            if bdict['MT'][i] == 'Str':
                clist = list(map(self.checktype,df.iloc[:,col]))
                for k in range(0,len(clist)):
                    if clist[k] == False:
                        ic = self.is_currency(df.iloc[k,col])
                        ip = self.is_percantage(df.iloc[k,col])
                        if ic == 1 or ic == 2:
                            df.iloc[k,col] = self.sp_currency(df.iloc[k,col], ic)
                            sssc = sssc + 1
                        elif ip == 1:
                            df.iloc[k,col] = self.sp_percentage(df.iloc[k,col], ip)
                            sssc = sssc + 1
                    elif clist[k] == True:
                        bugs += [k]
                    if sssc > len(clist)/2:
                        bugs = []
                bug += bugs

        bug = list(set(bug))
        return bug


    def Search_sm_bug(self, df, bdict):
        bug = []
        bugs = []
        sssc = 0
        for i in range(0,len(bdict['SM'])):

            col = bdict['SM'][i]

            if bdict['SMT'][i] == 'Num':
                clist = list(map(self.checktype,df.iloc[:,col]))
                for k in range(0,len(clist)):
                    if clist[k] == False:
                        ic = self.is_currency(df.iloc[k,col])
                        ip = self.is_percantage(df.iloc[k,col])
                        if ic == 1 or ic == 2:
                            df.iloc[k,col] = self.sp_currency(df.iloc[k,col], ic)
                        elif ip == 1:
                            df.iloc[k,col] = self.sp_percentage(df.iloc[k,col], ip)
                        else:
                            bug += [k]

            if bdict['SMT'][i] == 'Str':
                clist = list(map(self.checktype,df.iloc[:,col]))
                for k in range(0,len(clist)):
                    if clist[k] == False:
                        ic = self.is_currency(df.iloc[k,col])
                        ip = self.is_percantage(df.iloc[k,col])
                        if ic == 1 or ic == 2:
                            df.iloc[k,col] = self.sp_currency(df.iloc[k,col], ic)
                            sssc = sssc + 1
                        elif ip == 1:
                            df.iloc[k,col] = self.sp_percentage(df.iloc[k,col], ip)
                            sssc = sssc + 1
                    elif clist[k] == True:
                        bugs += [k]
                    if sssc > len(clist)/2:
                        bugs = []
                bug += bugs

        bug = list(set(bug))
        return bug


    def delrow(self, df, bug):
        df = df.drop(bug, axis = 0)
        return df


    def sm_change(self, df, adc):

        for (col, dic) in adc.items():
            l = len(df.iloc[:,col])
            for i in range(0,l):
                if str(df.iloc[i,col]) in dic.keys():
                    df.iloc[i,col] = dic[str(df.iloc[i,col])]

        return df


    def read_canshu(self, file):
        df = pd.read_table(file, header = None ,sep = ',')
        l = df.shape[0]
        Dict = dict()

        for i in range(0,l):
            temp = dict()
            for j in range(0,100):
                if 1+2*j > df.shape[1]-1 or pd.isnull(df.iloc[i,1+2*j]):
                    break
                else:
                    temp[df.iloc[i,1+2*j]] = df.iloc[i,2+2*j]
            Dict[df.iloc[i,0]] = temp
        return Dict


    def show_sm_dis(self, df, bdict):
        AD = dict()
        if len(bdict['SM']) > 0:
            for i in range(0,len(bdict['SM'])):
                col = bdict['SM'][i]

                Dict = dict()

                if bdict['SMT'][i] == 'Str':
                    for item in range(0,df.shape[0]):

                        if pd.isnull(df.iloc[item,col]):
                            continue
                        elif df.iloc[item,col] in Dict:
                            Dict[df.iloc[item,col]] = Dict[df.iloc[item,col]] + 1
                        else:
                            Dict[df.iloc[item,col]] = 1

                else:
                    Dict['Numerical'] = bdict['SMC'][i]
                    for item in range(0,df.shape[0]):
                        if pd.isnull(df.iloc[item,col]):
                            continue
                        if self.checktype(df.iloc[item,col]) == False and df.iloc[item,col] in Dict:
                            Dict[df.iloc[item,col]] = Dict[df.iloc[item,col]] + 1
                        elif self.checktype(df.iloc[item,col]) == False:
                            Dict[df.iloc[item,col]] = 1

                AD[col] = Dict
        return AD


    def write_csv(self, AD):
        with open('Showing_Outlier.csv', 'w') as csv_file:
            writer = csv.writer(csv_file)
            for ind, mydict in AD.items():
                for key, value in mydict.items():
                    writer.writerow([ind, key, value])


    def Typo_Handling1(self, df):
        dic = self.Split_Mixing(df)
        bug = self.Search_m_bug(df, dic)
        sbug = self.Search_sm_bug(df, dic)
        dic = self.Split_Mixing(df)
        AD = self.show_sm_dis(df, dic)
        self.write_csv(AD)
        return df


    def Typo_Handling2(self, parameter_file):
        df = self.Typo_Handling1(self.ReadData())
        adc = self.read_canshu(parameter_file)
        df = self.sm_change(df, adc)
        dic = self.Split_Mixing(df)
        bug = self.Search_m_bug(df, dic)
        sbug = self.Search_sm_bug(df, dic)
        df = self.delrow(df, bug)
        sbug = list(set(sbug) - set(bug))
        df = self.delrow(df, sbug)
        df = df.reset_index(drop=True)
        dic = self.Split_Mixing(df)

        for i in range(0,df.shape[1]):
            try:
                df.iloc[:,i] = pd.to_numeric(df.iloc[:,i])
            except ValueError:
                i

        return df


    def DropTargetNA(self):
        '''Return target variable'''
        raw = self.Typo_Handling2('/Users/Leslie/OneDrive/NEWA/VirtualDataScientist/params_typo.csv')
        df = raw[raw[self.target].notnull()].reset_index(drop=True)
        return df




class Preprocessing2(object):

    def __init__(self, dataframe, NACriteriaCol = 0.3):
        self.df = dataframe
        self.NACriteriaCol = NACriteriaCol

    def ZipCodeRecognize(self):
        df = self.df
        colnames = df.columns

        def ColNamesNotExist():
            pos = []
            for i in range(len(colnames)):
                col = colnames[i]
                if col.split(':')[0] == 'Unnamed':
                    pos += [i]

            return pos

        def StreetAddress(x):
            myre = r'^[A-Za-z0-9_]* (.*) (.*) [a-zA-Z]{2} [0-9]{5}(-[0-9]{4})?$'
            m = re.match(myre, x)
            return bool(m)

        def ExtractZipCode(x):
            result = re.search(r'.*(\d{5}(\-\d{4})?)$', x).groups()[0]
            return result

        ColPosition = np.array(ColNamesNotExist())
        Index = df.index
        Coltemp = []

        for col in ColPosition:
            variable = df[[col]]
            position = random.sample(Index, 10)
            units = variable.ix[position,:].values.flatten()
            Coltemp += [sum(map(StreetAddress, units))]

        AddressCol = df[ColPosition[np.array(Coltemp) == 10]]
        df['ZipCode'] = map(ExtractZipCode, AddressCol)


    def SevereCol(self):
        '''
        Return column names with too many missing values
        and number of column names
        '''
        df = self.self
        nrow = df.shape[0]
        colnames = df.columns[df.isnull().any()]
        colnames_missing = []
        missing_ratio = []
        types = []
        col_missing = df.isnull()
        for col in colnames:
            ratio = sum(col_missing[col])/float(nrow)
            if ratio >= self.NACriteriaCol:
                colnames_missing += [col]
                missing_ratio += [ratio]
                types += [mode(map(type, df[col]))]

        return colnames_missing, colnames, types, missing_ratio






class SevereColumnProcess(object):

    def __init__(self, DataFrame, ColNames_MissSevere, ColNames_Miss, ColTypes,
                 MissRatio, Methods, NACriteriaRow = .4):
        self.methods = Methods
        self.df = DataFrame
        self.colnames_misssevere = ColNames_MissSevere
        self.coltype = ColTypes
        self.missratio = MissRatio
        self.NACriteriaRow = NACriteriaRow
        self.colnames_miss = ColNames_Miss


    def RetrieveSevereCol(self):
        '''
        Custormers choose preferred methods for the columns.
        Return a dataframe.
        ATTENTION: The options for methods are: 'ReplaceWith X', 'Mean', 'Median', 'Mode', 'Drop'
        '''
        def InsertProcess(dataframe, colnames, methods):
            for i in range(len(colnames)):

                if methods[i] == 'Mode':
                    column = dataframe[colnames[i]].copy()
                    pos = column.isnull().values.flatten()
                    mode_value = mode(column.ix[~pos])
                    length = sum(pos)
                    column.ix[pos] = np.array([mode_value]*length)
                    dataframe[colnames[i]] = column

                elif methods[i] == 'Mean':
                    column = dataframe[colnames[i]].copy()
                    pos = column.isnull().values.flatten()
                    column.ix[~pos] = map(int, column.ix[~pos])
                    mean_value = np.mean(column.ix[~pos])
                    length = sum(pos)
                    column.ix[pos] = np.array([mean_value]*length)
                    dataframe[colnames[i]] = column

                elif methods[i] == 'Drop':
                    dataframe = dataframe.drop(colnames[i], axis=1)

                elif methods[i].split()[0] == 'ReplaceWith':
                    column = dataframe[colnames[i]].copy()
                    pos = column.isnull().values.flatten()
                    replace_value = methods[i].split()[1]
                    length = sum(pos)
                    column.ix[pos] = np.array([replace_value]*length)
                    dataframe[colnames[i]] = column

            return dataframe

        result = InsertProcess(dataframe = self.df, colnames = self.colnames_misssevere, methods = self.methods)
        return result


    def SlightCol(self):
        df = self.df
        nrow = df.shape[0]
        colnames_missslight = self.colnames_miss.difference(self.colnames_misssevere)
        miss_ratio = []
        types = []
        col_missing = df.isnull()
        for col in colnames_missslight:
            ratio = sum(col_missing[col])/float(nrow)
            miss_ratio += [ratio]
            types += [mode(map(type, df[col]))]

        return colnames_missslight, types, miss_ratio


    def RetrieveSlightCol(self):
        '''
        Drop the rows whose missing values are more than 'NACriteriaRow'(Defined by customers or default)
        '''
        colnames_slight, types, miss_ratio = self.SlightCol()
        dataframe = self.df
        df_slight =dataframe[colnames_slight]
        df_severe = self.RetrieveSevereCol()
        df = pd.concat([df_slight, df_severe], axis=1)
        ncol = df_slight.shape[1]
        nrow = df.shape[0]
        missing = df_slight.isnull()

        for i in range(nrow):
            if sum(missing.ix[i])/float(ncol) >= self.NACriteriaRow:
                df = df.drop([i])

        '''
        Impute the missing values in whole dataframe.
        If type is FLOAT, impute mean or median.
        If type is INT, impute rounded mean, median or mode.
        If type is STR, impute mode.
        '''
        colnamesNA = df.columns[df.isnull().any()]
        for colname in colnamesNA:
            col_type = mode(map(type, df[colname]))

            if col_type in [np.float64, np.float32, float]:
                position = df[colname].isnull()
                impute_method = random.sample(['mean', 'median'], 1)
                if impute_method == 'mean':
                    df.ix[position, colname] = np.mean(df.ix[~position, colname])
                elif impute_method == 'median':
                    df.ix[position, colname] = np.median(df.ix[~position, colname])

            elif col_type in [np.int64, np.int32, int]:
                position = df[colname].isnull()
                impute_method = random.sample(['mean', 'median', 'mode'])
                if impute_method == 'mode':
                    df.ix[position, colname] = mode(df.ix[~position, colname])
                elif impute_method == 'mean':
                    df.ix[position, colname] = round(np.mean(df.ix[~position, colname]))
                elif impute_method == 'median':
                    df.ix[position, colname] = round(np.median(df.ix[~position, colname]))

            elif col_type == str:
                position = df[colname].isnull()
                df.ix[position, colname] = mode(df.ix[~position, colname])

        df = df.reset_index(drop=True)
        return df


    def Encode(self):
        df = self.RetrieveSlightCol()
        position = df.apply(lambda x: mode(map(type, x))) == str
        df.ix[:,position.values] = df.ix[:,position.values].apply(lambda x: pd.factorize(x)[0]+1)

        return df
