## Reconstruction

Créer un environnement avec la bibliothèque standard, puis observer la
frontière sans installer de dépendance.

Sous PowerShell :

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -c "import sys; print(sys.executable); print(sys.prefix); print(sys.base_prefix); print(sys.prefix != sys.base_prefix)"
```

Sous Linux ou macOS :

```bash
python3 -m venv .venv
./.venv/bin/python -c "import sys; print(sys.executable); print(sys.prefix); print(sys.base_prefix); print(sys.prefix != sys.base_prefix)"
```

L'expérience doit montrer deux préfixes distincts et la valeur `True`. Elle
n'établit encore rien sur le resolver, le lockfile ou le packaging : elle isole
seulement le mécanisme de l'environnement virtuel.
