# Repeating-Key XOR Cipher Cracker

Welcome to the Repeating-Key XOR Cipher Cracker! This project is an implementation of an algorithm designed to cryptanalyze and break ciphertexts encrypted with a repeating-key XOR cipher.

This tool is particularly effective when one or more **known** words are present in the plaintext, which can significantly optimize the decryption process.

## Table of Contents
  ### 1.About the Project
  ### 2. Cryptanalysis Steps
  ### 3. Features
  ### 4. Usage
  ### 5. Limitations
  ### 6. Contributing

## About the Project
The XOR cipher is a simple yet widely used encryption technique. The repeating-key XOR cipher encrypts plaintext using a fixed-size key repeated over the entire plaintext length. While easy to implement, it is vulnerable to statistical analysis and cryptanalysis due to its deterministic nature.

This project provides a robust implementation to:

  **Identify the most probable key length using Hamming distances.** 
  **Break the ciphertext into blocks and transpose them.**
  **Use single-byte XOR decryption techniques to recover each byte of the key.**
  **Decrypt the ciphertext to reveal the plaintext.**
  **If you know or suspect one or more words in the plaintext, this tool allows you to use them to optimize the decryption process, saving computational resources and improving accuracy.**


## Cryptanalysis Steps
The attack on a repeating-key XOR cipher involves the following steps:

  ### 1. Determine Key Length
  The first step is to determine the most probable key length:
    Compute normalized Hamming distances between consecutive blocks of ciphertext for various key lengths.
    Select the key lengths with the smallest Hamming distances, as they are likely to produce consistent patterns.
  
  ### 2. Block Transposition
  Once the key length is identified:
    Split the ciphertext into blocks equal to the key length.
    Transpose the blocks such that each transposed block contains bytes encrypted with the same key byte.
  
  ### 3. Solve Each Transposed Block
  Each transposed block can now be treated as a single-byte XOR cipher:
    I used statistical techniques like English letter frequencies and check for printable results with tolerating 5% of text to be make of non printable chars in order to identify the most probable key byte for each position.
    Incorporate user-provided keywords (if any) to further refine the results.
  
  ### 4. Reconstruct the Key
  Combine the identified key bytes to reconstruct the repeating key.
  
  ### 5. Decrypt the Ciphertext
  Use the reconstructed key to XOR-decrypt the ciphertext, revealing the plaintext.
  
  ### 6. Prioritize Results
  If keywords are provided, prioritize results containing these words.
  Otherwise, rank results based on English letter frequency scores.

## Features
  **Keyword Optimization:** If the plaintext contains known words, you can specify them to speed up the decryption process.
  **Flexible Input Formats:** Supports ciphertext in hexadecimal, ASCII string, or bytes.
  **Top Results Logging:** Outputs the best decrypted messages to the console and a log file.
  **Adjustable Key Length:** The code tests keys of up to 30 characters by default but can be extended for longer keys on more powerful machines and depends on the case.

# Usage

  ## Prerequisites
    Python 3.x installed on your system.
  ## Running the Program
  Clone this repository:
      
      git clone https://github.com/AnisOuersighni/Repeating-Key-XOR-Cipher-Cracker.git
      cd xor-cipher-cracker

  Generate the ciphertext using the xor_generator.py script and put your key
    
    Run the script:
      python3 xor_cracker.py

# Limitations
### Key Length Constraint:
  The tool is tested for keys of up to 5 characters. Beyond this, the computational complexity grows exponentially (256^k possibilities for a key of length k).
  If you have a high-performance machine, feel free to test it and it should give you accurate results.

### Memory Usage:
  Generating all possible keys and testing them can consume significant memory, especially for longer key lengths used for encryption.
  The code uses optimizations like limiting candidates for each key byte to reduce memory overhead.

### Keyword Dependency:
  If no keywords are provided, the algorithm relies on general English frequency scoring, which may not be effective for non-English plaintext.

### Logging:
  if no keyword provided, you will need to search for thousands of line to find the adequate plaintext with the key  that give the **full** readable and correct plaintext. since the algo will judge the key is good if it outputs a readable char when used in inverse.


# Contributing
Feel free to suggest improvements, report issues, or contribute to make this project better! 😊
