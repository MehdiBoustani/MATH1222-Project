import numpy as np
import matplotlib.pyplot as plt
import random

# CONSTANTS
SIMULATIONS = 10000
STEPS = 100

beta = 0.5
mu = 0.1
alpha = 0.05

initialConfig =  np.array([1, 1, 0])

# Store average number of servers counts during simulations 
averageCounts = np.zeros((STEPS, 3))  # For V, I, and P counts

# Store average time befire the eradication of the virus
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

        for v in range(V):
            if random.random() < InfectionProb :
                num_servers_V_to_I += 1

        for i in range(I):
            if random.random() < mu :
                num_servers_I_to_P += 1

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
plt.plot(averageCounts[:, 0], label='Vulnérables (V)')
plt.plot(averageCounts[:, 1], label='Infectés (I)')
plt.plot(averageCounts[:, 2], label='Protégés (P)')

plt.xlabel('Temps')
plt.ylabel('Nombre de serveurs')
plt.legend()
plt.title('Nombre moyen de serveurs dans chaque catégorie : {} Simulations'.format(SIMULATIONS))
plt.show()