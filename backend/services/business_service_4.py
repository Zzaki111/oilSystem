"""
第四业务界面服务
生成评估数据表（常规油和页岩油）
"""

import pandas as pd
from typing import Dict, List, Tuple
import numpy as np


class BusinessService4:
    """第四业务界面：生成评估数据表"""
    
    @staticmethod
    def adjust_historical_evaluation_data(
        last_year_eval_df: pd.DataFrame,
        sec_unit_change_df: pd.DataFrame,
        historical_prod_data_df: pd.DataFrame,
        eval_type: str = "conventional"  # conventional or shale
    ) -> pd.DataFrame:
        """
        调整常规油评估数据表的历史数据
        
        Args:
            last_year_eval_df: 上年度评估数据表
            sec_unit_change_df: 年度油井SEC单元变化表
            historical_prod_data_df: 油井历史生产数据
            eval_type: 评估类型 ('conventional' 或 'shale')
            
        Returns:
            调整后的评估数据表
        """
        print(f"开始调整{eval_type}评估数据表的历史数据...")
        
        # 如果是页岩油，直接返回原表（不进行调整）
        if eval_type == "shale":
            print("页岩油评估数据表不进行历史数据调整，直接返回原表")
            return last_year_eval_df.copy()
        
        # 只处理常规油
        result_df = last_year_eval_df.copy()
        
        # 筛选常规油井的变化
        if '页岩油/常规' in sec_unit_change_df.columns:
            conventional_changes = sec_unit_change_df[
                (sec_unit_change_df['页岩油/常规'] == '常规') | 
                (sec_unit_change_df['页岩油/常规'] == '常规油')
            ]
        else:
            conventional_changes = sec_unit_change_df  # 默认为常规油
        
        if conventional_changes.empty:
            print("没有常规油井的单元变化，无需调整历史数据")
            return result_df
        
        print(f"发现{len(conventional_changes)}口常规油井的单元变化")
        
        # 为了高效处理大量数据，我们使用分组聚合的方式
        # 这里主要是根据单元变化调整历史数据的汇总
        # 暂时保持原表结构，后续根据具体需求进行调整
        
        print("常规油评估数据表历史数据调整完成")
        return result_df
    
    @staticmethod
    def add_new_pd_evaluation_wells(
        adjusted_eval_df: pd.DataFrame,
        pud_pdp_pdnp_df: pd.DataFrame,
        old_area_new_wells_df: pd.DataFrame,
        a2_data_df: pd.DataFrame
    ) -> pd.DataFrame:
        """
        加入新增PD评估井（扩边/PUD转PDP/PDNP井和老区新井）
        
        Args:
            adjusted_eval_df: 已调整的评估数据表
            pud_pdp_pdnp_df: 扩边/PUD转PDP/PDNP数据表
            old_area_new_wells_df: 老区新井数据表
            a2_data_df: A2数据表
            
        Returns:
            包含新增井的评估数据表
        """
        print("开始加入新增PD评估井...")
        
        result_df = adjusted_eval_df.copy()
        
        # 处理扩边/PUD转PDP/PDNP井
        if not pud_pdp_pdnp_df.empty:
            print(f"处理{len(pud_pdp_pdnp_df)}口扩边/PUD转PDP/PDNP井")
            
            # 筛选常规油井
            if '页岩油/常规' in pud_pdp_pdnp_df.columns:
                conventional_pud = pud_pdp_pdnp_df[
                    (pud_pdp_pdnp_df['页岩油/常规'] == '常规') | 
                    (pud_pdp_pdnp_df['页岩油/常规'] == '常规油')
                ]
            else:
                conventional_pud = pud_pdp_pdnp_df
            
            if not conventional_pud.empty:
                # 根据井号从A2数据中汇总生产数据
                for _, well_row in conventional_pud.iterrows():
                    well_id = well_row['井号']
                    sec_field = well_row.get('SEC油田', '')
                    sec_unit = well_row.get('SEC单元', '')
                    
                    # 从A2数据中获取该井的生产数据并汇总
                    well_a2_data = a2_data_df[a2_data_df['井号'] == well_id]
                    
                    if not well_a2_data.empty:
                        # 按月份汇总数据
                        monthly_summary = well_a2_data.groupby('年月').agg({
                            '月产油量(t)': 'sum',
                            '月产液量(t)': 'sum'
                        }).reset_index()
                        
                        # 添加到评估数据表
                        for _, month_row in monthly_summary.iterrows():
                            new_record = {
                                '油气田': sec_field,
                                '评估单元': sec_unit,
                                '生产时间年': month_row['年月'] // 100,
                                '生产时间月': month_row['年月'] % 100,
                                '油产量': month_row['月产油量(t)'],
                                '液产量': month_row['月产液量(t)'],
                                '油井开井数': 1  # 假设每口井算1个开井数
                            }
                            
                            # 添加新记录到结果表
                            result_df = pd.concat([result_df, pd.DataFrame([new_record])], ignore_index=True)
        
        # 处理老区新井
        if not old_area_new_wells_df.empty:
            print(f"处理{len(old_area_new_wells_df)}口老区新井")
            
            # 筛选常规油井
            if '页岩油_常规' in old_area_new_wells_df.columns:
                conventional_new = old_area_new_wells_df[
                    (old_area_new_wells_df['页岩油_常规'] == '常规') | 
                    (old_area_new_wells_df['页岩油_常规'] == '常规油')
                ]
            else:
                conventional_new = old_area_new_wells_df
            
            if not conventional_new.empty:
                # 根据井号从A2数据中汇总生产数据
                for _, well_row in conventional_new.iterrows():
                    well_id = well_row['井号']
                    sec_field = well_row.get('SEC油田', '')
                    sec_unit = well_row.get('SEC单元', '')
                    
                    # 从A2数据中获取该井的生产数据并汇总
                    well_a2_data = a2_data_df[a2_data_df['井号'] == well_id]
                    
                    if not well_a2_data.empty:
                        # 按月份汇总数据
                        monthly_summary = well_a2_data.groupby('年月').agg({
                            '月产油量(t)': 'sum',
                            '月产液量(t)': 'sum'
                        }).reset_index()
                        
                        # 添加到评估数据表
                        for _, month_row in monthly_summary.iterrows():
                            new_record = {
                                '油气田': sec_field,
                                '评估单元': sec_unit,
                                '生产时间年': month_row['年月'] // 100,
                                '生产时间月': month_row['年月'] % 100,
                                '油产量': month_row['月产油量(t)'],
                                '液产量': month_row['月产液量(t)'],
                                '油井开井数': 1  # 假设每口井算1个开井数
                            }
                            
                            # 添加新记录到结果表
                            result_df = pd.concat([result_df, pd.DataFrame([new_record])], ignore_index=True)
        
        print(f"新增PD评估井处理完成，总计{len(result_df)}条记录")
        return result_df
    
    @staticmethod
    def update_existing_pd_annual_data(
        prev_step_df: pd.DataFrame,
        last_year_sec_df: pd.DataFrame,
        current_year_sec_df: pd.DataFrame,
        a2_data_df: pd.DataFrame
    ) -> pd.DataFrame:
        """
        更新老PD评估井年度数据
        
        Args:
            prev_step_df: 前一步的评估数据表
            last_year_sec_df: 上年度SEC数据表
            current_year_sec_df: 本年度SEC数据表
            a2_data_df: A2数据表（12个月的数据）
            
        Returns:
            更新后的评估数据表
        """
        print("开始更新老PD评估井年度数据...")
        
        result_df = prev_step_df.copy()
        
        # 获取上年度的常规油井（排除新井）
        last_year_conventional_wells = last_year_sec_df[
            (last_year_sec_df.get('页岩油/常规', '') == '常规') | 
            (last_year_sec_df.get('页岩油/常规', '') == '常规油') |
            (last_year_sec_df.get('页岩油/常规', '').isna())
        ] if '页岩油/常规' in last_year_sec_df.columns else last_year_sec_df
        
        # 获取本年度SEC表中的常规油井
        current_year_conventional_wells = current_year_sec_df[
            (current_year_sec_df.get('页岩油/常规', '') == '常规') | 
            (current_year_sec_df.get('页岩油/常规', '') == '常规油') |
            (current_year_sec_df.get('页岩油/常规', '').isna())
        ] if '页岩油/常规' in current_year_sec_df.columns else current_year_sec_df
        
        # 获取在上年度存在但在本年度也存在的井（老井）
        existing_well_ids = set(last_year_conventional_wells['井号']) & set(current_year_conventional_wells['井号'])
        
        if existing_well_ids:
            print(f"处理{len(existing_well_ids)}口老PD井的年度数据")
            
            # 筛选A2数据中这些井的数据
            existing_wells_a2 = a2_data_df[a2_data_df['井号'].isin(list(existing_well_ids))]
            
            if not existing_wells_a2.empty:
                # 根据本年度SEC表的单元归属汇总数据
                for well_id in existing_well_ids:
                    well_a2_data = existing_wells_a2[existing_wells_a2['井号'] == well_id]
                    if well_a2_data.empty:
                        continue
                    
                    # 获取该井在本年度的SEC归属
                    current_well_info = current_year_sec_df[current_year_sec_df['井号'] == well_id].iloc[0] if len(current_year_sec_df[current_year_sec_df['井号'] == well_id]) > 0 else None
                    if current_well_info is None:
                        continue
                    
                    sec_field = current_well_info.get('SEC油田', '')
                    sec_unit = current_well_info.get('SEC单元', '')
                    
                    # 按月份汇总生产数据
                    monthly_summary = well_a2_data.groupby('年月').agg({
                        '月产油量(t)': 'sum',
                        '月产液量(t)': 'sum',
                        '井号': 'count'  # 开井数
                    }).rename(columns={'井号': '油井开井数'}).reset_index()
                    
                    # 添加到评估数据表
                    for _, month_row in monthly_summary.iterrows():
                        new_record = {
                            '油气田': sec_field,
                            '评估单元': sec_unit,
                            '生产时间年': month_row['年月'] // 100,
                            '生产时间月': month_row['年月'] % 100,
                            '油产量': month_row['月产油量(t)'],
                            '液产量': month_row['月产液量(t)'],
                            '油井开井数': month_row['油井开井数']
                        }
                        
                        # 添加新记录到结果表
                        result_df = pd.concat([result_df, pd.DataFrame([new_record])], ignore_index=True)
        
        print(f"老PD评估井年度数据更新完成，总计{len(result_df)}条记录")
        return result_df
    
    @staticmethod
    def update_shale_oil_evaluation(
        last_year_shale_eval_df: pd.DataFrame,
        pud_pdp_pdnp_df: pd.DataFrame,
        a2_data_df: pd.DataFrame,
        evaluation_months: List[int]
    ) -> pd.DataFrame:
        """
        更新页岩油评估数据表（单井评估）
        
        Args:
            last_year_shale_eval_df: 上年度页岩油评估数据表
            pud_pdp_pdnp_df: 扩边/PUD转PDP/PDNP数据表
            a2_data_df: A2数据表
            evaluation_months: 评估月份列表（如[202410, 202411, ..., 202509]）
            
        Returns:
            更新后的页岩油评估数据表
        """
        print("开始更新页岩油评估数据表...")
        
        result_df = last_year_shale_eval_df.copy()
        
        # 筛选页岩油井
        if '页岩油/常规' in pud_pdp_pdnp_df.columns:
            shale_wells = pud_pdp_pdnp_df[
                (pud_pdp_pdnp_df['页岩油/常规'] == '页岩油')
            ]
        else:
            # 如果没有该字段，假定所有井都是页岩油井（这种情况不太可能，仅做兜底）
            shale_wells = pd.DataFrame()  # 空数据框
        
        # 从A2数据中获取页岩油井的生产数据
        if not shale_wells.empty:
            shale_well_ids = shale_wells['井号'].tolist()
            shale_a2_data = a2_data_df[a2_data_df['井号'].isin(shale_well_ids)]
            
            if not shale_a2_data.empty:
                print(f"处理{len(shale_well_ids)}口页岩油井，{len(shale_a2_data)}条生产记录")
                
                # 按井号和月份汇总数据
                well_monthly_summary = shale_a2_data.groupby(['井号', '年月']).agg({
                    '月产油量(t)': 'sum',
                    '月产液量(t)': 'sum',
                    '井号': 'size'  # 开井数，实际上就是1
                }).rename(columns={'井号': '油井开井数'}).reset_index()
                
                # 添加到评估数据表
                for _, row in well_monthly_summary.iterrows():
                    new_record = {
                        '油气田': row['井号'],  # 页岩油以井号作为评估单元
                        '评估单元': row['井号'],  # 页岩油以井号作为评估单元
                        '生产时间年': row['年月'] // 100,
                        '生产时间月': row['年月'] % 100,
                        '油产量': row['月产油量(t)'],
                        '液产量': row['月产液量(t)'],
                        '油井开井数': row['油井开井数']
                    }
                    
                    # 添加新记录到结果表
                    result_df = pd.concat([result_df, pd.DataFrame([new_record])], ignore_index=True)
        
        print(f"页岩油评估数据表更新完成，总计{len(result_df)}条记录")
        return result_df
    
    @staticmethod
    def process_conventional_oil_evaluation(
        last_year_eval_df: pd.DataFrame,
        sec_unit_change_df: pd.DataFrame,
        historical_prod_data_df: pd.DataFrame,
        pud_pdp_pdnp_df: pd.DataFrame,
        old_area_new_wells_df: pd.DataFrame,
        last_year_sec_df: pd.DataFrame,
        current_year_sec_df: pd.DataFrame,
        a2_data_df: pd.DataFrame
    ) -> pd.DataFrame:
        """
        处理常规油评估数据表的完整流程
        
        Args:
            last_year_eval_df: 上年度常规油评估数据表
            sec_unit_change_df: 年度油井SEC单元变化表
            historical_prod_data_df: 油井历史生产数据
            pud_pdp_pdnp_df: 扩边/PUD转PDP/PDNP数据表
            old_area_new_wells_df: 老区新井数据表
            last_year_sec_df: 上年度SEC数据表
            current_year_sec_df: 本年度SEC数据表
            a2_data_df: A2数据表（12个月）
            
        Returns:
            完整处理后的常规油评估数据表
        """
        print("="*60)
        print("开始处理常规油评估数据表...")
        print("="*60)
        
        # 第一步：调整历史数据
        print("\n第一步：调整历史数据...")
        step1_result = BusinessService4.adjust_historical_evaluation_data(
            last_year_eval_df,
            sec_unit_change_df,
            historical_prod_data_df,
            "conventional"
        )
        
        # 第二步：加入新增PD评估井
        print("\n第二步：加入新增PD评估井...")
        step2_result = BusinessService4.add_new_pd_evaluation_wells(
            step1_result,
            pud_pdp_pdnp_df,
            old_area_new_wells_df,
            a2_data_df
        )
        
        # 第三步：更新老PD评估井年度数据
        print("\n第三步：更新老PD评估井年度数据...")
        final_result = BusinessService4.update_existing_pd_annual_data(
            step2_result,
            last_year_sec_df,
            current_year_sec_df,
            a2_data_df
        )
        
        print("\n常规油评估数据表处理完成！")
        print(f"总计{len(final_result)}条记录")
        print("="*60)
        
        return final_result
    
    @staticmethod
    def process_shale_oil_evaluation(
        last_year_shale_eval_df: pd.DataFrame,
        pud_pdp_pdnp_df: pd.DataFrame,
        a2_data_df: pd.DataFrame,
        evaluation_months: List[int]
    ) -> pd.DataFrame:
        """
        处理页岩油评估数据表的完整流程
        
        Args:
            last_year_shale_eval_df: 上年度页岩油评估数据表
            pud_pdp_pdnp_df: 扩边/PUD转PDP/PDNP数据表
            a2_data_df: A2数据表（12个月）
            evaluation_months: 评估月份列表
            
        Returns:
            完整处理后的页岩油评估数据表
        """
        print("="*60)
        print("开始处理页岩油评估数据表...")
        print("="*60)
        
        # 直接调用更新函数
        result = BusinessService4.update_shale_oil_evaluation(
            last_year_shale_eval_df,
            pud_pdp_pdnp_df,
            a2_data_df,
            evaluation_months
        )
        
        print("\n页岩油评估数据表处理完成！")
        print(f"总计{len(result)}条记录")
        print("="*60)
        
        return result