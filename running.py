from functions import *
import logging 
import matplotlib.pyplot as plt
logger = logging.getLogger(__name__)
logging.basicConfig( level=logging.INFO)

np.random.seed(4242)

tau_chain1 = tau_MCMC(.01, 10**5)

simply_plot_the_chain(tau_chain1)

emp_mean_tau, emp_sd_tau = np.mean(tau_chain1), np.std(tau_chain1)
plt.hist(tau_chain1, bins = 30)
plt.title(f"x bar {emp_mean_tau:.1f} s {emp_sd_tau:.1f}")
plt.show()