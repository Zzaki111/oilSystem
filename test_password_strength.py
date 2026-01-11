import re

def validate_password_strength(password):
    """验证密码强度，必须包含小写字母、大写字母、数字和特殊符号中的至少3项"""
    has_lower = bool(re.search(r'[a-z]', password))
    has_upper = bool(re.search(r'[A-Z]', password))
    has_digit = bool(re.search(r'\d', password))
    has_special = bool(re.search(r'[!@#$%^&*(),.?:{}|<>]', password))
    
    conditions = [has_lower, has_upper, has_digit, has_special]
    true_count = sum(conditions)
    
    return true_count >= 3

# 测试各种密码
test_passwords = [
    'weakpass',           # 只有小写，不符合
    'StrongPass',         # 大写+小写，不符合
    'StrongPass123',      # 大写+小写+数字，符合
    'StrongPass!',        # 大写+小写+特殊字符，符合
    'Strong1!',          # 大写+小写+数字+特殊字符，符合
    '12345678',          # 只有数字，不符合
    'StrongPass123!'     # 全部，符合
]

for pwd in test_passwords:
    result = validate_password_strength(pwd)
    print(f'密码: {pwd:15} 强度: {result}')