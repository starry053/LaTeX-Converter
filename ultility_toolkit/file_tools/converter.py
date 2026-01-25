import os
import csv
from typing import Optional, List
from pathlib import Path

class FileConverter:
    def __init__(self, target_file: Optional[str] = None, target_dir: Optional[str] = None):
        self.target_file = target_file if target_file and os.path.isfile(target_file) else None
        self.target_dir = target_dir if target_dir and os.path.isdir(target_dir) else None
        if not self.target_file and not self.target_dir:
            raise ValueError("必须指定目标文件或目标目录")

    def txt2csv(self, delimiter: str = ',', ext_filter: str = ".txt") -> List[str]:
        result = []
        files = [self.target_file] if self.target_file else [f for f in os.listdir(self.target_dir) if f.endswith(ext_filter)]
        for file in files:
            file_path = os.path.join(self.target_dir, file) if self.target_dir else file
            csv_path = os.path.splitext(file_path)[0] + ".csv"
            try:
                with open(file_path, 'r', encoding='utf-8') as f_in, open(csv_path, 'w', encoding='utf-8', newline='') as f_out:
                    writer = csv.writer(f_out, delimiter=delimiter)
                    for line in f_in:
                        writer.writerow(line.strip().split(delimiter))
                result.append(f"成功: {file} -> {os.path.basename(csv_path)}")
            except Exception as e:
                result.append(f"失败: {file} - {str(e)}")
        return result

    def csv2txt(self, delimiter: str = ',', ext_filter: str = ".csv") -> List[str]:
        result = []
        files = [self.target_file] if self.target_file else [f for f in os.listdir(self.target_dir) if f.endswith(ext_filter)]
        for file in files:
            file_path = os.path.join(self.target_dir, file) if self.target_dir else file
            txt_path = os.path.splitext(file_path)[0] + ".txt"
            try:
                with open(file_path, 'r', encoding='utf-8') as f_in, open(txt_path, 'w', encoding='utf-8') as f_out:
                    reader = csv.reader(f_in, delimiter=delimiter)
                    for row in reader:
                        f_out.write(delimiter.join(row) + '\n')
                result.append(f"成功: {file} -> {os.path.basename(txt_path)}")
            except Exception as e:
                result.append(f"失败: {file} - {str(e)}")
        return result

    def batch_change_ext(self, old_ext: str, new_ext: str) -> List[str]:
        if not old_ext.startswith('.'):
            old_ext = '.' + old_ext
        if not new_ext.startswith('.'):
            new_ext = '.' + new_ext
        result = []
        files = [self.target_file] if self.target_file else os.listdir(self.target_dir)
        for file in files:
            if not file.endswith(old_ext):
                continue
            file_path = os.path.join(self.target_dir, file) if self.target_dir else file
            new_file = os.path.splitext(file)[0] + new_ext
            new_path = os.path.join(self.target_dir, new_file) if self.target_dir else new_file
            if os.path.exists(new_path):
                result.append(f"跳过 {file}: 新文件已存在")
                continue
            os.rename(file_path, new_path)
            result.append(f"成功: {file} -> {new_file}")
        return result
