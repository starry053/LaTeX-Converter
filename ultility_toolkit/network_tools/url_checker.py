import requests
from typing import Dict, List, Optional
from urllib.parse import urlparse

class URLChecker:
    def __init__(self, timeout: int = 5):
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })
        self.session.max_redirects = 10

    def check_single(self, url: str) -> Dict:
        if not urlparse(url).scheme:
            url = f"http://{url}"
        try:
            res = self.session.head(url, timeout=self.timeout, allow_redirects=True)
        except:
            res = self.session.get(url, timeout=self.timeout, allow_redirects=True)
        try:
            res.raise_for_status()
            return {
                "URL": url,
                "状态码": res.status_code,
                "最终URL": res.url,
                "响应时间(ms)": round(res.elapsed.total_seconds() * 1000, 2),
                "服务器": res.headers.get("Server", "未知"),
                "状态": "有效"
            }
        except requests.exceptions.RequestException as e:
            return {
                "URL": url,
                "状态": "无效",
                "错误信息": str(e)
            }

    def check_batch(self, urls: List[str]) -> List[Dict]:
        results = []
        for url in urls:
            results.append(self.check_single(url))
        return results

    def is_reachable(self, url: str) -> bool:
        try:
            if not urlparse(url).scheme:
                url = f"http://{url}"
            res = self.session.get(url, timeout=self.timeout, stream=True)
            return res.status_code in [200, 301, 302]
        except:
            return False
