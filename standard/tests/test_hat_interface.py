"""tools/hat_interface.py: the HAT interface v2 data, its schemas and the spec tables generated from it."""
import json
import pathlib
import shutil
import subprocess
import sys
import tomllib

import jsonschema
import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import hat_interface as hi  # noqa: E402

IFACE = ROOT / "interfaces" / "hat-v2"
GOLDEN = ROOT / "tests" / "golden"
FIX = ROOT / "tests" / "fixtures"
TOOL = ROOT / "tools" / "hat_interface.py"
BLOCKS = ["contact-list", "power-ratings", "power-margins", "power-roles", "pogo-field"]


def validator(name):
    schema = json.loads((IFACE / f"{name}.schema.json").read_text())
    jsonschema.Draft202012Validator.check_schema(schema)
    return jsonschema.Draft202012Validator(schema)


def data(name):
    return tomllib.loads((IFACE / f"{name}.toml").read_text())


@pytest.mark.parametrize("name", ["contacts", "power"])
def test_data_is_valid(name):
    assert list(validator(name).iter_errors(data(name))) == []


@pytest.mark.parametrize("path", sorted((FIX / "identity" / "good").glob("*.json")), ids=lambda p: p.stem)
def test_identity_good(path):
    assert list(validator("identity").iter_errors(json.loads(path.read_text()))) == []


@pytest.mark.parametrize("path", sorted((FIX / "identity" / "bad").glob("*.json")), ids=lambda p: p.stem)
def test_identity_bad(path):
    assert list(validator("identity").iter_errors(json.loads(path.read_text())))


@pytest.mark.parametrize("block", BLOCKS)
def test_render_matches_golden(block):
    assert hi.render_blocks(hi.load(IFACE))[block] == (GOLDEN / f"{block}.golden").read_text().rstrip("\n")


def test_field_holds_every_function_pin():
    contacts = data("contacts")
    field = [c for row in contacts["field"]["row"] for c in row["contacts"]]
    assert all(len(row["contacts"]) == contacts["field"]["columns"] for row in contacts["field"]["row"])
    names = [p for f in contacts["function"] for p in f["pins"]]
    assert sorted(set(field)) == sorted(names)
    assert len(field) == 20


def test_power_rails_match_the_field():
    field = [c for row in data("contacts")["field"]["row"] for c in row["contacts"]]
    rails = {r["name"]: r for r in data("power")["rail"]}
    assert rails["VBUS"]["pogo_contacts"] == field.count("VBUS")
    assert rails["GND"]["pogo_contacts"] + 5 == field.count("GND")


def test_consistency_errors_name_the_problem():
    model = hi.load(IFACE)
    model["contacts"]["field"]["row"][1]["contacts"][0] = "GND"
    assert any(e["code"] == "hat-interface.pin-count" for e in hi.consistency(model))


def run(*args):
    return subprocess.run([sys.executable, str(TOOL), *args], capture_output=True, text=True)


@pytest.fixture
def repo(tmp_path):
    for sub in ("interfaces", "docs/specs"):
        shutil.copytree(ROOT / sub, tmp_path / sub)
    return tmp_path


def test_spec_is_current():
    r = run("render", "--check", "--json", "--root", str(ROOT))
    assert r.returncode == 0, r.stdout + r.stderr
    doc = json.loads(r.stdout)
    assert doc["schema"] == "opendap.check-result/v1"
    assert {x["verdict"] for x in doc["results"]} == {"pass"}


def test_check_fails_on_a_stale_spec(repo):
    spec = repo / "docs/specs/interface-v2.md"
    spec.write_text(spec.read_text().replace("| **Row B** | VBUS |", "| **Row B** | GND |"))
    r = run("render", "--check", "--json", "--root", str(repo))
    assert r.returncode == 1
    failed = [x for x in json.loads(r.stdout)["results"] if x["verdict"] == "fail"]
    assert [x["id"] for x in failed] == ["pogo-field"]


def test_render_repairs_and_dry_run_does_not(repo):
    spec = repo / "docs/specs/interface-v2.md"
    stale = spec.read_text().replace("| 4 (2 pairs) |", "| 5 (2 pairs) |")
    spec.write_text(stale)
    assert run("render", "--dry-run", "--root", str(repo)).returncode == 0
    assert spec.read_text() == stale
    assert run("render", "--root", str(repo)).returncode == 0
    assert run("render", "--check", "--root", str(repo)).returncode == 0


def test_invalid_data_is_a_failure_with_a_code(repo):
    p = repo / "interfaces/hat-v2/power.toml"
    p.write_text(p.read_text().replace('id = "sink"', 'id = "charger"'))
    r = run("render", "--check", "--root", str(repo))
    assert r.returncode == 1
    assert "hat-interface.schema" in r.stderr


def test_missing_markers_are_reported(repo):
    spec = repo / "docs/specs/interface-v2.md"
    spec.write_text(spec.read_text().replace("<!-- generated:pogo-field:end -->", ""))
    r = run("render", "--check", "--root", str(repo))
    assert r.returncode == 1
    assert "hat-interface.markers" in r.stderr


def test_usage():
    assert run("--help").returncode == 0
    assert run("render", "--bogus").returncode == 2
    assert run("explode").returncode == 2
