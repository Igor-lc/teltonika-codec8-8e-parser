# teltonika-codec8-8e-parser
Teltonika Codec 8 &amp; 8E parser in Python - decodes GPS, IO data, and verifies CRC. Ready-to-use for trackers!

## Code Example
Enter full packet hex: 00000000000000750803000001ab8a798c68002dede3ecf8d3c040030900240c00c9000301150302422972430de80000000001ab8a799438002dedca34f8d3deb8030a002a0d00c90003011503024228f0430dd40000000001ab8a799c08002dedad1af8d3fa20030a00310c00c9000301150302422968430dde00000300009280

======================================================================
FINAL CORRECTED TELTONIKA CODEC 8/8E PARSER
======================================================================
Packet Structure:
   Preamble: 00000000
   Data Field Length: 117 bytes
   Codec ID: 0x08 (Codec 8)
   Total Expected Length: 129 bytes
   Actual Length: 129 bytes
   Number of Data Records: 3
----------------------------------------------------------------------

RECORD 1/3:
   ========================================
   Timestamp: 1836274257000 ms -> 04:10:57 10-03-2028 (UTC)
   Priority: 0
   GPS Data:
      Longitude: 77.0565100°
      Latitude: -12.0340416°
      Altitude: 777 m
      Angle: 36°
      Satellites: 12
      Speed: 22 km/h (raw: 22 km/h)
   Event ID: 0
   Total IO Elements: 3
   1-byte IO count: 1
      IO ID 21: 3
   2-byte IO count: 2
      IO ID 66: 10.610 V
      IO ID 67: 3.560 V
   4-byte IO count: 0
   8-byte IO count: 0
   RECORD 1 PARSED SUCCESSFULLY
   ----------------------------------------

RECORD 2/3:
   ========================================
   Timestamp: 1836274259000 ms -> 04:10:59 10-03-2028 (UTC)
   Priority: 0
   GPS Data:
      Longitude: 77.0558516°
      Latitude: -12.0332616°
      Altitude: 778 m
      Angle: 42°
      Satellites: 13
      Speed: 21 km/h (raw: 21 km/h)
   Event ID: 0
   Total IO Elements: 3
   1-byte IO count: 1
      IO ID 21: 3
   2-byte IO count: 2
      IO ID 66: 10.480 V
      IO ID 67: 3.540 V
   4-byte IO count: 0
   8-byte IO count: 0
   RECORD 2 PARSED SUCCESSFULLY
   ----------------------------------------

RECORD 3/3:
   ========================================
   Timestamp: 1836274261000 ms -> 04:11:01 10-03-2028 (UTC)
   Priority: 0
   GPS Data:
      Longitude: 77.0551066°
      Latitude: -12.0325600°
      Altitude: 778 m
      Angle: 49°
      Satellites: 12
      Speed: 20 km/h (raw: 20 km/h)
   Event ID: 0
   Total IO Elements: 3
   1-byte IO count: 1
      IO ID 21: 3
   2-byte IO count: 2
      IO ID 66: 10.600 V
      IO ID 67: 3.550 V
   4-byte IO count: 0
   8-byte IO count: 0
   RECORD 3 PARSED SUCCESSFULLY
   ----------------------------------------

Number of Data 2: 3

CRC VERIFICATION:
   Data for CRC: 0x0803000001AB8A798C68002DEDE3ECF8D3C040030900240C00C9000301150302422972430DE80000000001AB8A799438002DEDCA34F8D3DEB8030A002A0D00C90003011503024228F0430DD40000000001AB8A799C08002DEDAD1AF8D3FA20030A00310C00C9000301150302422968430DDE000003 (117 bytes)
   Calculated CRC: 0x9280
   Packet CRC: 0x00009280
   CRC CHECK PASSED!

FINAL SUMMARY:
   Expected records: 3
   Successfully parsed: 3
   Incomplete records: 0
   Failed records: 0
   ALL RECORDS PARSED SUCCESSFULLY
======================================================================

Process finished with exit code 0

**Note:** The timestamps in this example show year 2028 due to active Radio-Electronic Warfare (REB) interference in the area.
