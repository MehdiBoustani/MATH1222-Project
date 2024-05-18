import numpy as np
import matplotlib.pyplot as plt
from copy import deepcopy

# CONSTANTS
SIMULATIONS = 25
STEPS = 60

# Transition probabilites
beta1 = 0.006
beta2 = beta1 / 2
mu = 0.2

alpha = 0

W_e = np.load("We.npy") # Adjacency matrix -- Connections between entreprises
N_s = np.load("Ns.npy") # Number of servers of each entreprise -- vector
nbEntreprises = len(W_e)

# Enumerate servers
V = 0 
I = 1
P = 2

# Define our network containing all entreprises and their connections
def initNetwork():
    network = {}
    for entreprise in range(nbEntreprises):
        # Number of servers for each entreprise
        nbServers = N_s[entreprise]
        
        # Connected entreprises to the current 
        connectedEntreprises = np.where(W_e[entreprise] == 1)[0].tolist()

        # {entreprise : {'connections' : [], 'servers' : [] } }
        network[entreprise] = {
            "connections": connectedEntreprises,
            "servers": [nbServers, 0, 0]
        }

    return network

"""
    @brief : gets the number of intern infected servers and the total number of the extern infected servers (connected entreprises)

    @param entreprise : an entreprise
    @param infectionsList : a list of all infections at the current step (not updated)

    @returns : tuple() : number of intern infected servers, number of extern infected servers

    """
def getNbInfected(network, entreprise, infectionsList):
    internInfected = network[entreprise]['servers'][I] # number of infected servers inside the entreprise
    externInfected = 0

    # search for servers in connections
    for e in network[entreprise]['connections']:

        # add the number of outside infected servers to our counter
        externInfected += infectionsList[e]
    
    return internInfected, externInfected

def getCurrentNumbers(network):
    # currentServers = np.zeros(3, dtype=int) # store number of servers in each category
    currentInfections = np.empty(nbEntreprises)
    for e in network:
        currentInfections[e] = network[e]['servers'][I]
        # currentServers[V] += network[e]['servers'][V]
        # currentServers[I] += network[e]['servers'][I]
        # currentServers[P] += network[e]['servers'][P]
    
    return currentInfections #, currentServers

def simulate(network, timeSteps):

    totalServers_e0 = np.zeros((3, STEPS), dtype=int)  # Array to store total number of servers in each category at each step 

    for s in range(timeSteps):
        # currentInfections, currentServers = getCurrentNumbers(network)
        currentInfections = getCurrentNumbers(network)

        totalServers_e0[:, s] += network[0]['servers']

        # print("Vulnerables = {}, Infected = {}, Protected = {} at step {}".format(currentServers[V], currentServers[I], currentServers[P], s))
        for e in network:
            internInfected, externInfected = getNbInfected(network, e, currentInfections)
             # probability of a vulnerable server to be infected
            infectionProb = 1 - ((1-beta1)**internInfected) * ((1-beta2)**externInfected)
            
            nbServers_V_to_I = 0
            nbServers_I_to_P = 0

            # internInfected = I(t)
            nbVulnerables = network[e]['servers'][V] # V(t)
            nbProtected = network[e]['servers'][P]   # P(t)

            for v in range(nbVulnerables):
                if np.random.rand() < infectionProb :
                    nbServers_V_to_I += 1
            
            for i in range(internInfected):
                if np.random.rand() < mu :
                    nbServers_I_to_P += 1

            network[e]['servers'][V] -= nbServers_V_to_I # V(t+1)
            network[e]['servers'][I] += nbServers_V_to_I - nbServers_I_to_P # I(t+1)
            network[e]['servers'][P] += nbServers_I_to_P # P(t+1)

    # return the array to store total number of servers in each category at each step for entreprise 0
    return totalServers_e0

def main():
    initialNetwork = initNetwork()

    # Initial state : the virus attacks company/entreprise 0 -> one infected server
    initialNetwork[0]['servers'][I] += 1
    initialNetwork[0]['servers'][V] -= 1

    # Array to store number of servers in each categorie at each step for ALL simulations
    averageServers_e0 = np.zeros((3, STEPS))

    for sim in range(SIMULATIONS):
        network = deepcopy(initialNetwork)
        totalServers_e0 = simulate(network, STEPS)
        averageServers_e0 += totalServers_e0
    
    averageServers_e0 /= SIMULATIONS

    # Plotting
    plt.plot(range(STEPS), averageServers_e0[V], label='Vulnérables (V)')
    plt.plot(range(STEPS), averageServers_e0[I], label='Infectés (I)')
    plt.plot(range(STEPS), averageServers_e0[P], label='Protégés (P)')

    # Plot
    plt.xlabel('Temps')
    plt.ylabel('Nombre de serveurs')
    plt.title('Nombre moyen de serveurs "Entreprise 0" : {} Simulations'.format(SIMULATIONS))
    plt.legend()
    plt.show()

main()