import argparse
import asyncio
import aiohttp
from urllib.parse import urljoin

# Default list of payloads to check for hidden paths
DEFAULT_PAYLOADS = [
    "/.htaccess.swp",
    "ca-key.pem",
    "token_auth.csv",
    # Add more payloads here
]

async def check_hidden_path(session, url, path, output_file):
    """
    Asynchronously checks if a given path exists on the website.

    Args:
        session (aiohttp.ClientSession): The aiohttp client session.
        url (str): The base URL of the website.
        path (str): The path to check.
        output_file (str): The path of the output file.
    """
    try:
        async with session.get(urljoin(url, path)) as response:
            if response.status == 200:
                result = f"Found hidden path: {urljoin(url, path)}"
                print(result)
                with open(output_file, 'a') as file:
                    file.write(result + '\n')
    except Exception as e:
        # Ignore any exceptions
        pass

async def main():
    """
    Main function to run the path finder tool.
    """
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Find hidden paths on a website.")
    parser.add_argument("-u", "--url", required=True, help="Base URL to check for hidden paths.")
    parser.add_argument("-w", "--payload-list", default="payloads.txt", help="Path to a file containing a list of payloads for hidden paths.")
    args = parser.parse_args()

    # Extract command-line arguments
    url = args.url.rstrip('/')
    payload_list_path = args.payload_list

    # Read payloads from the specified file
    try:
        with open(payload_list_path, 'r') as file:
            payloads = [payload.strip() for payload in file.readlines()]
    except FileNotFoundError:
        print("Error: Payload list file not found.")
        return

    print(f"Checking hidden paths at {url}...")

    # Output file for saving results
    output_file = "hidden_paths.txt"

    # Create aiohttp client session
    async with aiohttp.ClientSession() as session:
        tasks = []
        # Create tasks to check each payload asynchronously
        for payload in payloads:
            tasks.append(check_hidden_path(session, url, payload, output_file))
        # Run all tasks concurrently
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
