from functions import *
import logging 
import matplotlib.pyplot as plt
logger = logging.getLogger(__name__)
logging.basicConfig( level=logging.INFO)

tau = 5
print(tau)
a, b = get_total_precision_and_precision_weighted_average(tau)
print(a, "\n", b)

mus = [mu_given_tau(5) for _ in range(200)]
print(np.mean(mus), np.var(mus))
plt.hist(mus, bins =20)
plt.show()