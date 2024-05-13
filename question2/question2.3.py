import numpy as np
import matplotlib.pyplot as plt
from scipy.sparse import csr_matrix
import random

# CONSTANTS
SIMULATIONS = 10
STEPS = 100

# Transitions
beta = 0.3
mu = 0.4
alpha = 0.05
#alpha = 0.1
#alpha = 0.2


transition_probs = {
    'V': {'V': 1-beta, 'I': beta, 'P': 0},
    'I': {'V': 0, 'I': 1-mu, 'P': mu},
    'P': {'V': alpha, 'I': 0, 'P': 1-alpha}
}

W  = np.loadtxt("Wsf.txt")

N = len(W) # number of servers

# Use sparse matrix data structure : CSR
sparseW = csr_matrix(W)

# Initial state
initialConfig = ['V', 'I'] * (N // 2)
np.random.shuffle(initialConfig)

# Time (in STEPS) until the eradication of the virus
eradicationTime = 0

countsI_all = []

for sim in range(SIMULATIONS):
    current_configuration = initialConfig
 
    eradicated = False

    countsI = [N/2]

    for i in range(STEPS-1): # ti
        
        # Check if we have reached virus eradication
        if not eradicated :
            if 'I' not in current_configuration :
                eradicated = True

            else :
                eradicationTime += 1

        countsI.append(0)

        next_configuration = []
        
        for j in range(N):            
                
            serverState = current_configuration[j]

            # Check connections
            if serverState == 'V':        

                # Connected servers to the current server
                connectedServers = sparseW[j].indices
                connectedSize = len(connectedServers)

                if connectedSize > 0 :
                    k = 0
                    infectable = False
                    
                    while k < connectedSize and not infectable :

                        if current_configuration[connectedServers[k]] == 'I' :
                            # the current server can be infected
                            transition_probs['V']['V'], transition_probs['V']['I'] = 1-beta, beta

                            # we can stop when an connected server is infected
                            infectable = True
                        else :
                            # no connected server was infected
                            transition_probs['V']['V'], transition_probs['V']['I'] = 1, 0
                        
                        k += 1
                
                else : 
                    transition_probs['V']['V'], transition_probs['V']['I'] = 1, 0

            # choose the next state based on transition probabilites
            nextState = random.choices(list(transition_probs[serverState].keys()), weights=list(transition_probs[serverState].values()))[0]

            # get the probability to be in the chosen state
            prob = transition_probs[serverState][nextState]


            if nextState == 'I' :
                countsI[i+1] += prob
        
            next_configuration.append(nextState)
        
        # Update to new states 
        current_configuration =  next_configuration

    countsI_all.append(countsI)

# Eradication average time
if eradicated :
    print("La temps moyen pour l'eradication du virus = ", eradicationTime/SIMULATIONS)
else :
    print("Le virus n'a pas complètement disparu dans le réseau")

average_countsI = np.mean(countsI_all, axis=0)
# Plotting
time_STEPS = range(STEPS)
plt.plot(time_STEPS, average_countsI, label='I')
plt.xlabel('Temps')
plt.ylabel('Nombre de serveurs')
plt.ylim(0, N)
plt.title('Nombre moyen de serveurs dans chaque catégorie : {} Simulations'.format(SIMULATIONS))
plt.legend()
plt.show()