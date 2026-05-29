"""Tests ciblés du formatage des termes de glossaire."""

from __future__ import annotations

import unittest

from glossarylib import formater_terme, occurrences_texte


class GlossaryLibTest(unittest.TestCase):
    """Protège les invariants éditoriaux du formateur."""

    def test_formater_est_idempotent(self) -> None:
        texte = "Token puis tokens."
        attendu = "[[glossaire/token|Token]] puis **tokens**."

        formate, vues = formater_terme(texte, "token", "token", 0)
        reformate, nouvelles_vues = formater_terme(
            formate,
            "token",
            "token",
            0,
        )

        self.assertEqual(attendu, formate)
        self.assertEqual(attendu, reformate)
        self.assertEqual(2, vues)
        self.assertEqual(2, nouvelles_vues)

    def test_liens_et_code_restant_proteges(self) -> None:
        texte = (
            "[documentation token\n"
            "suite](https://example.test/token)\n"
            "`token`\n"
            "```text\n"
            "token\n"
            "```\n"
            "token"
        )

        formate, vues = formater_terme(texte, "token", "token", 0)

        self.assertIn("](https://example.test/token)", formate)
        self.assertIn("```text\ntoken\n```", formate)
        self.assertTrue(formate.endswith("[[glossaire/token|token]]"))
        self.assertEqual(1, vues)

    def test_pluriel_du_premier_mot_est_reconnu(self) -> None:
        texte = (
            "[[glossaire/token-de-controle|Tokens de contrôle]] puis "
            "**token de contrôle**."
        )

        occurrences = occurrences_texte(
            texte,
            "token de contrôle",
            "token-de-controle",
        )

        self.assertEqual(
            ["glossaire", "gras"],
            [occurrence.statut for occurrence in occurrences],
        )


if __name__ == "__main__":
    unittest.main()
