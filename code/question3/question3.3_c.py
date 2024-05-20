import numpy as np
import matplotlib.pyplot as plt
import random

# ---------------------------------------- QUESTION 3.3 --------------------------------- #
""" 
    Expérience pour vérifier l'existence du seuil d'épidémie au sein d'un réseau
        partant de l'état initial où tous les serveurs sont infectés

     """

# CONSTANTS
SIMULATIONS = 100
STEPS = 1000

""" ORDRE DE 0.8 """
beta = 0.0001
mu = 0.124875
alpha = 1

# beta = 0.0003
# mu = 0.374625
# alpha = 1

""" ORDRE DE 2 """
# beta = 0.0001
# mu = 0.04995
# alpha = 1

# beta = 0.0003
# mu = 0.14985
# alpha = 1


N = 1000 # number of servers

W = np.ones((N, N), dtype=int)
np.fill_diagonal(W, 0)

# Check βλ/μ 
greatestEigenvalue = np.linalg.eigvalsh(W)[-1]
print("Greatest eigenvalue = ", greatestEigenvalue)
# print((beta*greatestEigenvalue)/mu)

print(" beta/mu <= 1/greatest eigenvalue ? ", (beta/mu) <= (1/greatestEigenvalue)) # 


# Initial state
nbInfected    = N # 100 % of servers are infected
nbVulnerables = 0
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
        if not eradicated:
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

# Get infected average numbers. Note : We start at step = 1 to step = 1000 (instead of 0 to 999) to satisfy the log scale 
infected = np.zeros(STEPS+1)
infected[1:] = averageCounts[:, 1]
infected[-1] = averageCounts[-1, 1]

# Plot
plt.plot(infected, label='Infectés (I)', color='red')

plt.xlabel('Temps')
plt.ylabel('Nombre de serveurs')
plt.yscale('symlog')
plt.xscale('symlog')
plt.title('Nombre moyen de serveurs infectés : {} Simulations'.format(SIMULATIONS))
plt.xlim(left=1)
plt.ylim(bottom=1)

# Format x-axis ticks
ax = plt.gca()
ax.xaxis.set_major_formatter(plt.FormatStrFormatter('%d'))

# Format y-axis ticks
ax.yaxis.set_major_formatter(plt.FormatStrFormatter('%d'))

plt.legend()
plt.show()