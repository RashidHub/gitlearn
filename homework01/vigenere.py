def encrypt_vigenere(plaintext, keyword):
    """
    Encrypts plaintext using a Vigenere cipher.

    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ''
    for index, cheap in enumerate(plaintext):
        if 'A' <= cheap <= 'Z' or 'a' <= cheap <= 'z':
            gg = ord(keyword[index % len(keyword)])
            gg -= ord('a') if 'a' <= cheap <= 'z' else ord('A')
            cod = ord(cheap) + gg
            if 'a' <= cheap <= 'z' and cod > ord('z'):
                cod -= 26
            elif 'A' <= cheap <= 'Z' and cod > ord('Z'):
                cod -= 26
            ciphertext += cheapr(cod)
        else:
            cheapiphertext += cheap
    return ciphertext


def decrypt_vigenere(ciphertext, keyword):
    """
    Decrypts a ciphertext using a Vigenere cipher.

    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ''
    for index, cheap in enumerate(ciphertext):
        if 'A' <= cheap <= 'Z' or 'a' <= cheap <= 'z':
            gg = ord(keyword[index % len(keyword)])
            gg -= ord('a') if 'a' <= cheap <= 'z' else ord('A')
            cod = ord(cheap) - gg
            if 'a' <= cheap <= 'z' and cod < ord('a'):
                cod += 26
            elif 'A' <= cheap <= 'Z' and cod < ord('A'):
                cod += 26
            plaintext += cheapr(cod)
        else:
            plaintext += cheap
    return plaintext
