# OpenDAP HAT Standard

The OpenDAP HAT Standard: the interface between the T1 and its HATs, device side and accessory side. A HAT swaps the basic back cover for a HAT case; this standard defines that rear interface (mechanics, pinout, electrical, power and identification over USB), plus reference designs and a compliance kit for accessory developers.

## Layout

- `interfaces/hat-v2/`: the HAT interface v2 as data: `contacts.toml` (functions, electrical classes, pogo field), `power.toml` (rails, contact ratings, power roles) and the JSON Schemas `opendap.hat-contacts/v1`, `opendap.hat-power/v1` and `opendap.hat-identity/v1` (the identity record's fields). The spec's tables are generated from it.
- `tools/hat_interface.py`: renders those tables into [`docs/specs/interface-v2.md`](docs/specs/interface-v2.md) (`render`), or checks them (`render --check`, `--json`); tested in `tests/`.
- `spec/`
- `reference-designs/`
- `compliance/`
- `export/`
- `docs/`

## License

This repository follows the [REUSE](https://reuse.software) layout: license texts live in `LICENSES/` and `REUSE.toml` maps each path to its license.

- Default: **Creative Commons Attribution-ShareAlike 4.0** (`CC-BY-SA-4.0`)
- `reference-designs/`: **CERN Open Hardware Licence v2 – Weakly Reciprocal** (`CERN-OHL-W-2.0`)
- `compliance/`: **GNU GPL v3.0 or later** (`GPL-3.0-or-later`)
- `export/`: **CERN Open Hardware Licence v2 – Weakly Reciprocal** (`CERN-OHL-W-2.0`)
- `docs/`: **Creative Commons Attribution-ShareAlike 4.0** (`CC-BY-SA-4.0`)
- `tools/`, `tests/`: **GNU GPL v3.0 or later** (`GPL-3.0-or-later`)
- `interfaces/**/*.schema.json`: **Mozilla Public License 2.0** (`MPL-2.0`); the interface data itself follows the default

Copyright © 2026 The OpenDAP Project.
