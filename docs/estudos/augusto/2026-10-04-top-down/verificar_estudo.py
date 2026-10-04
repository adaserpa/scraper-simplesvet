"""Verifica documentacao e fontes sem importar ou executar o scraper."""
import ast
import csv
import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]

def main():
    manifest = json.loads((HERE / "manifesto.json").read_text(encoding="utf-8"))
    for item in manifest["files"]:
        path = ROOT / item["path"]
        data = path.read_bytes()
        assert hashlib.sha256(data).hexdigest() == item["sha256"], path
        blob = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
        assert blob == item["blob_sha"], path
        if path.suffix == ".py":
            ast.parse(data.decode("utf-8"))
    for name in ["inventario-arquivos.csv", "inventario-simbolos.csv",
                 "inventario-interacoes.csv", "dicionario-dados.csv", "achados.csv"]:
        with (HERE / name).open(encoding="utf-8", newline="") as file:
            rows = list(csv.DictReader(file))
            assert rows, name
            for row in rows:
                if "path" in row:
                    source = ROOT / row["path"]
                    assert source.exists(), source
                    if "line" in row:
                        assert 1 <= int(row["line"]) <= len(source.read_text(encoding="utf-8").splitlines())
    for path in HERE.glob("*.md"):
        content = path.read_text(encoding="utf-8")
        for link in re.findall(r"\]\(([^)]+)\)", content):
            if not link.startswith(("http:", "https:", "#")):
                assert (HERE / link.split("#")[0]).exists(), (path, link)
        for source, first, last in re.findall(
            r"/blob/[0-9a-f]{40}/([^#)]+)#L(\d+)-L(\d+)", content
        ):
            count = len((ROOT / source).read_text(encoding="utf-8").splitlines())
            assert 1 <= int(first) <= int(last) <= count, (path, source, first, last)
    print("OK: hashes, sintaxe das fontes, inventarios, links locais e linhas de evidencia.")
    print("Automacao nao executada; SimplesVet nao acessado.")

if __name__ == "__main__":
    main()
