import pandas as pd
import numpy as np
from typing import Dict, List, Optional

class DataAnalyzer:
    def __init__(self, data_file: str):
        self.data_file = data_file
        self.data = self._load_data()

    def _load_data(self) -> pd.DataFrame:
        ext = self.data_file.split('.')[-1].lower()
        if ext == 'csv':
            return pd.read_csv(self.data_file)
        elif ext in ['xlsx', 'xls']:
            return pd.read_excel(self.data_file)
        else:
            raise ValueError("仅支持CSV/Excel格式")

    def basic_stats(self, cols: Optional[List[str]] = None) -> Dict:
        cols = cols or self.data.select_dtypes(include=[np.number]).columns
        stats = self.data[cols].describe().T
        stats['变异系数'] = stats['std'] / stats['mean']
        stats['中位数'] = self.data[cols].median()
        return stats.round(4).to_dict()

    def correlation_analysis(self, method: str = "pearson") -> Dict:
        num_data = self.data.select_dtypes(include=[np.number])
        corr = num_data.corr(method=method)
        return corr.round(4).to_dict()

    def missing_value_analysis(self) -> Dict:
        missing = self.data.isnull().sum()
        missing_rate = (missing / len(self.data)) * 100
        result = {
            "缺失值数量": missing.to_dict(),
            "缺失率(%)": missing_rate.round(2).to_dict()
        }
        return result

    def outlier_detection(self, col: str, method: str = "iqr") -> List:
        if col not in self.data.select_dtypes(include=[np.number]).columns:
            raise ValueError(f"列{col}非数值型")
        data_series = self.data[col].dropna()
        if method == "iqr":
            q1 = data_series.quantile(0.25)
            q3 = data_series.quantile(0.75)
            iqr = q3 - q1
            lower = q1 - 1.5 * iqr
            upper = q3 + 1.5 * iqr
            outliers = data_series[(data_series < lower) | (data_series > upper)].tolist()
        elif method == "zscore":
            z_scores = (data_series - data_series.mean()) / data_series.std()
            outliers = data_series[abs(z_scores) > 3].tolist()
        else:
            raise ValueError("仅支持iqr/zscore方法")
        return outliers
