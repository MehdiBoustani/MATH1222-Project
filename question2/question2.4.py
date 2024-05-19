import numpy as np
import matplotlib.pyplot as plt

# CONSTANTS
SIMULATIONS = 50
STEPS = 1000

# --------------- Transitions ------------------ #

# # """ ORDRE DE 0.8 """
beta = 0.01
mu = 0.12575
alpha = 1

# beta = 0.03 
# mu = 0.37725
# alpha = 1


# # """ ORDRE DE 2 """
# beta = 0.03
# mu = 0.1509
# alpha = 1

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

V = 0
I = 1
P = 2

# Initial state
nbInfected    = N
nbVulnerables = 0
nbProtected   = 0

initialConfig = np.array([I] * nbInfected)

# Time (in STEPS) until the eradication of the virus
eradicationTime = 0

# Lists to store counts of servers (infected) at each time step for ALL SIMULATIONS
totalCountsI = np.zeros(STEPS)

for sim in range(SIMULATIONS):
    current_configuration = initialConfig

    eradicated = False

    totalCountsI[0] += nbInfected
    
    i = 0
    # continue until eradication
    while i < STEPS and not eradicated:

        if not eradicated and I not in current_configuration:
            eradicationTime += i
            eradicated = True

        next_configuration = []
        
        # Run through servers
        for j in range(N):            
                
            serverState = current_configuration[j]
            
            # current server = V
            if serverState == V:
                if not eradicated :
                    # vector multiplication to get the number of connected and infected nodes
                    connectedInfected = np.dot(current_configuration % 2, W[j])
                else : 
                    connectedInfected = 0
               
                V_to_V = (1-beta)**connectedInfected
               
                V_to_I = 1 - V_to_V

                if np.random.rand() <= V_to_I :
                    nextState = I
                    totalCountsI[i+1] += 1
                    
                else :
                    nextState = V
                    
            # current server = I
            elif serverState == I :
               
                if np.random.rand() <= I_to_P : 
                    nextState = P # I to P

                else :
                    nextState = I # I to I
                    totalCountsI[i+1] += 1

            # current server = P
            elif serverState == P :
                
                if np.random.rand() <= P_to_V :
                    nextState = V # P to V

                else :
                    nextState = P # P to P

            next_configuration.append(nextState)
        i += 1

        current_configuration = np.array(next_configuration)

if eradicated :
    print("La temps moyen pour l'eradication du virus = ", eradicationTime/SIMULATIONS)
else :
    print("Le virus n'a pas été éradiqué après {} pas de temps".format(STEPS))

# Get the average counts over all SIMULATIONS
totalCountsI /= SIMULATIONS

# Plotting
timeSteps = range(1, STEPS+1)
plt.plot(timeSteps, totalCountsI, label='Infectés (I)', color='red')

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