# Produit matrice-vecteur v = A.u
import numpy as np
from mpi4py import MPI


globCom = MPI.COMM_WORLD.Dup()
nbp     = globCom.size
rank    = globCom.rank
name    = MPI.Get_processor_name()

# Dimension du problème (peut-être changé)
dim = 120

Nloc=dim//nbp

# Initialisation de la matrice
A = np.array([[(i+j) % dim+1. for i in range(dim)] for j in range(dim)])
#print(f"A = {A}")

# Initialisation du vecteur u
u = np.array([i+1. for i in range(dim)])
#print(f"u = {u}")

v=np.zeros(dim)

for k in range(dim):    
    for j in range(rank*Nloc,(rank+1)*Nloc) :
        v[k]+=A[k,j]*u[j]

for r in range(nbp):
    if r!=rank:
        globCom.send(v,dest=r)

for i in range(nbp-1):
    Status=MPI.Status()
    v_tmp=globCom.recv(source=MPI.ANY_SOURCE,status=Status)
    v+=v_tmp


    print("A.u = ",np.array(v))

