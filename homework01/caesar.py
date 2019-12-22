def encrypt_caesar(plaintext):
    """
    Encrypts plaintext using a Caesar cipher.

    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    ciphertext = ''
    for cheap in plaintext:
        if 'A' <= cheap <= 'Z' or 'a' <= cheap <= 'z':
            cod = ord(cheap) + 3
            if cod < ord('a') and cod > ord('Z') or cod > ord('z'):
                cod -= 26
            ciphertext += chr(cod)
        else:
            ciphertext += cheap
    return ciphertext


def decrypt_caesar(ciphertext):
    """
    Decrypts a ciphertext using a Caesar cipher.

    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    plaintext = ''
    for cheap in ciphertext:
        if 'A' <= cheap <= 'Z' or 'a' <= cheap <= 'z':
            cod = ord(cheap) - 3
            if cod < ord('A') and cod > ord('Z') or cod < ord('a'):
                cod += 26
            plaintext += chr(cod)
        else:
            plaintext += cheap
    return plaintext
    
