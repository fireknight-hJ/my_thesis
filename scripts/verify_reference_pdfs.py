#!/usr/bin/env python3
"""
Verify PDFs in references_pdf/ against ref/refs.bib titles (via INDEX.md filename->bibkey).
Detect duplicates and likely wrong files; optional download from known open URLs.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
REF_BIB = ROOT / "ref" / "refs.bib"
INDEX_MD = ROOT / "references_pdf" / "INDEX.md"
PDF_DIR = ROOT / "references_pdf"


def parse_index_mapping() -> dict[str, str]:
    """filename.pdf -> bibtex key"""
    text = INDEX_MD.read_text(encoding="utf-8", errors="replace")
    m: dict[str, str] = {}
    for line in text.splitlines():
        if not line.strip().startswith("|"):
            continue
        parts = [p.strip() for p in line.split("|")]
        if len(parts) < 4:
            continue
        fn = parts[1]
        key = parts[2]
        if not fn.endswith(".pdf") or key in ("文件名", "--------"):
            continue
        m[fn] = key
    return m


def load_bib_titles() -> dict[str, str]:
    """Minimal BibTeX title extraction (avoids bibtexparser/pyparsing version issues)."""
    text = REF_BIB.read_text(encoding="utf-8", errors="replace")
    out: dict[str, str] = {}
    for m in re.finditer(r"^@\w+\{\s*([^,\s]+)\s*,", text, re.MULTILINE):
        key = m.group(1).strip()
        start = m.end()
        nxt = re.search(r"\n@", text[start:])
        block = text[start:] if not nxt else text[start : start + nxt.start()]
        tm = re.search(r"\btitle\s*=\s*", block, re.I)
        if not tm:
            continue
        rest = block[tm.end() :].lstrip()
        if not rest:
            continue
        if rest[0] == "{":
            depth = 0
            j = 0
            for j, ch in enumerate(rest):
                if ch == "{":
                    depth += 1
                elif ch == "}":
                    depth -= 1
                    if depth == 0:
                        out[key] = rest[1:j]
                        break
        elif rest[0] == '"':
            endq = rest.find('"', 1)
            if endq != -1:
                out[key] = rest[1:endq]
    return out


def strip_latex_braces(s: str) -> str:
    s = re.sub(r"\\[a-zA-Z]+\{([^}]*)\}", r"\1", s)
    s = re.sub(r"\{|\}", "", s)
    s = s.replace("--", "-")
    return re.sub(r"\s+", " ", s).strip()


def norm_tokens(s: str) -> set[str]:
    s = re.sub(r"[^\w\s]", " ", s.lower())
    return {w for w in s.split() if len(w) > 2}


def overlap_score(expected: str, haystack: str) -> float:
    e = norm_tokens(expected)
    h = norm_tokens(haystack)
    if not e:
        return 1.0
    return len(e & h) / len(e)


def chinese_coverage(expected: str, haystack: str) -> float:
    chars = [c for c in expected if "\u4e00" <= c <= "\u9fff"]
    if not chars:
        return 1.0
    return sum(1 for c in chars if c in haystack) / len(chars)


def pdf_fingerprint(path: Path) -> tuple[str, str, str, int]:
    """Returns (md5, meta_title, text_sample, page_count)"""
    data = path.read_bytes()
    h = hashlib.md5(data).hexdigest()
    if not data.startswith(b"%PDF"):
        return h, "", "", 0
    try:
        r = PdfReader(str(path))
        n = len(r.pages)
        meta = r.metadata or {}
        mt = (meta.get("/Title") or meta.get("/title") or "") or ""
        if isinstance(mt, bytes):
            mt = mt.decode("utf-8", errors="replace")
        parts = []
        for i in range(min(3, n)):
            t = r.pages[i].extract_text() or ""
            parts.append(t)
        sample = "\n".join(parts)[:8000]
        return h, mt, sample, n
    except Exception as e:
        return h, "", f"__READ_ERROR__ {e}", 0


# Known open-access download URLs (bib key -> url). Extend as needed.
DOWNLOAD_URLS: dict[str, str] = {
    "clements2020halucinator": "https://www.usenix.org/system/files/sec20-clements.pdf",
    "firmadyne": "https://www.usenix.org/system/files/conference/usenixsecurity16/sec16_paper_chen.pdf",
    "avatar": "https://www.ndss-symposium.org/wp-content/uploads/2017/09/ndss2017_08A-3_Zaddach_paper.pdf",
    "iotfuzzer": "https://www.ndss-symposium.org/wp-content/uploads/2018/02/ndss2018_01A-3_Chen_paper.pdf",
    "firmalice": "https://www.ndss-symposium.org/wp-content/uploads/2017/09/ndss2015_08A-3_Shoshitaishvili_paper.pdf",
    "driller": "https://www.ndss-symposium.org/wp-content/uploads/2017/09/ndss2016_08A-1_Stephens_paper.pdf",
    "qsym": "https://www.usenix.org/system/files/conference/usenixsecurity18/usenixsecurity18-yun.pdf",
    "angora": "https://www.computer.org/csdl/pds/api/csdl/proceedings/download-article/18OmNyT1xMg/pdf",  # may fail - IEEE
    "pretender": "https://www.usenix.org/system/files/usenixsecurity19-gustafson.pdf",
    "firmafl": "https://www.usenix.org/system/files/usenixsecurity19-zheng.pdf",
    "fengp2020p2im": "https://www.usenix.org/system/files/usenixsecurity20-feng.pdf",
    "mirai2018": "https://www.usenix.org/system/files/conference/usenixsecurity17/usenixsecurity17-antonakakis.pdf",
    "pararehosting": "https://www.usenix.org/system/files/usenixsecurity22-li-wenqiang.pdf",
    "fuzzware": "https://www.usenix.org/system/files/usenixsecurity22-scharnowski.pdf",
    "firmadyne": "https://www.usenix.org/system/files/conference/usenixsecurity16/sec16_paper_chen.pdf",
    "vaswani2017attention": "https://arxiv.org/pdf/1706.03762.pdf",
    "brown2020language": "https://arxiv.org/pdf/2005.14165.pdf",
    "openai2023gpt4": "https://arxiv.org/pdf/2303.08774.pdf",
    "touvron2023llama": "https://arxiv.org/pdf/2302.13971.pdf",
    "roziere2023code": "https://arxiv.org/pdf/2308.12950.pdf",
    "li2023starcoder": "https://arxiv.org/pdf/2305.06161.pdf",
    "radford2018improving": "https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf",
    "feng2020codebert": "https://arxiv.org/pdf/2002.08155.pdf",
    "wang2021codet5": "https://arxiv.org/pdf/2109.00859.pdf",
    "chen2021evaluating": "https://arxiv.org/pdf/2107.03374.pdf",
    "hendrycks2021measuring": "https://arxiv.org/pdf/2105.09938.pdf",
    "austin2021program": "https://arxiv.org/pdf/2108.07732.pdf",
    "wei2022cot": "https://arxiv.org/pdf/2201.11903.pdf",
    "wei2022finetuned": "https://arxiv.org/pdf/2109.01652.pdf",
    "schick2023toolformer": "https://arxiv.org/pdf/2302.04761.pdf",
    "chen2023teaching": "https://arxiv.org/pdf/2304.05128.pdf",
    "zheng2023codegeex": "https://arxiv.org/pdf/2303.17568.pdf",
    "pearce2022examining": "https://arxiv.org/pdf/2207.08264.pdf",
    "ziegler2022productivity": "https://arxiv.org/pdf/2205.01829.pdf",
    "du2022glm": "https://aclanthology.org/2022.acl-long.26.pdf",
    "fan2023automated": "https://arxiv.org/pdf/2301.06947.pdf",
    "uemu": "https://dl.acm.org/doi/pdf/10.1145/3460120.3485382",  # may need cookie - try
    "laelaps": "https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=9662273",  # often paywalled
    "avatar2": "https://www.ndss-symposium.org/wp-content/uploads/2018/07/bar2018_26_Muench_paper.pdf",
}

# Remove unreliable / duplicate keys
DOWNLOAD_URLS.pop("angora", None)  # IEEE link unreliable


def download(url: str, dest: Path, timeout: int = 120) -> tuple[bool, str]:
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = Request(url, headers={"User-Agent": "Mozilla/5.0 thesis-ref-fix"})
    try:
        with urlopen(req, timeout=timeout) as resp:
            data = resp.read()
        if (not data.startswith(b"%PDF")) and (b"%PDF" not in data[:2000]):
            return False, f"not a PDF ({len(data)} bytes)"
        dest.write_bytes(data)
        return True, f"ok {len(data)} bytes"
    except (HTTPError, URLError, TimeoutError, OSError) as e:
        return False, str(e)


def main() -> int:
    file_to_key = parse_index_mapping()
    titles = load_bib_titles()
    pdfs = sorted(PDF_DIR.glob("*.pdf"))
    by_hash: dict[str, list[str]] = {}
    rows = []

    for p in pdfs:
        fn = p.name
        key = file_to_key.get(fn)
        if not key:
            rows.append({"file": fn, "error": "not in INDEX.md"})
            continue
        expected = titles.get(key)
        if not expected:
            rows.append({"file": fn, "bibkey": key, "error": "no title in refs.bib"})
            continue
        exp_clean = strip_latex_braces(expected)
        md5, meta, sample, pages = pdf_fingerprint(p)
        by_hash.setdefault(md5, []).append(fn)

        is_zh = any("\u4e00" <= c <= "\u9fff" for c in exp_clean)
        if is_zh:
            cov = chinese_coverage(exp_clean, sample)
            meta_s = overlap_score(exp_clean, meta) if meta else 0.0
            score = max(cov, meta_s)
            ok = cov >= 0.45 or meta_s >= 0.3
        else:
            s_meta = overlap_score(exp_clean, meta) if meta else 0.0
            s_body = overlap_score(exp_clean, sample)
            score = max(s_meta, s_body)
            # Short titles (e.g. "QSYM: ...") need lower bar
            min_score = 0.22 if len(norm_tokens(exp_clean)) < 6 else 0.28
            ok = score >= min_score or exp_clean.lower()[:40] in sample.lower()

        tiny_suspect = p.stat().st_size < 80_000 and not is_zh and pages > 0

        rows.append(
            {
                "file": fn,
                "bibkey": key,
                "expected_title": exp_clean[:120],
                "bytes": p.stat().st_size,
                "pages": pages,
                "md5": md5,
                "meta_title": (meta or "")[:200],
                "score": round(score, 3),
                "ok": ok and not tiny_suspect,
                "tiny_suspect": tiny_suspect,
            }
        )

    dupes = {h: fs for h, fs in by_hash.items() if len(fs) > 1}

    bad = [r for r in rows if isinstance(r, dict) and r.get("ok") is False]
    report_path = PDF_DIR / "verification_report.json"
    report_path.write_text(
        json.dumps({"duplicates": dupes, "rows": rows, "bad_count": len(bad)}, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print("=== Duplicate MD5 (same file reused) ===")
    for h, fs in sorted(dupes.items(), key=lambda x: -len(x[1])):
        print(h, fs)

    print("\n=== Likely wrong / unchecked ===")
    for r in rows:
        if not isinstance(r, dict):
            continue
        if r.get("error"):
            print("ERR", r)
            continue
        if r.get("duplicates"):
            pass
        if r.get("ok") is False:
            print(
                f"BAD {r['file']} key={r['bibkey']} score={r['score']} "
                f"size={r['bytes']} pages={r['pages']} meta={r.get('meta_title','')[:80]!r}"
            )

    # Apply downloads for bad entries that have URLs
    fix = "--fix" in sys.argv
    if fix:
        backup = PDF_DIR / "_wrong_backup"
        backup.mkdir(exist_ok=True)
        for r in bad:
            if "bibkey" not in r:
                continue
            key = r["bibkey"]
            url = DOWNLOAD_URLS.get(key)
            if not url:
                print(f"SKIP no URL for {key}")
                continue
            fn = r["file"]
            dest = PDF_DIR / fn
            bak = backup / fn
            if not bak.exists():
                bak.write_bytes(dest.read_bytes())
            ok, msg = download(url, dest)
            print(f"DOWNLOAD {fn} <- {url} => {ok} {msg}")

    print(f"\nWrote {report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
