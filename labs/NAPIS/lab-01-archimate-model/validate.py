"""Validate an ArchiMate Open Exchange starter file (stdlib only)."""
import sys
import xml.etree.ElementTree as ET

NS = {"a": "http://www.opengroup.org/xsd/archimate/3/"}

def local(tag):
    return tag.split("}", 1)[-1] if "}" in tag else tag

def validate(path, strict=False):
    errors, warnings = [], []
    try:
        tree = ET.parse(path)
    except ET.ParseError as e:
        return [f"XML parse error: {e}"], []
    root = tree.getroot()
    # collect elements
    elements = {}
    for el in root.iter():
        if local(el.tag) == "element":
            ident = el.get("identifier")
            if not ident:
                errors.append("element without identifier")
                continue
            if ident in elements:
                errors.append(f"duplicate element id: {ident}")
            elements[ident] = el.get("type", "?")
    if not elements:
        # fallback: namespace-less search
        for el in root.findall(".//element") + root.findall(".//{*}element"):
            pass
        errors.append("no <element> entries found (wrong namespace?)")
    # relationships
    rels = []
    for r in root.iter():
        if local(r.tag) == "relationship":
            rels.append(r)
            rid = r.get("identifier", "?")
            for end in ("source", "target"):
                ref = r.get(end)
                if ref not in elements:
                    errors.append(f"relationship {rid}: {end} '{ref}' not found")
    # views reference check
    view_nodes = 0
    for v in root.iter():
        if local(v.tag) in ("view", "views"):
            pass
        if local(v.tag) == "node":
            ref = v.get("elementRef")
            view_nodes += 1
            if ref not in elements:
                errors.append(f"view node elementRef '{ref}' not found")
        if local(v.tag) == "connection":
            ref = v.get("relationshipRef")
            if ref not in [r.get("identifier") for r in rels]:
                errors.append(f"connection relationshipRef '{ref}' not found")
    # coverage warning
    used = set()
    for v in root.iter():
        if local(v.tag) == "node" and v.get("elementRef"):
            used.add(v.get("elementRef"))
    for eid in elements:
        if eid not in used:
            warnings.append(f"element {eid} not used in any view")
    return errors, warnings

def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    strict = "--strict" in sys.argv
    if not args:
        print("usage: python3 validate.py [--strict] model.xml")
        sys.exit(2)
    path = args[0]
    errors, warnings = validate(path, strict)
    tree = ET.parse(path)
    n_el = sum(1 for e in tree.getroot().iter() if local(e.tag) == "element")
    n_rel = sum(1 for e in tree.getroot().iter() if local(e.tag) == "relationship")
    n_view = sum(1 for e in tree.getroot().iter() if local(e.tag) == "view")
    for w in warnings:
        print(f"WARN: {w}")
    if errors:
        for e in errors:
            print(f"ERROR: {e}")
        sys.exit(1)
    if strict and warnings:
        print("STRICT: warnings treated as errors")
        sys.exit(1)
    print(f"OK: {n_el} elements, {n_rel} relationships, {n_view} views in {path}")

if __name__ == "__main__":
    main()
