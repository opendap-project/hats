# Reference designs

Reference designs for both sides of the HAT Case: electronics in [KiCad](https://www.kicad.org) 10 and mechanics in [FreeCAD](https://www.freecad.org) 1.1.

## Layout

- `<design>/hardware/`: electronics, following the same conventions as the `hardware/` folder of any HAT repository.
- `<design>/case/`: mechanics, following the same conventions as the `case/` folder of any HAT repository.

## Designs

| Design | Folder | What it is | Interface | Status |
|---|---|---|---|---|
| USB-C port HAT | `usb-c-port/` (no files yet) | A HAT whose only function is one USB-C receptacle on its outside: it exposes the device's HAT USB port to standard USB-C devices and chargers, and is the reference HAT for makers and the path to prototype with any USB-C board | Interface v2 pads (all 20 contacts). A USB 3 hub carries the OpenDAP HAT identity capability (interface v2 §7) and feeds one downstream USB-C receptacle: USB 3 Gen 1 and USB 2.0, reversible (`CC1`, `CC2` and a SuperSpeed orientation mux). Its own USB PD controller runs that receptacle. Dual-role HAT (§5.2): it sinks from the device and sources what is plugged in, within the device's offer (T1: 5 V, up to 1.5 A, less the HAT's own draw); with a charger plugged in, it becomes a USB PD source to the device at the voltages the device accepts (T1: 5 V). The device stays USB host: the receptacle is a host port and cannot connect the device to a computer. Firmware of every programmable chip recoverable over USB (§8). Receptacle `VBUS` and `CC` protected as an external USB-C port | Proposed ([RFC 0015](https://github.com/opendap-project/rfcs/blob/main/text/0015-hat-connector-pogo-field-and-usb-c-port-hat.md)) |
