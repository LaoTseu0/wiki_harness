## Limites et cas d'échec

- **La reconstruction ne prouve pas** — le comportement du décodeur d'un
  tokenizer SentencePiece ou byte-level particulier.
- **Praxis ne garantit pas encore** — que chaque fragment décodable est déjà
  publiable devant une stop sequence.
- **Échec provoqué** — finaliser un flux au milieu d'un caractère doit produire
  une erreur typée.
- **Ouverture ultérieure** — [[16-conditions-arret|Borner la génération]] et le
  Parcours 2 pour le streaming de transport.
