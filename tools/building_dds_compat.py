"""Native asset storage guard, retaining historical format-only hash evidence.

The historical module name is retained for existing report validators.
"""
import hashlib
import struct

RGBA = (0xff, 0xff00, 0xff0000, 0xff000000)
BGRA = (0xff0000, 0xff00, 0xff, 0xff000000)


def assert_export_layout(payload, relative):
    assert struct.unpack_from("<IIIII", payload, 88) == (32, *BGRA), "Non-native export layout: " + relative


def matches_export_hash(payload, expected, relative):
    """Accept only identical bytes or an exact lossless RGBA-to-BGRA transcode."""
    expected = expected.lower()
    if hashlib.sha256(payload).hexdigest() == expected:
        return True
    if struct.unpack_from("<IIII", payload, 92) != BGRA:
        return False
    canonical = bytearray(payload)
    struct.pack_into("<IIII", canonical, 92, *RGBA)
    canonical[128::4], canonical[130::4] = canonical[130::4], canonical[128::4]
    return hashlib.sha256(canonical).hexdigest() == expected
