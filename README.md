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
