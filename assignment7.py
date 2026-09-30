from collections import Counter


# Generate 5x5 Playfair Key Matrix
def generate_key_matrix(keyword):
    keyword = keyword.upper().replace("J", "I")
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"

    key = ""

    # Add keyword letters without repetition
    for ch in keyword:
        if ch.isalpha() and ch not in key:
            key += ch

    # Add remaining alphabet letters
    for ch in alphabet:
        if ch not in key:
            key += ch

    matrix = []

    for i in range(0, 25, 5):
        matrix.append(list(key[i:i + 5]))

    return matrix


# Prepare plaintext
def prepare_plaintext(plaintext):
    # Remove spaces and special characters
    plaintext = ''.join(
        ch for ch in plaintext.upper()
        if ch.isalpha()
    )

    # Combine I/J
    plaintext = plaintext.replace("J", "I")

    return plaintext


# Create digraphs
def create_digraphs(plaintext):
    digraphs = []
    i = 0

    while i < len(plaintext):

        # Last character
        if i == len(plaintext) - 1:
            digraphs.append(plaintext[i] + "X")
            i += 1

        # Repeated letters
        elif plaintext[i] == plaintext[i + 1]:
            digraphs.append(plaintext[i] + "X")
            i += 1

        # Normal pair
        else:
            digraphs.append(plaintext[i] + plaintext[i + 1])
            i += 2

    return digraphs


# Find position of a character in matrix
def find_position(matrix, character):
    for row in range(5):
        for col in range(5):
            if matrix[row][col] == character:
                return row, col


# Encrypt one pair
def encrypt_pair(pair, matrix):
    a, b = pair

    r1, c1 = find_position(matrix, a)
    r2, c2 = find_position(matrix, b)

    # Same row
    if r1 == r2:
        return (
            matrix[r1][(c1 + 1) % 5] +
            matrix[r2][(c2 + 1) % 5]
        )

    # Same column
    elif c1 == c2:
        return (
            matrix[(r1 + 1) % 5][c1] +
            matrix[(r2 + 1) % 5][c2]
        )

    # Rectangle rule
    else:
        return (
            matrix[r1][c2] +
            matrix[r2][c1]
        )


# Playfair Encryption
def playfair_encrypt(digraphs, matrix):
    ciphertext = ""

    for pair in digraphs:
        ciphertext += encrypt_pair(pair, matrix)

    return ciphertext


# Decrypt one pair
def decrypt_pair(pair, matrix):
    a, b = pair

    r1, c1 = find_position(matrix, a)
    r2, c2 = find_position(matrix, b)

    # Same row
    if r1 == r2:
        return (
            matrix[r1][(c1 - 1) % 5] +
            matrix[r2][(c2 - 1) % 5]
        )

    # Same column
    elif c1 == c2:
        return (
            matrix[(r1 - 1) % 5][c1] +
            matrix[(r2 - 1) % 5][c2]
        )

    # Rectangle rule
    else:
        return (
            matrix[r1][c2] +
            matrix[r2][c1]
        )


# Playfair Decryption
def playfair_decrypt(ciphertext, matrix):
    plaintext = ""

    for i in range(0, len(ciphertext), 2):
        pair = ciphertext[i:i + 2]
        plaintext += decrypt_pair(pair, matrix)

    return plaintext


# Digraph Frequency Analysis
def digraph_frequency(ciphertext):
    digraphs = []

    for i in range(0, len(ciphertext), 2):
        digraphs.append(ciphertext[i:i + 2])

    return Counter(digraphs)


# Verification
def verify(original_plaintext, decrypted_text):
    original = prepare_plaintext(original_plaintext)

    # Remove padding X at the end
    decrypted = decrypted_text

    if decrypted.endswith("X"):
        decrypted = decrypted[:-1]

    if original == decrypted:
        return "SUCCESS"
    else:
        return "VERIFICATION FAILED"


# Main Program
def main():

    # Given Input
    keyword = "MONARCHY"
    plaintext = "INSTRUMENTS"

    # Generate Key Matrix
    matrix = generate_key_matrix(keyword)

    print("Key Matrix:")
    for row in matrix:
        print(" ".join(row))

    # Prepare Plaintext
    prepared = prepare_plaintext(plaintext)

    # Create Digraphs
    digraphs = create_digraphs(prepared)

    print("\nPrepared Digraphs:")
    print(" ".join(digraphs))

    # Encryption
    ciphertext = playfair_encrypt(digraphs, matrix)

    print("\nCiphertext:")
    print(ciphertext)

    # Decryption
    decrypted = playfair_decrypt(ciphertext, matrix)

    print("\nDecrypted Text:")
    print(decrypted)

    # Digraph Frequency
    frequency = digraph_frequency(ciphertext)

    print("\nDigraph Frequency:")
    for pair, count in frequency.items():
        print(pair, ":", count)

    # Verification
    result = verify(plaintext, decrypted)

    print("\nVerification:")
    print(result)


# Run program
if __name__ == "__main__":
    main()
