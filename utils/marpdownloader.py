import requests
import os
import zipfile
from settings import settings

def get_latest_release_download_url(username, repository, file_extension):
    api_url = f"https://api.github.com/repos/{username}/{repository}/releases/latest"
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        for asset in data.get("assets", []):
            download_url = asset.get("browser_download_url")
            if download_url and download_url.endswith(file_extension):
                return download_url
    else:
        print(f"Failed to fetch latest release information. Status code: {response.status_code}")

    return None

def download_file(url, file_name):
    response = requests.get(url, stream=True)
    with open(file_name, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)

# Replace these variables with the desired GitHub repository information
def download_marp_cli(force_download=False):
    github_username = "marp-team"
    repo_name = "marp-cli"
    file_extension = "win.zip"  # Replace this with your desired file extension (e.g., "win.zip")

    download_url = get_latest_release_download_url(github_username, repo_name, file_extension)
    if download_url:
        file_name = download_url.split("/")[-1]
        download_version = file_name.split("-")[2]
        current_version = settings.marp_version
        if download_version != current_version or force_download:
            download_file(download_url, file_name)
            with zipfile.ZipFile(file_name, 'r') as zip_ref:
                zip_ref.extractall()
            settings.set_setting("marp_version", download_version)
            os.remove(file_name)

    else:
        raise Exception("Failed to get the download URL for the latest release.")
    
if __name__ == "__main__":
    download_marp_cli(force_download=True)