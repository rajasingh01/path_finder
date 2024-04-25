
# Path Finder

Path Finder is a Python script that helps in finding hidden paths on a website. It utilizes asynchronous requests to check multiple paths concurrently, making the process faster.

## Functionality

- Searches for hidden paths on a website.
- Supports custom payload lists.
- Outputs results to a text file.

## Usage

1. Clone the repository:
git clone https://github.com/your_username/path_finder.git

2. Navigate to the directory:
cd path_finder

3. Run the script:
python3 path_finder.py -u <URL> [-w <payload_list_file>]

- `-u, --url`: Base URL to check for hidden paths.
- `-w, --payload-list`: (Optional) Path to a file containing a list of payloads for hidden paths. Default is `payloads.txt`.
- `-h` : for all functional detail needed.

4. Wait for the script to finish. The results will be saved in a file named `hidden_paths.txt` in the same directory.

## Contribution

Contributions are welcome! If you have any ideas for improvements or new features, feel free to fork the repository and submit a pull request.

Please ensure that your code follows the PEP 8 style guide and includes appropriate documentation.
