import httpx
from typing import Any, Dict, Optional, List
from .settings import settings

class KeywordComClient:
    def __init__(self, base_url: Optional[str] = None, api_key: Optional[str] = None,
                 auth_scheme: Optional[str] = None, auth_header: Optional[str] = None, timeout: float = 30.0):
        self.base_url = (base_url or settings.KEYWORD_COM_BASE_URL).rstrip("/")
        self.api_key = api_key or settings.KEYWORD_COM_API_KEY
        self.auth_scheme = auth_scheme or settings.KEYWORD_COM_AUTH_SCHEME
        self.auth_header = auth_header or settings.KEYWORD_COM_AUTH_HEADER
        self.timeout = timeout
        self._client = httpx.Client(timeout=timeout)

    def _headers(self) -> Dict[str, str]:
        if self.auth_header.lower() == "authorization":
            return {"Authorization": f"{self.auth_scheme} {self.api_key}"}
        else:
            # Send both, in case the API requires a custom header while also accepting Authorization
            return {self.auth_header: self.api_key, "Authorization": f"{self.auth_scheme} {self.api_key}"}

    def request(self, method: str, path: str, *, params: Dict[str, Any] = None, json: Any = None) -> httpx.Response:
        url = f"{self.base_url}{path}"
        resp = self._client.request(method, url, headers=self._headers(), params=params, json=json)
        resp.raise_for_status()
        return resp

    def list_projects(self) -> List[Dict[str, Any]]:
        path = settings.ENDPOINT_LIST_PROJECTS
        r = self.request("GET", path)
        data = r.json()
        if isinstance(data, dict) and "data" in data:
            return data["data"]
        if isinstance(data, list):
            return data
        return [data]

    def create_project(self, name: str, domain: str, location: str = "United States", search_engine: str = "google.com") -> Dict[str, Any]:
        path = settings.ENDPOINT_CREATE_PROJECT
        payload = {"name": name, "domain": domain, "location": location, "search_engine": search_engine}
        r = self.request("POST", path, json=payload)
        return r.json()

    def list_project_keywords(self, project_id: str) -> List[Dict[str, Any]]:
        path = settings.ENDPOINT_LIST_PROJECT_KEYWORDS.format(project_id=project_id)
        r = self.request("GET", path)
        data = r.json()
        if isinstance(data, dict) and "data" in data:
            return data["data"]
        if isinstance(data, list):
            return data
        return [data]

    def add_keywords(self, project_id: str, keywords: List[str], location: str = "United States", device: str = "desktop") -> Dict[str, Any]:
        path = settings.ENDPOINT_ADD_KEYWORDS.format(project_id=project_id)
        payload = {"keywords": keywords, "location": location, "device": device}
        r = self.request("POST", path, json=payload)
        return r.json()

    def refresh_serp(self, project_id: str) -> Dict[str, Any]:
        path = settings.ENDPOINT_REFRESH_SERP.format(project_id=project_id)
        r = self.request("POST", path)
        return r.json()

    def get_keyword_history(self, keyword_id: str) -> Dict[str, Any]:
        path = settings.ENDPOINT_GET_KEYWORD_HISTORY.format(keyword_id=keyword_id)
        r = self.request("GET", path)
        return r.json()