import numpy as np
import matplotlib.pyplot as plt
import random

# CONSTANTS
SIMULATIONS = 10000
STEPS = 200

# Transitions
beta = 0.5
mu = 0.1
alpha = 0.05

transition_probs = {
    'V': {'V': 1-beta, 'I': beta, 'P': 0},
    'I': {'V': 0, 'I': 1-mu, 'P': mu},
    'P': {'V': alpha, 'I': 0, 'P': 1-alpha}
}

# Connection matrix
W = np.array([
                [0, 1],
                [1, 0],
            ])

# Initial state
initialConfig = random.choice([['V', 'I'], ['I', 'V']])
networkSize = len(initialConfig)

# Time (in STEPS) until the eradication of the virus
eradicationTime = 0

# Lists to store counts of servers in each category at each time step for ALL SIMULATIONS
totalCountsV = np.zeros(STEPS)
totalCountsI = np.zeros(STEPS)
totalCountsP = np.zeros(STEPS)

for sim in range(SIMULATIONS):
    current_configuration = initialConfig
 
    eradicated = False

    totalCountsV[0] += 1
    totalCountsI[0] += 1

    
    for i in range(STEPS-1): # ti

        # Check if we have reached virus eradication
        if not eradicated and 'I' not in current_configuration:
            eradicationTime += i
            eradicated = True

        next_configuration = []
        
        for j in range(networkSize):            
                
            serverState = current_configuration[j]

            # check connections
            if serverState == 'V':

                k = 0
                infectable = False

                # Check connections and infection
                while k < networkSize and not infectable:
                    if k != j and W[j][k] == 1: # must be connected 

                        if current_configuration[k] == 'I' : # a connected server is infected
                            # the current server can be infected
                            transition_probs['V']['V'], transition_probs['V']['I'] = 1-beta, beta
                            infectable = True
                        else :
                            # no connected server was infected
                            transition_probs['V']['V'], transition_probs['V']['I'] = 1, 0

                    k += 1 # next server
          
            # Choose the next state based on transition probabilites
            nextState = random.choices(list(transition_probs[serverState].keys()), weights=list(transition_probs[serverState].values()))[0]

            prob = transition_probs[serverState][nextState]

            if nextState == 'V':
                totalCountsV[i+1] += prob
            
            elif nextState == 'I' :
                totalCountsI[i+1] += prob

            elif nextState == 'P' :
                totalCountsP[i+1] += prob
            
            # Update current server state to the next state   
            next_configuration.append(nextState)
        
        current_configuration =  next_configuration


print("La temps moyen pour l'eradication du virus = ", eradicationTime/SIMULATIONS)

# Get the average counts over all SIMULATIONS
for i in range(STEPS):
    totalCountsV[i] /= SIMULATIONS
    totalCountsI[i] /= SIMULATIONS
    totalCountsP[i] /= SIMULATIONS

# Plotting
time_steps = range(STEPS)
plt.plot(time_steps, totalCountsV, label='V')
plt.plot(time_steps, totalCountsI, label='I')
plt.plot(time_steps, totalCountsP, label='P')
plt.xlabel('Temps')
plt.ylabel('Nombre de serveurs')
plt.title('Nombre moyen de serveurs dans chaque catégorie : {} SIMULATIONS'.format(SIMULATIONS))
plt.legend()
plt.show()