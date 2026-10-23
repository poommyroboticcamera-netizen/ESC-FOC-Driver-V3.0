**Language:** English · [ไทย](README_TH.md)

This repository currently publishes firmware and hardware files. Use the links above to switch the project documentation language.

<div align="center">

<a href="hardware/README.md"><img src="docs/assets/esc-foc-v3-board.png" alt="ESC FOC Driver V3.0 PCB" width="70%"></a>

# ESC-FOC-Driver-V3.0

**STM32F405 + DRV8302 three-phase BLDC/PMSM motor driver with custom VESC firmware, ADC test results and SolidWorks case model**

![MCU](https://img.shields.io/badge/MCU-STM32F405RGT6-0B1220?style=for-the-badge&logo=stmicroelectronics&logoColor=38BDF8)
![Driver](https://img.shields.io/badge/Gate_Driver-DRV8302-2563EB?style=for-the-badge)
![Firmware](https://img.shields.io/badge/Firmware-VESC_6.00-7C3AED?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Engineering_Prototype-DC2626?style=for-the-badge)

[Hardware & Schematic](hardware/README.md) · [Firmware](#firmware-included-in-the-project) · [Test results](#latest-test-status) · [3D & Enclosure](#3d-model-and-case) · [Get started](#start-using-on-the-bench)

</div>

---

## Project overview

Three-phase motor control board for developing and testing BLDC/PMSM using **STM32F405RGT6** together with **DRV8302** and firmware adjusted from VESC 6.00 for the circuit. `vesc4_12B02` The project combines schematic, firmware with flash, source snapshots, board inspection results, and mechanical assembly drawings in one place.

This document is formatted after [ESC-FOC-Drive-V02](https://github.com/poommyroboticcamera-netizen/ESC-FOC-Drive-V02) The firmware and pin mapping files in this repo are specific to the DRV8302 B02 board.

> [!IMPORTANT]
> **Status as of October 19, 2026: In the process of bringing-up and checking for ADC problems** The latest model returned to the board and read via USB is `DRV8302_B02_R2` Read FOC status and `FAULT_CODE_NONE` Yes, but ADC oscillations have been found and motor driving has not yet been confirmed. Do not interpret the idle status without fault as having passed Motor Detection or being ready to drive the load.

## Hardware overview

| list | details |
|:--|:--|
| MCU | STM32F405RGT6, crystal 8 MHz |
| Gate driver | Texas Instruments DRV8302 |
| Power stage | Three-phase MOSFET bridge |
| Current sense | 2 shunts, 0.5 mΩ; amplifier gain 10 V/V |
| Current ADC | BR_SO1 → PB1 / ADC9, BR_SO2 → PB0 / ADC8 |
| Bus / phase divider | 39 kΩ / 2.2 kΩ according to hardware profile |
| FET temperature | NTC 10 kΩ B3450 with resistor 10 kΩ |
| Firmware interface | VESC Tool via USB; SWD for flash and debug |
| Schematic | [SCH_SchematicV01_2_2026-10-19.pdf](hardware/schematic/SCH_SchematicV01_2_2026-10-19.pdf) |

The above values ​​are circuit data and configuration To start testing There is no continuous power rating or confirmed thermal test results yet.

## Firmware included in the project

| Model/file set | used for | status |
|:--|:--|:--|
| [B02 initial package](output/firmware/DRV8302_B02/) | Firmware, factory HEX includes bootloader, BIN, ELF, map and source. | Keep the original set for reference. |
| [B02 R2](output/firmware/DRV8302_B02_R2/) | ADC prescaler /4, 21 MHz | Return to board and check latest USB; The ADC problem still exists. |
| [R3](output/firmware/DRV8302_B02_R3/) | Experimental acquisition time | Eliminated: ADC rank timing does not match. |
| [R4](output/firmware/DRV8302_B02_R4/) | Adjust ADC rank timing to match. | Still found peak |
| [R5](output/firmware/DRV8302_B02_R5/) | Experiment with ADC 10.5 MHz | Still found peak |
| [R6](output/firmware/DRV8302_B02_R6/) | Currents first / half-DMA interrupt | Still found peak |

**B02 initial package is the initial flash preparation package, not R2** Documents and checksums within the package are stored as of creation time. Read the latest status section. [ADC comparison results](output/firmware/diagnostics/ADC_COMPARISON_TH.md) and [recovery verification](output/firmware/diagnostics/recovery_verified.json)

- [B02 First Flash Guide](output/firmware/DRV8302_B02/README_TH.md)
- [Source snapshot includes diagnostic fixes](firmware/source/vesc-6.00-b02-diagnostic-source.zip)
- [How to prepare source and build](firmware/README.md)
- [SHA-256 of the files in the project](SHA256SUMS.txt)

## Default value for commissioning

| fee | Default Configuration of B02 |
|:--|:--|
| Motor current | +5 / -2 A |
| Input current | +2 / -0.5 A |
| Absolute current fault | 10 A |
| Voltage limits | 10–30 V |
| Battery cut start / end | 11 / 10 V |
| Maximum Duty | 20% |
| Speed limit | ±10,000 ERPM |
| Power limit | +50 / -10 W |
| FET temperature limit | Start reducing at 60 °C, finish at 75 °C |
| External app | APP_NONE |

Table values ​​are software limits in the header, not hardware and configuration limits. that are recorded on the board or written from the VESC Tool can override the default values. Must read back before testing every time.

## Latest test status

| section | Results with evidence |
|:--|:--|
| Flash / read-back | Return R2 and verify successfully. |
| USB communication | Read the name `DRV8302_B02_R2` and firmware 6.00 |
| Motor configuration | Read back as FOC |
| Idle fault | `FAULT_CODE_NONE` At the post-recovery examination |
| Bus voltage | Approximately 24 V according to telemetry |
| ADC current sampling | It still oscillates and peaks above the fault threshold when converted to the firmware scale. |
| Independent ADC | Oscillations were also observed at SO1, SO2 and VREFINT even without DMA/USB/PWM. |
| Motor Detection / Load driving | Not yet confirmed |

Data from ADC converted to amperes. **This is not the actual current measured with the current probe** VDDA/VSSA, reference, decoupling, and additional signal paths must be checked. Fault history during boot includes DRV and UNDER_VOLTAGE. which still needs to find the cause

read [First round inspection report](output/firmware/diagnostics/RESULT_TH.md), [Comparison results and independent ADC](output/firmware/diagnostics/ADC_COMPARISON_TH.md) and [All raw data](output/firmware/diagnostics/)

## 3D model and case

<div align="center">
<img src="docs/assets/esc-foc-v3-enclosure.png" alt="ESC FOC Driver V3.0 enclosure assembly" width="80%">
</div>

Files from the project's 3D folder are located in [hardware/mechanical](hardware/mechanical/):

- [caseV03.SLDASM](hardware/mechanical/caseV03.SLDASM) — assembly of the case
- [pro.SLDASM](hardware/mechanical/pro.SLDASM) — another assembly of the project
- parts file `.SLDPRT`, exchange form `.STEP` and mesh `.STL` contained in the source folder

Using SolidWorks, open the assembly and search for references from the same folder. If the assembly refers to external parts not available in this kit, additional files must be linked. Haven't inspected the rebuild assembly or certified the fit of the actual piece.

## Start using on the bench

1. Download or clone the project and read. [Hardware manual](hardware/README.md) and [Test limitations](output/firmware/diagnostics/ADC_COMPARISON_TH.md)
2. Disconnect the motor and command cable. Check for short circuits and the 3.3 V rail before using a current limiting supply.
3. Connect ST-Link via SWDIO / SWCLK / GND / NRST / VTref according to the manual. Do not enter 5 V into the 3.3 V pin.
4. Select the correct firmware revision: factory HEX of B02 contains the bootloader; HEX of R2–R6 is the firmware file for each experimental version.
5. Read the flash instructions before proceeding. The first install script has a full-chip erase which erases all original configuration.
6. After flashing, read back hardware name, motor/app configuration, fault, bus voltage and current offset with VESC Tool that supports firmware 6.00.
7. Correct and verify ADC signals including gate PWM/dead time before doing Motor Detection or ordering rotation.

> [!WARNING]
> The board is still under development. Use a current-limiting supply and prepare to cut power immediately. A typical bench supply may not be able to receive power from regenerative braking. The regen limit in the firmware does not guarantee bus overvoltage protection.

## Project structure

```text
├── hardware/
│   ├── schematic/          # Schematic PDF
│   └── mechanical/         # SolidWorks, STEP, STL
├── firmware/
│   └── source/             # VESC source snapshot + custom profiles
├── output/firmware/
│   ├── DRV8302_B02/        # Initial firmware / bootloader package
│   ├── DRV8302_B02_R2/     # Revision most recently checked over USB
│   ├── DRV8302_B02_R3–R6/  # Experimental revisions (separate directories)
│   └── diagnostics/        # test reports and data
├── tools/                  # Build and diagnostic scripts
├── docs/assets/            # board and enclosure images
└── SHA256SUMS.txt
```

## Source and usage rights

VESC firmware reference [vedderb/bldc commit 4b822f0](https://github.com/vedderb/bldc/tree/4b822f0f944918957c55391ca0672925153f3fde) and [VESC bootloader](https://github.com/vedderb/bldc-bootloader) By storing the bootloader commit in [bootloader_commit.txt](output/firmware/DRV8302_B02/bootloader_commit.txt) VESC firmware and related modifications apply. GPL-3.0-or-later according to the original file header The library maintains the license for each section in the source archive.

The hardware, mechanical, and image files in this repository have not yet been licensed.

**Developed by [poommyroboticcamera-netizen](https://github.com/poommyroboticcamera-netizen)**
