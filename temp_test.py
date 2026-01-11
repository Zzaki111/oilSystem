import re

def validate_password_strength(password):
    has_lower = bool(re.search(r'[a-z]', password))
    has_upper = bool(re.search(r'[A-Z]', password))
    has_digit = bool(re.search(r'\d', password))
    has_special = bool(re.search(r'[!@#$%^&*(),.?:{}|<>]', password))
    
    conditions = [has_lower, has_upper, has_digit, has_special]
    true_count = sum(conditions)
    
    return true_count >= 3

# 测试
user_accounts = {
    'admin': 'yangjunOil2026'  # 初始密码
}

print('初始密码:', user_accounts.get('admin'))
print('密码强度测试 - NewStrongPass456@:', validate_password_strength('NewStrongPass456@'))

# 模拟密码修改
old_password = 'yangjunOil2026'
new_password = 'NewStrongPass456@'
username = 'admin'

if username in user_accounts and user_accounts[username] == old_password:
    user_accounts[username] = new_password
    print('密码修改成功')
else:
    print('原密码错误')

print('修改后的密码:', user_accounts.get('admin'))

# 测试新密码是否有效
if username in user_accounts and user_accounts[username] == new_password:
    print('新密码验证成功 - 可以使用新密码登录')
else:
    print('新密码验证失败')

# 测试旧密码是否无效
if username in user_accounts and user_accounts[username] == 'yangjunOil2026':
    print('旧密码仍然有效')
else:
    print('旧密码已失效 - 此为正确行为')
