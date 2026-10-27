#!/usr/bin/env python3
"""hat_interface: render the HAT interface v2 spec tables from interfaces/hat-v2/, or check that they are current.

The contact list, pogo field, contact ratings, contact margins and power roles of
docs/specs/interface-v2.md sit between <!-- generated:<block>:start --> and
<!-- generated:<block>:end --> markers and are generated from interfaces/hat-v2/contacts.toml
and power.toml, after validating both against their schemas and against each other.
"""
import argparse
import datetime
import json
import pathlib
import sys
import tomllib
from fractions import Fraction

SUMMARY = "render the HAT interface v2 spec tables from interfaces/hat-v2/, or check that they are current"
IFACE = pathlib.Path("interfaces/hat-v2")
SPEC = pathlib.Path("docs/specs/interface-v2.md")
BLOCKS = ("contact-list", "power-ratings", "power-margins", "power-roles", "pogo-field")
FIX = "python3 tools/hat_interface.py render"
# BRD-049: continuous use at or below 70 % of a contact's rating, the fault ceiling at or below 100 %.
CONTINUOUS_LIMIT, CEILING_LIMIT = Fraction(70), Fraction(100)


def error(code, message, hint, fix=FIX):
    return {"code": code, "message": message, "hint": hint, "fix": fix}


# ---- data -------------------------------------------------------------------------------------------------------


def load(iface):
    """The interface's data documents as {"contacts": …, "power": …}."""
    return {name: tomllib.loads((iface / f"{name}.toml").read_text()) for name in ("contacts", "power")}


def schema_errors(model, iface):
    import jsonschema

    out = []
    for name, doc in model.items():
        schema = json.loads((iface / f"{name}.schema.json").read_text())
        for e in jsonschema.Draft202012Validator(schema).iter_errors(doc):
            where = "/".join(str(p) for p in e.absolute_path) or "(document)"
            out.append(error("hat-interface.schema", f"{name}.toml {where}: {e.message}",
                             f"fix the data in {iface / name}.toml to match {name}.schema.json", f"$EDITOR {iface / name}.toml"))
    return out


def field_contacts(contacts):
    return [c for row in contacts["field"]["row"] for c in row["contacts"]]


def margins(rail, contact):
    """Per-contact current and percent of the contact's rating: continuous, one open, ceiling, ceiling one open."""
    n, rating = contact["contacts_per_rail"], Fraction(str(contact["rating_a"]))
    out = {}
    for key, total in (("continuous", rail["rating_a"]), ("ceiling", rail["fault_ceiling_a"])):
        total = Fraction(str(total))
        out[key] = (total / n, total / n / rating * 100)
        if contact["one_contact_open"] and n > 1:
            out[key + "_open"] = (total / (n - 1), total / (n - 1) / rating * 100)
    return out


def consistency(model):
    """Errors where the data disagrees with itself: field shape, pins, rail counts and the BRD-049 margins."""
    contacts, power = model["contacts"], model["power"]
    out, field = [], field_contacts(contacts)
    for row in contacts["field"]["row"]:
        if len(row["contacts"]) != contacts["field"]["columns"]:
            out.append(error("hat-interface.field-shape", f"row {row['name']} has {len(row['contacts'])} contacts, not {contacts['field']['columns']}",
                             "every field row has one contact per column"))
    pins = {p for f in contacts["function"] for p in f["pins"]}
    for name in sorted(set(field) - pins):
        out.append(error("hat-interface.unknown-pin", f"field contact {name} belongs to no function", "add it to a function's pins or fix the field"))
    for name in sorted(pins - set(field)):
        out.append(error("hat-interface.pin-count", f"function pin {name} is not in the field", "place it in the field or remove it"))
    rails = {r["name"]: r for r in power["rail"]}
    for name, rail in rails.items():
        placed = field.count(name)
        if (name == "VBUS" and placed != rail["pogo_contacts"]) or placed < rail["pogo_contacts"]:
            out.append(error("hat-interface.pin-count", f"power.toml gives {rail['pogo_contacts']} pogo contacts to {name}; the field has {placed}",
                             "the rail's pogo_contacts and the field must agree"))
    vbus = rails.get("VBUS")
    for contact in power["contact"] if vbus else []:
        for key, (_, pct) in margins(vbus, contact).items():
            limit = CEILING_LIMIT if key.startswith("ceiling") else CONTINUOUS_LIMIT
            if pct > limit:
                out.append(error("hat-interface.margin", f"{contact['name']}: {key} at {float(pct):.0f} % of its rating, above {limit} % (BRD-049)",
                                 "add contacts or choose a contact with a higher rating"))
    return out


# ---- rendering ----------------------------------------------------------------------------------------------------


def num(x):
    return str(x) if isinstance(x, int) else repr(x)


def half_up(x, places):
    scale = 10 ** places
    v = (Fraction(x) * scale + Fraction(1, 2)).__floor__()
    return f"{v / scale:.{places}f}" if places else str(v)


def table(header, rows):
    lines = ["| " + " | ".join(header) + " |", "|" + "---|" * len(header)]
    return "\n".join(lines + ["|" + "".join(f" {c} |" if c else " |" for c in r) for r in rows])


def contact_list(contacts):
    field, rows = field_contacts(contacts), []
    for f in contacts["function"]:
        signals = ", ".join(f"`{s['name']}`" + (f" ({s['direction']})" if "direction" in s else "") for s in f["signals"])
        count = sum(field.count(p) for p in f["pins"])
        pairs = f.get("pairs")
        cell = f"{count} ({pairs} pair{'s' if pairs > 1 else ''})" if pairs else str(count)
        rows.append([f["name"], signals, cell, f.get("electrical_class", "—"), f.get("notes", "")])
    rows.append(["**Total**", "", f"**{len(field)}**", "", ""])
    return table(["Function", "Signals (direction)", "Pogo contacts", "Electrical class", "Notes"], rows)


def pogo_field(contacts):
    cols = contacts["field"]["columns"]
    rows = [[f"**Row {r['name']}**", *r["contacts"]] for r in contacts["field"]["row"]]
    return table(["Col", *map(str, range(1, cols + 1))], rows)


def with_extra(n, extra):
    return f"{n} (+ {extra})" if extra else str(n)


def power_ratings(power):
    rows = []
    for r in power["rail"]:
        rating = f"{num(r['rating_a'])} A" + (f" {r['rating_note']}" if "rating_note" in r else "")
        rows.append([f"`{r['name']}`" + (f" ({r['role']})" if "role" in r else ""), r.get("voltage", "—"), r["direction"], rating,
                     f"{num(r['fault_ceiling_a'])} A", with_extra(r["pogo_contacts"], r.get("pogo_contacts_extra")),
                     with_extra(r["t1_flat_cable_contacts"], r.get("t1_flat_cable_contacts_extra")) if "t1_flat_cable_contacts" in r else "—"])
    header = ["Rail", "Voltage", "Direction", "Interface rating (continuous)", "Interface fault ceiling", "Pogo contacts", "DF40 contacts (T1)"]
    return table(header, rows)


def power_margins(power):
    vbus, rows = next(r for r in power["rail"] if r["name"] == "VBUS"), []
    for c in power["contact"]:
        m = margins(vbus, c)
        cell = (lambda k: f"{half_up(m[k][0], 2)} A ({half_up(m[k][1], 0)} %)" if k in m else "—")
        rating = f"{num(c['rating_a'])} A" + (f" ({c['rating_note']})" if "rating_note" in c else "")
        rows.append([c["name"], rating, c["rails"], cell("continuous"), cell("continuous_open"), cell("ceiling"), cell("ceiling_open")])
    header = ["Contact", "Rating", "Rail", "Continuous per contact", "With one contact open", "At the fault ceiling", "Ceiling, one contact open"]
    return table(header, rows)


def power_roles(power):
    return table(["HAT role", "What it does", "Negotiation"], [[f"**{r['name']}**", r["does"], r["negotiation"]] for r in power["role"]])


def render_blocks(model):
    c, p = model["contacts"], model["power"]
    return {"contact-list": contact_list(c), "power-ratings": power_ratings(p), "power-margins": power_margins(p),
            "power-roles": power_roles(p), "pogo-field": pogo_field(c)}


def markers(block):
    return f"<!-- generated:{block}:start -->", f"<!-- generated:{block}:end -->"


def splice(text, blocks):
    """(new text, {block: current?}, errors): each block's content replaced between its markers."""
    status, errs = {}, []
    for block, body in blocks.items():
        start, end = markers(block)
        i, j = text.find(start), text.find(end)
        if i < 0 or j < i:
            errs.append(error("hat-interface.markers", f"{SPEC} has no {start} … {end} pair",
                              f"put the markers around the {block} table", f"$EDITOR {SPEC}"))
            continue
        new = f"{start}\n\n{body}\n\n"
        status[block] = text[i:j] == new
        text = text[:i] + new + text[j:]
    return text, status, errs


# ---- command line -------------------------------------------------------------------------------------------------


def report(root, status, errs):
    results = [{"id": b, "verdict": "pass" if ok else "fail",
                "message": "current" if ok else f"not current: run {FIX}"} for b, ok in status.items()]
    results += [{"id": e["code"], "rule": e["code"], "verdict": "fail", "message": e["message"]} for e in errs]
    return {"schema": "opendap.check-result/v1", "tool": {"name": "hat_interface"},
            "subject": {"repo": "hat-standard", "path": str(SPEC)},
            "generated": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "results": results}


def parser():
    p = argparse.ArgumentParser(prog="hat_interface", description=f"hat_interface: {SUMMARY}",
                                formatter_class=argparse.RawDescriptionHelpFormatter, epilog="""examples:
  python3 tools/hat_interface.py render              write the generated tables into the spec
  python3 tools/hat_interface.py render --check      exit 1 when a table is not current (pre-commit)
  python3 tools/hat_interface.py render --check --json   the same as an opendap.check-result/v1 document
exit status: 0 current or written, 1 a table is not current or the data is invalid, 2 usage error""")
    sub = p.add_subparsers(dest="verb", required=True, metavar="VERB")
    r = sub.add_parser("render", help="render the spec tables from the data (validates the data first)")
    r.add_argument("--check", action="store_true", help="write nothing; exit 1 when a table is not current")
    r.add_argument("--dry-run", action="store_true", help="write nothing; report what would change, exit 0")
    r.add_argument("--json", action="store_true", help="print an opendap.check-result/v1 document on stdout")
    r.add_argument("--root", type=pathlib.Path, default=pathlib.Path(__file__).resolve().parents[1], help="repository root (default: this script's)")
    return p


def main(argv=None):
    args = parser().parse_args(argv)
    root, iface, spec = args.root, args.root / IFACE, args.root / SPEC
    model = load(iface)
    errs = schema_errors(model, iface)
    errs += [] if errs else consistency(model)
    status = {}
    if not errs:
        text = spec.read_text()
        new, status, errs = splice(text, render_blocks(model))
        if not errs and not args.check and not args.dry_run and new != text:
            spec.write_text(new)
            status = dict.fromkeys(status, True)
    for e in errs:
        print(f"error[{e['code']}]: {e['message']}\n  hint: {e['hint']}\n  fix: {e['fix']}", file=sys.stderr)
    stale = [b for b, ok in status.items() if not ok]
    for b in stale:
        print(f"{SPEC}: {b} is not current; run {FIX}", file=sys.stderr)
    if args.json:
        print(json.dumps(report(root, status, errs)))
    return 1 if errs or (stale and args.check) else 0


if __name__ == "__main__":
    sys.exit(main())
