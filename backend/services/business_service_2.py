"""
第二业务界面服务
对比本年度与上年度A2表，识别注销井、新投井、归属变化井
"""

import pandas as pd
from typing import Dict, List, Tuple, Set


class BusinessService2:
    """第二业务界面：对比本年度与上年度A2表"""
    
    @staticmethod
    def compare_a2_tables(last_year_a2: pd.DataFrame, this_year_a2: pd.DataFrame) -> Dict[str, pd.DataFrame]:
        """
        对比本年度与上年度A2表，识别各类井
        
        Args:
            last_year_a2: 上年度A2数据表
            this_year_a2: 本年度A2数据表
            
        Returns:
            字典，包含以下键值对：
            - "cancelled_wells": 注销停产或转注井
            - "new_wells": 新投井
            - "unit_changed_wells": 单元归属变化井
        """
        # 确保井号为字符串类型
        last_year_a2["井号"] = last_year_a2["井号"].astype(str)
        this_year_a2["井号"] = this_year_a2["井号"].astype(str)
        
        # 获取井号集合
        last_year_wells = set(last_year_a2["井号"].unique())
        this_year_wells = set(this_year_a2["井号"].unique())
        
        # 1. 识别注销井（上年度有，本年度没有）
        cancelled_well_ids = last_year_wells - this_year_wells
        cancelled_wells_df = last_year_a2[last_year_a2["井号"].isin(cancelled_well_ids)].copy()
        cancelled_wells_df = cancelled_wells_df.drop_duplicates(subset=["井号"])
        
        # 2. 识别新投井（本年度有，上年度没有）
        new_well_ids = this_year_wells - last_year_wells
        new_wells_df = this_year_a2[this_year_a2["井号"].isin(new_well_ids)].copy()
        new_wells_df = new_wells_df.drop_duplicates(subset=["井号"])
        # 添加新井类型字段，默认为空，需要后续人工标注
        new_wells_df["新井类型"] = ""
        
        # 3. 识别单元归属变化井（两表共有，但大油田或单元发生变化）
        common_well_ids = last_year_wells & this_year_wells
        unit_changed_wells = BusinessService2._identify_unit_changed_wells(
            last_year_a2, this_year_a2, common_well_ids
        )
        
        print(f"注销井: {len(cancelled_wells_df)}口")
        print(f"新投井: {len(new_wells_df)}口")
        print(f"单元变化井: {len(unit_changed_wells)}口")
        
        return {
            "cancelled_wells": cancelled_wells_df,
            "new_wells": new_wells_df,
            "unit_changed_wells": unit_changed_wells
        }
    
    @staticmethod
    def _identify_unit_changed_wells(
        last_year_a2: pd.DataFrame, 
        this_year_a2: pd.DataFrame, 
        common_well_ids: Set[str]
    ) -> pd.DataFrame:
        """
        识别单元归属变化的井
        
        Args:
            last_year_a2: 上年度A2数据表
            this_year_a2: 本年度A2数据表
            common_well_ids: 共同井号集合
            
        Returns:
            单元变化井DataFrame
        """
        changed_wells = []
        
        for well_id in common_well_ids:
            # 获取上年度数据（取第一条记录）
            last_year_record = last_year_a2[last_year_a2["井号"] == well_id].iloc[0]
            last_year_field = last_year_record.get("大油田", "")
            last_year_unit = last_year_record.get("单元", "")
            
            # 获取本年度数据（取第一条记录）
            this_year_record = this_year_a2[this_year_a2["井号"] == well_id].iloc[0]
            this_year_field = this_year_record.get("大油田", "")
            this_year_unit = this_year_record.get("单元", "")
            
            # 判断是否发生变化
            field_changed = last_year_field != this_year_field
            unit_changed = last_year_unit != this_year_unit
            
            if field_changed or unit_changed:
                # 构建变化描述
                field_change_desc = ""
                unit_change_desc = ""
                
                if field_changed:
                    field_change_desc = f"{last_year_field}-,{this_year_field}+"
                
                if unit_changed:
                    unit_change_desc = f"{last_year_unit}-,{this_year_unit}+"
                
                changed_wells.append({
                    "井号": well_id,
                    "上年度大油田": last_year_field,
                    "本年度大油田": this_year_field,
                    "上年度单元": last_year_unit,
                    "本年度单元": this_year_unit,
                    "大油田变化": field_change_desc,
                    "单元变化": unit_change_desc,
                    "投产日期": this_year_record.get("投产日期", ""),
                    "油藏类型": this_year_record.get("油藏类型", "")
                })
        
        return pd.DataFrame(changed_wells)
    
    @staticmethod
    def classify_new_wells(
        new_wells_df: pd.DataFrame,
        pud_pdp_pdnp_df: pd.DataFrame = None
    ) -> Dict[str, pd.DataFrame]:
        """
        对新投井进行分类
        
        Args:
            new_wells_df: 新投井DataFrame
            pud_pdp_pdnp_df: 扩边/PUD转PDP/PDNP数据表（当年度）
            
        Returns:
            分类后的字典：
            - "pud_pdp_pdnp_wells": 扩边/PUD转PDP/PDNP井
            - "old_area_new_wells": 老区新井（需要人工确认）
            - "non_evaluated_wells": 不参评井
        """
        # 如果提供了PUD/扩边表，则从新投井中区分出来
        pud_pdp_pdnp_wells = pd.DataFrame()
        remaining_wells = new_wells_df.copy()
        
        if pud_pdp_pdnp_df is not None and not pud_pdp_pdnp_df.empty:
            pud_well_ids = set(pud_pdp_pdnp_df["井号"].astype(str).unique())
            pud_pdp_pdnp_wells = new_wells_df[new_wells_df["井号"].isin(pud_well_ids)].copy()
            remaining_wells = new_wells_df[~new_wells_df["井号"].isin(pud_well_ids)].copy()
        
        # 剩余的井标记为待分类（需要人工标注为"老区新井"或"不参评"）
        old_area_new_wells = remaining_wells.copy()
        old_area_new_wells["新井类型"] = "老区新井"
        
        # 不参评井初始为空，需要人工标注
        non_evaluated_wells = pd.DataFrame()
        
        print(f"扩边/PUD转PDP/PDNP井: {len(pud_pdp_pdnp_wells)}口")
        print(f"老区新井（待确认）: {len(old_area_new_wells)}口")
        
        return {
            "pud_pdp_pdnp_wells": pud_pdp_pdnp_wells,
            "old_area_new_wells": old_area_new_wells,
            "non_evaluated_wells": non_evaluated_wells
        }
    
    @staticmethod
    def get_historical_a2_data(
        well_ids: List[str], 
        a2_tables: List[pd.DataFrame]
    ) -> pd.DataFrame:
        """
        获取指定井号的历史A2数据
        
        Args:
            well_ids: 井号列表
            a2_tables: A2数据表列表（多个月份）
            
        Returns:
            历史数据DataFrame
        """
        # 合并所有A2表
        all_data = pd.concat(a2_tables, ignore_index=True)
        
        # 筛选指定井号
        historical_data = all_data[all_data["井号"].isin(well_ids)].copy()
        
        # 按井号和年月排序
        historical_data = historical_data.sort_values(by=["井号", "年月"])
        
        print(f"获取{len(well_ids)}口井的历史数据，共{len(historical_data)}条记录")
        
        return historical_data
