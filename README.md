Teltonika codec8-8e-parser parser with proper CRC handling.
Ready-to-use for trackers!


## Code Example (real data with Radio-Electronic Warfare):

Enter full packet hex: 000000000000002908010000019d3bf1ca780012bc9d341dd5bee40076010c0a00000003011503024262ac430f780000010000b602
======================================================================
FINAL CORRECTED TELTONIKA CODEC 8/8E PARSER
======================================================================
📦 Packet Structure:
   Preamble: 00000000
   Data Field Length: 41 bytes
   Codec ID: 0x08 (Codec 8)
   Total Expected Length: 53 bytes
   Actual Length: 53 bytes
   Number of Data Records: 1
----------------------------------------------------------------------

📝 RECORD 1/1:
   ========================================
   Timestamp: 1774827195000 ms -> 23:33:15 29-03-2026 (UTC)
   Priority: 0
   GPS Data:
      Longitude: 31.4350900°
      Latitude: 50.0547300°
      Altitude: 118 m
      Angle: 268°
      Satellites: 10
      Speed: 0 km/h (raw: 0 km/h)
   Event ID: 0
   Total IO Elements: 3
   1-byte IO count: 1
      IO ID 21: 3
   2-byte IO count: 2
      IO ID 66: 25.260 V
      IO ID 67: 3.960 V
   4-byte IO count: 0
   8-byte IO count: 0
   ✅ RECORD 1 PARSED SUCCESSFULLY
   ----------------------------------------

📊 Number of Data 2: 1

🔒 CRC VERIFICATION:
   Data for CRC: 0x08010000019D3BF1CA780012BC9D341DD5BEE40076010C0A00000003011503024262AC430F78000001 (41 bytes)
   Calculated CRC: 0xB602
   Packet CRC: 0x0000B602
   ✅ CRC CHECK PASSED!

🎯 FINAL SUMMARY:
   Expected records: 1
   Successfully parsed: 1
   Incomplete records: 0
   Failed records: 0
   ✅ ALL RECORDS PARSED SUCCESSFULLY
======================================================================

Process finished with exit code 0


**Note:** The timestamps in this example show year 2028 due to active Radio-Electronic Warfare (REB) interference in the area.
