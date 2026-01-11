"""
Flask后端应用
提供RESTful API接口
"""

from flask import Flask, request, jsonify, send_file, render_template, redirect, url_for, session
from flask_cors import CORS
import os
import sys
import traceback
import pandas as pd
import hashlib
import json

# 添加项目路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.data_io import DataImportExport
from services.business_service_1 import BusinessService1
from services.business_service_2 import BusinessService2
from services.business_service_3 import BusinessService3
from services.business_service_4 import BusinessService4

# 配置路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(BASE_DIR, 'frontend', 'templates')
STATIC_DIR = os.path.join(BASE_DIR, 'frontend', 'static')
INPUT_DIR = os.path.join(BASE_DIR, 'data', 'input')
OUTPUT_DIR = os.path.join(BASE_DIR, 'data', 'output')

app = Flask(__name__, 
            template_folder=TEMPLATE_DIR,
            static_folder=STATIC_DIR)
app.secret_key = 'oil_system_secret_key_2026_for_authentication'
CORS(app)

# 确保目录存在
os.makedirs(INPUT_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 全局缓存数据
cached_data = {}

# 用户账户数据
user_accounts = {
    'admin': 'yangjunOil2026'  # 初始密码
}


@app.route('/')
def index():
    """首页 - 如果未登录则跳转到登录页"""
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')


@app.route('/login')
def login():
    """登录页面"""
    return render_template('login.html')


@app.route('/change_password')
def change_password():
    """修改密码页面"""
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login'))
    return render_template('change_password.html')


@app.route('/api/login', methods=['POST'])
def api_login():
    """登录API接口"""
    try:
        data = request.json
        username = data.get('username')
        password = data.get('password')
        
        # 默认账户验证
        if username in user_accounts and user_accounts[username] == password:
            session['logged_in'] = True
            session['username'] = username
            return jsonify({'success': True, 'message': '登录成功'})
        else:
            return jsonify({'success': False, 'message': '用户名或密码错误'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'登录失败: {str(e)}'})


@app.route('/api/logout', methods=['POST'])
def api_logout():
    """登出API接口"""
    session.pop('logged_in', None)
    session.pop('username', None)
    return jsonify({'success': True, 'message': '已登出'})


@app.route('/api/change_password', methods=['POST'])
def api_change_password():
    """修改密码API接口"""
    try:
        if 'logged_in' not in session or not session['logged_in']:
            return jsonify({'success': False, 'message': '请先登录'})
        
        data = request.json
        username = data.get('username')
        old_password = data.get('old_password')
        new_password = data.get('new_password')
        
        # 验证输入参数
        if not all([username, old_password, new_password]):
            return jsonify({'success': False, 'message': '请填写完整的账户信息'})
        
        # 验证当前登录用户与请求修改的用户是否一致
        if session['username'] != username:
            return jsonify({'success': False, 'message': '无权修改其他用户的密码'})
        
        # 验证原密码是否正确
        if username in user_accounts and user_accounts[username] == old_password:
            # 密码强度验证
            if not validate_password_strength(new_password):
                return jsonify({'success': False, 'message': '新密码必须包含小写字母、大写字母、数字和特殊符号中的至少3项'})
            
            # 更新密码
            user_accounts[username] = new_password
            return jsonify({'success': True, 'message': '密码修改成功'})
        else:
            return jsonify({'success': False, 'message': '原密码错误'})
            
    except Exception as e:
        return jsonify({'success': False, 'message': f'修改密码失败: {str(e)}'})


def validate_password_strength(password):
    """验证密码强度，必须包含小写字母、大写字母、数字和特殊符号中的至少3项"""
    import re
    
    has_lower = bool(re.search(r'[a-z]', password))
    has_upper = bool(re.search(r'[A-Z]', password))
    has_digit = bool(re.search(r'\d', password))
    has_special = bool(re.search(r'[!@#$%^&*(),.?:{}|<>]', password))
    
    conditions = [has_lower, has_upper, has_digit, has_special]
    true_count = sum(conditions)
    
    return true_count >= 3


@app.route('/api/upload', methods=['POST'])
def upload_file():
    """上传文件接口"""
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'message': '没有文件上传'})
        
        file = request.files['file']
        file_type = request.form.get('type', '')
        
        if file.filename == '':
            return jsonify({'success': False, 'message': '文件名为空'})
        
        # 保存文件
        file_path = os.path.join(INPUT_DIR, file.filename)
        file.save(file_path)
        
        # 读取并缓存数据
        if file_type == 'a2':
            df = DataImportExport.read_a2_table(file_path)
        elif file_type == 'sec':
            df = DataImportExport.read_sec_table(file_path)
        elif file_type == 'evaluation':
            df = DataImportExport.read_evaluation_table(file_path)
        elif file_type in ['unit_change', 'new_wells', 'pud_pdp_pdnp']:
            # 单元变化表、老区新井表、PUD转PDP表使用通用读取
            df = DataImportExport.read_excel(file_path)
        elif file_type in ['sec_unit_change', 'historical_prod']:
            # SEC单元变化表、历史生产数据表使用通用读取
            df = DataImportExport.read_excel(file_path)
        else:
            df = DataImportExport.read_excel(file_path)
        
        # 缓存数据
        cache_key = f"{file_type}_{file.filename}"
        cached_data[cache_key] = df
        
        return jsonify({
            'success': True,
            'message': f'文件上传成功，共{len(df)}行数据',
            'cache_key': cache_key,
            'rows': len(df),
            'columns': list(df.columns)
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'上传失败: {str(e)}'})


@app.route('/api/business1/compare', methods=['POST'])
def business1_compare():
    """业务1：对比A2表与SEC表"""
    try:
        data = request.json
        a2_key = data.get('a2_key')
        sec_key = data.get('sec_key')
        year_month = data.get('year_month')
        
        if a2_key not in cached_data or sec_key not in cached_data:
            return jsonify({'success': False, 'message': '数据未找到，请先上传文件'})
        
        a2_df = cached_data[a2_key]
        sec_df = cached_data[sec_key]
        
        # 执行对比
        result_df = BusinessService1.compare_a2_sec_tables(a2_df, sec_df, int(year_month))
        
        # 构建树形结构
        tree = BusinessService1.build_tree_structure(sec_df)
        
        # 保存结果
        output_file = DataImportExport.save_with_timestamp(
            result_df, OUTPUT_DIR, f"{year_month}_油井单元属性表"
        )
        
        # 缓存结果
        cache_key = f"result_business1_{year_month}"
        cached_data[cache_key] = result_df
        
        return jsonify({
            'success': True,
            'message': '对比完成',
            'cache_key': cache_key,
            'output_file': os.path.basename(output_file),
            'tree_structure': tree,
            'statistics': {
                'total': len(result_df),
                'evaluated': len(result_df[result_df['是否参评'] == '是']),
                'not_evaluated': len(result_df[result_df['是否参评'] == '否'])
            }
        })
        
    except Exception as e:
        traceback.print_exc()
        return jsonify({'success': False, 'message': f'处理失败: {str(e)}'})


@app.route('/api/business2/compare', methods=['POST'])
def business2_compare():
    """业务2：对比本年度与上年度A2表"""
    try:
        data = request.json
        last_year_key = data.get('last_year_key')
        this_year_key = data.get('this_year_key')
        year = data.get('year')
        
        if last_year_key not in cached_data or this_year_key not in cached_data:
            return jsonify({'success': False, 'message': '数据未找到，请先上传文件'})
        
        last_year_a2 = cached_data[last_year_key]
        this_year_a2 = cached_data[this_year_key]
        
        # 执行对比
        result = BusinessService2.compare_a2_tables(last_year_a2, this_year_a2)
        
        # 保存结果
        cancelled_file = DataImportExport.save_with_timestamp(
            result['cancelled_wells'], OUTPUT_DIR, f"{year}_注销井"
        )
        new_wells_file = DataImportExport.save_with_timestamp(
            result['new_wells'], OUTPUT_DIR, f"{year}_新投井"
        )
        unit_changed_file = DataImportExport.save_with_timestamp(
            result['unit_changed_wells'], OUTPUT_DIR, f"{year}_SEC单元变化表"
        )
        
        # 缓存结果
        cached_data[f"cancelled_wells_{year}"] = result['cancelled_wells']
        cached_data[f"new_wells_{year}"] = result['new_wells']
        cached_data[f"unit_changed_wells_{year}"] = result['unit_changed_wells']
        
        return jsonify({
            'success': True,
            'message': '对比完成',
            'statistics': {
                'cancelled': len(result['cancelled_wells']),
                'new': len(result['new_wells']),
                'unit_changed': len(result['unit_changed_wells'])
            },
            'output_files': {
                'cancelled': os.path.basename(cancelled_file),
                'new_wells': os.path.basename(new_wells_file),
                'unit_changed': os.path.basename(unit_changed_file)
            }
        })
        
    except Exception as e:
        traceback.print_exc()
        return jsonify({'success': False, 'message': f'处理失败: {str(e)}'})


@app.route('/api/business3/generate', methods=['POST'])
def business3_generate():
    """业务3：生成本年度SEC数据表"""
    try:
        data = request.json
        last_year_sec_key = data.get('last_year_sec_key')
        unit_change_key = data.get('unit_change_key')
        old_area_wells_key = data.get('old_area_wells_key', '')
        pud_pdp_pdnp_key = data.get('pud_pdp_pdnp_key', '')
        this_year = int(data.get('this_year'))
        this_year_month = int(data.get('this_year_month'))
        
        if last_year_sec_key not in cached_data:
            return jsonify({'success': False, 'message': 'SEC数据未找到'})
        
        last_year_sec = cached_data[last_year_sec_key]
        unit_change_df = cached_data.get(unit_change_key, pd.DataFrame())
        old_area_new_wells = cached_data.get(old_area_wells_key, pd.DataFrame())
        pud_pdp_pdnp_df = cached_data.get(pud_pdp_pdnp_key, pd.DataFrame())
        
        # 生成本年度SEC表
        result_df = BusinessService3.generate_this_year_sec_table(
            last_year_sec,
            unit_change_df,
            old_area_new_wells,
            pud_pdp_pdnp_df,
            this_year,
            this_year_month
        )
        
        # 保存结果
        output_file = DataImportExport.save_with_timestamp(
            result_df, OUTPUT_DIR, f"{this_year_month}_SEC数据表"
        )
        
        # 缓存结果
        cache_key = f"sec_table_{this_year_month}"
        cached_data[cache_key] = result_df
        
        return jsonify({
            'success': True,
            'message': 'SEC数据表生成完成',
            'cache_key': cache_key,
            'output_file': os.path.basename(output_file),
            'total_wells': len(result_df)
        })
        
    except Exception as e:
        traceback.print_exc()
        return jsonify({'success': False, 'message': f'处理失败: {str(e)}'})


@app.route('/api/business4/generate_conventional', methods=['POST'])
def business4_generate_conventional():
    """业务4：生成常规油评估数据表"""
    try:
        data = request.json
        
        # 获取所有必需的数据缓存键
        last_year_eval_key = data.get('last_year_eval_key')
        sec_unit_change_key = data.get('sec_unit_change_key')
        historical_prod_data_key = data.get('historical_prod_data_key')
        pud_pdp_pdnp_key = data.get('pud_pdp_pdnp_key')
        old_area_new_wells_key = data.get('old_area_new_wells_key')
        last_year_sec_key = data.get('last_year_sec_key')
        current_year_sec_key = data.get('current_year_sec_key')
        a2_data_key = data.get('a2_data_key')
        
        # 验证必需数据
        required_keys = [last_year_eval_key, sec_unit_change_key, historical_prod_data_key,
                       pud_pdp_pdnp_key, old_area_new_wells_key, last_year_sec_key,
                       current_year_sec_key, a2_data_key]
        if not all(required_keys):
            return jsonify({'success': False, 'message': '缺少必需的输入数据'})
        
        # 从缓存中获取数据
        last_year_eval_df = cached_data.get(last_year_eval_key)
        sec_unit_change_df = cached_data.get(sec_unit_change_key)
        historical_prod_data_df = cached_data.get(historical_prod_data_key)
        pud_pdp_pdnp_df = cached_data.get(pud_pdp_pdnp_key)
        old_area_new_wells_df = cached_data.get(old_area_new_wells_key)
        last_year_sec_df = cached_data.get(last_year_sec_key)
        current_year_sec_df = cached_data.get(current_year_sec_key)
        a2_data_df = cached_data.get(a2_data_key)
        
        if any(df is None for df in [last_year_eval_df, sec_unit_change_df, 
                                   historical_prod_data_df, pud_pdp_pdnp_df,
                                   old_area_new_wells_df, last_year_sec_df,
                                   current_year_sec_df, a2_data_df]):
            return jsonify({'success': False, 'message': '数据未找到，请先上传所有必需的文件'})
        
        # 调用业务服务处理常规油评估数据
        result_df = BusinessService4.process_conventional_oil_evaluation(
            last_year_eval_df,
            sec_unit_change_df,
            historical_prod_data_df,
            pud_pdp_pdnp_df,
            old_area_new_wells_df,
            last_year_sec_df,
            current_year_sec_df,
            a2_data_df
        )
        
        # 保存结果
        output_file = DataImportExport.save_with_timestamp(
            result_df, OUTPUT_DIR, f"常规油评估数据表_本年度"
        )
        
        # 缓存结果
        cache_key = f"conventional_eval_table_{int(pd.Timestamp.now().timestamp())}"
        cached_data[cache_key] = result_df
        
        return jsonify({
            'success': True,
            'message': '常规油评估数据表生成完成',
            'cache_key': cache_key,
            'output_file': os.path.basename(output_file),
            'total_records': len(result_df)
        })
        
    except Exception as e:
        traceback.print_exc()
        return jsonify({'success': False, 'message': f'处理失败: {str(e)}'})


@app.route('/api/business4/generate_shale', methods=['POST'])
def business4_generate_shale():
    """业务4：生成页岩油评估数据表"""
    try:
        data = request.json
        
        # 获取所有必需的数据缓存键
        last_year_shale_eval_key = data.get('last_year_shale_eval_key')
        pud_pdp_pdnp_key = data.get('pud_pdp_pdnp_key')
        a2_data_key = data.get('a2_data_key')
        evaluation_months = data.get('evaluation_months', [])
        
        # 验证必需数据
        required_keys = [last_year_shale_eval_key, pud_pdp_pdnp_key, a2_data_key]
        if not all(required_keys):
            return jsonify({'success': False, 'message': '缺少必需的输入数据'})
        
        # 从缓存中获取数据
        last_year_shale_eval_df = cached_data.get(last_year_shale_eval_key)
        pud_pdp_pdnp_df = cached_data.get(pud_pdp_pdnp_key)
        a2_data_df = cached_data.get(a2_data_key)
        
        if any(df is None for df in [last_year_shale_eval_df, pud_pdp_pdnp_df, a2_data_df]):
            return jsonify({'success': False, 'message': '数据未找到，请先上传所有必需的文件'})
        
        # 调用业务服务处理页岩油评估数据
        result_df = BusinessService4.process_shale_oil_evaluation(
            last_year_shale_eval_df,
            pud_pdp_pdnp_df,
            a2_data_df,
            evaluation_months
        )
        
        # 保存结果
        output_file = DataImportExport.save_with_timestamp(
            result_df, OUTPUT_DIR, f"页岩油评估数据表_本年度"
        )
        
        # 缓存结果
        cache_key = f"shale_eval_table_{int(pd.Timestamp.now().timestamp())}"
        cached_data[cache_key] = result_df
        
        return jsonify({
            'success': True,
            'message': '页岩油评估数据表生成完成',
            'cache_key': cache_key,
            'output_file': os.path.basename(output_file),
            'total_records': len(result_df)
        })
        
    except Exception as e:
        traceback.print_exc()
        return jsonify({'success': False, 'message': f'处理失败: {str(e)}'})


@app.route('/api/download/<filename>')
def download_file(filename):
    """下载文件"""
    try:
        file_path = os.path.join(OUTPUT_DIR, filename)
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        return jsonify({'success': False, 'message': f'下载失败: {str(e)}'})


@app.route('/api/cached_data', methods=['GET'])
def get_cached_data():
    """获取缓存数据列表"""
    data_list = []
    for key, df in cached_data.items():
        data_list.append({
            'key': key,
            'rows': len(df),
            'columns': len(df.columns)
        })
    return jsonify({'success': True, 'data': data_list})


if __name__ == '__main__':
    print(f"数据输入目录: {INPUT_DIR}")
    print(f"数据输出目录: {OUTPUT_DIR}")
    print("启动Flask服务...")
    app.run(host='0.0.0.0', port=5001, debug=False)
