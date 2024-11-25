from functions import *
import logging 
import matplotlib.pyplot as plt
logger = logging.getLogger(__name__)
logging.basicConfig( level=logging.INFO)

np.random.seed(4242)

tau_chain1 = tau_MCMC(5, 1000)

#visualise tau
simply_plot_the_chain(tau_chain1, title = "tau MCMC")
emp_mean_tau, emp_sd_tau = np.mean(tau_chain1), np.std(tau_chain1)
plt.hist(tau_chain1, bins = 30)
plt.suptitle("histogram of tau")
plt.title(f"x bar {emp_mean_tau:.1f},  s {emp_sd_tau:.1f}")
plt.show()

effect_in_A = []
max_effect = []
for tau in tau_chain1:
    mu = mu_given_tau(tau)

    theta = theta_given_hyperparams(mu, tau, DATA["yBar.j"], DATA["sigma.j"])
    print(type(theta), theta)
    effect_in_A.append(theta[0]) # look we just know A will be the first
    max_effect.append(max(theta))

fig , ( ax1, ax2) = plt.subplots(1,2)
ax1.hist(effect_in_A, bins = 30)
ax1.set_title("effect in school A")
ax2.hist(max_effect, bins = 30)
ax2.set_title("largest effect")
plt.show()