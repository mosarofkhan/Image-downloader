import asyncio
import aiofiles
import aiohttp
import os
import sys
from bs4 import BeautifulSoup
from tqdm import tqdm  # Import tqdm

# Define your ASCII art here
ascii_art = '''                                                                                                      
##     ##  #######   ######     ###    ########   #######  ######## ##    ## ##     ##    ###    ##    ##
###   ### ##     ## ##    ##   ## ##   ##     ## ##     ## ##       ##   ##  ##     ##   ## ##   ###   ##
#### #### ##     ## ##        ##   ##  ##     ## ##     ## ##       ##  ##   ##     ##  ##   ##  ####  ##
## ### ## ##     ##  ######  ##     ## ########  ##     ## ######   #####    ######### ##     ## ## ## ##
##     ## ##     ##       ## ######### ##   ##   ##     ## ##       ##  ##   ##     ## ######### ##  ####
##     ## ##     ## ##    ## ##     ## ##    ##  ##     ## ##       ##   ##  ##     ## ##     ## ##   ###
##     ##  #######   ######  ##     ## ##     ##  #######  ##       ##    ## ##     ## ##     ## ##    ##
                         @ Www.mosarofkhan.com
                         @ https://www.facebook.com/shuvo137/
                         @ mosarofkhanshuvo@gmail.com
'''

async def download_image(session, url, folder):
    try:
        async with session.get(url) as response:
            if response.status == 200:
                filename = os.path.join(folder, os.path.basename(url))
                file_size = int(response.headers.get("Content-Length", 0))
                downloaded = 0

                with tqdm(total=file_size, unit="B", unit_scale=True, unit_divisor=1024, file=sys.stdout) as pbar:
                    async with aiofiles.open(filename, "wb") as img_file:
                        while True:
                            chunk = await response.content.read(1024)
                            if not chunk:
                                break
                            await img_file.write(chunk)
                            downloaded += len(chunk)
                            pbar.update(len(chunk))

                print(f"Downloaded: {url}")
            else:
                print(f"Failed to download: {url} (Status Code: {response.status})")
    except Exception as e:
        print(f"Error downloading {url}: {str(e)}")

async def main():
    download_folder = "Download"
    os.makedirs(download_folder, exist_ok=True)

    async with aiohttp.ClientSession() as session:
        with open("Link.txt", "r") as url_file:
            urls = [url.strip() for url in url_file]

        for url in urls:
            try:
                async with session.get(url) as response:
                    if response.status == 200:
                        soup = BeautifulSoup(await response.text(), 'html.parser')
                        header_content_right = soup.find('div', class_='header-content-right')
                        if header_content_right:
                            download_link = header_content_right.find('a', class_='btn btn-download default')
                            if download_link:
                                image_url = download_link.get('href')
                                await download_image(session, image_url, download_folder)
                            else:
                                print(f"Download link not found on {url}.")
                        else:
                            print(f"Header content not found on {url}.")
                    else:
                        print(f"Failed to retrieve the web page {url}. Status code:", response.status)
            except Exception as e:
                print(f"Error accessing {url}: {str(e)}")

    print("Download completed.")

if __name__ == "__main__":
    print(ascii_art)  # Display the ASCII art
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
