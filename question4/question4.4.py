import numpy as np
import matplotlib.pyplot as plt
from copy import deepcopy

# CONSTANTS

SIMULATIONS = 25
STEPS = 250

# Transition probabilites
beta1 = 0.006
beta2 = beta1 / 2
mu_network = 0.2

alpha = 0

W_e = np.load("We.npy") # Adjacency matrix -- Connections between entreprises
N_s = np.load("Ns.npy") # Number of servers of each entreprise -- vector
nbEntreprises = len(W_e)

# Enumerate servers
V = 0 
I = 1
P = 2

SEGI = 220

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
    currentServers = np.zeros(3, dtype=int) # store number of servers in each category
    currentInfections = np.empty(nbEntreprises)
    for e in network:
        currentInfections[e] = network[e]['servers'][I]
        currentServers[V] += network[e]['servers'][V]
        currentServers[I] += network[e]['servers'][I]
        currentServers[P] += network[e]['servers'][P]
    
    return currentInfections, currentServers

def simulate(network, timeSteps, mu_SEGI):

    totalServers = np.zeros((3, STEPS), dtype=int)  # Array to store total number of servers in each category at each step 

    maxInfectedSEGI = 0

    step = 0
    eradicated = False
    while step < timeSteps+1 and not eradicated:

        currentInfections, currentServers = getCurrentNumbers(network)

        if currentServers[I] == 0:
            eradicated = True
        
        infectedSEGI = network[SEGI]['servers'][I]
        if infectedSEGI > maxInfectedSEGI :
            maxInfectedSEGI = infectedSEGI

        for e in network:
            internInfected, externInfected = getNbInfected(network, e, currentInfections)
             # probability of a vulnerable server to be infected
            infectionProb = 1 - ((1-beta1)**internInfected) * ((1-beta2)**externInfected)
            
            nbServers_V_to_I = 0
            nbServers_I_to_P = 0

            # internInfected = I(t)
            nbVulnerables = network[e]['servers'][V] # V(t)
            nbProtected = network[e]['servers'][P]   # P(t)

            if e == SEGI :
                mu = mu_SEGI
            else :
                mu = mu_network

            for v in range(nbVulnerables):
                if np.random.rand() < infectionProb :
                    nbServers_V_to_I += 1
            
            for i in range(internInfected):
                if np.random.rand() < mu :
                    nbServers_I_to_P += 1


            network[e]['servers'][V] -= nbServers_V_to_I # V(t+1)
            network[e]['servers'][I] += nbServers_V_to_I - nbServers_I_to_P # I(t+1)
            network[e]['servers'][P] += nbServers_I_to_P # P(t+1)
        
        step += 1

    return maxInfectedSEGI

def main():
    initialNetwork = initNetwork()

    # Initial state : the virus attacks company/entreprise 0 -> one infected server
    initialNetwork[0]['servers'][I] += 1
    initialNetwork[0]['servers'][V] -= 1

    mu_SEGI = mu_network

    target = 0.01

    targetReached = False
    delta_mu = 0.01

    while not targetReached:

        count_exceed_10 = 0

        for sim in range(SIMULATIONS):
            network = deepcopy(initialNetwork)

            maxInfectedSEGI = simulate(network, STEPS, mu_SEGI)
            if maxInfectedSEGI > 10:
                count_exceed_10 += 1

        dangerProb = count_exceed_10/SIMULATIONS

        if dangerProb < target :
            targetReached = True
        
        else :
            mu_SEGI += delta_mu
    
    print("la valeur de μ du nouvel antivirus devrait être autour de : ", mu_SEGI)

    print("Probabilité d'avoir au moins 20 pourcent de machines infectées simultanément au SEGI est de {} avec μ = {} ".format(dangerProb, mu_SEGI))

main()