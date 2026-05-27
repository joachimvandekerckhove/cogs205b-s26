import math
from scipy.integrate import quad

class BayesFactor:
    def __init__(self, n, k):
        if not isinstance(n, int) or isinstance(n, bool):
            raise TypeError("n must be an integer")
        if not isinstance(k, int) or isinstance(k, bool):
            raise TypeError("k must be an integer")
        
        if n < 0 or k < 0:
            raise ValueError("n and k cannot be negative")
        if k > n:
            raise ValueError("k cannot be larger than n")
        
        self.n = n
        self.k = k

    def likelihood(self, theta):
        if not isinstance(theta, (int, float)) or isinstance(theta, bool):
            raise TypeError("Theta must be an integer or float")
        if not (0 <= theta <= 1):
            raise ValueError("Theta must be within the range [0, 1]")
        
        # Binomial likelihood: P(k | n, theta) = C(n, k) * theta^k * (1 - theta)^(n - k)
        # math.comb is available in Python 3.8+
        comb = math.comb(self.n, self.k)
        return comb * (theta**self.k) * ((1 - theta)**(self.n - self.k))

    def evidence_slab(self):
        # Slab prior: theta ~ Uniform(0, 1), density p(theta | slab) = 1
        # evidence = integral of likelihood(theta) * 1 d_theta from 0 to 1
        integrand = lambda theta: self.likelihood(theta)
        result, _ = quad(integrand, 0, 1)
        return float(result)

    def evidence_spike(self):
        # Spike prior: theta ~ Uniform(0.47, 0.53), density p(theta | spike) = 1 / (0.53 - 0.47)
        # evidence = integral of likelihood(theta) * (1 / 0.06) d_theta from 0.47 to 0.53
        prior_density = 1 / (0.53 - 0.47)
        integrand = lambda theta: self.likelihood(theta) * prior_density
        result, _ = quad(integrand, 0.47, 0.53)
        return float(result)

    def bayes_factor(self):
        slab_ev = self.evidence_slab()
        spike_ev = self.evidence_spike()
        
        if slab_ev == 0 or abs(slab_ev) < 1e-15:
            raise ValueError("Bayes Factor undefined; slab evidence ≈ 0")
        
        return float(spike_ev / slab_ev)