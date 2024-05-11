import numpy as np
import matplotlib.pyplot as plt
import random

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


# Time (in steps) until the eradication of the virus
eradicationTime = 0

# Lists to store counts of servers in each category at each time step for ALL simulations
countsV_all = []
countsI_all = []
countsP_all = []

simulations = 1000
steps = 200

for sim in range(simulations):
    current_configuration = initialConfig
 
    eradicated = False

    # List to store counts of servers in each category at each time step
    countsV = [1]
    countsI = [1]
    countsP = [0]

    for i in range(steps-1): # ti

        # Check if we have reached virus eradication
        if not eradicated and 'I' not in current_configuration:
            eradicationTime += i
            eradicated = True

        countsV.append(0)
        countsI.append(0)
        countsP.append(0)

        next_configuration = []
        
        for j in range(networkSize):            
                
            serverState = current_configuration[j]

            # check connections
            if serverState == 'V':

                k = 0
                infectable = False
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

          
            # choose the next state based on transition probabilites
            nextState = random.choices(list(transition_probs[serverState].keys()), weights=list(transition_probs[serverState].values()))[0]

            prob = transition_probs[serverState][nextState]

            if nextState == 'V':
                countsV[i+1] += prob
            
            elif nextState == 'I' :
                countsI[i+1] += prob

            elif nextState == 'P' :
                countsP[i+1] += prob
            

            # update current server state to the next state
            
            next_configuration.append(nextState)
        
        current_configuration =  next_configuration

  
    countsV_all.append(countsV)
    countsI_all.append(countsI)
    countsP_all.append(countsP)

print("La temps moyen pour l'eradication du virus = ", eradicationTime/simulations)

# Calculate the average counts over all simulations


average_countsV = np.mean(countsV_all, axis=0)    
average_countsI = np.mean(countsI_all, axis=0)
average_countsP = np.mean(countsP_all, axis=0)

# Plotting
time_steps = range(steps)
plt.plot(time_steps, average_countsV, label='V')
plt.plot(time_steps, average_countsI, label='I')
plt.plot(time_steps, average_countsP, label='P')
plt.xlabel('Temps')
plt.ylabel('Nombre de serveurs')
plt.title('Nombre moyen de serveurs dans chaque catégorie')
plt.legend()
plt.show()


# test PYDTMC
# import pydtmc
# p = [ [0.45, 0, 0, 0.05, 0, 0.05, 0, 0.45, 0],
#     [0, 0.45, 0.05, 0, 0.05, 0, 0, 0.45, 0],
#     [0.045, 0, 0.855, 0, 0, 0.005, 0.095, 0, 0],
#     [0, 0.045, 0, 0.855, 0.005, 0, 0.095, 0, 0],
#     [0, 0, 0, 0, 0.95, 0, 0, 0, 0.05],
#     [0, 0, 0, 0, 0, 0.95, 0, 0, 0.05],
#     [0, 0, 0, 0, 0.0475, 0.0475, 0.9025, 0, 0.0025],
#     [0, 0, 0.09, 0.09, 0, 0, 0.01, 0.81, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 1]]
# mc = pydtmc.MarkovChain(p, ['IV', 'VI', 'IP', 'PI', 'VP', 'PV', 'PP', 'II', 'VV'])
# print(mc)
# print(mc.transient_states)
# print(mc.steady_states)
# print(mc.simulate(100, seed=32))
