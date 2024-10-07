import hashlib
import random
import time
import base64
from cryptography.fernet import Fernet

def hash_with_nonce(nonce, solution):
    """Hash the nonce and solution together."""
    return hashlib.sha256(f"{nonce}{solution}".encode()).hexdigest()

def server_setup(difficulty, max_solution, data_to_encrypt):
    start_time = time.time()
    # Generate a random nonce
    nonce = random.getrandbits(64)

    # Randomly select a starting point within the solution space
    start_solution = random.randint(0, max_solution)

    # Find a solution that meets the difficulty requirement
    solution = start_solution
    while True:
        hash_result = hash_with_nonce(nonce, solution)
        if hash_result.startswith('0' * difficulty):
            break
        solution += 1
        if solution > max_solution:
            solution = 0  # Wrap around if exceeding max_solution

    # Use the solution as a symmetric key
    symmetric_key = hashlib.sha256(str(solution).encode()).digest()[:32]  # Use first 32 bytes
    symmetric_key_b64 = base64.urlsafe_b64encode(symmetric_key)  # Base64 encode the key
    fernet = Fernet(symmetric_key_b64)
    encrypted_data = fernet.encrypt(data_to_encrypt.encode())

    # Hash the solution for the client
    hashed_solution = hashlib.sha256(str(solution).encode()).hexdigest()

    print(f"Server setup time: {time.time() - start_time:.6f} seconds")
    return nonce, encrypted_data, hashed_solution

def client_solve(nonce, encrypted_data, hashed_solution, difficulty, max_solution):
    start_time = time.time()
    # Try to find the solution
    solution = 0
    while True:
        hash_result = hash_with_nonce(nonce, solution)
        if hash_result.startswith('0' * difficulty):
            # Verify the solution by comparing hashes
            if hashlib.sha256(str(solution).encode()).hexdigest() == hashed_solution:
                break
        solution += 1
        if solution > max_solution:
            solution = 0  # Wrap around if exceeding max_solution

    # Use the solution as a symmetric key
    symmetric_key = hashlib.sha256(str(solution).encode()).digest()[:32]  # Use first 32 bytes
    symmetric_key_b64 = base64.urlsafe_b64encode(symmetric_key)  # Base64 encode the key
    fernet = Fernet(symmetric_key_b64)
    decrypted_data = fernet.decrypt(encrypted_data).decode()

    print(f"Client solve time: {time.time() - start_time:.6f} seconds")
    return decrypted_data



difficulty = 4  # Number of leading zeros required in the hash
max_solution = 3000000  # Upper bound for the solution space
data_to_encrypt = "Secret data"
nonce, encrypted_data, hashed_solution = server_setup(difficulty, max_solution, data_to_encrypt)
decrypted_data = client_solve(nonce, encrypted_data, hashed_solution, difficulty, max_solution)

# Assert that the decrypted data matches the original data
assert decrypted_data == data_to_encrypt, "Decryption failed!"

print("Decryption successful! Data matches.")