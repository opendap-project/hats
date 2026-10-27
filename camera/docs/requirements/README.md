# Camera HAT requirements

Requirements for this project.

| ID | Requirement | Priority | Status |
|---|---|---|---|
| CAM-001 | This HAT is a complete project: hardware, case, firmware, software, Blackbird OS package and its own tooling. | must | Confirmed |
| CAM-002 | Its Blackbird OS software shall be a custom implementation built on popular open-source software for its domain, optimized for this HAT and the board. | must | Confirmed |
| CAM-003 | It shall mount through the HAT Case Standard. | must | Confirmed |
| CAM-004 | It may include on-board AI features. | should | Draft |
| CAM-005 | The HAT shall turn the device into an action camera. | must | Confirmed |
| CAM-006 | The HAT shall reach the device only through its USB port and meet the minimum conditions of [hat-standard interface v2](https://github.com/opendap-project/hat-standard/blob/main/docs/specs/interface-v2.md) (HCS-027 to HCS-031): standard USB classes, the identity capability, USB PD power rules, firmware recoverable over USB. | must | Draft |
| CAM-007 | The HAT shall carry its own image processing and present video as UVC: an ISP for uncompressed video within a USB 3 Gen 1 link, and an encoder for modes beyond it. On-board AI (CAM-004) runs on the HAT. | must | Draft |
| CAM-008 | The HAT shall record video at 3840 × 2160 and at least 60 fps, in H.265 and H.264, to storage on the HAT. | must | Draft |
| CAM-009 | While recording, the HAT shall send the device a live preview as uncompressed UVC video, with its audio and stabilisation data, so the device is its viewfinder and controller. | must | Draft |
| CAM-010 | The HAT shall carry its own gyroscope, sampled at 1 kHz or more and time-stamped against each frame's exposure, for in-camera stabilisation; every recording shall carry the gyro track and the lens profile in a documented open format. | must | Draft |
| CAM-011 | The HAT shall record stereo audio from its own microphones as PCM in the video file, with wind-noise detection, and present it to the device as USB Audio Class 2. | must | Draft |
| CAM-012 | The camera SoC and image sensor shall have public data sheets or mainline Linux drivers; the ISP and encoder shall be usable without an NDA-only SDK; every compromise (binary firmware, sensor documentation) shall be documented (HCS-005). | must | Draft |
| CAM-013 | The HAT shall run its highest video mode from the device's 5 V supply within the power it declares, and shall show when the device cannot supply it (T1-045). | must | Draft |
| CAM-014 | The HAT shall keep every touchable surface within IEC 62368-1 TS1 limits, shed its heat through its own case without raising the device's battery temperature, and step down its video mode visibly, never silently. | must | Draft |
| CAM-015 | Recording indicators, visible from the front and the back, shall be wired to the image sensor and microphone power, so they cannot be off while the HAT records. | must | Draft |
| CAM-016 | The HAT shall contain no radio transmitter; wireless sharing goes through the device. | must | Draft |
| CAM-017 | The HAT should be sealed to IP68 on its own, and a housing accessory should let the device and the HAT go under water. | should | Draft |
| CAM-018 | The HAT should carry standard mounts: two-prong action-camera fingers and a 1/4"-20 thread. | should | Draft |
| CAM-019 | The lens should be user-swappable (M12), with published lens profiles for every offered lens. | should | Draft |
| CAM-020 | The HAT should carry its own battery as a USB PD dual-role HAT, to extend recording and to record detached from the device. | should | Draft |

## Context

- CAM-008 to CAM-020: recorded as **Draft**; CAM-008 to CAM-016 are must, CAM-017 to CAM-020 should.
- CAM-008, CAM-009: 4K60 H.265 at 100–150 Mb/s uses 3–5 % of the USB 3 Gen 1 isochronous ceiling (3145.7 Mb/s, USB 3.2 §8.12.6), while uncompressed 4K60 NV12 (5972 Mb/s) and raw 4K60 Bayer RAW10 (4977 Mb/s) do not fit. A 720p30 NV12 preview is 332 Mb/s, about 10.5 % of that ceiling. Recording on the HAT keeps the master file next to the encoder, independent of the USB link and of the device's state.
- CAM-010: a gyro track and lens profile in an open format let full-strength stabilisation run afterwards with open tools such as Gyroflow (GPL-3.0), which reads CAMM and `.gcsv` input.
- CAM-012: RFC 0014 removed CSI-2 from the HAT bus, so image processing stays on the HAT (CAM-007).
- CAM-013, CAM-014: interface v2 gives a HAT 5 V at up to 1.5 A from the T1. The HAT's power at 4K60 and the heat its case can shed are **UNVERIFIED** until they are measured on the first prototype; the TS1 touch-temperature row of IEC 62368-1 is **UNVERIFIED**.
- CAM-016: with no transmitter on the HAT, wireless sharing uses the device's own radio and certified antenna.
- CAM-005: reworded without a product name; the intent is unchanged.
