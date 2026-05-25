## Savoir le situer

**Processus** —
[[generator/guardrails/schema/processus/generation-token.canvas|de l'échange à la réponse générée]],
dont l'étape `inference` ouvre
[[generator/guardrails/schema/processus/inference-transformer.canvas|le passage avant du
Transformer]].  
[[glossaire/input|Input]] global : messages structurés. [[glossaire/output|Output]] global : texte généré et raison
d'arrêt.  
Grandes étapes : tokenisation → inférence → logits → boucle.

**Étape ouverte** — `tokenisation | reinjection → inference → logits`.  
**Input** : prompt complet au premier passage, puis nouveau token et cache
compatible. **Output** : logits du prochain token et cache étendu.  
Responsabilité : distinguer le calcul initial du préfixe de l'extension
incrémentale.

**L'essentiel** — le [[glossaire/prefill|prefill]] calcule le prompt et construit les clés et valeurs
de chaque couche. Le [[glossaire/decode|decode]] réutilise ce cache et ne calcule les nouveaux
états que pour les positions ajoutées.

**Recomposer** — le cache accélère les retours de la boucle vers l'inférence,
mais ne change ni le [[glossaire/tokenizer|tokenizer]], ni la politique de [[glossaire/sampling|sampling]], ni la condition
d'arrêt.

![[prefill-decode-kv-cache.canvas]]
