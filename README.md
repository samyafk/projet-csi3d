# projet-csi3d

### TODO
1. Sortir la liste des edges et une liste binaire associée
2. Màj de la liste des binaires en fonction de si collapsable :
	a. Checker si plus de deux vertex connectés en commun
	b. Checker que pas de quadrilatère : checker si chaque edge forme un quad avec les autres
3. Parcourir la liste et pour chaque edge :
	a. Collapse si possible -> écriture des opérations : duplication du point, translations
	b. Màj de la liste de edges (supprimer les 3 edges)
	c. Màj de la liste des collapsables (mettre les edges adjacents à non collapsable)

___

Plus tard :
Truc en papillon
Métrique d'erreur