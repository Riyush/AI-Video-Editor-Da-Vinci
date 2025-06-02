import binascii
import zlib
import gzip
import json
import struct
import re
import bz2, lzma
from base64 import b64decode

try:
    import msgpack
except ImportError:
    msgpack = None

with open("Timeline_Item_Blob_before.txt", 'r') as f1:
    hex_string_before = f1.read().strip()

with open("Timeline_Item_Blob_after.txt", 'r') as f2:
    hex_string_after = f2.read().strip()

with open ("Timeline_Item_Blob_next_frame.txt", 'r') as f3:
    hex_string_after_next_frame = f3.read().strip()

# Convert hex string to raw bytes
blob_before = bytes.fromhex(hex_string_before)
print(blob_before)
blob_after = bytes.fromhex(hex_string_after)

blob_next_keyframe = bytes.fromhex(hex_string_after_next_frame)

def extract_ascii_strings(data, min_length=4):
    # Finds ASCII substrings of a certain minimum length
    return re.findall(rb'[\x20-\x7E]{%d,}' % min_length, data)

def diff_blobs(blob1, blob2):
    for i, (b1, b2) in enumerate(zip(blob1, blob2)):
        if b1 != b2:
            print(f"Offset {i:04X}: {b1:02X} -> {b2:02X}")
    if len(blob1) != len(blob2):
        print(f"Blobs differ in length: {len(blob1)} vs {len(blob2)}")

#diff_blobs(blob_before, blob_after)
    
def interpret_as_float32(hex_bytes):
    # Convert from hex to float assuming little endian
    b = bytes.fromhex(hex_bytes)
    try:
        return struct.unpack('<f', b)[0]
    except:
        return "Invalid"

def analyze_bytes(hex_string):
    b = bytes.fromhex(hex_string)
    results = {}
    for size in [1, 2, 4]:  # byte widths
        for i in range(len(b) - size + 1):
            chunk = b[i:i+size]
            try:
                results[f"{i}:{i+size}"] = {
                    "int": int.from_bytes(chunk, "little"),
                    "hex": chunk.hex(),
                    "signed": int.from_bytes(chunk, "little", signed=True)
                }
            except:
                continue
    return results

def print_bits(hex_string):
    return ' '.join(f"{b:08b}" for b in bytes.fromhex(hex_string))

def analyze_diff(before_hex, after_hex):
    # Convert hex strings to byte arrays
    before_bytes = bytes.fromhex(before_hex)
    after_bytes = bytes.fromhex(after_hex)
    
    print(f"{'Offset':<8} {'Before':<20} {'After':<20} {'Change?'}")
    for i in range(0, len(before_bytes), 4):
        b_chunk = before_bytes[i:i+4]
        a_chunk = after_bytes[i:i+4]
        
        b_hex = b_chunk.hex()
        a_hex = a_chunk.hex()
        
        b_int = int.from_bytes(b_chunk, byteorder='big')
        a_int = int.from_bytes(a_chunk, byteorder='big')

        print(f"{i:<8} {b_hex:<20} {a_hex:<20} {'YES' if b_chunk != a_chunk else ''}")
