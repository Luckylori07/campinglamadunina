"""Verifica che tutte le lingue abbiano le stesse chiavi di traduzione."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from i18n import S
base = set(S["it"])
ok = True
for l, d in S.items():
    miss, extra = base - set(d), set(d) - base
    if miss or extra:
        ok = False
        print(l, "mancanti:", sorted(miss), "extra:", sorted(extra))
print("OK: stesse chiavi in", ", ".join(S), f"({len(base)} chiavi)" if ok else "")
sys.exit(0 if ok else 1)
