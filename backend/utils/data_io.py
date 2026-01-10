"""
数据导入导出工具
支持Excel文件的读取和写入
"""

import pandas as pd
from typing import Dict, List, Optional, Union
import os
from datetime import datetime


class DataImportExport:
    """数据导入导出类"""
    
    @staticmethod
    def read_excel(file_path: str, sheet_name: Union[str, int] = 0) -> pd.DataFrame:
        """
        读取Excel文件
        
        Args:
            file_path: Excel文件路径
            sheet_name: 工作表名称或索引
            
        Returns:
            DataFrame对象
        """
        try:
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            print(f"成功读取文件: {file_path}, 共{len(df)}行数据")
            return df
        except Exception as e:
            raise Exception(f"读取Excel文件失败: {str(e)}")
    
    @staticmethod
    def write_excel(df: pd.DataFrame, file_path: str, sheet_name: str = "Sheet1") -> None:
        """
        写入Excel文件
        
        Args:
            df: DataFrame对象
            file_path: 输出文件路径
            sheet_name: 工作表名称
        """
        try:
            # 确保输出目录存在
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            # 写入Excel
            with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name=sheet_name, index=False)
            
            print(f"成功写入文件: {file_path}, 共{len(df)}行数据")
        except Exception as e:
            raise Exception(f"写入Excel文件失败: {str(e)}")
    
    @staticmethod
    def read_a2_table(file_path: str) -> pd.DataFrame:
        """
        读取A2数据表
        
        Args:
            file_path: A2表文件路径
            
        Returns:
            DataFrame对象
        """
        df = DataImportExport.read_excel(file_path)
        
        # 验证必需字段
        required_fields = ["井号", "大油田", "单元", "年月", "月产油量(t)"]
        missing_fields = [f for f in required_fields if f not in df.columns]
        
        # 兼容处理：如果没有带单位的字段名，检查是否有不带单位的
        if "月产油量(t)" in missing_fields and "月产油量" in df.columns:
            df["月产油量(t)"] = df["月产油量"]
            missing_fields = [f for f in required_fields if f not in df.columns]
        
        if missing_fields:
            raise Exception(f"A2表缺少必需字段: {missing_fields}")
        
        # 确保井号为字符串类型
        df["井号"] = df["井号"].astype(str)
        
        return df
    
    @staticmethod
    def read_sec_table(file_path: str) -> pd.DataFrame:
        """
        读取SEC数据表
        
        Args:
            file_path: SEC表文件路径
            
        Returns:
            DataFrame对象
        """
        df = DataImportExport.read_excel(file_path)
        
        # 验证必需字段
        required_fields = ["井号", "SEC油田", "SEC单元"]
        missing_fields = [f for f in required_fields if f not in df.columns]
        
        if missing_fields:
            raise Exception(f"SEC表缺少必需字段: {missing_fields}")
        
        # 确保井号为字符串类型
        df["井号"] = df["井号"].astype(str)
        
        return df
    
    @staticmethod
    def read_evaluation_table(file_path: str) -> pd.DataFrame:
        """
        读取评估数据表
        
        Args:
            file_path: 评估表文件路径
            
        Returns:
            DataFrame对象
        """
        df = DataImportExport.read_excel(file_path)
        
        # 验证必需字段
        required_fields = ["油气田", "评估单元", "生产时间年", "生产时间月"]
        missing_fields = [f for f in required_fields if f not in df.columns]
        
        if missing_fields:
            raise Exception(f"评估表缺少必需字段: {missing_fields}")
        
        return df
    
    @staticmethod
    def batch_read_a2_tables(file_paths: List[str]) -> pd.DataFrame:
        """
        批量读取多个A2表并合并
        
        Args:
            file_paths: A2表文件路径列表
            
        Returns:
            合并后的DataFrame
        """
        dfs = []
        for file_path in file_paths:
            df = DataImportExport.read_a2_table(file_path)
            dfs.append(df)
        
        # 合并所有数据
        combined_df = pd.concat(dfs, ignore_index=True)
        
        # 按年月和井号排序
        combined_df = combined_df.sort_values(by=["年月", "井号"])
        
        print(f"成功合并{len(file_paths)}个A2表, 共{len(combined_df)}行数据")
        
        return combined_df
    
    @staticmethod
    def save_with_timestamp(df: pd.DataFrame, base_path: str, prefix: str) -> str:
        """
        保存文件并添加时间戳
        
        Args:
            df: DataFrame对象
            base_path: 基础路径
            prefix: 文件名前缀
            
        Returns:
            保存的文件路径
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"{prefix}_{timestamp}.xlsx"
        file_path = os.path.join(base_path, file_name)
        
        DataImportExport.write_excel(df, file_path)
        
        return file_path
    
    @staticmethod
    def get_year_month_from_filename(filename: str) -> Optional[int]:
        """
        从文件名中提取年月信息
        
        Args:
            filename: 文件名，如 "a2-202309.xlsx" 或 "SEC数据表-202309.xlsx"
            
        Returns:
            年月数字，如 202309，如果提取失败返回None
        """
        import re
        
        # 匹配6位数字的年月
        pattern = r'(\d{6})'
        match = re.search(pattern, filename)
        
        if match:
            return int(match.group(1))
        
        return None
