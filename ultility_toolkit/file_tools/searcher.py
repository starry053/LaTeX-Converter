import os
import re
from typing import List, Optional, Tuple

class FileSearcher:
    def __init__(self, target_dir: str):
        if not os.path.isdir(target_dir):
            raise ValueError(f"目录不存在: {target_dir}")
        self.target_dir = target_dir

    def search_by_name(self, keyword: str, case_sensitive: bool = True, ext_filter: Optional[str] = None) -> List[str]:
        result = []
        flags = 0 if case_sensitive else re.IGNORECASE
        reg = re.compile(re.escape(keyword), flags)
        for root, _, files in os.walk(self.target_dir):
            for file in files:
                if ext_filter and not file.endswith(ext_filter):
                    continue
                if reg.search(file):
                    result.append(os.path.join(root, file))
        return result

    def search_by_content(self, keyword: str, case_sensitive: bool = True, ext_filter: Optional[str] = None) -> List[Tuple[str, int]]:
        result = []
        flags = 0 if case_sensitive else re.IGNORECASE
        reg = re.compile(re.escape(keyword), flags)
        for root, _, files in os.walk(self.target_dir):
            for file in files:
                if ext_filter and not file.endswith(ext_filter):
                    continue
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        for line_num, line in enumerate(f, 1):
                            if reg.search(line):
                                result.append((file_path, line_num))
                                break
                except:
                    continue
        return result

    def search_by_size(self, min_size: Optional[int] = None, max_size: Optional[int] = None) -> List[str]:
        result = []
        for root, _, files in os.walk(self.target_dir):
            for file in files:
                file_path = os.path.join(root, file)
                file_size = os.path.getsize(file_path)
                if (min_size is None or file_size >= min_size) and (max_size is None or file_size <= max_size):
                    result.append(file_path)
        return result
