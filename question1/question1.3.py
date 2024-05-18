import numpy as np
import matplotlib.pyplot as plt


# ------------------------------------------ QUESTION 1.3 --------------------------------------------- #

N = 2 # number of servers
timeSteps = 200 # time steps

# probabilities
beta = 0.5
mu = 0.1
alpha = 0.05

# ORDER OF STATES :  IV VI IP PI VP PV PP II VV

# transition matrix
P = np.array([
            [(1-mu)*(1-beta), 0, 0, mu*beta, 0, mu*(1-beta), 0, beta*(1-mu), 0],
            [0, (1-mu)*(1-beta), mu*beta, 0, mu*(1-beta), 0, 0, beta*(1-mu), 0],
            [alpha*(1-mu), 0, (1-mu)*(1-alpha), 0, 0, mu*alpha, mu*(1-alpha), 0, 0],
            [0, alpha*(1-mu), 0, (1-mu)*(1-alpha), mu*alpha, 0, mu*(1-alpha), 0, 0],
            [0, 0, 0, 0, 1-alpha, 0, 0, 0, alpha],
            [0, 0, 0, 0, 0, 1-alpha, 0, 0, alpha],
            [0, 0, 0, 0, alpha*(1-alpha), alpha*(1-alpha), np.power((1-alpha), 2), 0, np.power((alpha), 2)],
            [0, 0, mu*(1-mu), mu*(1-mu), 0, 0, mu**2, (1-mu)**2, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 1]

            ])

# initial state
                         # IV   VI  IP PI VP PV PP II VV
current_state = np.array([0.5, 0.5, 0, 0, 0, 0, 0, 0, 0])


averageServers_V = []
averageServers_I = []
averageServers_P = []

for i in range(timeSteps):
    # Average time for each categorie in each step
    averageServers_V.append((current_state[0] + current_state[1] + current_state[4] + current_state[5] + N*current_state[8]))
    averageServers_I.append((current_state[0] + current_state[1] + current_state[2] + current_state[3] + N*current_state[7]))
    averageServers_P.append((current_state[2] + current_state[3] + current_state[4] + current_state[5] + N*current_state[6]))

    current_state = np.dot(current_state, P)
    print(current_state)

# plotting 
plt.plot(range(timeSteps), averageServers_V, label='Vulnérables (V)')
plt.plot(range(timeSteps), averageServers_I, label='Infectés (I)')
plt.plot(range(timeSteps), averageServers_P, label='Protégés (P)')

plt.xlabel('Temps')
plt.ylabel('Nombre moyen de serveurs')
plt.title('Évolution du nombre moyen de serveurs dans chaque catégorie')
plt.legend()
plt.grid(True)
plt.show()
