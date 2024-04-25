import argparse
import asyncio
import aiohttp
from urllib.parse import urljoin

async def check_hidden_path(session, url, path, output_file):
    try:
        async with session.get(urljoin(url, path)) as response:
            if response.status == 200:
                result = f"Found hidden path: {urljoin(url, path)}"
                print(result)
                with open(output_file, 'a') as file:
                    file.write(result + '\n')
    except Exception as e:
        pass

async def main():
    parser = argparse.ArgumentParser(description="Find hidden paths on a website.")
    parser.add_argument("-u", "--url", required=True, help="Base URL to check for hidden paths.")
    parser.add_argument("-w", "--payload-list", default="payloads.txt", help="Path to a file containing a list of payloads for hidden paths.")
    args = parser.parse_args()

    url = args.url.rstrip('/')
    payload_list_path = args.payload_list

    try:
        with open(payload_list_path, 'r') as file:
            payloads = file.readlines()
            payloads = [payload.strip() for payload in payloads]
    except FileNotFoundError:
        print("Error: Payload list file not found.")
        return

    print(f"Checking hidden paths at {url}...")

    output_file = "hidden_paths.txt"

    async with aiohttp.ClientSession() as session:
        tasks = []
        for payload in payloads:
            tasks.append(check_hidden_path(session, url, payload, output_file))
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
