import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

def integrer(g, x):
    n_rectangles=1000
    t = np.linspace(0, x, n_rectangles)
    largeur = x / n_rectangles
    somme = 0
    for i in range(n_rectangles):
        somme += g(t[i]) * largeur
    return somme

def trouver_parametres(g):
    x_m=10
    n_points=1000
    x = np.linspace(0.01, x_m, n_points)
    P = np.zeros(n_points)
    
    for i in range(n_points):
        G_x = integrer(g, x[i])
        P[i] = -2 * G_x / (x[i]**2)
        
    resultats = []
    max_P = 0
    
    for i in range(1, n_points - 1):
        if P[i] > P[i-1] and P[i] > P[i+1]:
            if P[i] > 0 and P[i] > max_P:
                resultats.append((x[i], P[i]))
        if P[i] > max_P:
            max_P = P[i]
            
    return resultats

def tracer_solution(g, c, mu):
    def dQ(x, Q): 
        G_Q = integrer(g, Q)
        interieur = mu * (Q**2) + 2 * G_Q
        if interieur < 0:
            interieur = 0    
        return -np.sqrt(interieur)

    Q_initial = [c * 0.96] #lancement legerement inferieur a c
    intervalle_x = (0, 100)  
    
    resultat = solve_ivp(dQ, intervalle_x, Q_initial, max_step=0.1) #ode solver 
    
    plt.plot(resultat.t, resultat.y[0])
    plt.xlabel("x")
    plt.ylabel("Q(x) (Position)")
    plt.show()




def g_test_1(x):
    return (x**3) - (x**2)

def g_test_2(x):
    return (x**3) - 4*(x**2)

resultats_1 = trouver_parametres(g_test_1)
c1, mu1 = resultats_1[0]
print(f"fonction1 Paramètres trouvés -> c = {c1:.3f}, mu = {mu1:.3f}")
resultats_2 = trouver_parametres(g_test_2)
c2, mu2 = resultats_2[0]
print(f"fonction2 Paramètres trouvés -> c = {c2:.3f}, mu = {mu2:.3f}")
