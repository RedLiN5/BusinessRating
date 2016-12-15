from rating.InvesteeRating import InvesteeScore
import time

start = time.time()
data = InvesteeScore(investee='Meta')
print('Final score:', data.investee_final_score())
print('Runing time: %s Secs' % round(time.time()-start,2))