from etl import Preprocessing

pre = Preprocessing('../data/mydata.csv')
df = pre.preprocess()
print df.shape
