import numpy as np
import matplotlib.pyplot as plt
from copy import deepcopy

# CONSTANTS
SIMULATIONS = 25
STEPS = 150

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

"""
    @brief : Initializes a network using We and Ns 
    @returns : dict() : the created network

    """
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
    @brief : gets the number of intern infected servers (i.e inside the entreprise) and the total number of the extern infected servers (of connected entreprises)

    @param network : a dictionnary giving a network
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


"""
    @brief : Creates two lists : a list containing the current infections, and a list containing total servers in each category for all network

    @param network : a dictionnary giving a network

    @returns : List() : List containing the number of infected servers in each entreprise of the network
               List() : a list containing total number of servers in each category for all network

    """
def getCurrentNumbers(network):
    currentServers = np.zeros(3, dtype=int) # store number of servers in each category
    currentInfections = np.empty(nbEntreprises)
    for e in network:
        currentInfections[e] = network[e]['servers'][I]
        currentServers[V] += network[e]['servers'][V]
        currentServers[I] += network[e]['servers'][I]
        currentServers[P] += network[e]['servers'][P]
    
    return currentInfections, currentServers


"""
    @brief : Simulates the markov chain of our network for a given number of steps

    @param network : a dictionnary giving a network
    @param timeSteps : the steps (duration) of the simulator

    @returns np array of arrays containing the total number of servers in each category at every step

    """
def simulate(network, timeSteps):

    totalServers = np.zeros((3, STEPS), dtype=int)  # Array to store total number of servers in each category at each step 

    for s in range(timeSteps):
        currentInfections, currentServers = getCurrentNumbers(network)
        totalServers[:, s] += currentServers
        

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

    return totalServers


def main():
    initialNetwork = initNetwork()

    # Initial state : the virus attacks company/entreprise 0 -> one infected server
    initialNetwork[0]['servers'][I] += 1
    initialNetwork[0]['servers'][V] -= 1

    # Array to store number of servers in each categorie at each step for ALL simulations
    averageServers = np.zeros((3, STEPS))

    for sim in range(SIMULATIONS):
        network = deepcopy(initialNetwork)
        totalServers = simulate(network, STEPS)
        averageServers += totalServers
    
    averageServers /= SIMULATIONS

    # Plotting
    plt.plot(range(STEPS), averageServers[V], label='Vulnérables (V)')
    plt.plot(range(STEPS), averageServers[I], label='Infectés (I)')
    plt.plot(range(STEPS), averageServers[P], label='Protégés (P)')

    # Plot
    plt.xlabel('Temps')
    plt.ylabel('Nombre de serveurs')
    plt.title('Nombre moyen de serveurs dans le réseau : {} Simulations'.format(SIMULATIONS))
    plt.legend()
    plt.show()

main()