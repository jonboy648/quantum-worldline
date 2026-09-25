#!/usr/bin/env python3
"""
zenodo_v5_build.py -- build, upload and VERIFY the v5 correction draft. NEVER publishes.

Usage:
  python zenodo_v5_build.py render    # notice.md -> notice.pdf, merged PDF, description.html
  python zenodo_v5_build.py upload    # replace/add files on draft 22080720 (deletes same-name first)
  python zenodo_v5_build.py metadata  # PUT canonical metadata (rebuilt, never echoed from GET)
  python zenodo_v5_build.py verify    # re-GET the draft and check everything against local truth
  python zenodo_v5_build.py all       # render + upload + metadata + verify

There is deliberately no 'publish' subcommand. Publishing is a separate, explicit human action.
"""
import io, json, os, re, subprocess, sys, urllib.request
import requests
from pypdf import PdfReader, PdfWriter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
DEP = 22080720
API = "https://zenodo.org/api/deposit/depositions/%d" % DEP
TOK = open(os.path.expanduser("~/.zenodo-token")).read().strip()
H = {"Authorization": "Bearer " + TOK}

MANUSCRIPT = os.path.join(ROOT, "research", "paper-draft-scipost.pdf")   # 24 pp, unaltered v4 file
MERGED = os.path.join(HERE, "paper-draft-scipost.pdf")

# (remote filename, local path)
CT = os.path.join(ROOT, "research", "tools", "channel-test")
FILES = [
    ("paper-draft-scipost.pdf", MERGED),
    ("SIM-2026-072-alpha-retraction.json", os.path.join(ROOT, "research", "data", "simulations", "SIM-2026-072.json")),
    ("SIM-2026-073-channel-test.json", os.path.join(ROOT, "research", "data", "simulations", "SIM-2026-073.json")),
    ("SIM-2026-074-kramers-wannier-ring.json", os.path.join(ROOT, "research", "data", "simulations", "SIM-2026-074.json")),
    ("channel-test-PREREGISTRATION.md", os.path.join(CT, "PREREGISTRATION.md")),
    ("ring-test-PREREGISTRATION-RING.md", os.path.join(CT, "PREREGISTRATION-RING.md")),
    ("qw_channel_test.py", os.path.join(CT, "qw_channel_test.py")),
    ("qw_ring_test.py", os.path.join(CT, "qw_ring_test.py")),
    ("qw_channel_common.py", os.path.join(CT, "qw_channel_common.py")),
    ("test_gates.py", os.path.join(CT, "test_gates.py")),
    ("qw_alpha_reanalysis.py", os.path.join(ROOT, "research", "tools", "force-reanalysis", "qw_alpha_reanalysis.py")),
    ("qw_alpha_figure.py", os.path.join(ROOT, "research", "tools", "force-reanalysis", "qw_alpha_figure.py")),
    ("alpha_reanalysis_figure.pdf", os.path.join(ROOT, "research", "tools", "force-reanalysis", "alpha_reanalysis_figure.pdf")),
    ("ERRATA.md", os.path.join(ROOT, "research", "ERRATA.md")),
]

ORIGINAL_ABSTRACT_MARK = "The abstract of the original manuscript follows unchanged"


def render():
    os.chdir(HERE)
    subprocess.run(["pandoc", "notice.md", "-o", "notice.pdf", "--pdf-engine=pdflatex",
                    "-V", "geometry:margin=0.7in", "-V", "fontsize=10pt"], check=True)
    subprocess.run(["pandoc", "notice.md", "-t", "html", "-o", "notice_body.html"], check=True)
    w = PdfWriter()
    for src in ("notice.pdf", MANUSCRIPT):
        for pg in PdfReader(src).pages:
            w.add_page(pg)
    with open(MERGED, "wb") as f:
        w.write(f)
    n_notice = len(PdfReader("notice.pdf").pages)
    n_all = len(PdfReader(MERGED).pages)
    # description: new notice body + the original abstract block preserved from the current draft
    cur = open("description_current.html", encoding="utf-8").read()
    i = cur.find(ORIGINAL_ABSTRACT_MARK)
    assert i > 0, "original-abstract marker not found in description_current.html"
    tail = cur[cur.rfind("<p", 0, i):]
    body = open("notice_body.html", encoding="utf-8").read()
    # headings -> bold paragraphs (Zenodo's sanitizer keeps p/strong/em/ul/li, not h1-h6 reliably)
    body = re.sub(r"<h[1-6][^>]*>", "<p><strong>", body)
    body = re.sub(r"</h[1-6]>", "</strong></p>", body)
    # table -> list: Zenodo strips <table>. Rebuild the withdrawal table as one <li> per row.
    def table_to_list(mt):
        rows = re.findall(r"<tr>(.*?)</tr>", mt.group(0), flags=re.S)
        items = []
        for row in rows[1:]:  # skip header
            cells = [re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", c)).strip()
                     for c in re.findall(r"<td[^>]*>(.*?)</td>", row, flags=re.S)]
            if len(cells) == 4:
                items.append("<li><strong>%s.</strong> Was: %s. Now: %s. Why: %s.</li>" % tuple(cells))
        return "<ul>\n" + "\n".join(items) + "\n</ul>"
    body = re.sub(r"<table>.*?</table>", table_to_list, body, flags=re.S)
    assert "<table" not in body and "<h2" not in body and 'id="' not in body
    desc = ('<p><strong>CORRECTION NOTICE (v5, 2026-09-06). The central result of v1-v4 is WITHDRAWN. '
            'This record has not been peer reviewed.</strong></p>\n' + body + "\n" + tail)
    open("description.html", "w", encoding="utf-8").write(desc)
    print("render: notice %d pp, merged %d pp, description %d chars" % (n_notice, n_all, len(desc)))


def upload():
    d = requests.get(API, headers=H).json()
    assert d["state"] == "unsubmitted", d["state"]
    bucket = d["links"]["bucket"]
    existing = {f["filename"]: f for f in d["files"]}
    for name, path in FILES:
        assert os.path.exists(path), path
        if name in existing:
            r = requests.delete(existing[name]["links"]["self"], headers=H)
            assert r.status_code in (204, 404), (name, r.status_code, r.text[:200])
        with open(path, "rb") as fh:
            r = requests.put(bucket + "/" + name, data=fh, headers=H)
        assert r.status_code in (200, 201), (name, r.status_code, r.text[:300])
        print("uploaded", name, os.path.getsize(path))
    # remove anything on the draft that is not in FILES (stale names)
    d = requests.get(API, headers=H).json()
    keep = {n for n, _ in FILES}
    for f in d["files"]:
        if f["filename"] not in keep:
            requests.delete(f["links"]["self"], headers=H)
            print("removed stale", f["filename"])


def metadata():
    desc = open(os.path.join(HERE, "description.html"), encoding="utf-8").read()
    md = {
        "upload_type": "publication",
        "publication_type": "preprint",
        "publication_date": "2026-09-06",
        "title": "Power-Law Holographic Forces and Causal Transport in MERA Quantum Circuits",
        "creators": [{"name": "Cackler, Jon", "affiliation": "Independent Researcher",
                      "orcid": "0009-0008-2011-5944"}],
        "description": desc,
        "access_right": "open",
        "license": "cc-by-4.0",
        "version": "v5",
        "keywords": ["MERA", "tensor networks", "AdS/CFT", "quantum simulation", "conformal field theory",
                     "holographic force", "Kramers-Wannier duality", "correction", "retraction"],
        "notes": ("Version 5 is a CORRECTION. The central result of versions 1-4 (force exponent "
                  "alpha = 3.92 +/- 0.16, stress-tensor exchange, and its claimed universality) is withdrawn "
                  "as a fitting artifact. The registered discriminating test is void (Kramers-Wannier "
                  "self-duality). No corrected exponent is established. This record has not been peer "
                  "reviewed. The manuscript PDF is unaltered; a correction notice is prepended."),
        "related_identifiers": [
            {"identifier": "https://github.com/jonboy648/quantum-worldline", "relation": "isSupplementedBy",
             "resource_type": "software", "scheme": "url"},
        ],
        "prereserve_doi": True,
    }
    r = requests.put(API, headers={**H, "Content-Type": "application/json"}, data=json.dumps({"metadata": md}))
    assert r.status_code == 200, (r.status_code, r.text[:500])
    print("metadata PUT ok; version", r.json()["metadata"].get("version"))


def verify():
    d = requests.get(API, headers=H).json()
    m = d["metadata"]
    checks = []
    def c(name, ok, detail=""):
        checks.append((name, bool(ok), detail)); print(("PASS " if ok else "FAIL ") + name + ("  " + detail if detail else ""))
    c("state unsubmitted (nothing published)", d["state"] == "unsubmitted" and not d["submitted"])
    c("version v5", m.get("version") == "v5")
    c("publication_date 2026-09-06", m.get("publication_date") == "2026-09-06")
    c("title unchanged", m.get("title") == "Power-Law Holographic Forces and Causal Transport in MERA Quantum Circuits")
    c("creator + orcid survived PUT", m.get("creators", [{}])[0].get("orcid") == "0009-0008-2011-5944")
    c("license survived PUT", m.get("license") in ("cc-by-4.0", "CC-BY-4.0"))
    c("related_identifiers survived PUT", bool(m.get("related_identifiers")))
    desc = re.sub(r"\s+", " ", re.sub("<[^>]+>", " ", m.get("description", "")))   # pandoc wraps lines
    c("description leads with correction", desc.strip().startswith("CORRECTION NOTICE"))
    c("description says not peer reviewed", "not been peer reviewed" in desc)
    c("description does NOT name the journal", "Physical Review" not in desc and "PRD" not in desc)
    c("description flags replacement as provisional", "provisional" in desc and "open question" in desc)
    c("description carries SIM-074 / Kramers-Wannier", "Kramers-Wannier" in desc and "SIM-2026-074" in desc)
    c("description keeps original abstract", ORIGINAL_ABSTRACT_MARK in desc and "3.92 +/- 0.16 (24q)" in desc)
    c("no em dash in description", "—" not in m.get("description", ""))
    remote = {f["filename"]: f for f in d["files"]}
    for name, path in FILES:
        c("file present + size matches: " + name, name in remote and remote[name]["filesize"] == os.path.getsize(path),
          "" if name in remote else "MISSING")
    c("no stale files on draft", set(remote) == {n for n, _ in FILES}, str(set(remote) - {n for n, _ in FILES}))
    # download the merged PDF back and inspect
    url = remote["paper-draft-scipost.pdf"]["links"]["download"] + "?access_token=" + TOK
    data = urllib.request.urlopen(url).read()
    r = PdfReader(io.BytesIO(data))
    p1 = r.pages[0].extract_text()
    c("remote PDF page count = notice + 24", len(r.pages) == len(PdfReader(os.path.join(HERE, "notice.pdf")).pages) + 24, str(len(r.pages)))
    c("remote PDF page 1 is the notice", p1.startswith("CORRECTION NOTICE"))
    c("remote PDF notice has no journal name", "Physical Review" not in p1 + r.pages[1].extract_text())
    c("manuscript body unaltered (page after notice = original page 1)",
      "SciPost Physics Submission" in r.pages[len(r.pages) - 24].extract_text())
    n_fail = sum(1 for _, ok, _ in checks if not ok)
    print("\n%d/%d checks pass" % (len(checks) - n_fail, len(checks)))
    json.dump({"draft": DEP, "checks": checks}, open(os.path.join(HERE, "verify_result.json"), "w"), indent=1)
    sys.exit(1 if n_fail else 0)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "verify"
    steps = {"render": [render], "upload": [upload], "metadata": [metadata], "verify": [verify],
             "all": [render, upload, metadata, verify]}[cmd]
    for s in steps:
        s()
