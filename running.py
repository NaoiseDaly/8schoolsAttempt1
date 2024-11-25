from functions import *
import logging 
import matplotlib.pyplot as plt
logger = logging.getLogger(__name__)
logging.basicConfig( level=logging.INFO)

np.random.seed(457)

tau_chain1 = tau_MCMC(5, 10 )

simply_plot_the_chain(tau_chain1)

# plt.hist(tau_chain1, bins = 20)
# plt.show()