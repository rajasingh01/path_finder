import argparse
import asyncio
import aiohttp
from urllib.parse import urljoin

DEFAULT_PAYLOADS = [
    "/.htaccess.swp",
    "ca-key.pem",
    "token_auth.csv",
    # Add more payloads here
]

async def check_hidden_path(session, url, path, output_file, show_status_code, show_page_size):
    """
    Asynchronously checks if a given path exists on the website.

    Args:
        session (aiohttp.ClientSession): The aiohttp client session.
        url (str): The base URL of the website.
        path (str): The path to check.
        output_file (str): The path of the output file.
        show_status_code (bool): Whether to display the status code.
        show_page_size (bool): Whether to display the page size.
    """
    try:
        async with session.get(urljoin(url, path)) as response:
            if response.status == 200:
                page_size = len(await response.read())
                if is_valid_path(response.status, page_size):
                    result = f"Found hidden path: {urljoin(url, path)}"
                    if show_status_code:
                        result += f", Status Code: {response.status}"
                    if show_page_size:
                        result += f", Page Size: {page_size} bytes"
                    print(result)
                    with open(output_file, 'a') as file:
                        file.write(result + '\n')
    except Exception as e:
        # Ignore any exceptions
        pass

def is_valid_path(status_code, page_size):
    """
    Checks if a path is valid based on the status code and page size.

    Args:
        status_code (int): The HTTP status code of the response.
        page_size (int): The size of the response body.

    Returns:
        bool: True if the path is valid, False otherwise.
    """
    # Exclude paths with status codes indicating redirection or error
    if status_code >= 300:
        return False
    # Exclude paths with response size less than 100 bytes
    if page_size < 100:
        return False
    return True

async def main():
    parser = argparse.ArgumentParser(description="Find hidden paths on a website.")
    parser.add_argument("url", help="Base URL to check for hidden paths.")
    parser.add_argument("-w", "--payload-list", default="payloads.txt", help="Path to a file containing a list of payloads for hidden paths.")
    parser.add_argument("-sc", "--show-status-code", action="store_true", help="Display the status code of the page.")
    parser.add_argument("-ps", "--show-page-size", action="store_true", help="Display the size of the page.")
    args, unknown_args = parser.parse_known_args()

    url = args.url.rstrip('/')
    payload_list_path = args.payload_list
    show_status_code = args.show_status_code
    show_page_size = args.show_page_size

    try:
        with open(payload_list_path, 'r') as file:
            payloads = [payload.strip() for payload in file.readlines()]
    except FileNotFoundError:
        print("Error: Payload list file not found.")
        return

    print(f"Checking hidden paths at {url}...")

    output_file = "hidden_paths.txt"

    async with aiohttp.ClientSession() as session:
        tasks = []
        for payload in payloads:
            tasks.append(check_hidden_path(session, url, payload, output_file, show_status_code, show_page_size))
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
