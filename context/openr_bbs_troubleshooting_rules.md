# OPEN-R Troubleshooting Rules

Compact rules for retrieval and expert-system prompting. Each rule is backed by specific BBS message IDs.

## SDK stick fails to boot

- Symptom: AIBO powers off, hangs, or seems dead when booting an SDK Memory Stick.
- Checks:
  - Verify flash ROM / firmware level.
  - Verify the Memory Stick has the full expected file layout.
  - Check whether the base image is WCONSOLE instead of WLAN or BASIC.
  - Check battery level and try a known-good stick.
  - Suspect hardware only after the above pass.
- Source messages: Msg 714, Msg 716, Msg 722

## Service or subject NOT FOUND

- Symptom: Runtime reports `... NOT FOUND` while connecting objects or services.
- Checks:
  - Inspect `OBJECTS.CFG` and `CONNECT.CFG`.
  - Confirm generated stubs and names match exactly.
  - Verify `REGISTER_ALL_ENTRY` runs in `DoInit()`.
- Source messages: Msg 683, Msg 686, Msg 690

## selector out of range

- Symptom: Aperios reports `selector out of range` or `intraDeliver selector is out of range`.
- Checks:
  - Inspect selector counts and generated entries.
  - Check `stub.cfg` and object registration.
  - Treat it as wiring/glue failure before suspecting application logic.
- Source messages: Msg 336

## sTIMEOUT / error 28

- Symptom: Logs mention `error 28` or `sTIMEOUT` during object lifecycle.
- Checks:
  - Check whether `DoStart()` or `DoStop()` blocks or never returns.
  - Move long-running work out of lifecycle callbacks.
- Source messages: Msg 671, Msg 704

## All joints move wildly when commanding one joint

- Symptom: Setting one joint causes unrelated joints to move to extreme positions.
- Checks:
  - Verify the joint command vector length.
  - If the vector declares all joints, populate all joint values before sending it.
- Source messages: Msg 719, Msg 723

## WLAN config accepted in peer-to-peer but hangs via access point

- Symptom: AIBO boots in ad-hoc mode but hangs or fails with AP mode.
- Checks:
  - Inspect `WLANCONF.TXT` formatting carefully.
  - Do not include spaces around `KEY=VALUE` assignments.
- Source messages: Msg 543, Msg 552

## Current OPEN-R stack needs static IP

- Symptom: User wants DHCP or dynamic assignment on older OPEN-R LAN support.
- Checks:
  - Assume a known static IP is required unless using a different software stack.
  - Do not infer DHCP support from newer commercial AIBO products.
- Source messages: Msg 693, Msg 700, Msg 701

## UDP send path stalls or reports busy

- Symptom: First UDP packet never completes or next packet reports `UDP_CONNECTION_BUSY`.
- Checks:
  - Treat send as asynchronous and verify completion before the next packet.
  - Check callback flow and pacing.
- Source messages: Msg 402

## Image transfer or large payload misbehaves

- Symptom: Passing camera/image arrays between objects leads to failures or unexpected copies.
- Checks:
  - Remember `SetData(ptr, size)` copies to shared memory.
  - Check `OStatus` return codes.
  - Use explicit shared-memory handling if zero-copy semantics are required.
- Source messages: Msg 696, Msg 697

## R-CODE feature seems missing on ERS-7M3

- Symptom: R-CODE WLAN or support assumptions fail on ERS-7M3.
- Checks:
  - Verify the exact R-CODE version and model support window.
  - Older R-CODE Ver2 did not support ERS-7M3 WLAN at first.
- Source messages: Msg 1944, Msg 1945, Msg 1954, Msg 1955
