# POW-Lock Encryption

Work-Lock Encryption is a proof-of-work based encryption system designed to ensure that the client performs significant computational work to decrypt data encrypted by the server. The server performs minimal work, making it efficient for scenarios where the server needs to offload computational effort to the client.

## Features

- **Minimal Server Work**: The server quickly encrypts data using a symmetric key derived from a computational puzzle.
- **Client-Side Proof-of-Work**: The client must solve a puzzle to derive the symmetric key and decrypt the data.
- **Configurable Difficulty**: The difficulty of the puzzle can be adjusted to control the computational effort required by the client.
- **Work-Lock Chain**: An alternative implementation that mitigates parallel processing by requiring the client to solve a series of sequential puzzles, where each solution is dependent on the previous one. This approach is safer against parallel processing but may be less efficient than the original implementation.

## How It Works

1. **Server Setup**:
   - The server generates a random nonce and selects a random starting point within a defined solution space.
   - It finds a solution that meets a specified difficulty requirement and uses this solution as a symmetric key to encrypt data.
   - The server provides the client with the nonce, encrypted data, and a hash of the solution.

2. **Client Solve**:
   - The client receives the nonce, encrypted data, and the hash of the solution.
   - It performs computational work to find the solution that matches the hash.
   - Once the solution is found, the client uses it as a symmetric key to decrypt the data.

## Usage

### Prerequisites

- Python 3.x
- `cryptography` library (optional, used for Fernet sym encryption in the example)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/work-lock-encryption.git
   cd work-lock-encryption
   ```

2. Install the required Python packages:
   ```bash
   pip install cryptography
   ```

### Running the Code

1. Open `work_lock.py` and adjust the `difficulty` and `max_solution` parameters as needed.
2. Run the script:
   ```bash
   python work_lock.py
   ```

### Configuration

- **Difficulty**: Adjust the `difficulty` parameter to control the number of leading zeros required in the hash. I recommend leaving it at 4, because the time complexity increases exponentially \(O(2^k)\) and becomes nearly impossible for the client. To properly adjust the difficulty, read below.

- **Max Solution**: Set the `max_solution` parameter to define the upper bound for the solution space. "3000000" is recommended, averaging about 0.025 seconds for the server and 1.2 seconds for the client. This should be the value changed to increase the difficulty, due to its linear impact on the resolve time.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## Acknowledgments

- This project uses the `cryptography` library for encryption and decryption.
