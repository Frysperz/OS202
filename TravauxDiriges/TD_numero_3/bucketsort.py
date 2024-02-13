import numpy as np
from mpi4py import MPI
from time import time

def parallel_bucket_sort(data):
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    nbp = comm.Get_size()

    local_data = np.array_split(data, nbp)[rank]
    local_buckets = [[] for _ in range(nbp)]

    # Répartition locale
    for item in local_data:
        bucket_index = int(item * nbp)
        local_buckets[bucket_index].append(item)

    # Tri local
    deb = time()
    local_buckets = [sorted(bucket) for bucket in local_buckets]
    fin = time()
    print(f"Temps du calcul des sous tableaux : {fin-deb}")

    # Collecte des résultats
    all_buckets = comm.gather(local_buckets, root=0)

    if rank == 0:
        # Tri final
        sorted_data = [item for bucket in all_buckets for sublist in bucket for item in sublist]
        sorted_data.sort()

        return sorted_data

data = np.random.random(100)  

if MPI.COMM_WORLD.Get_rank() == 0:
    print("Tableau non trié :", data)


sorted_data = parallel_bucket_sort(data)

if MPI.COMM_WORLD.Get_rank() == 0:
    print("Tableau trié :", sorted_data)

