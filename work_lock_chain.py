import hashlib
import random
import time
import base64
from cryptography.fernet import Fernet

def hash_with_nonce(nonce, solution):
    """Hash the nonce and solution together."""
    return hashlib.sha256(f"{nonce}{solution}".encode()).hexdigest()

def server_setup(difficulty, max_solution, solution_number, data_to_encrypt):
    start_time = time.time()
    # Generate a random nonce
    nonce = random.getrandbits(64)

    # Initialize the solution chain
    solutions = []
    solution_hashes = []
    current_nonce = nonce

    for step in range(solution_number):
        # Randomly select a starting point within the solution space
        start_solution = random.randint(0, max_solution)
        current_max_solution = max_solution
        attempts = 0
        max_attempts = 10  # Fail-safe to prevent infinite loops

        while attempts < max_attempts:
            solution = start_solution
            found = False
            while solution <= current_max_solution:
                hash_result = hash_with_nonce(current_nonce, solution)
                if hash_result.startswith('0' * difficulty):
                    found = True
                    break
                solution += 1

            if found:
                break

            # If no solution found, reduce the upper bound and retry
            current_max_solution = start_solution
            start_solution = random.randint(0, current_max_solution)
            attempts += 1

        if not found:
            raise RuntimeError("Failed to find a solution within the given constraints.")

        # Store the solution and update the nonce for the next step
        solutions.append(solution)
        solution_hashes.append(hashlib.sha256(str(solution).encode()).hexdigest())
        current_nonce = hash_result  # Use the hash as the nonce for the next step

    # Use the final solution as a symmetric key
    final_solution = solutions[-1]
    symmetric_key = hashlib.sha256(str(final_solution).encode()).digest()[:32]  # Use first 32 bytes
    symmetric_key_b64 = base64.urlsafe_b64encode(symmetric_key)  # Base64 encode the key
    fernet = Fernet(symmetric_key_b64)
    encrypted_data = fernet.encrypt(data_to_encrypt.encode())

    print(f"Server setup time: {time.time() - start_time:.6f} seconds")
    return nonce, encrypted_data, solution_hashes

def client_solve(nonce, encrypted_data, solution_hashes, difficulty, max_solution, solution_number):
    start_time = time.time()
    current_nonce = nonce

    for step in range(solution_number):
        # Try to find the solution
        solution = 0
        while True:
            hash_result = hash_with_nonce(current_nonce, solution)
            if hash_result.startswith('0' * difficulty):
                # Verify the solution by comparing hashes
                if hashlib.sha256(str(solution).encode()).hexdigest() == solution_hashes[step]:
                    current_nonce = hash_result  # Update nonce for the next step
                    break
            solution += 1
            if solution > max_solution:
                solution = 0  # Wrap around if exceeding max_solution

    # Use the final solution as a symmetric key
    symmetric_key = hashlib.sha256(str(solution).encode()).digest()[:32]  # Use first 32 bytes
    symmetric_key_b64 = base64.urlsafe_b64encode(symmetric_key)  # Base64 encode the key
    fernet = Fernet(symmetric_key_b64)
    decrypted_data = fernet.decrypt(encrypted_data).decode()

    print(f"Client solve time: {time.time() - start_time:.6f} seconds")
    return decrypted_data


if __name__ == "__main__":
    # Example usage
    difficulty = 4  # Number of leading zeros required in the hash
    max_solution = 1000000  # Upper bound for the solution space
    solution_number = 5  # Number of sequential solutions required
    data_to_encrypt = "Secret data"
    nonce, encrypted_data, solution_hashes = server_setup(difficulty, max_solution, solution_number, data_to_encrypt)
    decrypted_data = client_solve(nonce, encrypted_data, solution_hashes, difficulty, max_solution, solution_number)

    # Assert that the decrypted data matches the original data
    assert decrypted_data == data_to_encrypt, "Decryption failed!"

    print("Decryption successful! Data matches.")