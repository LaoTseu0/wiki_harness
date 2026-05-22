## Décision et dépôt dans Praxis

- **Décision** — Praxis n'implémente pas les poids d'**embedding** d'un modèle
  réel. Le laboratoire peut les inspecter à travers le runtime.
- **Alternatives** — recopier l'architecture d'un modèle dans `generation`, ou
  traiter l'**embedding** comme un service de recherche sémantique.
- **Critère** — le Parcours 0 doit ouvrir le mécanisme qui explique la frontière
  identifiants–tenseurs sans réécrire un moteur tensoriel.
- **Coût accepté** — l'inspection dépend d'un runtime et d'un **checkpoint**
  explicitement versionnés.
- **Condition de révision** — le Parcours 1 définira la frontière d'inférence et
  les formats de poids réellement servis.
- **Contrat** — aucun contrat public : ce mécanisme reste interne au modèle.
- **Invariant et tests** — le tokenizer et le **checkpoint** ont un **vocabulaire**
  compatible ; les identifiants restent dans les bornes.
