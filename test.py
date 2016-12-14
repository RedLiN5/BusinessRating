from data.Normalization import DataNormalization

data = DataNormalization()
normal_score = data.normal()
print(normal_score.shape)