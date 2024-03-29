# Calcul de l'ensemble de Mandelbrot en python
import numpy as np
from dataclasses import dataclass
from PIL import Image
from math import log
from time import time
import matplotlib.cm
from mpi4py import MPI

globCom = MPI.COMM_WORLD.Dup()
nbp     = globCom.size
rank    = globCom.rank
name    = MPI.Get_processor_name()

root = 0

@dataclass
class MandelbrotSet:
    max_iterations: int
    escape_radius:  float = 2.0

    def __contains__(self, c: complex) -> bool:
        return self.stability(c) == 1

    def convergence(self, c: complex, smooth=False, clamp=True) -> float:
        value = self.count_iterations(c, smooth)/self.max_iterations
        return max(0.0, min(value, 1.0)) if clamp else value

    def count_iterations(self, c: complex,  smooth=False) -> int | float:
        z:    complex
        iter: int

        # On vérifie dans un premier temps si le complexe
        # n'appartient pas à une zone de convergence connue :
        #   1. Appartenance aux disques  C0{(0,0),1/4} et C1{(-1,0),1/4}
        if c.real*c.real+c.imag*c.imag < 0.0625:
            return self.max_iterations
        if (c.real+1)*(c.real+1)+c.imag*c.imag < 0.0625:
            return self.max_iterations
        #  2.  Appartenance à la cardioïde {(1/4,0),1/2(1-cos(theta))}
        if (c.real > -0.75) and (c.real < 0.5):
            ct = c.real-0.25 + 1.j * c.imag
            ctnrm2 = abs(ct)
            if ctnrm2 < 0.5*(1-ct.real/max(ctnrm2, 1.E-14)):
                return self.max_iterations
        # Sinon on itère
        z = 0
        for iter in range(self.max_iterations):
            z = z*z + c
            if abs(z) > self.escape_radius:
                if smooth:
                    return iter + 1 - log(log(abs(z)))/log(2)
                return iter
        return self.max_iterations


# On peut changer les paramètres des deux prochaines lignes
mandelbrot_set = MandelbrotSet(max_iterations=50, escape_radius=10)
width, height = 1024, 1024

scaleX = 3./width
scaleY = 2.25/height
# Calcul de l'ensemble de mandelbrot :
deb = time()
# fonctionnement du gather : gather(vec_loc,vec,0) -> gather(entrée, sortie, processus_arrivée)

ligne=0

if rank == 0:
    convergence_finale = np.empty((width, height), dtype=np.double)
    
    # Envoi des première lignes
    for k in range(1,nbp):
        globCom.send(ligne,dest=k)
        ligne+=1

    while ligne < height-1:
        # Récupération du travail
        Status = MPI.Status() #le statut permet de récupérer la source quand on reçoit de any_source
        convergence,j = globCom.recv(source=MPI.ANY_SOURCE, status = Status)
        
        #Ajout du travail
        convergence_finale[j,:] = convergence

        # Envoi d'un nouveau travail
        globCom.send(ligne, dest=Status.Get_source())
        ligne+=1
    
    # Condition d'arrêt
    # Il faut encore recevoir les dernières lignes qu'on a envoyées
    
    for _ in range(nbp-1):
        Status = MPI.Status() #le statut permet de récupérer la source quand on reçoit de any_source
        convergence,j = globCom.recv(source=MPI.ANY_SOURCE, status = Status)
            
        #Ajout du travail
        convergence_finale[j,:] = convergence   

    for k in range(1,nbp):
        globCom.send(None,dest=k)



else :
    while True :
        ligne = globCom.recv(source=root)

        # Cas d'arrêt
        if ligne == None:
            break

        convergence = np.empty(width, dtype=np.double)
        for x in range(width):
            c = complex(-2. + scaleX*x, -1.125 + scaleY * ligne)
            convergence[x] = mandelbrot_set.convergence(c, smooth=True)
        globCom.send((convergence,ligne), dest=root)



fin = time()
print(f"Temps du calcul de l'ensemble de Mandelbrot : {fin-deb}",rank)



# Constitution de l'image résultante :
deb = time()
if rank == 0 :    
    image = Image.fromarray(np.uint8(matplotlib.cm.plasma(convergence_finale)*255))
    fin = time()
    print(f"Temps de constitution de l'image : {fin-deb}")
    image.show()
# On enregistre l'image dans le dossier car je n'arrive pas à l'afficher autrement.
    image.save("mandelbrot_maitre_esclave.png")
