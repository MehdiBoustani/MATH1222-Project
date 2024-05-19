import numpy as np
import matplotlib.pyplot as plt
import random

# CONSTANTS
SIMULATIONS = 10000
STEPS = 200

# --------------- Transitions ------------------ #

beta = 0.5
mu = 0.1
alpha = 0.05

V_to_I = beta
V_to_V =  1 - beta

I_to_P = mu
I_to_I = 1 - mu

P_to_V = alpha
P_to_P = 1 - alpha

# ------------------------------------------- #

# Connection matrix
W = np.array([[0, 1], [1, 0]])
N = len(W) # number of servers

V = 0
I = 1
P = 2

# Initial state
nbInfected    = 1
nbVulnerables = 1
nbProtected   = 0

array1 = np.array([I, V])
array2 = np.array([V, I])

# Choose randomly between the two arrays
initialConfig = random.choice([array1, array2])

# Time (in STEPS) until the eradication of the virus
eradicationTime = 0

# Lists to store counts of servers in each category at each time step for ALL SIMULATIONS
totalCountsV = np.zeros(STEPS)
totalCountsI = np.zeros(STEPS)
totalCountsP = np.zeros(STEPS)

for sim in range(SIMULATIONS):
    currentConfiguration = initialConfig

    eradicated = False

    # number of servers in initial configuration
    totalCountsV[0] += np.sum(currentConfiguration == V)
    totalCountsI[0] += np.sum(currentConfiguration == I)
    totalCountsP[0] += np.sum(currentConfiguration == P)
        
    for i in range(STEPS-1): # time steps

        if not eradicated and I not in currentConfiguration:
            eradicationTime += i
            eradicated = True

        nextConfiguration = []
        
        # Run through servers
        for j in range(N):            
                
            serverState = currentConfiguration[j]
            
            # current server = V
            if serverState == V:
                if not eradicated :

                    # Vector multiplication to get the number of connected and infected nodes
                    connectedInfected = np.dot(currentConfiguration % 2, W[j])
                else : 
                    connectedInfected = 0
               
                V_to_V = (1-beta)**connectedInfected
               
                V_to_I = 1 - V_to_V

                if np.random.rand() <= V_to_I :
                    nextState = I # V to I
                    totalCountsI[i+1] += 1
                    
                else :
                    nextState = V # V to V
                    totalCountsV[i+1] += 1
                    
            # current server = I
            elif serverState == I :

                if np.random.rand() <= I_to_P : 
                    nextState = P # I to P
                    totalCountsP[i+1] += 1

                else :
                    nextState = I # I to I
                    totalCountsI[i+1] += 1

            # current server = P
            elif serverState == P :
                
                if np.random.rand() <= P_to_V :
                    nextState = V # P to V
                    totalCountsV[i+1] += 1

                else :
                    nextState = P # P to P
                    totalCountsP[i+1] += 1

            nextConfiguration.append(nextState)
        
        currentConfiguration = np.array(nextConfiguration)

if eradicated :
    print("La temps moyen pour l'eradication du virus = ", eradicationTime/SIMULATIONS)
else :
    print("Le virus n'a pas été éradiqué après {} pas de temps".format(STEPS))

    
# Get the average counts over all SIMULATIONS
totalCountsV /= SIMULATIONS
totalCountsI /= SIMULATIONS
totalCountsP /= SIMULATIONS

timeSteps = range(STEPS)
plt.plot(timeSteps, totalCountsV, label='Vulnérables (V)')
plt.plot(timeSteps, totalCountsI, label='Infectés (I)')
plt.plot(timeSteps, totalCountsP, label='Protégés (P)')

plt.xlabel('Temps')
plt.ylabel('Nombre moyen de serveurs')
plt.title('Évolution du nombre moyen de serveurs : {} Simulations'.format(SIMULATIONS))
plt.legend()
plt.show()