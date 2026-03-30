#!/usr/bin/env python3
from __future__ import annotations

import io
import json
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
REF_BIB = ROOT / "ref" / "refs.bib"
PDF_DIR = ROOT / "references_pdf"
INDEX_MD = PDF_DIR / "INDEX.md"
MAP_PATH = Path(__file__).resolve().parent / "reference_pdf_urls.json"


def load_sources() -> dict[str, str]:
    d = json.loads(MAP_PATH.read_text(encoding="utf-8"))
    return {k: v for k, v in d.items() if isinstance(v, str) and v.startswith("http")}


def parse_index() -> dict[str, str]:
    m: dict[str, str] = {}
    for line in INDEX_MD.read_text(encoding="utf-8", errors="replace").splitlines():
        if not line.strip().startswith("|"):
            continue
        p = [x.strip() for x in line.split("|")]
        if len(p) < 4:
            continue
        fn, key = p[1], p[2]
        if fn.endswith(".pdf") and key not in ("文件名", "--------"):
            m[fn] = key
    return m


def load_titles() -> dict[str, str]:
    text = REF_BIB.read_text(encoding="utf-8", errors="replace")
    out: dict[str, str] = {}
    for mm in re.finditer(r"^@\w+\{\s*([^,\s]+)\s*,", text, re.MULTILINE):
        key = mm.group(1).strip()
        start = mm.end()
        nxt = re.search(r"\n@", text[start:])
        block = text[start:] if not nxt else text[start : start + nxt.start()]
        tm = re.search(r"\btitle\s*=\s*", block, re.I)
        if not tm:
            continue
        rest = block[tm.end() :].lstrip()
        if rest.startswith("{"):
            depth = 0
            for j, ch in enumerate(rest):
                if ch == "{":
                    depth += 1
                elif ch == "}":
                    depth -= 1
                    if depth == 0:
                        out[key] = rest[1:j]
                        break
        elif rest.startswith('"'):
            eq = rest.find('"', 1)
            if eq != -1:
                out[key] = rest[1:eq]
    return out


def strip_tex(s: str) -> str:
    s = re.sub(r"\$[^\$]*\$", "", s)
    s = re.sub(r"\\[a-zA-Z]+\{([^}]*)\}", r"\1", s)
    s = re.sub(r"\{|\}", "", s)
    return re.sub(r"\s+", " ", s).strip()


def overlap(exp: str, blob: str) -> float:
    def tok(x: str) -> set[str]:
        x = re.sub(r"[^\w\s]", " ", x.lower())
        return {w for w in x.split() if len(w) > 2}

    e, b = tok(exp), tok(blob)
    return len(e & b) / len(e) if e else 1.0


def fetch(url: str, timeout: int = 180):
    req = Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; thesis-ref-fix/1.0)"})
    try:
        with urlopen(req, timeout=timeout) as r:
            data = r.read()
    except (HTTPError, URLError, TimeoutError, OSError) as e:
        return None, str(e)
    if data.startswith(b"%PDF") or (b"%PDF" in data[:4000]):
        return data, "ok"
    return None, "not_pdf"


def sample_pdf(data: bytes) -> str:
    try:
        r = PdfReader(io.BytesIO(data))
        t = []
        for i in range(min(4, len(r.pages))):
            t.append(r.pages[i].extract_text() or "")
        return "\n".join(t)[:12000]
    except Exception as e:
        return "read_err %s" % e


def main() -> int:
    dry = "--dry-run" in sys.argv
    sources = load_sources()
    fn_key = parse_index()
    titles = load_titles()
    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    backup = PDF_DIR / ("_backup_%s" % ts)
    log: list[dict] = []
    if not dry:
        backup.mkdir(parents=True, exist_ok=True)

    for fn, bib in sorted(fn_key.items()):
        url = sources.get(bib)
        if not url:
            log.append({"file": fn, "bibkey": bib, "action": "skip_no_url"})
            continue
        dest = PDF_DIR / fn
        exp = strip_tex(titles.get(bib, ""))
        if dry:
            print("DRY", fn, bib)
            continue
        if dest.exists():
            shutil.copy2(dest, backup / fn)
        data, err = fetch(url)
        if data is None:
            log.append({"file": fn, "bibkey": bib, "ok": False, "error": err})
            print("FAIL", fn, err)
            continue
        s = sample_pdf(data)
        sc = overlap(exp, s) if exp else 1.0
        zh = [c for c in exp if "\u4e00" <= c <= "\u9fff"]
        if zh:
            sc = max(sc, sum(1 for c in zh if c in s) / len(zh))
        lo = 0.12 if len(exp) < 30 else 0.18
        if "arxiv.org" in url and len(data) > 35000:
            lo = 0.0
        if sc < lo and "read_err" not in s:
            log.append({"file": fn, "bibkey": bib, "ok": False, "error": "title_mismatch %.3f" % sc})
            print("WARN", fn, "overlap", sc)
            continue
        dest.write_bytes(data)
        log.append({"file": fn, "bibkey": bib, "ok": True, "bytes": len(data)})
        print("OK", fn, len(data))
    rep = PDF_DIR / ("fix_report_%s.json" % ts)
    if not dry:
        rep.write_text(json.dumps(log, indent=2, ensure_ascii=False), encoding="utf-8")
        print("Backup", backup)
        print("Report", rep)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
