# HATs

The OpenDAP HAT Standard and the OpenDAP HATs, in one repository:

| Folder | Content |
| --- | --- |
| [`standard/`](standard/README.md) | The OpenDAP HAT Standard: the interface between the T1 and its HATs (mechanics, pinout, electrical, power, identification over USB), reference designs and a compliance kit |
| [`radio/`](radio/README.md) | Radio HAT: software-defined radio based on HackRF Pro |
| [`camera/`](camera/README.md) | Camera HAT: action camera |
| [`outdoor/`](outdoor/README.md) | Outdoor HAT: satellite messaging with SOS, multi-band GNSS, LoRa mesh and its own battery |
| [`concepts/`](concepts/) | HATs without design work yet: their requirements and concept art (NAS, oscilloscope, powerbank, recorder, VNA) |

A concept becomes a folder of its own when its design starts. Each folder keeps its own `docs/` and `REUSE.toml`; the licence texts are in `LICENSES/`. The folders came from the former `hat-standard` and `hat-<name>` repositories with their history ([RFC 0017](https://github.com/opendap-project/rfcs/blob/main/text/0017-naming-and-topology.md)).

## License

This repository follows the [REUSE](https://reuse.software) layout: licence texts in `LICENSES/`, and each folder's `REUSE.toml` maps its paths. Copyright © 2026 The OpenDAP Project.
