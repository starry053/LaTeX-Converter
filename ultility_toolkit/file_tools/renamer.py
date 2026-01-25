import os
import re
from typing import List, Optional

class FileRenamer:
    def __init__(self, target_dir: str):
        if not os.path.isdir(target_dir):
            raise ValueError(f"目录不存在: {target_dir}")
        self.target_dir = target_dir
        self.file_list = self._get_file_list()

    def _get_file_list(self) -> List[str]:
        return [f for f in os.listdir(self.target_dir) if os.path.isfile(os.path.join(self.target_dir, f))]

    def rename_by_prefix(self, prefix: str, start_num: int = 1, ext_filter: Optional[str] = None) -> List[str]:
        renamed_files = []
        current_num = start_num
        for filename in self.file_list:
            if ext_filter and not filename.endswith(ext_filter):
                continue
            name, ext = os.path.splitext(filename)
            new_filename = f"{prefix}{current_num}{ext}"
            old_path = os.path.join(self.target_dir, filename)
            new_path = os.path.join(self.target_dir, new_filename)
            if os.path.exists(new_path):
                renamed_files.append(f"跳过 {filename}: 新文件名已存在")
                continue
            os.rename(old_path, new_path)
            renamed_files.append(f"成功: {filename} -> {new_filename}")
            current_num += 1
        return renamed_files

    def rename_by_replace(self, old_str: str, new_str: str, case_sensitive: bool = True) -> List[str]:
        renamed_files = []
        flags = 0 if case_sensitive else re.IGNORECASE
        for filename in self.file_list:
            new_filename = re.sub(old_str, new_str, filename, flags=flags)
            if new_filename == filename:
                continue
            old_path = os.path.join(self.target_dir, filename)
            new_path = os.path.join(self.target_dir, new_filename)
            if os.path.exists(new_path):
                renamed_files.append(f"跳过 {filename}: 新文件名已存在")
                continue
            os.rename(old_path, new_path)
            renamed_files.append(f"成功: {filename} -> {new_filename}")
        return renamed_files

    def rename_by_regex(self, pattern: str, repl: str) -> List[str]:
        renamed_files = []
        reg = re.compile(pattern)
        for filename in self.file_list:
            new_filename = reg.sub(repl, filename)
            if new_filename == filename:
                continue
            old_path = os.path.join(self.target_dir, filename)
            new_path = os.path.join(self.target_dir, new_filename)
            if os.path.exists(new_path):
                renamed_files.append(f"跳过 {filename}: 新文件名已存在")
                continue
            os.rename(old_path, new_path)
            renamed_files.append(f"成功: {filename} -> {new_filename}")
        return renamed_files
