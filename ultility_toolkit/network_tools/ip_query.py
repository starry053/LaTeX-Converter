import requests
import socket
from typing import Dict, Optional, List  # 核心修复：添加 List 导入

class IPQuery:
    """IP地址查询/域名解析工具类"""
    def __init__(self, timeout: int = 5):
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        })

    def _local_ip(self) -> str:
        """获取本机内网IP（备用：公网IP需额外接口）"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            # 连接到公共DNS，仅用于获取本机出口IP，不发送数据
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            return local_ip
        except Exception as e:  # 补全异常捕获的变量名
            print(f"获取本机IP失败，使用默认值：{e}")
            return "127.0.0.1"

    def query(self, ip: Optional[str] = None) -> Dict[str, str]:  # 补全返回值类型注解
        """
        查询IP地址的详细信息
        :param ip: 待查询IP，None则查本机内网IP
        :return: 包含IP信息的字典
        """
        ip = ip or self._local_ip()
        try:
            res = self.session.get(
                url=f"http://ip-api.com/json/{ip}?lang=zh-CN",
                timeout=self.timeout
            )
            res.raise_for_status()  # 触发HTTP状态码异常
            data = res.json()
            
            if data.get("status") != "success":
                return {"错误": data.get("message", "查询失败")}
            
            # 格式化返回结果，避免None值显示异常
            return {
                "查询IP": ip,
                "国家": data.get("country") or "未知",
                "地区": data.get("regionName") or "未知",
                "城市": data.get("city") or "未知",
                "运营商": data.get("isp") or "未知",
                "经纬度": f"{data.get('lat', '未知')},{data.get('lon', '未知')}",
                "时区": data.get("timezone") or "未知",
                "ASN": data.get("as") or "未知"
            }
        except requests.exceptions.RequestException as e:
            return {"错误": f"网络异常: {str(e)}"}
        except Exception as e:
            return {"错误": f"查询失败: {str(e)}"}

    def domain2ip(self, domain: str) -> List[str]:  # 现在List已导入，不会报错
        """
        解析域名对应的IP列表
        :param domain: 待解析域名（如baidu.com）
        :return: IP列表，失败则返回错误信息列表
        """
        try:
            # 获取域名的所有IPv4地址
            ip_list = [info[4][0] for info in socket.getaddrinfo(domain, 80) if info[0] == socket.AF_INET]
            # 去重并返回，避免重复IP
            unique_ips = list(set(ip_list))
            return unique_ips if unique_ips else ["未解析到IP地址"]
        except socket.gaierror as e:
            return [f"域名解析失败: {str(e)}"]
        except Exception as e:
            return [f"错误: {str(e)}"]

# 测试代码（可选，方便调试）
if __name__ == "__main__":
    ipq = IPQuery()
    # 测试IP查询
    print("=== 本机IP信息 ===")
    for k, v in ipq.query().items():
        print(f"{k}: {v}")
    
    # 测试域名解析
    print("\n=== 百度域名解析 ===")
    ips = ipq.domain2ip("baidu.com")
    for ip in ips:
        print(ip)
