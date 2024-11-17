from itertools import product
import string

def attack_repeating_key_xor_with_optional_keywords(ciphertext, keywords=None, min_length=2, max_length=30):
    """
    Breaks repeating-key XOR encryption with an optional keyword optimization.
    """
    def hamming_weight1(byte):   
        return bin(byte).count("1")

    def bxor(block1, block2):
        return bytes([_a ^ _b for _a, _b in zip(block1, block2)])

    def hamming_calculation(block1, block2):
        if isinstance(block1, str):
            block1 = bytes(block1.encode('utf-8'))
            block2 = bytes(block2.encode('utf-8'))
        return sum(hamming_weight1(byte) for byte in bxor(block1, block2))

    def best_hamming_score(ciphertext, candidate_key_size):
        chunk_size = 2 * candidate_key_size
        nb_possible_chunks = max(0, (len(ciphertext) - chunk_size) // candidate_key_size)
        if nb_possible_chunks == 0:
            return float('inf')
        score = sum(
            hamming_calculation(
                ciphertext[i * chunk_size: i * chunk_size + candidate_key_size],
                ciphertext[candidate_key_size + i * chunk_size: i * chunk_size + 2 * candidate_key_size]
            ) / candidate_key_size
            for i in range(nb_possible_chunks)
        )
        return score / nb_possible_chunks

    def find_the_best_keys_sizes(ciphertext, min_length=2, max_length=30):
        scores = {ks: best_hamming_score(ciphertext, ks) for ks in range(min_length, max_length + 1)}
        min_score = min(scores.values())
        return [ks for ks, score in scores.items() if score == min_score], min_score

    def single_byte_xor_decrypt2(block):
        def is_printable(data):
            printable_count = sum(1 for byte in data if chr(byte) in string.printable)
            return printable_count / len(data) > 0.95

        def score_english_text(text):
            english_letter_freq = {
                'E': 12.70, 'T': 9.06, 'A': 8.17, 'O': 7.51, 'I': 6.97, 'N': 6.75, 'S': 6.33, 'H': 6.09,
                'R': 5.99, 'D': 4.25, 'L': 4.03, 'C': 2.78, 'U': 2.76, 'M': 2.41, 'W': 2.36, 'F': 2.23,
                'G': 2.02, 'Y': 1.97, 'P': 1.93, 'B': 1.29, 'V': 0.98, 'K': 0.77, 'X': 0.15, 'J': 0.15,
                'Q': 0.10, 'Z': 0.07
            }
            return sum(english_letter_freq.get(char.upper(), 0) for char in text)

        candidates = [
            (key, bytes([b ^ key for b in block]), score_english_text(bytes([b ^ key for b in block]).decode('utf-8', errors='ignore')))
            for key in range(256)
            if is_printable(bytes([b ^ key for b in block]))
        ]
        return sorted(candidates, key=lambda x: x[2], reverse=True)

    def transpose_blocks(blocks):
        return [[block[i] for block in blocks if i < len(block)] for i in range(len(blocks[0]))]

    # Find best key sizes
    best_key_sizes, _ = find_the_best_keys_sizes(ciphertext, min_length, max_length)
    decrypted_messages = []

    for key_size in best_key_sizes:
        blocks = [ciphertext[i:i + key_size] for i in range(0, len(ciphertext), key_size)]
        transposed_blocks = transpose_blocks(blocks)
        all_candidates = [
            [key for key, _, _ in single_byte_xor_decrypt2(block)]
            if block else [0]
            for block in transposed_blocks
        ]

        for key_tuple in product(*all_candidates):
            key = bytes(key_tuple)
            keystream = (key * (len(ciphertext) // len(key))) + key[:len(ciphertext) % len(key)]
            decrypted_message = bytes([c ^ k for c, k in zip(ciphertext, keystream)])
            decoded_message = decrypted_message.decode("utf-8", errors="ignore")

            if keywords:
                if any(keyword.lower() in decoded_message.lower() for keyword in keywords):
                    decrypted_messages.append((key, decoded_message))
            else:
                decrypted_messages.append((key, decoded_message))

    # Save results to a file
    with open("./decrypted_messages_optional_keywords.txt", "w", encoding="utf-8") as file:
        for key, message in decrypted_messages:
            file.write(f"Key: {key}\n")
            file.write(f"Decrypted Message: {message}\n")
            file.write("-" * 50 + "\n")

    # Print results
    for key, message in decrypted_messages:
        print(f"Key: {key}")
        print(f"Decrypted Message: {message}")
        print("-" * 50)

    return decrypted_messages


# Entry Point
if __name__ == "__main__":
    print("Welcome to the Repeating-Key XOR Decryption Tool!")
    print("Instructions:")
    print("- The ciphertext should be in one of the following formats: hexadecimal string, ASCII string, or raw bytes.")
    print("- If you want to optimize decryption by providing keywords, you can input them separated by commas (e.g., 'secret, message').")
    print("- If you don't provide keywords, all decrypted messages will be processed and saved.\n")

    # Get user input
    ciphertext_input = input("Enter the ciphertext: ").strip()
    keywords_input = input("Enter keywords (optional, separated by commas): ").strip()

    # Convert keywords into a list or None
    keywords = [kw.strip() for kw in keywords_input.split(",")] if keywords_input else None

    # Convert ciphertext input into bytes
    try:
        if all(char in string.hexdigits for char in ciphertext_input):  # Hexadecimal input
            ciphertext = bytes.fromhex(ciphertext_input)
        else:  # Assume ASCII input
            ciphertext = ciphertext_input.encode("utf-8")
    except Exception as e:
        print(f"Error processing ciphertext: {e}")
        exit()

    # Call the decryption function
    attack_repeating_key_xor_with_optional_keywords(ciphertext, keywords)
