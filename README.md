# IngenuityProject
Projet de fin d'études

Notes meeting 1:
-Commencer par programmer un graphe simple (voir diapo 2 de la présentation mais ne pas tenir compte des fréquence ni des délais) ==> fait
-Faire une classe générique pour les canaux et les acteurs ==> fait
-Faire un tableau pour les acteurs et un tableau pour les canaux  ==> fait
-Ne pas utiliser de flottant pour représentant les échanges de jetons
  =>utiliser plutôt le numérateur pour le nombre de jeton produits par l'acteur et un diviseur au niveau des canaux pour réprésenté le dénominateur
-Réprésenter le graphe uniquement par des acteurs et des noeuds. Pas besoin d'utiliser des listes chaînées  ==> OK
-Précision au niveau du graphe : les numéro entre crochets représentent le nombre de jetons initial
-Ne pas tout mettre au niveau des acteurs: dans ce cas utiliser une méthode production et consommation pour les canaux  ==> je ne vois pas comment respecter ça

Notes meeting 2:
-au niveau du constructeur de Channel, donner une valeur par défaut =1 à diviseur
-implémenter une classe pour gérer le temps de façon logique et ensuite vérifier la consistance du modèle
-cela fait que l'utilisation des thread devient inutile
-chaque événement doit se produire à un tic de l'horloge logique
-cette horloge logique ne respecte pas forcément le temps réel, c'est nous qui définissons la durée que représente un tic d'horloge logique
-si l'horloge logique tombe sur un wait, on l'incrémente du temps d'attente nécessaire et on lui dit ce qui devra se passer après cet incrément (concrètement, on met dans une liste ordonnée sur le temps, le temps d'exécution et l'acteur qui doit s'exécuter ex:[(50,A),(100,C),(120,B)]) 
