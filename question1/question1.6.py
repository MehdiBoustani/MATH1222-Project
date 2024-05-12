import numpy as np
import matplotlib.pyplot as plt

# --------------------------------------- QUESTION 1.6 (a) --------------------------------------------- #

N = 2 # nombre de serveurs
timeSteps = 150 # pas de temps

# Probabilités
beta = 0.5
mu = 0.1
alpha = 0.05

# Matrice de transition des états
P = np.array([
            [(1-mu)*(1-beta), mu*beta, mu*(1-beta), 0, beta*(1-mu), 0],

            [alpha*(1-mu), (1-mu)*(1-alpha), mu*alpha, mu*(1-alpha), 0, 0],

            [0, 0, 1-alpha, 0, 0, alpha],

            [0, 0, 2*alpha*(1-alpha), np.power((1-alpha), 2), 0, np.power((alpha), 2)],

            [0, 2*mu*(1-mu), 0, mu**2, (1-mu)**2, 0],

            [0, 0, 0, 0, 0, 1]

            ])

# Etat initial
current_state = np.array([1, 0, 0, 0, 0, 0])

averageServers_V = []
averageServers_I = []
averageServers_P = []


for i in range(timeSteps):
    averageServers_V.append(current_state[0] + current_state[2] + N*current_state[5])
    averageServers_I.append(current_state[0] + current_state[1] + N*current_state[4])
    averageServers_P.append(current_state[1] + current_state[2] + N*current_state[3])

    current_state = np.dot(current_state, P)


plt.plot(range(timeSteps), averageServers_V, label='Vulnérables (V)')
plt.plot(range(timeSteps), averageServers_I, label='Infectés (I)')
plt.plot(range(timeSteps), averageServers_P, label='Protégés (P)')

plt.xlabel('Temps')
plt.ylabel('Nombre moyen de serveurs')
plt.title('Évolution du nombre moyen de serveurs dans chaque catégorie')
plt.legend()
plt.grid(True)
plt.show()


