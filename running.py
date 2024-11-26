from functions import *
import logging 
import matplotlib.pyplot as plt
logger = logging.getLogger(__name__)
logging.basicConfig( level=logging.INFO)

np.random.seed(42421)

tau_chain1 = tau_MCMC(5, 10000)

#visualise tau
simply_plot_the_chain(tau_chain1, title = "tau MCMC")
emp_mean_tau, emp_sd_tau = np.mean(tau_chain1), np.std(tau_chain1)
plt.hist(tau_chain1, bins = 30)
plt.suptitle("histogram of tau")
plt.title(f"x bar {emp_mean_tau:.1f},  s {emp_sd_tau:.1f}")
plt.show()


effects = np.ndarray(shape = (len(tau_chain1), len("ABCDEFGH")) )
for i, tau in enumerate(tau_chain1):

    effects[i] = theta_given_hyperparams(mu_given_tau(tau), tau, DATA["yBar.j"], DATA["sigma.j"])

effects = pd.DataFrame(effects).rename(columns = dict(  enumerate("ABCDEFGH") ) )

fig , ( ax1, ax2) = plt.subplots(1,2)
ax1.hist(effects["A"], bins = 30)
ax1.set_title("effect in school A")
ax2.hist(effects.max(axis =1), bins = 30)
ax2.set_title("largest effect")
plt.show()
print("posterior quantiles")
print(
    effects.quantile(q = [.025, .25, .5, .75, .975]).round(0).astype(np.int32)
)