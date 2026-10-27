# OpenDAP HAT Standard

The OpenDAP HAT Standard: the interface between the T1 and its HATs, device side and accessory side. A HAT swaps the basic back cover for a HAT case; this standard defines that rear interface (mechanics, pinout, electrical, power and identification over USB), plus reference designs and a compliance kit for accessory developers.

<!-- >>> odapkit sync: managed block from the workspace templates; edit them, not this block -->
Part of [OpenDAP](https://github.com/opendap-project). This repository is Open Source.

Contributor rules (English, confirmed information only, REUSE licensing, the `docs/` layout and its skills): the [contributor guide](https://github.com/opendap-project/.github/blob/main/CONTRIBUTING.md).
<!-- <<< odapkit sync -->

## Working here

- The HAT interface v2 contact, power and pogo-field tables are edited in `interfaces/hat-v2/*.toml`; the spec's tables between `generated` markers are rendered with `python3 tools/hat_interface.py render` and checked in pre-commit. Values are copied from a cited source, never inferred.
- Requirements are edited in `docs/requirements/requirements.toml`; `docs/requirements/README.md` is rendered from it with `odapkit req render` and never edited by hand.
