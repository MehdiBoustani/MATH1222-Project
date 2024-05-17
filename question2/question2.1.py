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
    current_configuration = initialConfig.copy()
    
    eradicated = False

    totalCountsV[0] += current_configuration.count('V')
    totalCountsI[0] += current_configuration.count('I')
    totalCountsP[0] += current_configuration.count('P')
    
    for i in range(1, STEPS):
        if not eradicated and 'I' not in current_configuration:
            eradicationTime += i
            eradicated = True
        
        next_configuration = []
        
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
plt.xlabel('Temps')
plt.ylabel('Nombre de serveurs')
plt.title('Nombre moyen de serveurs dans chaque catégorie : {} SIMULATIONS'.format(SIMULATIONS))
plt.legend()
plt.show()
