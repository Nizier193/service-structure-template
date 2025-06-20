from typing import (
    Dict, List, Optional
)
import requests

from core.config import config

class PingAPI():
    def __init__(self) -> None:
        self.baseurl = config.BACKEND_BASEURL

    def ping(self) -> Optional[Dict]:
        url = self.baseurl.rstrip("/") + "/ping"
        response = requests.get(url)

        if response.status_code != 200:
            return None
        
        return response.json()
    
    def get_pings(self, window: int) -> List:
        url = self.baseurl.rstrip("/") + "/ping/list"

        response = requests.get(
            url, params={"size": window}
        )

        if response.status_code != 200:
            return []
        return response.json()