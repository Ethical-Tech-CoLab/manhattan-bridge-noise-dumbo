"""Validate the GitHub issue forms against the published schema.

A YAML issue form that fails GitHub's parser does not error visibly - it
degrades to a plain body textarea, which is exactly the failure mode this
form exists to prevent. So it is checked against the schema rather than
eyeballed.
"""
import glob
import json
import os
import sys
import urllib.request

import yaml
import jsonschema

SCHEMA_URL = "https://json.schemastore.org/github-issue-forms.json"
CACHE = os.path.join(os.environ.get("TEMP", "."), "github-issue-forms.json")

if os.path.exists(CACHE):
    schema = json.load(open(CACHE, encoding="utf-8"))
    print("schema: cached")
else:
    req = urllib.request.Request(SCHEMA_URL, headers={"User-Agent": "curl/8"})
    raw = urllib.request.urlopen(req, timeout=30).read().decode("utf-8")
    schema = json.loads(raw)
    open(CACHE, "w", encoding="utf-8").write(raw)
    print("schema: fetched %d bytes" % len(raw))

root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ISSUE_TEMPLATE")
bad = 0
for f in sorted(glob.glob(os.path.join(root, "*.yml"))):
    name = os.path.basename(f)
    doc = yaml.safe_load(open(f, encoding="utf-8"))
    if name == "config.yml":
        # config.yml is a different schema; check it structurally.
        ok = isinstance(doc.get("blank_issues_enabled"), bool)
        for cl in doc.get("contact_links", []):
            ok = ok and {"name", "url", "about"} <= set(cl)
        print("%-18s %s" % (name, "ok" if ok else "MALFORMED"))
        bad += 0 if ok else 1
        continue

    errs = sorted(jsonschema.Draft7Validator(schema).iter_errors(doc),
                  key=lambda e: list(e.path))
    ids = [b.get("id") for b in doc["body"] if b.get("id")]
    dup = len(ids) != len(set(ids))
    if errs or dup:
        bad += 1
        print("%-18s %d SCHEMA ERRORS%s" % (name, len(errs),
                                            ", DUPLICATE IDS" if dup else ""))
        for e in errs[:8]:
            print("    %s: %s" % ("/".join(str(x) for x in e.path), e.message[:150]))
    else:
        kinds = {}
        for b in doc["body"]:
            kinds[b["type"]] = kinds.get(b["type"], 0) + 1
        req = sum(1 for b in doc["body"]
                  if (b.get("validations") or {}).get("required"))
        print("%-18s ok  %d fields %s, %d required, %d unique ids"
              % (name, len(doc["body"]),
                 ",".join("%s=%d" % kv for kv in sorted(kinds.items())),
                 req, len(set(ids))))

sys.exit(1 if bad else 0)
