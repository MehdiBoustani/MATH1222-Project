import numpy as np
import matplotlib.pyplot as plt

# CONSTANTS
SIMULATIONS = 50
STEPS = 50

# --------------- Transitions ------------------ #

beta = 0.3
mu = 0.4
alpha = 0
# alpha = 0.05
# alpha = 0.1
# alpha = 0.15 
# alpha = 0.2

V_to_I = beta
V_to_V =  1 - beta

I_to_P = mu
I_to_I = 1 - mu

P_to_V = alpha
P_to_P = 1 - alpha

# ------------------------------------------- #

# Connection matrix
W  = np.loadtxt("Wsf.txt")
N = len(W) # number of servers

# V = 0
# I = 1
# P = 2

# Initial state
nbInfected    = int(0.005 * N)
nbVulnerables = N - nbInfected
nbProtected   = 0

initialConfig = np.array([1] * nbInfected + [0] * nbVulnerables)
np.random.shuffle(initialConfig)

# Time (in STEPS) until the eradication of the virus
eradicationTime = 0

# Lists to store counts of servers in each category at each time step for ALL SIMULATIONS
totalCountsV = np.zeros(STEPS)
totalCountsI = np.zeros(STEPS)
totalCountsP = np.zeros(STEPS)

for sim in range(SIMULATIONS):
    current_configuration = initialConfig

    eradicated = False

    totalCountsV[0] += nbVulnerables
    totalCountsI[0] += nbInfected
    totalCountsP[0] += nbProtected

    for i in range(STEPS-1): # time steps

        V_to_I = beta
        V_to_V =  1 - beta

        if not eradicated and 1 not in current_configuration:
            eradicationTime += i
            eradicated = True

        next_configuration = []
        
        # Run through servers
        for j in range(N):            
                
            serverState = current_configuration[j]
            
            # current server = V
            if serverState == 0:
                if not eradicated :
                    # vector multiplication to get the number of connected and infected nodes
                    connectedInfected = np.dot(current_configuration % 2, W[j])
                else : 
                    connectedInfected = 0
               
                V_to_V = (1-beta)**connectedInfected
               
                V_to_I = 1 - V_to_V

                if np.random.rand() <= V_to_I :
                    nextState = 1
                    totalCountsI[i+1] += V_to_I
                    
                else :

                    nextState = 0
                    totalCountsV[i+1] += V_to_V
                    
            # current server = I
            elif serverState == 1 :
               
                if np.random.rand() <= I_to_P : 
                    nextState = 2 # I to P
                    totalCountsP[i+1] += I_to_P

                else :
                    nextState = 1 # I to I
                    totalCountsI[i+1] += I_to_I

            # current server = I
            elif serverState == 2 :
                
                if np.random.rand() <= P_to_V :
                    nextState = 0 # P to V
                    totalCountsV[i+1] += P_to_V

                else :
                    nextState = 2 # P to P
                    totalCountsP[i+1] += P_to_P

            next_configuration.append(nextState)
        
        current_configuration = np.array(next_configuration)

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
plt.title('Évolution du nombre moyen de serveurs dans chaque catégorie')
plt.legend()
plt.show()