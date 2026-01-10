"""
第三业务界面服务
生成本年度SEC数据表
"""

import pandas as pd
from typing import Dict, List


class BusinessService3:
    """第三业务界面：生成本年度SEC数据表"""
    
    @staticmethod
    def adjust_sec_unit(
        last_year_sec: pd.DataFrame,
        unit_change_df: pd.DataFrame,
        this_year: int
    ) -> pd.DataFrame:
        """
        调整SEC单元归属
        
        Args:
            last_year_sec: 上年度SEC数据表
            unit_change_df: 单元变化表
            this_year: 本年度年份（4位数字，如2025）
            
        Returns:
            调整后的SEC数据表
        """
        # 复制上年度SEC表
        result_df = last_year_sec.copy()
        
        # 添加本年度SEC油田和SEC单元字段
        this_year_field_col = f"{this_year}SEC油田"
        this_year_unit_col = f"{this_year}SEC单元"
        
        # 先用上年度的SEC归属填充
        result_df[this_year_field_col] = result_df["SEC油田"]
        result_df[this_year_unit_col] = result_df["SEC单元"]
        
        # 根据单元变化表更新归属
        if not unit_change_df.empty:
            for _, change_row in unit_change_df.iterrows():
                well_id = str(change_row["井号"])
                
                # 根据本年度的A2归属推导SEC归属
                # 这里需要有SEC单元的映射关系，暂时先用A2单元作为SEC单元
                new_field = change_row.get("本年度大油田", "")
                new_unit = change_row.get("本年度单元", "")
                
                # 更新对应井的SEC归属
                mask = result_df["井号"] == well_id
                result_df.loc[mask, this_year_field_col] = new_field
                result_df.loc[mask, this_year_unit_col] = new_unit
        
        print(f"调整SEC单元归属完成，共{len(result_df)}口井")
        
        return result_df
    
    @staticmethod
    def add_old_area_new_wells(
        sec_df: pd.DataFrame,
        old_area_new_wells: pd.DataFrame
    ) -> pd.DataFrame:
        """
        导入老区新井
        
        Args:
            sec_df: 当前SEC数据表
            old_area_new_wells: 老区新井数据表
            
        Returns:
            添加老区新井后的SEC数据表
        """
        if old_area_new_wells.empty:
            print("没有老区新井需要添加")
            return sec_df
        
        # 筛选出已标记为"老区新井"的井
        valid_old_area_wells = old_area_new_wells[
            old_area_new_wells["新井类型"] == "老区新井"
        ].copy()
        
        if valid_old_area_wells.empty:
            print("没有有效的老区新井需要添加")
            return sec_df
        
        # 准备要添加的数据（确保字段对齐）
        wells_to_add = valid_old_area_wells.copy()
        
        # 确保有SEC归属字段
        if "SEC油田" not in wells_to_add.columns:
            wells_to_add["SEC油田"] = wells_to_add.get("大油田", "")
        if "SEC单元" not in wells_to_add.columns:
            wells_to_add["SEC单元"] = wells_to_add.get("单元", "")
        
        # 设置参评标志
        wells_to_add["是否参评"] = "是"
        wells_to_add["页岩油/常规"] = wells_to_add.get("页岩油_常规", "常规")
        
        # 确保基本字段存在，以匹配SEC表结构
        required_cols = ["井号", "大油田", "单元", "井别", "井型", "油藏类型", "投产日期", "当前层位", "关闭层位"]
        for col in required_cols:
            if col not in wells_to_add.columns:
                wells_to_add[col] = ""
        
        # 合并数据
        result_df = pd.concat([sec_df, wells_to_add], ignore_index=True)
        
        # 去重（防止重复添加）
        result_df = result_df.drop_duplicates(subset=["井号"], keep="last")
        
        print(f"添加老区新井完成，新增{len(valid_old_area_wells)}口井，总计{len(result_df)}口井")
        
        return result_df
    
    @staticmethod
    def add_pud_pdp_pdnp_wells(
        sec_df: pd.DataFrame,
        pud_pdp_pdnp_df: pd.DataFrame
    ) -> pd.DataFrame:
        """
        导入上年度扩边/PUD转PDP/PDNP井
        
        Args:
            sec_df: 当前SEC数据表
            pud_pdp_pdnp_df: 扩边/PUD转PDP/PDNP数据表
            
        Returns:
            添加扩边/PUD井后的SEC数据表
        """
        if pud_pdp_pdnp_df.empty:
            print("没有扩边/PUD转PDP/PDNP井需要添加")
            return sec_df
        
        # 验证必需字段
        required_fields = ["井号", "SEC油田", "SEC单元"]
        missing_fields = [f for f in required_fields if f not in pud_pdp_pdnp_df.columns]
        
        if missing_fields:
            raise Exception(f"扩边/PUD转PDP/PDNP数据表缺少必需字段: {missing_fields}")
        
        # 检查SEC油田和SEC单元是否有空值
        empty_sec_field = pud_pdp_pdnp_df[
            (pud_pdp_pdnp_df["SEC油田"].isna()) | (pud_pdp_pdnp_df["SEC油田"] == "")
        ]
        empty_sec_unit = pud_pdp_pdnp_df[
            (pud_pdp_pdnp_df["SEC单元"].isna()) | (pud_pdp_pdnp_df["SEC单元"] == "")
        ]
        
        if not empty_sec_field.empty or not empty_sec_unit.empty:
            error_wells = list(empty_sec_field["井号"]) + list(empty_sec_unit["井号"])
            raise Exception(f"以下井的SEC油田或SEC单元为空，请完善: {error_wells}")
                
        # 准备要添加的数据
        wells_to_add = pud_pdp_pdnp_df.copy()
        wells_to_add["是否参评"] = "是"
        
        # 确保基本字段存在，以匹配SEC表结构
        required_cols = ["井号", "大油田", "单元", "井别", "井型", "油藏类型", "投产日期", "当前层位", "关闭层位"]
        for col in required_cols:
            if col not in wells_to_add.columns:
                wells_to_add[col] = ""
        
        # 合并数据
        result_df = pd.concat([sec_df, wells_to_add], ignore_index=True)
        
        # 去重
        result_df = result_df.drop_duplicates(subset=["井号"], keep="last")
                
        print(f"添加扩边/PUD转PDP/PDNP井完成，新增{len(pud_pdp_pdnp_df)}口井，总计{len(result_df)}口井")
                
        return result_df
    
    @staticmethod
    def generate_this_year_sec_table(
        last_year_sec: pd.DataFrame,
        unit_change_df: pd.DataFrame,
        old_area_new_wells: pd.DataFrame,
        pud_pdp_pdnp_df: pd.DataFrame,
        this_year: int,
        this_year_month: int
    ) -> pd.DataFrame:
        """
        生成本年度SEC数据表（完整流程）
        
        Args:
            last_year_sec: 上年度SEC数据表
            unit_change_df: 单元变化表
            old_area_new_wells: 老区新井数据表
            pud_pdp_pdnp_df: 扩边/PUD转PDP/PDNP数据表
            this_year: 本年度年份
            this_year_month: 本年度月份（6位数字，如202509）
            
        Returns:
            本年度SEC数据表
        """
        print(f"\n开始生成{this_year_month}年度SEC数据表...")
        
        # 第一步：调整SEC单元归属
        print("\n步骤1: 调整SEC单元归属")
        result_df = BusinessService3.adjust_sec_unit(last_year_sec, unit_change_df, this_year)
        
        # 第二步：导入老区新井
        print("\n步骤2: 导入老区新井")
        result_df = BusinessService3.add_old_area_new_wells(result_df, old_area_new_wells)
        
        # 第三步：导入扩边/PUD转PDP/PDNP井
        print("\n步骤3: 导入扩边/PUD转PDP/PDNP井")
        result_df = BusinessService3.add_pud_pdp_pdnp_wells(result_df, pud_pdp_pdnp_df)
        
        # 更新年月字段
        result_df["年月"] = this_year_month
        
        print(f"\n生成{this_year_month}年度SEC数据表完成，共{len(result_df)}口井")
        
        return result_df
