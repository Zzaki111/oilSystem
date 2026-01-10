"""
第一业务界面服务
对比上年度A2表与SEC表，生成油井单元属性表
"""

import pandas as pd
from typing import Dict, List, Tuple


class BusinessService1:
    """第一业务界面：对比A2表与SEC表"""
    
    @staticmethod
    def compare_a2_sec_tables(a2_df: pd.DataFrame, sec_df: pd.DataFrame, year_month: int) -> pd.DataFrame:
        """
        对比上年度A2表与SEC表，生成油井单元属性表
        
        Args:
            a2_df: A2数据表DataFrame
            sec_df: SEC数据表DataFrame
            year_month: 年月，如202409
            
        Returns:
            油井单元属性表DataFrame
        """
        # 创建结果DataFrame
        result_data = []
        
        # 确保井号为字符串类型
        a2_df["井号"] = a2_df["井号"].astype(str)
        sec_df["井号"] = sec_df["井号"].astype(str)
        
        # 获取SEC表中的井号集合
        sec_well_set = set(sec_df["井号"].unique())
        
        # 遍历A2表中的所有井
        for _, row in a2_df.iterrows():
            well_id = str(row["井号"])
            
            # 判断是否参评（是否在SEC表中）
            is_evaluated = "是" if well_id in sec_well_set else "否"
            
            # 获取A2归属
            a2_field = row.get("大油田", "")
            a2_unit = row.get("单元", "")
            
            # 获取SEC归属（如果参评）
            sec_field = ""
            sec_unit = ""
            
            if is_evaluated:
                sec_record = sec_df[sec_df["井号"] == well_id]
                if not sec_record.empty:
                    sec_field = sec_record.iloc[0].get("SEC油田", "")
                    sec_unit = sec_record.iloc[0].get("SEC单元", "")
            
            # 添加记录
            result_data.append({
                "井号": well_id,
                "年月": year_month,
                "是否参评": is_evaluated,
                "A2油田": a2_field,
                "A2单元": a2_unit,
                "SEC油田": sec_field,
                "SEC单元": sec_unit
            })
        
        # 创建结果DataFrame
        result_df = pd.DataFrame(result_data)
        
        # 去重（同一井号可能有多条记录）
        result_df = result_df.drop_duplicates(subset=["井号"])
        
        print(f"生成油井单元属性表完成，共{len(result_df)}口井")
        print(f"参评井: {len(result_df[result_df['是否参评'] == '是'])}口")
        print(f"未参评井: {len(result_df[result_df['是否参评'] == '否'])}口")
        
        return result_df
    
    @staticmethod
    def get_well_sec_mapping(sec_df: pd.DataFrame) -> Dict[str, Tuple[str, str]]:
        """
        获取井号与SEC单元的映射关系
        
        Args:
            sec_df: SEC数据表DataFrame
            
        Returns:
            字典，key为井号，value为(SEC油田, SEC单元)元组
        """
        mapping = {}
        
        for _, row in sec_df.iterrows():
            well_id = str(row["井号"])
            sec_field = row.get("SEC油田", "")
            sec_unit = row.get("SEC单元", "")
            mapping[well_id] = (sec_field, sec_unit)
        
        return mapping
    
    @staticmethod
    def get_a2_sec_unit_mapping(a2_df: pd.DataFrame, sec_df: pd.DataFrame) -> pd.DataFrame:
        """
        获取A2单元与SEC单元的对应关系
        
        Args:
            a2_df: A2数据表DataFrame
            sec_df: SEC数据表DataFrame
            
        Returns:
            单元对应关系表DataFrame
        """
        # 合并A2和SEC数据
        merged_df = pd.merge(
            a2_df[["井号", "大油田", "单元"]],
            sec_df[["井号", "SEC油田", "SEC单元"]],
            on="井号",
            how="inner"
        )
        
        # 按A2单元和SEC单元分组统计
        unit_mapping = merged_df.groupby(["大油田", "单元", "SEC油田", "SEC单元"]).size().reset_index(name="井数")
        
        # 排序
        unit_mapping = unit_mapping.sort_values(by=["SEC油田", "SEC单元", "井数"], ascending=[True, True, False])
        
        print(f"生成单元对应关系表完成，共{len(unit_mapping)}个单元映射")
        
        return unit_mapping
    
    @staticmethod
    def build_tree_structure(sec_df: pd.DataFrame) -> Dict:
        """
        构建评估油田-评估单元-井号三级树形结构
        
        Args:
            sec_df: SEC数据表DataFrame
            
        Returns:
            树形结构字典
        """
        tree = {}
        
        for _, row in sec_df.iterrows():
            sec_field = row.get("SEC油田", "")
            sec_unit = row.get("SEC单元", "")
            well_id = str(row["井号"])
            
            # 初始化油田节点
            if sec_field not in tree:
                tree[sec_field] = {}
            
            # 初始化单元节点
            if sec_unit not in tree[sec_field]:
                tree[sec_field][sec_unit] = []
            
            # 添加井号
            if well_id not in tree[sec_field][sec_unit]:
                tree[sec_field][sec_unit].append(well_id)
        
        # 统计
        total_fields = len(tree)
        total_units = sum(len(units) for units in tree.values())
        total_wells = sum(len(wells) for units in tree.values() for wells in units.values())
        
        print(f"构建树形结构完成: {total_fields}个油田, {total_units}个单元, {total_wells}口井")
        
        return tree
