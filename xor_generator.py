import string 


def byte_xor(ba1, ba2):
    return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])


def multiple_lines_in_str_xor(input_string, key):
    lines = input_string.strip().split("\n")  # Split input into individual lines
    hex_results = []  # Store results for each line

    for line in lines:
        # Generate the repeating keystream
        keystream = (key * (len(line) // len(key))) + key[:len(line) % len(key)]
        
        # Perform XOR operation for the line
        result_bytes = byte_xor(line.encode('utf-8'), keystream.encode('utf-8'))
        hex_results.append(result_bytes.hex())  # Collect the result in hexadecimal

    print("--"*50)
    print("Hex results:\n" + "\n\n".join(hex_results))  # Print hex results separated by blank lines
    print("--"*50)



#key = input("enter your key to XOR with") 
secret ="SC2 Community is rock'ing it. Go Ahead and Solve this, I know you are capables guys !"
secret2="Aeezihf pdazpda zdpfozapodfjzepi fdazjfiezjfpeznskdvdsv eaofdzepofjezoezo pkdf^zekfez^fk Anis A7la Nas opzfjpzejzezfez"
key = "FEZ"

multiple_lines_in_str_xor(secret2,key)
