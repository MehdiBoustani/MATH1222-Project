import numpy as np
import matplotlib.pyplot as plt
from scipy.sparse import csr_matrix
import random

# CONSTANTS
SIMULATIONS = 10
STEPS = 100

# """ ORDRE DE 0.8 """
beta = 0.05
mu = 0.625
alpha = 1

# """ ORDRE DE 2 """
# beta = 0.1
# mu = 0.5
# alpha = 1


transition_probs = {
    'V': {'V': 1-beta, 'I': beta, 'P': 0},
    'I': {'V': 0, 'I': 1-mu, 'P': mu},
    'P': {'V': alpha, 'I': 0, 'P': 1-alpha}
}

W  = np.loadtxt("Wsf.txt")

N = len(W) # number of servers

# Use sparse matrix data structure : CSR
sparseW = csr_matrix(W)

greatestEigenvalue = np.linalg.eigvalsh(W)[-1]
print("Greatest eigenvalue = ", greatestEigenvalue)
print((beta*greatestEigenvalue)/mu)

print(" beta/mu <= greatest eigenvalue ? ", (beta/mu) <= (1/greatestEigenvalue)) # 


# Initial state
initialConfig = ['I'] * N

# Time (in STEPS) until the eradication of the virus
eradicationTime = 0

countsI_all = []

for sim in range(SIMULATIONS):
    current_configuration = initialConfig
 
    eradicated = False

    countsI = [N]

    for i in range(STEPS-1): # ti

        # Check if we have reached virus eradication
        if not eradicated and 'I' not in current_configuration:
            eradicationTime += i
            eradicated = True

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
print("La temps moyen pour l'eradication du virus = ", eradicationTime/SIMULATIONS)

average_countsI = np.mean(countsI_all, axis=0)

# Plotting
time_STEPS = range(STEPS)
plt.plot(time_STEPS, average_countsI, label='I')
plt.xlabel('Temps')
plt.ylabel('Nombre de serveurs')
plt.yscale('symlog')
plt.xscale('symlog')
plt.title('Nombre moyen de serveurs dans chaque catégorie : {} Simulations'.format(SIMULATIONS))

# Format x-axis ticks
plt.gca().xaxis.set_major_formatter(plt.FormatStrFormatter('%d'))

# Format y-axis ticks
plt.gca().yaxis.set_major_formatter(plt.FormatStrFormatter('%d'))
plt.legend()
plt.show()