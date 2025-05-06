import requests
from tqdm import tqdm
from pathlib import Path
import platform
import zipfile

CHROME_DRIVER = {
    "linux": "chromedriver_linux64.zip",
    "darwin": "chromedriver_mac64.zip",
    "darwin_arm64": "chromedriver_mac_arm64.zip",
    "win32": "chromedriver_win32.zip",
}

CHROME_DRIVER_EXEC = {
    "linux": "chromedriver.exe",
    "darwin": "chromedriver",
    "darwin_arm64": "chromedriver",
    "win32": "chromedriver",
}


USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; WOW64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.6788.76 Safari/537.36"


def get_driver():
    os_name = platform.system().lower()

    if os_name == "linux":
        return CHROME_DRIVER["linux"], CHROME_DRIVER_EXEC["linux"]
    elif os_name == "windows":
        return CHROME_DRIVER["win32"], CHROME_DRIVER_EXEC["win32"]
    elif os_name == "darwin":
        # Check for macOS architecture (x86_64 or arm64)
        arch = platform.machine().lower()
        if "arm64" in arch or "aarch64" in arch:
            return CHROME_DRIVER["darwin_arm64"], CHROME_DRIVER_EXEC["darwin_arm64"]
        else:
            return CHROME_DRIVER["darwin"], CHROME_DRIVER_EXEC["darwin"]
    else:
        raise ValueError("could not determine os type")


def download_file(url, path, chuck_size=1024):
    chuck_size = chuck_size

    # download url use requests with tqdm
    with requests.get(
        url,
        headers={
            "User-Agent": USER_AGENT,
        },
        stream=True,
    ) as r:
        with tqdm(
            total=int(r.headers.get("content-length")),
            unit="B",
            unit_scale=True,
            unit_divisor=chuck_size,
        ) as pbar:
            with open(path, "wb") as f:
                for data in r.iter_content(
                    chunk_size=chuck_size,
                ):
                    f.write(data)
                    pbar.update(len(data))


def unzip_file(path, out_dir):
    out_dir = Path(out_dir)
    path = Path(path)
    out_dir.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(path, "r") as zip_ref:
        zip_ref.extractall(out_dir)


if __name__ == "__main__":
    base_url = "https://chromedriver.storage.googleapis.com/114.0.5735.90"
    driver_dir = Path(__file__).parent / "chromedriver"

    driver_dir.mkdir(exist_ok=True)

    # check os
    driver, _ = get_driver()

    # download
    download_file(f"{base_url}/{driver}", driver_dir / driver)
    # unzip file
    unzip_file(driver_dir / driver, driver_dir)
    pass
