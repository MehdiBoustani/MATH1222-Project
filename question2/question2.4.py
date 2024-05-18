import numpy as np
import matplotlib.pyplot as plt

# CONSTANTS
SIMULATIONS = 10
STEPS = 1000

# --------------- Transitions ------------------ #

# # """ ORDRE DE 0.8 """
# beta = 0.02
# mu = 0.2515
# alpha = 1

# beta = 0.03 
# mu = 0.37725
# alpha = 1


# # """ ORDRE DE 2 """
beta = 0.03
mu = 0.1509
alpha = 1

# beta = 0.03
# mu = 0.1509
# alpha = 1


V_to_I = beta
V_to_V =  1 - beta

I_to_P = mu
I_to_I = 1 - mu

P_to_V = alpha
P_to_P = 1 - alpha

# ------------------------------------------- #

# Connection matrix
W  = np.loadtxt("Wsf.txt")
N = len(W) # number of servers

# Check βλ/μ 
greatestEigenvalue = np.linalg.eigvalsh(W)[-1]
print("Greatest eigenvalue = ", greatestEigenvalue)
print((beta*greatestEigenvalue)/mu)

print(" beta/mu <= 1/greatest eigenvalue ? ", (beta/mu) <= (1/greatestEigenvalue)) # 


# V = 0
# I = 1
# P = 2

# Initial state
nbInfected    = N
nbVulnerables = 0
nbProtected   = 0

initialConfig = np.array([1] * nbInfected + [0] * nbVulnerables)

# Time (in STEPS) until the eradication of the virus
eradicationTime = 0

# Lists to store counts of servers in each category at each time step for ALL SIMULATIONS
totalCountsV = np.zeros(STEPS)
totalCountsI = np.zeros(STEPS)
totalCountsP = np.zeros(STEPS)

for sim in range(SIMULATIONS):
    current_configuration = initialConfig

    eradicated = False

    totalCountsV[0] += nbVulnerables
    totalCountsI[0] += nbInfected
    totalCountsP[0] += nbProtected

    for i in range(STEPS-1): # time steps

        if not eradicated and 1 not in current_configuration:
            eradicationTime += i
            eradicated = True

        next_configuration = []
        
        # Run through servers
        for j in range(N):            
                
            serverState = current_configuration[j]
            
            # current server = V
            if serverState == 0:
                if not eradicated :
                    # vector multiplication to get the number of connected and infected nodes
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

# Plotting
time_STEPS = range(STEPS)
plt.plot(time_STEPS, totalCountsI, label='Infecté')
plt.xlabel('Temps')
plt.ylabel('Nombre de serveurs')
plt.yscale('symlog')
plt.xscale('symlog')
plt.title('Nombre moyen de serveurs infectés : {} Simulations'.format(SIMULATIONS))
plt.xlim(left=1)
plt.ylim(bottom=1)
# Format x-axis ticks
plt.gca().xaxis.set_major_formatter(plt.FormatStrFormatter('%d'))

# Format y-axis ticks
plt.gca().yaxis.set_major_formatter(plt.FormatStrFormatter('%d'))
plt.legend()
plt.show()