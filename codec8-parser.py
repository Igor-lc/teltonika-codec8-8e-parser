#!/usr/bin/env python3
# Teltonika parser with proper CRC handling

import sys
import argparse
from datetime import datetime, timezone


def read_be(data, idx, length, signed=False):
    """Read bytes as big-endian integer with bounds checking"""
    if idx + length > len(data):
        raise IndexError(f"Not enough data to read {length} bytes at index {idx}")
    return int.from_bytes(data[idx:idx + length], byteorder='big', signed=signed)


def ts_to_str(ms):
    """Convert timestamp milliseconds to readable string"""
    if ms == 0:
        return "0000000000000 (ZERO)"
    try:
        dt = datetime.fromtimestamp(ms / 1000.0, tz=timezone.utc)
        return f"{ms} ms -> {dt.strftime('%H:%M:%S %d-%m-%Y')} (UTC)"
    except Exception:
        return f"{ms} ms -> (INVALID)"


def coordinate_formatter_direct(bytes_data):
    """Convert coordinate bytes to decimal directly"""
    coordinate = int.from_bytes(bytes_data, byteorder='big', signed=True)
    return coordinate / 10000000.0


def crc16_arc(data):
    """Calculate CRC-16/ARC for Teltonika packets"""
    crc = 0
    for byte in data:
        crc ^= byte
        for _ in range(8):
            if crc & 1:
                crc = (crc >> 1) ^ 0xA001
            else:
                crc >>= 1
    return crc


def parse_io_element(data, idx, io_count, io_size, codec_type):
    """Parse IO elements based on size and codec type with proper bounds checking"""
    elements = []
    for _ in range(io_count):
        # Read IO ID
        try:
            if codec_type == 0x08:
                if idx >= len(data): break
                io_id = data[idx]
                idx += 1
            else:  # Codec 8 Extended
                io_id = read_be(data, idx, 2)
                idx += 2
        except (IndexError, ValueError):
            break

        # Read value based on size
        try:
            if io_size == 1:
                if idx >= len(data): break
                value = data[idx]
                idx += 1
                elements.append((io_id, value))
            elif io_size == 2:
                value = read_be(data, idx, 2)
                idx += 2
                elements.append((io_id, value))
            elif io_size == 4:
                value = read_be(data, idx, 4)
                idx += 4
                elements.append((io_id, value))
            elif io_size == 8:
                if idx + 8 > len(data): break
                value_bytes = data[idx:idx + 8]
                # Try to convert to int if it makes sense
                try:
                    value = int.from_bytes(value_bytes, byteorder='big', signed=False)
                    elements.append((io_id, value))
                except:
                    elements.append((io_id, value_bytes.hex()))
                idx += 8
        except (IndexError, ValueError):
            break

    return elements, idx


def parse_packet(hex_input, speed_in_knots=False):
    try:
        data = bytes.fromhex(hex_input.strip())
    except Exception as e:
        print(f"❌ Invalid hex input: {e}")
        return

    if len(data) < 16:
        print("❌ Packet too short")
        return

    print("=" * 70)
    print("FINAL CORRECTED TELTONIKA CODEC 8/8E PARSER")
    print("=" * 70)

    # Parse header with bounds checking
    try:
        preamble = data[0:4]
        data_field_length = read_be(data, 4, 4)
        codec_id = data[8]
    except (IndexError, ValueError) as e:
        print(f"❌ Error parsing header: {e}")
        return

    # CORRECTED: Total packet length = header(8) + data_field + CRC(4)
    total_packet_length = 8 + data_field_length + 4

    print(f"📦 Packet Structure:")
    print(f"   Preamble: {preamble.hex().upper()}")
    print(f"   Data Field Length: {data_field_length} bytes")
    print(f"   Codec ID: 0x{codec_id:02X} ({'Codec 8' if codec_id == 0x08 else 'Codec 8 Extended'})")
    print(f"   Total Expected Length: {total_packet_length} bytes")
    print(f"   Actual Length: {len(data)} bytes")

    if codec_id not in [0x08, 0x8E]:
        print(f"❌ Unsupported codec ID: 0x{codec_id:02X}")
        print("⚠️  Attempting partial parse despite unsupported codec...")

    # Check packet completeness
    if len(data) < total_packet_length:
        print(f"⚠️  INCOMPLETE PACKET - attempting partial parse")
        print(f"   Missing {total_packet_length - len(data)} bytes")
    elif len(data) > total_packet_length:
        print(f"⚠️  EXTRA DATA - packet has {len(data) - total_packet_length} extra bytes")

    idx = 9  # Start after codec ID

    # Parse number of records
    try:
        if codec_id == 0x08:
            num_records = data[idx]
            idx += 1
        else:  # Codec 8 Extended
            num_records = read_be(data, idx, 2)
            idx += 2
    except (IndexError, ValueError) as e:
        print(f"❌ Error reading number of records: {e}")
        num_records = 0

    print(f"   Number of Data Records: {num_records}")

    if num_records == 0:
        print("ℹ️  No data records in packet - may contain only IO data")

    print("-" * 70)

    records_parsed = 0
    incomplete_records = 0

    # Parse each record with granular error handling
    for rec_num in range(num_records):
        print(f"\n📝 RECORD {rec_num + 1}/{num_records}:")
        print(f"   {'=' * 40}")

        record_valid = True
        record_complete = True

        # Parse timestamp with error handling
        try:
            timestamp = read_be(data, idx, 8)
            idx += 8
            print(f"   Timestamp: {ts_to_str(timestamp)}")
        except (IndexError, ValueError) as e:
            print(f"   ❌ Error reading timestamp: {e}")
            record_valid = False
            record_complete = False
            break

        # Parse priority with error handling
        try:
            if idx >= len(data):
                print("   ❌ Not enough data for priority")
                record_valid = False
                record_complete = False
                break
            priority = data[idx]
            idx += 1
            print(f"   Priority: {priority}")
        except (IndexError, ValueError) as e:
            print(f"   ❌ Error reading priority: {e}")
            record_valid = False
            record_complete = False

        # Parse GPS data with error handling
        gps_data = {}
        try:
            # Longitude (4 bytes)
            if idx + 4 > len(data):
                print("   ❌ Not enough data for GPS coordinates")
                record_valid = False
                record_complete = False
            else:
                gps_data['longitude'] = coordinate_formatter_direct(data[idx:idx + 4])
                idx += 4

            # Latitude (4 bytes)
            if idx + 4 > len(data):
                print("   ❌ Not enough data for GPS coordinates")
                record_valid = False
                record_complete = False
            else:
                gps_data['latitude'] = coordinate_formatter_direct(data[idx:idx + 4])
                idx += 4

            # Altitude (2 bytes) - SIGNED for below sea level
            if idx + 2 > len(data):
                print("   ❌ Not enough data for GPS data")
                record_valid = False
                record_complete = False
            else:
                gps_data['altitude'] = read_be(data, idx, 2, signed=True)
                idx += 2

            # Angle (2 bytes)
            if idx + 2 > len(data):
                print("   ❌ Not enough data for GPS data")
                record_valid = False
                record_complete = False
            else:
                gps_data['angle'] = read_be(data, idx, 2)
                idx += 2

            # Satellites (1 byte)
            if idx >= len(data):
                print("   ❌ Not enough data for GPS data")
                record_valid = False
                record_complete = False
            else:
                gps_data['satellites'] = data[idx]
                idx += 1

            # Speed (2 bytes)
            if idx + 2 > len(data):
                print("   ❌ Not enough data for GPS data")
                record_valid = False
                record_complete = False
            else:
                gps_data['speed_raw'] = read_be(data, idx, 2)
                idx += 2

                # Handle speed units
                speed_value = gps_data['speed_raw']
                speed_unit = "knots" if speed_in_knots else "km/h"
                if speed_in_knots:
                    # Convert knots to km/h if needed (1 knot = 1.852 km/h)
                    speed_display = speed_value * 1.852
                    speed_unit_display = "km/h"
                else:
                    speed_display = speed_value
                    speed_unit_display = "km/h"

                print(f"   GPS Data:")
                print(f"      Longitude: {gps_data.get('longitude', 0):.7f}°")
                print(f"      Latitude: {gps_data.get('latitude', 0):.7f}°")
                print(f"      Altitude: {gps_data.get('altitude', 0)} m")
                print(f"      Angle: {gps_data.get('angle', 0)}°")
                print(f"      Satellites: {gps_data.get('satellites', 0)}")
                print(f"      Speed: {speed_display} {speed_unit_display} (raw: {speed_value} {speed_unit})")
        except (IndexError, ValueError) as e:
            print(f"   ❌ Error parsing GPS data: {e}")
            record_valid = False
            record_complete = False

        # Parse Event ID with error handling
        try:
            if codec_id == 0x08:
                if idx >= len(data):
                    print("   ❌ Not enough data for event ID")
                    record_valid = False
                    record_complete = False
                else:
                    event_id = data[idx]
                    idx += 1
            else:
                event_id = read_be(data, idx, 2)
                idx += 2
            print(f"   Event ID: {event_id}")
        except (IndexError, ValueError) as e:
            print(f"   ❌ Error reading event ID: {e}")
            record_valid = False
            record_complete = False

        # Parse IO elements with granular error handling
        try:
            # Number of Total IO elements
            if codec_id == 0x08:
                if idx >= len(data):
                    print("   ❌ Not enough data for total IO count")
                    record_valid = False
                    record_complete = False
                else:
                    total_io = data[idx]
                    idx += 1
            else:
                total_io = read_be(data, idx, 2)
                idx += 2
            print(f"   Total IO Elements: {total_io}")

            # Parse IO elements by size
            io_sizes = [(1, "1-byte"), (2, "2-byte"), (4, "4-byte"), (8, "8-byte")]

            for io_size, size_name in io_sizes:
                try:
                    # Read count for this IO size
                    if idx >= len(data): break

                    if codec_id == 0x08:
                        io_count = data[idx]
                        idx += 1
                    else:
                        io_count = read_be(data, idx, 2)
                        idx += 2

                    print(f"   {size_name} IO count: {io_count}")

                    if io_count > 0:
                        elements, idx = parse_io_element(data, idx, io_count, io_size, codec_id)

                        for io_id, value in elements:
                            # Apply scaling for known IO types
                            display_value = value
                            if io_size == 2 and io_id in [66, 67]:  # Voltages
                                display_value = value * 0.001
                                print(f"      IO ID {io_id}: {display_value:.3f} V")
                            elif isinstance(value, int):
                                print(f"      IO ID {io_id}: {value}")
                            else:
                                print(f"      IO ID {io_id}: {value}")
                except (IndexError, ValueError) as e:
                    print(f"   ❌ Error parsing {size_name} IO elements: {e}")
                    record_complete = False

            # For Codec 8 Extended, parse variable-length IO elements
            if codec_id == 0x8E and idx + 2 <= len(data):
                try:
                    var_io_count = read_be(data, idx, 2)
                    idx += 2
                    print(f"   X byte IO count: {var_io_count}")

                    if var_io_count > 0:
                        for _ in range(var_io_count):
                            if idx + 4 > len(data):
                                record_complete = False
                                break

                            io_id = read_be(data, idx, 2)
                            idx += 2
                            value_length = read_be(data, idx, 2)
                            idx += 2

                            if idx + value_length <= len(data):
                                value_data = data[idx:idx + value_length]
                                idx += value_length
                                print(f"      IO ID {io_id}: 0x{value_data.hex().upper()} (len: {value_length})")
                            else:
                                record_complete = False
                except (IndexError, ValueError) as e:
                    print(f"   ❌ Error parsing variable-length IO elements: {e}")
                    record_complete = False

        except (IndexError, ValueError) as e:
            print(f"   ❌ Error parsing IO elements: {e}")
            record_valid = False
            record_complete = False

        if record_valid:
            records_parsed += 1
            status = "PARSED SUCCESSFULLY" if record_complete else "PARSED WITH MISSING DATA"
            print(f"   ✅ RECORD {rec_num + 1} {status}")
        else:
            print(f"   ❌ RECORD {rec_num + 1} HAS ERRORS")

        if not record_complete:
            incomplete_records += 1

        print(f"   {'-' * 40}")

    # Parse Number of Data 2 (same size as initial number of records)
    try:
        if codec_id == 0x08:
            if idx < len(data):
                total_records_parsed = data[idx]
                idx += 1
                print(f"\n📊 Number of Data 2: {total_records_parsed}")
        else:  # Codec 8 Extended
            if idx + 2 <= len(data):
                total_records_parsed = read_be(data, idx, 2)
                idx += 2
                print(f"\n📊 Number of Data 2: {total_records_parsed}")
    except (IndexError, ValueError):
        print(f"\n📊 Could not read Number of Data 2")

    # CORRECTED CRC Verification - same as working parser
    print(f"\n🔒 CRC VERIFICATION:")
    try:
        if len(data) >= 4:
            # Calculate expected CRC for data[8:-4] (from Codec ID to before CRC)
            crc_data = data[8:-4]
            calculated_crc = crc16_arc(crc_data)

            # Get CRC from packet (last 4 bytes)
            crc_from_packet = int.from_bytes(data[-4:], byteorder='big')

            print(f"   Data for CRC: 0x{crc_data.hex().upper()} ({len(crc_data)} bytes)")
            print(f"   Calculated CRC: 0x{calculated_crc:04X}")
            print(f"   Packet CRC: 0x{crc_from_packet:08X}")

            # Compare (note: packet stores CRC as 4 bytes, but calculation gives 2 bytes)
            if calculated_crc == (crc_from_packet & 0xFFFF):
                print("   ✅ CRC CHECK PASSED!")
            else:
                print("   ❌ CRC CHECK FAILED!")
        else:
            print("   🔒 No CRC found (packet too short)")
    except Exception as e:
        print(f"   🔒 Error during CRC verification: {e}")

    print(f"\n🎯 FINAL SUMMARY:")
    print(f"   Expected records: {num_records}")
    print(f"   Successfully parsed: {records_parsed}")
    print(f"   Incomplete records: {incomplete_records}")
    print(f"   Failed records: {num_records - records_parsed}")

    if records_parsed == num_records and incomplete_records == 0:
        print("   ✅ ALL RECORDS PARSED SUCCESSFULLY")
    elif records_parsed == num_records and incomplete_records > 0:
        print(f"   ⚠️  ALL RECORDS PARSED, BUT {incomplete_records} HAVE MISSING DATA")
    elif records_parsed > 0:
        print(
            f"   ⚠️  PARTIAL SUCCESS - {records_parsed}/{num_records} records parsed ({incomplete_records} incomplete)")
    else:
        print("   ❌ NO RECORDS PARSED SUCCESSFULLY")

    print("=" * 70)


def main():
    parser = argparse.ArgumentParser(description='Teltonika Codec 8/8E Parser')
    parser.add_argument('hex_input', nargs='?', help='Hex string to parse')
    parser.add_argument('--knots', action='store_true', help='Assume speed is in knots (convert to km/h)')

    args = parser.parse_args()

    hex_input = args.hex_input
    if not hex_input:
        hex_input = input("Enter full packet hex: ").strip()

    parse_packet(hex_input, speed_in_knots=args.knots)


if __name__ == "__main__":
    main()