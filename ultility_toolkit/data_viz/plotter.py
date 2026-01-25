import os
import matplotlib.pyplot as plt
import pandas as pd
from typing import Optional, List, Tuple
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

class DataPlotter:
    def __init__(self, data_file: str):
        if not os.path.isfile(data_file):
            raise FileNotFoundError(f"数据文件不存在: {data_file}")
        self.data_file = data_file
        self.data = self._load_data()

    def _load_data(self) -> pd.DataFrame:
        ext = os.path.splitext(self.data_file)[1].lower()
        if ext == '.csv':
            return pd.read_csv(self.data_file)
        elif ext in ['.xlsx', '.xls']:
            return pd.read_excel(self.data_file)
        else:
            raise ValueError("仅支持CSV/Excel格式数据文件")

    def plot_bar(self, output_path: str = "bar_chart.png", x_col: Optional[str] = None, y_cols: Optional[List[str]] = None, title: str = "柱状图") -> None:
        x_col = x_col or self.data.columns[0]
        y_cols = y_cols or self.data.columns[1:]
        fig, ax = plt.subplots(figsize=(10, 6))
        self.data.plot(kind='bar', x=x_col, y=y_cols, ax=ax)
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.set_xlabel(x_col, fontsize=12)
        ax.set_ylabel("数值", fontsize=12)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(output_path, dpi=300)
        plt.close()

    def plot_line(self, output_path: str = "line_chart.png", x_col: Optional[str] = None, y_cols: Optional[List[str]] = None, title: str = "折线图") -> None:
        x_col = x_col or self.data.columns[0]
        y_cols = y_cols or self.data.columns[1:]
        fig, ax = plt.subplots(figsize=(10, 6))
        self.data.plot(kind='line', x=x_col, y=y_cols, marker='o', ax=ax)
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.set_xlabel(x_col, fontsize=12)
        ax.set_ylabel("数值", fontsize=12)
        plt.xticks(rotation=45, ha='right')
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.savefig(output_path, dpi=300)
        plt.close()

    def plot_pie(self, output_path: str = "pie_chart.png", label_col: str = None, value_col: str = None, title: str = "饼图") -> None:
        label_col = label_col or self.data.columns[0]
        value_col = value_col or self.data.columns[1]
        fig, ax = plt.subplots(figsize=(8, 8))
        self.data.plot(kind='pie', y=value_col, labels=self.data[label_col], autopct='%1.1f%%', ax=ax, legend=False)
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.set_ylabel('')
        plt.tight_layout()
        plt.savefig(output_path, dpi=300)
        plt.close()

    def plot_scatter(self, output_path: str = "scatter_chart.png", x_col: str = None, y_col: str = None, hue_col: Optional[str] = None, title: str = "散点图") -> None:
        x_col = x_col or self.data.columns[0]
        y_col = y_col or self.data.columns[1]
        fig, ax = plt.subplots(figsize=(10, 6))
        if hue_col and hue_col in self.data.columns:
            for hue, group in self.data.groupby(hue_col):
                ax.scatter(group[x_col], group[y_col], label=hue, s=50)
            ax.legend()
        else:
            ax.scatter(self.data[x_col], self.data[y_col], s=50)
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.set_xlabel(x_col, fontsize=12)
        ax.set_ylabel(y_col, fontsize=12)
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.savefig(output_path, dpi=300)
        plt.close()

    def plot_hist(self, output_path: str = "hist_chart.png", col: str = None, bins: int = 10, title: str = "直方图") -> None:
        col = col or self.data.columns[1]
        fig, ax = plt.subplots(figsize=(10, 6))
        self.data[col].plot(kind='hist', bins=bins, ax=ax, edgecolor='black')
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.set_xlabel(col, fontsize=12)
        ax.set_ylabel("频次", fontsize=12)
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.savefig(output_path, dpi=300)
        plt.close()
