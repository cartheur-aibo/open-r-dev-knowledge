# OPEN-R BBS Error Signature Index

Fast lookup for common runtime and build signatures discussed in the archive.

## command_not_found

- Messages tagged: 4
- Typical meaning: Missing or non-executable SDK tools such as the cross compiler or stub generator.
- Msg 54: question about how to build the samples!
- Msg 55: RE:question about how to build the samples!
- Msg 61: RE:question about how to build the samples!
- Msg 1580: How can I run start-rp-openr script?

## queue_overflow

- Messages tagged: 2
- Typical meaning: Producer/consumer imbalance, observer readiness issues, or message floods.
- Msg 648: Exceed max size of queue
- Msg 655: RE:Exceed max size of queue

## sTIMEOUT_error_28

- Messages tagged: 2
- Typical meaning: Lifecycle callback did not return, or another operation timed out.
- Msg 671: An error from OObjectManager
- Msg 704: RE:An error from OObjectManager

## selector_out_of_range

- Messages tagged: 2
- Typical meaning: Bad selector wiring, incomplete registration, or entry mismatch.
- Msg 336: programming help (intraDeliver selector out of range)
- Msg 337: RE:programming help (intraDeliver selector out of range)

## sendready_failed

- Messages tagged: 1
- Typical meaning: Observer/send readiness path is broken or overloaded.
- Msg 648: Exceed max size of queue

## service_not_found

- Messages tagged: 3
- Typical meaning: Object or service registration mismatch, often in generated glue or config.
- Msg 683: gServer.gMotionServer.gMotionCommand.S NOT FOUND
- Msg 686: RE:gServer.gMotionServer.gMotionCommand.S NOT FOUND
- Msg 690: RE:gServer.gMotionServer.gMotionCommand.S NOT FOUND

## tlb_exception

- Messages tagged: 3
- Typical meaning: Likely memory corruption or invalid access in user code.
- Msg 694: TLB Exception at "uniMailer"
- Msg 702: RE:TLB Exception at
- Msg 752: Is there anything wrong with the robot?

## udp_connection_busy

- Messages tagged: 1
- Typical meaning: UDP send path still busy when another packet is submitted.
- Msg 402: UDP sending problem
