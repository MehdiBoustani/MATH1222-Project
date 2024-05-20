import numpy as np
import matplotlib.pyplot as plt

# ------------------------------------------ QUESTION 1.5 DELTA --------------------------------------------- #

N = 2 # nombre de serveurs
timeSteps = 200 # pas de temps

# Probabilités
beta = 0.5
mu = 0.1
alpha = 0.05
delta = 0.05

TOLERANCE = 1e-6
# ORDER OF STATES : IV VI IP PI VP PV PP II VV

P = np.array([
            [(1-mu)*(1-beta), 0, 0, mu*beta, 0, mu*(1-beta), 0, beta*(1-mu), 0],

            [0, (1-mu)*(1-beta-delta), mu*(beta+delta), 0, mu*(1-beta-delta), 0, 0, (beta+delta)*(1-mu), 0],

            [alpha*(1-mu), 0, (1-mu)*(1-alpha), 0, 0, mu*alpha, mu*(1-alpha), 0, 0],

            [0, alpha*(1-mu), 0, (1-mu)*(1-alpha), mu*alpha, 0, mu*(1-alpha), 0, 0],

            [delta*alpha, 0, delta*(1-alpha), 0, (1-alpha)*(1-delta), 0, 0, 0, (1-delta)*alpha],

            [0, 0, 0, 0, 0, 1-alpha, 0, 0, alpha],

            [0, 0, 0, 0, alpha*(1-alpha), alpha*(1-alpha), np.power((1-alpha), 2), 0, np.power((alpha), 2)],

            [0, 0, mu*(1-mu), mu*(1-mu), 0, 0, mu**2, (1-mu)**2, 0],

            [delta, 0, 0, 0, 0, 0, 0, 0, 1-delta]

            ])

# ORDER OF STATES :        IV   VI  IP PI VP PV PP  II  VV
currentState = np.array([0.5, 0.5, 0, 0, 0, 0,  0,  0,  0])

averageServers_V = []
averageServers_I = []
averageServers_P = []

i = 0
stationnary = False
while i < timeSteps and not stationnary:
    # Calcul du nombre moyen de serveurs dans chaque catégorie
    averageServers_V.append((currentState[0] + currentState[1] + currentState[4] + currentState[5] + N*currentState[8]))
    averageServers_I.append((currentState[0] + currentState[1] + currentState[2] + currentState[3] + N*currentState[7]))
    averageServers_P.append((currentState[2] + currentState[3] + currentState[4] + currentState[5] + N*currentState[6]))

    nextState = np.dot(currentState, P)

    # Convergence vers la distribution stationnaire
    if np.all(np.abs(nextState - currentState) < TOLERANCE):
        print(f"Convergence atteinte à l'étape {i} vers la distribution stationnaire {currentState}")
        stationnary = True

    currentState = nextState

    i += 1

percentageS1 = currentState[0] + currentState[2] + currentState[7]
percentageS2 = currentState[1] + currentState[3] + currentState[7]

print(percentageS1)
# Calcul du pourcentage du temps passé dans l'etat infectieux en regime stationnaire
print(f"Pourcentage passé dans l'état infectieux en regime stationnaire Serveur 1 :  {percentageS1 * 100:.2f}% ")
print(f"Pourcentage passé dans l'état infectieux en regime stationnaire Serveur 2 :  {percentageS2 * 100:.2f}% ")


# Tracé des courbes pour chaque catégorie jusqu'à l'étape de convergence
plt.plot(range(i), averageServers_V, label='Vulnérables (V)')
plt.plot(range(i), averageServers_I, label='Infectés (I)')
plt.plot(range(i), averageServers_P, label='Protégés (P)')

# Ajustements finaux du tracé
plt.xlabel('Temps')
plt.ylabel('Nombre moyen de serveurs')
plt.title('Évolution du nombre moyen de serveurs dans chaque catégorie')
plt.legend()
plt.grid(True)
plt.ylim(0, 2)
plt.show()