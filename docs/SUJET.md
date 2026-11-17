# Sujet du projet : prévoir et rééquilibrer les stations Vélo'v à Lyon

Rédigé le 28 octobre 2026, avant la première ligne de code. L'avancement, les décisions et les observations sont dans le [journal de bord](JOURNAL.md).

## 1. Le contexte

Vélo'v compte plus de 400 stations et 5 000 vélos dans 22 communes, en service depuis 2005 ([source](https://www.data.gouv.fr/datasets/stations-velov-de-la-metropole-de-lyon/informations)). Le principe : on prend un vélo à une station A et on le dépose à une station B.

Les trajets ne sont pas équilibrés. Le matin, les flux vont des quartiers d'habitation vers les zones de travail (Part-Dieu, Presqu'île). Le soir, c'est l'inverse.

Les collines accentuent le déséquilibre. À la Croix-Rousse ou à Fourvière, on descend volontiers à vélo mais on remonte rarement. C'est une hypothèse à vérifier avec les données.

Ce déséquilibre crée deux échecs pour l'usager :

- **Station vide** : il n'y a pas de vélo à prendre.
- **Station pleine** : on ne peut pas déposer son vélo et il faut chercher une autre station.

## 2. Le problème réel aujourd'hui

Le service grandit plus vite que sa capacité à rester équilibré. En juin 2025, Vélo'v comptait entre 50 000 et 53 000 trajets par jour en moyenne, environ 43 % de plus qu'en 2024 ([Lyon Capitale, juillet 2025](https://www.lyoncapitale.fr/actualite/velo-v-a-lyon-100-000-abonnes-de-nouvelles-stations-et-quelques-questions)).

Pour compenser, l'opérateur JCDecaux déplace des vélos avec des équipes de régulation. Selon son directeur d'exploitation, ces équipes étaient très mobilisées sur les collines. Dans le Vieux-Lyon et la Presqu'île, des stations se vident dès le début de matinée, et il estime qu'il faudrait des dizaines de camions pour l'éviter (même source).

Les camions coûtent cher et ne peuvent pas être partout. La vraie question n'est donc pas « faut-il déplacer des vélos ? », mais : lesquels, d'où, vers où, quand et dans quel ordre.

Réagir quand une station est déjà vide, c'est trop tard : des usagers ont déjà échoué. Il faut **anticiper**, et c'est là que la prédiction devient utile.

## 3. La question du projet

**Avec un nombre limité de camions, quelles stations faut-il remplir ou vider, et dans quel ordre, pour minimiser le nombre d'usagers qui trouveront une station vide ou pleine dans les prochaines heures ?**

Elle se découpe en deux sous-questions : **prévoir** (quelles stations seront en difficulté et quand), puis **décider** (quelle tournée de camions fait le plus de bien).

## 4. Les données

Une source principale, gratuite et sous licence ouverte, plus deux sources d'appoint à choisir.

| Source | Ce qu'elle donne | Rôle dans le projet |
| --- | --- | --- |
| [Vélo'v temps réel](https://www.data.gouv.fr/datasets/stations-velov-de-la-metropole-de-lyon-disponibilites-temps-reel) (Métropole de Lyon / JCDecaux) | Par station : nom, adresse, nombre de bornettes, vélos et places disponibles, rafraîchi chaque minute | La donnée à prédire |
| Météo (source à choisir) | Température, pluie, vent, heure par heure | Variable explicative : on roule moins sous la pluie |
| Calendrier | Jours fériés, vacances scolaires | Variable explicative : les habitudes changent |

Trois limites à garder en tête :

- **Pas d'historique.** L'API donne une photo de l'instant présent. L'historique, c'est le projet qui le construit (brique 1).
- **Des stocks, pas des trajets.** On voit combien de vélos sont dans chaque station, pas qui va d'où à où. Les mouvements se déduisent des variations de stock.
- **Les camions sont invisibles.** Quand l'opérateur déplace des vélos, le stock change sans qu'un usager en soit la cause. Le modèle risque de confondre les deux.

## 5. Ce que je construis

Quatre briques, dans cet ordre. Chacune s'appuie sur la précédente.

1. **Collecte automatique.** Un script Python récupère l'état de toutes les stations à intervalle régulier et l'enregistre. GitHub Actions le lance tout seul, sans serveur.
   - Compétences : API, JSON, automatisation, nettoyage de données.
2. **Prédiction.** Question : combien de vélos dans telle station dans 1 heure ? D'abord une méthode naïve (« même valeur qu'il y a une semaine à la même heure »), puis un modèle de machine learning, gardé seulement s'il fait mieux.
   - Compétences : séries temporelles, préparation des variables, évaluation honnête d'un modèle (éviter la fuite de données).
3. **Optimisation.** À partir des prédictions, choisir les stations à servir et la tournée des camions. C'est un problème connu de recherche opérationnelle, proche des tournées de véhicules de mon [projet de planification](https://github.com/S-oumar/Optimisation-de-transport), modélisé avec CP-SAT ou en PLNE.
   - Compétences : modéliser des contraintes, transformer une prédiction en décision.
4. **Carte interactive.** Une page web montre les stations à risque et la tournée proposée.
   - Compétences : présenter un résultat technique à quelqu'un qui n'est pas technicien.

## 6. Le but final

Un projet que je sais expliquer du problème jusqu'au résultat.

- [ ] Un dépôt GitHub propre, avec un README qui raconte : problème, données, méthode, résultats chiffrés, limites.
- [ ] Une démo en ligne (la carte interactive).
- [ ] Une phrase de résultat défendable, du type : « mon modèle prévoit les ruptures X % mieux qu'une méthode naïve, et mon optimiseur réduit les ruptures attendues de Y % avec 2 camions ».

Les vrais chiffres X et Y viendront à la fin. On ne les invente pas avant.

## 7. Méthode de travail

Chaque étape suit le même cycle :

1. Comprendre la notion et le choix à faire.
2. Poser les hypothèses possibles et en débattre.
3. Décider, avec une justification écrite.
4. Coder.
5. Noter la décision dans le [journal de bord](JOURNAL.md).


Le journal sert de mémoire du projet. C'est lui qui permet de répondre à « pourquoi as-tu fait ce choix ? ».
