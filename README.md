# IngenuityProject
Projet de fin d'études

Notes meeting 1:
-Commencer par programmer un graphe simple (voir diapo 2 de la présentation mais ne pas tenir compte des fréquence ni des délais)
-Faire une classe générique pour les canaux et les acteurs
-Faire un tableau pour les acteurs et un tableau pour les canaux
-Ne pas utiliser de flottant pour représentant les échanges de jetons
  =>utiliser plutôt le numérateur pour le nombre de jeton produits par l'acteur et un diviseur au niveau des canaux pour réprésenté le dénominateur
-Réprésenter le graphe uniquement par des acteurs et des noeuds. Pas besoin d'utiliser des listes chaînées
-Précision au niveau du graphe : les numéro entre crochets représentent le nombre de jetons initial
-Ne pas tout mettre au niveau des acteurs: dans ce cas utiliser une méthode production et consommation pour les canaux

Notes meeting 2: 
-au niveau du constructeur de Channel, donner une valeur par défaut =1 à diviseur 
-implémenter une classe pour gérer le temps de façon logique et ensuite vérifier la consistance du modèle 
-cela fait que l'utilisation des thread devient inutile 
-chaque événement doit se produire à un tic de l'horloge logique 
-cette horloge logique ne respecte pas forcément le temps réel, c'est nous qui définissons la durée que représente un tic d'horloge logique 
-si l'horloge logique tombe sur un wait, on l'incrémente du temps d'attente nécessaire et on lui dit ce qui devra se passer après cet incrément (concrètement, on met dans une liste ordonnée sur le temps, le temps d'exécution et l'acteur qui doit s'exécuter ex:[(50,A),(100,C),(120,B)])

Résumé meeting 3:
Tâches à faire pour la prochaine fois:
-implémenter une fonction de calcul du vecteur de répétition (https://docs.sympy.org/latest/tutorials/intro-tutorial/matrices.html https://www.geeksforgeeks.org/python-sympy-matrix-nullspace-method/ https://docs.scipy.org/doc/scipy/reference/generated/scipy.linalg.null_space.html)
-vérifier que l'application du vecteur de répétition permet un retour à l'état initial (preuve de consistance)
-vérifier que les acteurs timés s'exécutent bien à la bonne fréquence
-créer une fonction permettant une vérification plus simple du respect de la fréquence d'exécution des acteurs (elle pourrait par exemple mettre fin à l'exécution après une itération complète du graphe)
-Tester notre implémentation sur un autre schéma (une partie du graphe final par exemple)
Remarques:
-Il n'est pas indispensable de supprimer les lignes de 0 de la matrice de topologie. Leur présence est essentiel pour montrer l'absence de deadlocks.
-Il est normal que les matrices topologiques soit singulières sinon cela traduit un problème
-Il y a probablement des erreurs au niveau du schéma final donc il faut y penser si notre implémentation de fonctionne pas dessus ou aboutie à des deadlock
-Au niveau des acteur avec des délais, la présence du délai traduit le fait que l'acteur doit pouvoir s'exécuter immédiatement après ce délai. Dans le schéma d'exemple, E devrait être en mesure de s'exécuter dès immédiatement après 50ms mais du fait de la fréquence imposé aux acteurs qui le précède, E ne peut s'exécuter qu'après 200ms. C'est don une erreur de spécification. La façon de la gérer est soit d'alléger la contrainte sur le délai, soit de mettre des jetons initiaux sur c6.
