# Autorégression

> [glossaire](index.md)

Le mode de génération des LLM : le modèle produit **un token à la fois**, et
chaque token produit est réinjecté dans l'entrée pour prédire le suivant. Il
n'y a pas de retour en arrière — un token tiré fait partie du contexte et ne
peut plus être effacé, le modèle ne peut que « se corriger » à la suite.

C'est la boucle de retour du processus
[d'un texte à un token](../_processus/generation-token.md), et la raison pour
laquelle une seule graine de tirage différente peut faire diverger toute une
phrase.
