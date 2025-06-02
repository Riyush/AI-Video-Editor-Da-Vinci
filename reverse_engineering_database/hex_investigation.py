import binascii

with open("TiItem_Blob_after_keyframe.txt", 'rb') as f1:
    hex_blob = f1.read()


blob_bytes = binascii.unhexlify(hex_blob)
print(blob_bytes.decode('utf-8', errors='ignore'))