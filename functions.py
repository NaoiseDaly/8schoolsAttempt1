import numpy as np
import matplotlib.pyplot as plt
import logging
logger = logging.getLogger(__name__)
from time import perf_counter
from scipy.stats import norm, uniform
import pandas as pd

DATA = pd.read_csv("data.txt").rename(index = dict( (i, letter) for i, letter in enumerate("ABCDEFGH") ) )

def get_total_precision_and_precision_weighted_average(tau:float):

    total_precision = np.sum( 1/(tau**2 +DATA["sigma.j"]**2)  )

    average = np.sum(DATA["yBar.j"]/(tau**2 +DATA["sigma.j"]**2 ) )
    precision_weighted_average = average/total_precision

    return total_precision, precision_weighted_average

def tau_MCMC(X0, max_t_iterations=10**3):
    """simulate tau, the population sd hyperparameter"""

    #start timing here
    start_time = perf_counter()

    def log_unnormalised_target_pdf(tau):
        """ log of tau's unnormalised pdf
         tau > 0 """
        if tau <= 0:
            return -np.inf #log of zero
        
        total_prec, mu_hat = get_total_precision_and_precision_weighted_average(tau)

        log_total_prec = np.log(total_prec)

        big_sum = np.log(DATA["sigma.j"]**2 + tau**2) + (DATA["yBar.j"] - mu_hat)**2/(DATA["sigma.j"]**2 + tau**2)
        big_sum = np.sum(big_sum)

        return -( log_total_prec + big_sum )
        
        
    def log_proposal_pdf(x, conditional):
        pass
    
    def proposal_sample(conditional):
        return uniform.rvs(loc = conditional-2.5, scale = 5)
    
    def log_alpha(current, new):
       r = log_unnormalised_target_pdf(new)-log_unnormalised_target_pdf(current)
       return min(0, r)
    
    chain = np.zeros(max_t_iterations)
    X_t = chain[0] = X0
    
    log_unif_rvs = np.log(uniform.rvs(size = max_t_iterations))
    for t in range(1, max_t_iterations):
        #propose a move from Q
        proposed_value = proposal_sample(X_t)#sample Q(.|X_t)
        #sample a uniform and take log
        log_u = log_unif_rvs[t]
        #get alpha on log scale
        log_alpha_prob = log_alpha(X_t, proposed_value)
        #decide if the chain accepts or rejects the move
        #this is setting X_t+1 but no point in creating another variable
        if log_u <= log_alpha_prob:
            X_t = proposed_value 
        #record the new state of the chain
        chain[t] = X_t

    #end timing now
    end_time = perf_counter()
    #record timing
    logger.info(
        f"chain took {round(end_time-start_time,3)} secs to simulate {max_t_iterations} iterations"
    )

    return chain

def theta_given_hyperparams(mu, tau, sample_mean ,sample_sd):

    var = 1/( 1/(sample_sd**2) + 1/(tau**2) )

    top = sample_mean/(sample_sd**2) + mu/(tau**2)

    theta_hat = top*var
    return norm.rvs(loc = theta_hat, scale = np.sqrt(var)  )


def mu_given_tau(tau):

    total_precision, mean = get_total_precision_and_precision_weighted_average(tau)
    sd = np.sqrt(1/total_precision) #get sqrt of variance for rvs() function

    return norm.rvs( loc = mean, scale = sd )

def simply_plot_the_chain(chain, with_burn_in = None, title:str = None, fmt_plt = "-"):
    """plot the chain over time
    
    optionally view the chain after different burn in points,
    it would be preferably to pick an odd number of burn in points"""

    if not with_burn_in:
        fig, ax = plt.subplots()
        ax.plot(chain, fmt_plt)
        ax.set_xlabel("t")
        ax.set_ylabel("X")
        if title:
            plt.suptitle(title)
        plt.show()
        return
    
    with_burn_in.insert(0, 0) #show the whole chain for reference

    num_subplots = len(with_burn_in)
    num_rows  = (num_subplots+1) //2
    fig, axes = plt.subplots( nrows = num_rows, ncols = 2)
    axes = np.array(axes).flatten() # easier to access subplots this way

    
    for burn_in_point, subplot in zip(with_burn_in, axes):
        subplot.plot(chain[burn_in_point:], fmt_plt)
        subplot.set_xlabel("t")
        subplot.set_ylabel("X")
        subplot.set_title(f"burn in after {burn_in_point}")
    
    if title:
        plt.suptitle(title)
    plt.show()