import numpy as np
import matplotlib.pyplot as plt
from scipy.sparse import csr_matrix
import random

# CONSTANTS
SIMULATIONS = 100
STEPS = 25

# Transitions
beta = 0.3
mu = 0.4
alpha = 0

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

# WE CAN ADD infectedNumber to avoid if not eradicated and 'I' not in current_configuration:

totalCountsV = np.zeros(STEPS)
totalCountsI = np.zeros(STEPS)
totalCountsP = np.zeros(STEPS)

for sim in range(SIMULATIONS):
    current_configuration = initialConfig
 
    eradicated = False

    totalCountsV[0] += (N / 2)
    totalCountsI[0] += (N / 2)

    for i in range(STEPS-1): # ti

        # Check if we have reached virus eradication
        if not eradicated and 'I' not in current_configuration:
            eradicationTime += i
            eradicated = True


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
                    # No server is connected : beta = 0
                    transition_probs['V']['V'], transition_probs['V']['I'] = 1, 0

            # choose the next state based on transition probabilites
            nextState = random.choices(list(transition_probs[serverState].keys()), weights=list(transition_probs[serverState].values()))[0]

            # get the probability to be in the chosen state
            prob = transition_probs[serverState][nextState]

            if nextState == 'V':
                totalCountsV[i+1] += prob
            
            elif nextState == 'I' :
                totalCountsI[i+1] += prob

            elif nextState == 'P' :
                totalCountsP[i+1] += prob
            
            next_configuration.append(nextState)
        
        # Update to new states 
        current_configuration =  next_configuration

# Eradication average time
if (eradicated):
    print("La temps moyen pour l'eradication du virus = ", eradicationTime/SIMULATIONS)
else :
    print("Le virus n'a pas été complètement éradiqué après {} Etaps".format(STEPS))

# Get average time
for i in range(STEPS):
    totalCountsV[i] /= SIMULATIONS
    totalCountsI[i] /= SIMULATIONS
    totalCountsP[i] /= SIMULATIONS

# Plotting
time_STEPS = range(STEPS)
plt.plot(time_STEPS, totalCountsV, label='V')
plt.plot(time_STEPS, totalCountsI, label='I')
plt.plot(time_STEPS, totalCountsP, label='P')
plt.xlabel('Temps')
plt.ylabel('Nombre de serveurs')
plt.ylim(0, N)
plt.title('Nombre moyen de serveurs dans chaque catégorie : {} Simulations'.format(SIMULATIONS))
plt.legend()
plt.show()