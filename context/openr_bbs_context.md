# Sony OPEN-R / Aperios BBS Knowledge Context

## Source

- Parsed from `src/Msgs_1_to_726.html`
- Parsed from `src/Msgs_727_to_1955.html`
- Coverage: 1,955 posts and replies
- Time span: 2002-02-13 to 2006-01-12

## What This Archive Is Good For

This archive is a practical knowledge source for:

- OPEN-R SDK setup and sample-program boot issues
- Aperios / OPEN-R object wiring and selector errors
- TCP/UDP and WLAN configuration on AIBO
- Motion control, joint command semantics, and timing
- Vision pipeline basics: camera access, YCbCr, CMVision, image transfer
- R-CODE capabilities and model-specific limitations
- Real-world debugging patterns from researchers and SDK support

This archive is less reliable for:

- modern tooling
- unavailable download links
- undocumented internals where only community guesses are given

When answers conflict, prefer:

1. `openrsupport@(Administrator)` / `AIBO SDE Support`
2. repeated community guidance that appears in multiple threads
3. isolated community speculation last

## Agent Use Guidance

When using this context in an expert system, assume:

- OPEN-R sits on top of Aperios and exposes the primary supported programming model.
- Many failures are integration failures, not algorithm failures: bad `stub.cfg`, missing registration, wrong Memory Stick layout, unsupported base software, outdated flash ROM, or model/version mismatch.
- AIBO behavior is strongly model-specific, especially around ERS-210/220/7, supercore, WLAN, and R-CODE compatibility.
- Community advice often assumes the stock SDK samples and Sony Memory Stick folder layout.

## Core Domain Model

### OPEN-R vs Aperios

- Aperios is the lower-level operating system; OPEN-R is the supported framework layer above it.
- Direct Aperios usage does exist, but the archive treats it as advanced and relatively underdocumented.
- Errors mentioning `MCOOPMailer`, `intraDeliver`, selectors, or queue limits usually indicate framework wiring or lifecycle mistakes rather than hardware faults.

### Objects, Subjects, Observers, and Selectors

- OPEN-R applications are built from objects connected through subjects/observers and service connections.
- Failures such as `... NOT FOUND`, selector range errors, or send-ready failures usually come from:
  - missing object registration
  - missing `REGISTER_ALL_ENTRY` in `DoInit()`
  - bad or incomplete `stub.cfg`
  - bad `CONNECT.CFG` / `OBJECTS.CFG`
  - mismatched selector counts or entries
- `DoStart()` and `DoStop()` correspond to selectors seen in some timeout logs.

### Frames and Timing

- Motion timing is frame-based.
- Community guidance treats frames as a small time unit used to schedule command progression.
- Fast motion should be implemented by planning target positions over time, not by repeatedly snapping joints to the current sensed position.

## High-Confidence Operational Truths

### Boot and sample-program troubleshooting

- If an SDK Memory Stick works in one AIBO, it should generally work in another of the same compatible class; if not, suspect ROM, battery, stick contents, or hardware.
- Common causes of boot failure:
  - incomplete Memory Stick contents
  - wrong base software variant
  - outdated flash ROM
  - low battery
  - bad Memory Stick
  - hardware issue
- The `WCONSOLE` base software is special-purpose. It is for debug-console access over LAN and may appear to fail to boot if used like a normal sample image.
- First-time SDK users often mistake `WCONSOLE` behavior for a broken stick or broken sample.

Evidence:

- Msg 714: flash ROM version matters for first SDK runs
- Msg 716: `WCONSOLE` requires telnet/debug-console workflow
- Msg 722: typical causes of SDK Memory Stick failure

### Toolchain and SDK installation

- A frequent early failure is simply that `mipsel-linux-g++` or `stubgen2` is not executable or not found at the expected SDK path.
- The archive shows recurring problems with SDK installation permissions, especially when installed as `root`.
- A practical fix from the archive:
  - `chmod -R a+r OPEN_R_SDK`
  - `chmod -R a+x OPEN_R_SDK/OPEN_R/bin`
- The build chain assumes Sony's cross tools and helper binaries are present exactly where sample Makefiles expect them.

Evidence:

- Msg 54: `mipsel-linux-g++` and `stubgen2` not found during sample builds
- Msg 1951: SDK tarball permissions can block header access and execution of `gzcp` / `stubgen2`

### Object lifecycle and timeout debugging

- Timeout `error 28` maps to `sTIMEOUT`.
- If `DoStart()` never returns, timeout errors appear and object startup can cascade into failure.
- Long-running or blocking work should not happen directly inside lifecycle callbacks without careful design.

Evidence:

- Msg 704: admin support explicitly identifies `selector 1` as `DoStart()`, `selector 2` as `DoStop()`, and `error 28` as `sTIMEOUT`

### Selector and queue errors are usually architectural

- `selector out of range` means the object/entry layout does not match what the runtime expects.
- `Exceed max size of queue` means a producer is outpacing a consumer, often because messages are sent faster than they can be drained or a ready/flow-control path is wrong.
- `SendReady failed` and `intraDeliver` errors should trigger inspection of selector definitions, observer readiness, and message backpressure.

Evidence:

- Msg 336: `intraDeliver selector out of range`
- Msg 648: queue overflow with `maxQueueSize=32`

## Topic-Specific Knowledge

### Motion and joint control

- When sending joint commands, make sure the command vector is fully populated for all joints declared in the request.
- A classic bug: trying to move one joint while sending a vector sized for `NUM_JOINTS` but leaving the other entries unset. This can drive unrelated joints to extreme positions.
- Joint speed is controlled indirectly by time progression across frames, not by a dedicated "speed" field in the common beginner sense.
- Safer motion comes from computing desired position over time, not from incrementing off noisy current encoder readings.

Evidence:

- Msg 723: unset joint entries can push other joints to extreme positions
- Msg 637: best-practice advice for smooth, lower-wear joint motion

### Networking and WLAN

- OPEN-R networking usually assumes a known IP address; DHCP support was not generally available in the older OPEN-R LAN stack discussed in the archive.
- Some commercial AIBO software later gained DHCP, but that does not imply the SDK stack supports it.
- `WLANCONF.TXT` formatting is brittle. At least one confirmed issue was caused by spaces around `KEY=VALUE`.
- For retrieving local/remote addresses in TCP flows, use the address fields in endpoint connect/listen message structures.
- The `"IPStack"` object name is fixed in the SDK's TCP/IP object model.

Evidence:

- Msg 675: use `TCPEndpointListenMsg` / `TCPEndpointConnectMsg` address fields
- Msg 701: current OPEN-R LAN support requires a known IP
- Msg 552: `WLANCONF.TXT` formatting without spaces fixed AP boot issues

### TCP/UDP programming

- The documentation for OPEN-R TCP/IP had known inaccuracies; sample code was often a better reference than the document.
- `Initialize()` should be invoked from `DoStart()`.
- Some documented `stub.cfg` entries and send-call examples were explicitly corrected by SDK support.
- `antEnvMsg::Receive()` is required in certain endpoint handlers even though some samples were stylistically inconsistent.
- If services are reported as `... NOT FOUND`, inspect object registration before assuming connect-graph syntax is wrong.

Evidence:

- Msg 665: doc corrections for `Initialize()` and extra entry usage
- Msg 684: `antEnvMsg::Receive()` guidance
- Msg 690: missing `REGISTER_ALL_ENTRY` caused service lookup failures

### Vision and camera handling

- Vision work in the archive revolves around raw AIBO camera data, YCbCr/YUV conversion, CMVision, and color table tuning.
- A recurring beginner need is simply obtaining the current camera image buffer in a usable array form.
- Color calibration is nontrivial; manual edits to vendor data files may fail if there is extra structure or validation beyond obvious bytes.
- Several users streamed image data over WLAN or converted camera buffers for external libraries, so remote vision processing is a common pattern.

Evidence:

- Msg 710: simplest-image-access question appears as a core workflow need
- Msg 592: confusion around YCbCr ranges and formulas
- Msg 402: UDP/TCP used for remote image transfer experiments
- Msg 1953: manual ERS-7 color-calibration edits likely hit hidden file structure or validation

### Shared memory and image transfer

- `SetData(ptr, size)` copies data into shared memory.
- That is convenient but may be wrong for high-volume image transfer if the design assumes zero-copy behavior.
- Check `OStatus` return codes on `SetData` and related API calls; the archive repeatedly suggests return-code inspection as a debugging habit.

Evidence:

- Msg 697: `SetData` copy semantics and `OStatus` advice

### R-CODE

- R-CODE is treated as simpler and more beginner-friendly for some tasks, but it is not a drop-in replacement for full OPEN-R behavior.
- The ERS-220 infrared distance sensor is exposed through the `Distance` RCODE variable, reported in millimeters.
- R-CODE support is model/version dependent. ERS-7M3 WLAN was not supported in R-CODE Ver2 at first, then later support was released.

Evidence:

- Msg 647: `Distance` variable semantics in R-CODE
- Msg 1945: ERS-7M3 WLAN unsupported in R-CODE Ver2
- Msg 1954 / 1955: later release adds ERS-7M3 R-CODE support

## Repeated Troubleshooting Heuristics

When debugging Sony OPEN-R / Aperios systems, the archive strongly suggests this order:

1. Verify model compatibility.
2. Verify flash ROM / firmware level.
3. Verify Memory Stick layout and base software choice.
4. Verify battery level and hardware health.
5. Verify `OBJECTS.CFG`, `CONNECT.CFG`, and generated stubs.
6. Verify `REGISTER_ALL_ENTRY`, selector counts, and lifecycle callbacks.
7. Verify the object is not blocking in `DoStart()` / `DoStop()`.
8. Check queue pressure, ready signaling, and whether message production exceeds consumption.
9. Inspect return codes (`OStatus`) instead of assuming success.
10. Prefer known-good SDK samples when docs and runtime behavior disagree.

## Representative Failure Signatures

- `Command not found` for `mipsel-linux-g++` or `stubgen2`
  - SDK install/path/permissions problem
- `... NOT FOUND`
  - unregistered entry/object or bad object graph
- `selector out of range`
  - selector count/entry mismatch
- `error 28`
  - `sTIMEOUT`, often lifecycle blockage
- `Exceed max size of queue`
  - backpressure / consumer lag / message flood
- `UDP_CONNECTION_BUSY`
  - asynchronous send path not yet clear for another packet
- TLB exception in unrelated object such as `uniMailer`
  - probable memory corruption from user code, not necessarily a fault in the named system object

## Suggested Persona For An Expert Advisor

An expert system built from this archive should behave like an old-school OPEN-R integration engineer:

- first ask for model, firmware, Memory Stick layout, and exact base software
- treat config files and generated glue as first-class debugging surfaces
- prefer sample-code conventions over ambiguous docs
- explain selector/observer/object errors in terms of registration and lifecycle
- warn about model/version-specific WLAN and R-CODE limitations
- assume resource limits are tight and queue overflows are real
- recommend checking return codes, `EMON.LOG`, and minimal reproducible sample images

## Limits Of This Context

- Some advice is community-generated and may reflect one model or one SDK revision only.
- The archive contains announcements, academic links, and product chatter in addition to technical content.
- A few topics reference files, tools, or downloads that are no longer easily available.
- The context is strongest for practical debugging and weaker for full API reference coverage.
