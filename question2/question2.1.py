import numpy as np
import matplotlib.pyplot as plt

# CONSTANTS
SIMULATIONS = 10000
STEPS = 100

# ----------- Transitions ----------- #
beta = 0.5
mu = 0.1
alpha = 0.05

V_to_I = beta
V_to_V =  1 - beta

I_to_P = mu
I_to_I = 1 - mu

P_to_V = alpha
P_to_P = 1 - alpha

# --------------------------------- #

# Connection matrix
W = np.array([
                [0, 1],
                [1, 0],
            ])
N = len(W)

# V = 0
# I = 1
# P = 2

# Choose initial configuration randomly
init1 = np.array([1, 0]) # IV 
init2 = np.array([0, 1]) # VI
randInit = np.random.randint(2) 
initialConfig = init1 if randInit == 0 else init2

# Time (in STEPS) until the eradication of the virus
eradicationTime = 0

# Lists to store counts of servers in each category at each time step for ALL SIMULATIONS
totalCountsV = np.zeros(STEPS)
totalCountsI = np.zeros(STEPS)
totalCountsP = np.zeros(STEPS)

for sim in range(SIMULATIONS):
    current_configuration = initialConfig.copy()
<<<<<<< Updated upstream
    
    eradicated = False

    totalCountsV[0] += current_configuration.count('V')
    totalCountsI[0] += current_configuration.count('I')
    totalCountsP[0] += current_configuration.count('P')
    
    for i in range(1, STEPS):
        if not eradicated and 'I' not in current_configuration:
=======

    eradicated = False

    totalCountsV[0] += 1
    totalCountsI[0] += 1

    for i in range(STEPS-1): # time steps

        V_to_I = beta
        V_to_V =  1 - beta

        if not eradicated and 1 not in current_configuration:
>>>>>>> Stashed changes
            eradicationTime += i
            eradicated = True
        
        next_configuration = []
        
<<<<<<< Updated upstream
        for j in range(networkSize):
            serverState = current_configuration[j]
            if serverState == 'V':
                infectable = any(current_configuration[k] == 'I' and W[j][k] == 1 for k in range(networkSize))
                if infectable:
                    transition_probs['V']['V'], transition_probs['V']['I'] = 1-beta, beta
                else:
                    transition_probs['V']['V'], transition_probs['V']['I'] = 1, 0

            nextState = random.choices(list(transition_probs[serverState].keys()), weights=list(transition_probs[serverState].values()))[0]
            next_configuration.append(nextState)
        
        current_configuration = next_configuration
        
        totalCountsV[i] += current_configuration.count('V')
        totalCountsI[i] += current_configuration.count('I')
        totalCountsP[i] += current_configuration.count('P')

# Calcul des moyennes
totalCountsV /= SIMULATIONS
totalCountsI /= SIMULATIONS
totalCountsP /= SIMULATIONS

print("Le temps moyen pour l'éradication du virus = ", eradicationTime / SIMULATIONS)

# Plotting
time_steps = range(STEPS)
plt.plot(time_steps, totalCountsV, label='V')
plt.plot(time_steps, totalCountsI, label='I')
plt.plot(time_steps, totalCountsP, label='P')
=======
        # Run through servers
        for j in range(N):            
                
            serverState = current_configuration[j]
            
            # current server = V
            if serverState == 0:
                if not eradicated :
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

>>>>>>> Stashed changes
plt.xlabel('Temps')
plt.ylabel('Nombre moyen de serveurs')
plt.title('Évolution du nombre moyen de serveurs dans chaque catégorie')
plt.legend()
plt.show()
