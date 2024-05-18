import numpy as np
import matplotlib.pyplot as plt
import random

# ---------------------------------------- QUESTION 3.3 --------------------------------- #
"""
     Impact du paramètre alpha sur la convergence du nombre de serveurs infectés 
        Avec un état initial de 0.5% de serveurs infectés.

    """

# CONSTANTS
SIMULATIONS = 100
STEPS = 100

beta = 0.3
mu = 0.4

# Test of different values of alpha
alpha = 0.01
# alpha = 0.03
# alpha = 0.05
# alpha = 0.1
# alpha = 0.15
# alpha = 0.2

N = 1000 # number of servers

# Initial state
nbInfected    = int(0.005 * N) # 0.5 % of servers are infected
nbVulnerables = N - nbInfected
nbProtected   = 0

initialConfig =  np.array([nbVulnerables, nbInfected, nbProtected])
currentConfig = np.copy(initialConfig)

averageCounts = np.zeros((STEPS, 3))  # For V, I, and P counts

eradicationTime = 0

for sim in range(SIMULATIONS):

    currentConfig = np.copy(initialConfig)

    counts = np.zeros((STEPS, 3))
    counts[0] = currentConfig
    eradicated = False

    for s in range(1, STEPS):
        
        V = currentConfig[0]
        I = currentConfig[1]
        P = currentConfig[2]

        if I == 0 and not eradicated:
            eradicationTime += s-1
            eradicated = True

        InfectionProb = 1 - (1 - beta) ** I

        num_servers_V_to_I = 0
        num_servers_I_to_P = 0
        num_servers_P_to_V = 0

        # V servers
        for v in range(V):
            if random.random() < InfectionProb :
                num_servers_V_to_I += 1

        # I servers
        for i in range(I):
            if random.random() < mu :
                num_servers_I_to_P += 1

        # P servers
        for p in range(P):
            if random.random() < alpha :
                num_servers_P_to_V += 1

        # Update servers numbers
        currentConfig[0] += num_servers_P_to_V - num_servers_V_to_I # V(t+1)
        currentConfig[1] += num_servers_V_to_I - num_servers_I_to_P # I(t+1)
        currentConfig[2] += num_servers_I_to_P - num_servers_P_to_V # P(t+1)

        counts[s] = currentConfig

    averageCounts += counts
       
if eradicated :
    print("La temps moyen pour l'eradication du virus = ", eradicationTime/SIMULATIONS)
else :
    print("Le virus n'a pas complètement disparu dans le réseau")


averageCounts /= SIMULATIONS # average numbers 

# Plot
# plt.plot(averageCounts[:, 0], label='Vulnérables (V)')
plt.plot(averageCounts[:, 1], label='Infectés (I)')
# plt.plot(averageCounts[:, 2], label='Protégés (P)')

plt.xlabel('Temps')
plt.ylabel('Nombre de serveurs')
plt.legend()
plt.title('Nombre moyen de serveurs infectés : {} Simulations'.format(SIMULATIONS))
plt.show()