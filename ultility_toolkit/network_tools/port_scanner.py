import socket
import threading
from typing import List, Tuple, Optional
from queue import Queue

class PortScanner:
    def __init__(self, host: str, timeout: float = 0.5):
        self.host = host
        self.timeout = timeout
        self.open_ports = []
        self.queue = Queue()
        self.lock = threading.Lock()

    def _scan_port(self, port: int):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(self.timeout)
                result = s.connect_ex((self.host, port))
                if result == 0:
                    with self.lock:
                        self.open_ports.append(port)
        except:
            pass

    def _worker(self):
        while not self.queue.empty():
            port = self.queue.get()
            self._scan_port(port)
            self.queue.task_done()

    def scan(self, start_port: int = 1, end_port: int = 1024, threads: int = 50) -> List[int]:
        if not (1 <= start_port <= end_port <= 65535):
            raise ValueError("端口范围必须1-65535，且start_port≤end_port")
        for port in range(start_port, end_port + 1):
            self.queue.put(port)
        for _ in range(threads):
            t = threading.Thread(target=self._worker, daemon=True)
            t.start()
        self.queue.join()
        self.open_ports.sort()
        return self.open_ports

    def scan_common_ports(self) -> List[Tuple[int, str]]:
        common_ports = {
            21: "FTP", 22: "SSH", 23: "Telnet", 80: "HTTP", 443: "HTTPS",
            3306: "MySQL", 6379: "Redis", 27017: "MongoDB", 8080: "Tomcat"
        }
        self.scan(1, 65535, 100)
        return [(p, common_ports.get(p, "未知服务")) for p in self.open_ports]
