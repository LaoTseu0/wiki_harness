# LoRA

> [carte du cours](../carte.md)

## L'essentiel

LoRA (« Low-Rank Adaptation ») est la technique qui a rendu le
fine-tuning abordable : au lieu de réentraîner des milliards de poids,
on **gèle le modèle** et on n'entraîne que de petites matrices
correctives. À connaître pour l'expliquer — et pour expliquer pourquoi
on ne s'en sert presque jamais.

## Le savoir

- **Le mécanisme** : pour une matrice de poids W (gelée), on apprend
  ΔW = **A × B** où A (d×r) et B (r×d) sont de **rang faible**
  (r = 8-64 typiquement). À l'inférence : W' = W + α·A·B. On entraîne
  ~0,1-1 % des paramètres — la mémoire d'optimiseur s'effondre
  d'autant.
- **QLoRA** : la base est en plus **quantisée en 4-bit** (NF4) pendant
  l'entraînement — un 7-8B se fine-tune sur un GPU grand public ou un
  Colab gratuit. Les adaptateurs restent en pleine précision.
- **Propriétés pratiques** : l'adaptateur pèse quelques dizaines de Mo,
  se distribue séparément, se fusionne (merge) dans la base ou se
  charge à chaud ; plusieurs adaptateurs peuvent partager une même
  base.
- **Quand c'est la bonne réponse** : imposer un *style* ou un *format*
  de sortie récurrent, un domaine lexical étroit, une tâche répétitive
  à petit modèle.
- **Quand ça ne l'est pas** (9 fois sur 10) : injecter des **faits**
  changeants ou sourçables → RAG
  ([2.3.5](../retrieval/rag-vs-fine-tuning.md)) ;
  suivre des instructions → prompt/few-shot d'abord ; et le
  fine-tuning peut **dégrader** les capacités générales (oubli
  catastrophique).

## En pratique

L'entrée glossaire = le vécu de la
[6.3](../production/culture-fine-tuning.md)
(LoRA d'un petit modèle sur Colab) résumé en un script/README : coût
réel, dataset minimal, avant/après mesuré — et la conclusion honnête.

## Pièges connus

- Fine-tuner pour des connaissances : les faits appris sont figés,
  non sourçables, et se périment — le RAG fait mieux pour moins cher.
- Dataset de 50 exemples bruités : le modèle apprend le bruit ; la
  qualité du dataset domine tous les hyperparamètres.
- Oublier le format d'entraînement (template de chat) à l'inférence :
  l'adaptateur semble « ne pas marcher » alors que le prompt ne matche
  pas.

## Se tester

> « Quand recommanderiez-vous un fine-tuning plutôt qu'un RAG ? »
> Style/format/domaine stable, volume d'appels justifiant
> l'investissement, données d'entraînement propres disponibles — pour
> des faits changeants ou sourçables, RAG ; et toujours prompt/few-shot
> en première intention.

## Références

- Hu et al., « LoRA: Low-Rank Adaptation of Large Language Models »
- Dettmers et al., « QLoRA » ; bibliothèque PEFT de Hugging Face
