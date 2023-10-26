def string_to_binary(s):
    """Convert a string to its binary representation."""
    return ''.join(format(ord(char), '08b') for char in s)

def binary_to_string(b):
    """Convert a binary representation back to its original string."""
    return ''.join(chr(int(b[i:i+8], 2)) for i in range(0, len(b), 8))