# UTF-8

Encodage variable qui représente chaque point de code Unicode avec un à quatre
octets. Une frontière de fragment peut couper cette suite d’octets.

Le signe « € » s’encode en trois octets, `E2 82 AC`. Une lecture qui s’arrête après
`E2 82` doit attendre le troisième octet pour décoder le signe.

[Reconnaître une séquence d’octets incomplète](../parcours/0-generation/01-unicode-octets.md#connaissances)
