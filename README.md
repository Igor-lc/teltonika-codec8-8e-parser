# teltonika-codec8-8e-parser
Teltonika Codec 8 &amp; 8E parser in Python - decodes GPS, IO data, and verifies CRC. Ready-to-use for trackers!

## Code Example
======================================================================
FINAL CORRECTED TELTONIKA CODEC 8/8E PARSER
======================================================================
 Packet Structure:
   Preamble: 00000000
   Data Field Length: 203 bytes
   Codec ID: 0x08 (Codec 8)
   Total Expected Length: 215 bytes
   Actual Length: 215 bytes
   Number of Data Records: 5
----------------------------------------------------------------------

 RECORD 1/5:
   ========================================
   Timestamp: 1836274140000 ms -> 04:09:00 10-03-2028 (UTC)
   Priority: 0
   GPS Data:
      Longitude: 77.0581533°
      Latitude: -12.0358533°
      Altitude: 983 m
      Angle: 20°
      Satellites: 11
      Speed: 201 km/h (raw: 201 km/h)
   Event ID: 0
   Total IO Elements: 4
   1-byte IO count: 2
      IO ID 21: 4
      IO ID 239: 0
   2-byte IO count: 2
      IO ID 66: 10.580 V
      IO ID 67: 3.600 V
   4-byte IO count: 0
   8-byte IO count: 0
    RECORD 1 PARSED SUCCESSFULLY
   ----------------------------------------

 RECORD 2/5:
   ========================================
   Timestamp: 1836274142000 ms -> 04:09:02 10-03-2028 (UTC)
   Priority: 0
   GPS Data:
      Longitude: 77.0577233°
      Latitude: -12.0349333°
      Altitude: 983 m
      Angle: 27°
      Satellites: 11
      Speed: 201 km/h (raw: 201 km/h)
   Event ID: 0
   Total IO Elements: 4
   1-byte IO count: 2
      IO ID 21: 4
      IO ID 239: 0
   2-byte IO count: 2
      IO ID 66: 10.570 V
      IO ID 67: 3.590 V
   4-byte IO count: 0
   8-byte IO count: 0
    RECORD 2 PARSED SUCCESSFULLY
   ----------------------------------------

 RECORD 3/5:
   ========================================
   Timestamp: 1836274144000 ms -> 04:09:04 10-03-2028 (UTC)
   Priority: 0
   GPS Data:
      Longitude: 77.0571933°
      Latitude: -12.0340666°
      Altitude: 983 m
      Angle: 33°
      Satellites: 11
      Speed: 201 km/h (raw: 201 km/h)
   Event ID: 0
   Total IO Elements: 4
   1-byte IO count: 2
      IO ID 21: 4
      IO ID 239: 0
   2-byte IO count: 2
      IO ID 66: 10.550 V
      IO ID 67: 3.600 V
   4-byte IO count: 0
   8-byte IO count: 0
    RECORD 3 PARSED SUCCESSFULLY
   ----------------------------------------

 RECORD 4/5:
   ========================================
   Timestamp: 1836274146000 ms -> 04:09:06 10-03-2028 (UTC)
   Priority: 0
   GPS Data:
      Longitude: 77.0565650°
      Latitude: -12.0332616°
      Altitude: 983 m
      Angle: 40°
      Satellites: 11
      Speed: 201 km/h (raw: 201 km/h)
   Event ID: 0
   Total IO Elements: 4
   1-byte IO count: 2
      IO ID 21: 4
      IO ID 239: 0
   2-byte IO count: 2
      IO ID 66: 10.540 V
      IO ID 67: 3.610 V
   4-byte IO count: 0
   8-byte IO count: 0
    RECORD 4 PARSED SUCCESSFULLY
   ----------------------------------------

 RECORD 5/5:
   ========================================
   Timestamp: 1836274148000 ms -> 04:09:08 10-03-2028 (UTC)
   Priority: 0
   GPS Data:
      Longitude: 77.0558483°
      Latitude: -12.0325316°
      Altitude: 983 m
      Angle: 46°
      Satellites: 11
      Speed: 201 km/h (raw: 201 km/h)
   Event ID: 0
   Total IO Elements: 4
   1-byte IO count: 2
      IO ID 21: 4
      IO ID 239: 0
   2-byte IO count: 2
      IO ID 66: 10.580 V
      IO ID 67: 3.600 V
   4-byte IO count: 0
   8-byte IO count: 0
    RECORD 5 PARSED SUCCESSFULLY
   ----------------------------------------

 Number of Data 2: 5

 CRC VERIFICATION:
   Data for CRC: 0x0805000001AB8A77C360002DEE241DF8D3797B03D700140B00C90004021504EF0002422954430E100000000001AB8A77CB30002DEE1351F8D39D6B03D7001B0B00C90004021504EF000242294A430E060000000001AB8A77D300002DEDFE9DF8D3BF4603D700210B00C90004021504EF0002422936430E100000000001AB8A77DAD0002DEDE612F8D3DEB803D700280B00C90004021504EF000242292C430E1A0000000001AB8A77E2A0002DEDCA13F8D3FB3C03D7002E0B00C90004021504EF0002422954430E10000005 (203 bytes)
   Calculated CRC: 0xC149
   Packet CRC: 0x0000C149
    CRC CHECK PASSED!

 FINAL SUMMARY:
   Expected records: 5
   Successfully parsed: 5
   Incomplete records: 0
   Failed records: 0
    ALL RECORDS PARSED SUCCESSFULLY
======================================================================

Process finished with exit code 0


**Note:** The timestamps in this example show year 2028 due to active Radio-Electronic Warfare (REB) interference in the area.
