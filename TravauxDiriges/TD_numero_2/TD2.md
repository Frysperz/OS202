# TD 2

## Question de cours 

Exercice 1.1 : 

Dans l'exemple donné dans le cours "more complicated case", nous pouvons distinguer deux scénarios. En effet le P2 reçoit 2 messages de nimporte qui, mais il envoie un message au P0, intercalé entre les $
Ainsi, on distingue deux cas : le cas où le premier message reçu par P2 est celui envoyé par P1 et le cas où c'est celui de P0.

1. Si le premier message reçu par P2 est celui envoyé par P0, alors P2 peut bien renvoyer un message à P0 puisque celui-ci est dorénavant en attente de message. Donc, il n'y a pas de blocage dans cette situation.

2. Si le premier message reçu par P2 est celui envoyé par P1, alors, à l'étape d'après, P2 essaye d'envoyer un message à P0. Or P0 essaye aussi d'envoyer un message à P2. Les 2 messages ne peuvent alors être "consommés", P0 et P2 attendent mutuellement la recpetion de leur message, il y a donc un interblocage.

On ne peut donc pas prévoir quel message sera reçu en premier, cela dépend de la rapidité des processeurs. Sans information supplémentaire, on suppose qu'elle est de 50%.

Exercice 1.2 : 

1. D'après la loi d’Amdhal, on peut prédire que l’accélération maximale que pourra obtenir Alice avec son code est : S(n) -> 1/f lorsque n>>1, avec f la fraction de ts (temps nécessaire pour exécuter le code de manière séquentielle) représentant la partie du code qui ne peut être parallélisée. Soit S(n) = 10.

2. Pour minimiser le gaspillage de ressources CPU, il est judicieux de déterminer un nombre de nœuds qui offre une accélération significative. La formule d'accélération maximale avec la loi d'Amdahl est liée au nombre de nœuds. En général, une augmentation linéaire du nombre de nœuds n'entraîne pas une accélération proportionnelle en raison de la partie séquentielle du code. Pour ce jeu de donné spécifique, il semble raisonnable de prendre à peu près 5 noeuds de calcul pour ne pas gaspiller de ressources CPU. 

3. La loi de Gustafon s'applique lorsque la taille du problème augmente avec le nombre de processeurs : on a S=1−P+P×n avec P=0.9 ici. Donc si on double la quantité de données à traiter et qu'on prend n=4, on a S=1.6.


## Mandelbrot 

1 processus en parallèle : ne compile pas, tourne dans le vide 
2 processus en parallèle : 
    Temps du calcul de l'ensemble de Mandelbrot : 6.1242170333862305
3 processus en parallèle : 
    Temps du calcul de l'ensemble de Mandelbrot : 4.5322654247283936
4 processus en parallèle :
    Temps du calcul de l'ensemble de Mandelbrot : 4.656396150588989
On s'attendrait à avoir un temps plus faible pour 4 processus en parallèle ..., je ne saurais expliquer pourquoi

