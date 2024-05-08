import json
from urllib.request import urlretrieve

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings

load_dotenv(".env")


class LoaderSettings(BaseSettings):
    google_url: str = Field(..., alias="AUTH_GOOGLE_CONFIG_URL")


def download_file(url: str) -> str:
    filename = "src/core/configs/" + url.split("/")[2]
    urlretrieve(url, filename)

    return filename


def get_JSON_config(url: str) -> dict[str, str]:
    filename = download_file(url)
    with open(filename) as json_file:
        data = json.load(json_file)
        return data
