/**
 * 主JavaScript文件
 * 处理前端交互逻辑
 */

// API基础URL
const API_BASE_URL = 'http://localhost:5000/api';

/**
 * 上传文件到服务器
 * @param {File} file - 文件对象
 * @param {string} type - 文件类型 (a2, sec, evaluation)
 * @returns {Promise} - 返回Promise对象
 */
async function uploadFile(file, type) {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('type', type);

    try {
        const response = await fetch(`${API_BASE_URL}/upload`, {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        return result;
    } catch (error) {
        console.error('上传文件失败:', error);
        throw error;
    }
}

/**
 * 下载文件
 * @param {string} filename - 文件名
 */
function downloadFile(filename) {
    window.open(`${API_BASE_URL}/download/${filename}`, '_blank');
}

/**
 * 格式化数字
 * @param {number} num - 数字
 * @returns {string} - 格式化后的字符串
 */
function formatNumber(num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

/**
 * 构建树形结构HTML
 * @param {object} tree - 树形数据
 * @returns {string} - HTML字符串
 */
function buildTreeHTML(tree) {
    let html = '<div class="tree-structure">';
    
    for (const field in tree) {
        html += `
            <div class="tree-node field-node">
                <span class="tree-toggle" onclick="toggleNode(this)">▶</span>
                <strong>${field}</strong> (${Object.keys(tree[field]).length}个单元)
            </div>
            <div class="tree-children" style="display: none;">
        `;
        
        for (const unit in tree[field]) {
            const wells = tree[field][unit];
            html += `
                <div class="tree-node unit-node">
                    <span class="tree-toggle" onclick="toggleNode(this)">▶</span>
                    ${unit} (${wells.length}口井)
                </div>
                <div class="tree-children" style="display: none;">
            `;
            
            wells.forEach(well => {
                html += `
                    <div class="tree-node well-node" style="margin-left: 40px;">
                        <span style="color: #999;">●</span> ${well}
                    </div>
                `;
            });
            
            html += '</div>';
        }
        
        html += '</div>';
    }
    
    html += '</div>';
    return html;
}

/**
 * 切换树节点展开/折叠
 * @param {HTMLElement} element - 切换元素
 */
function toggleNode(element) {
    const children = element.parentElement.nextElementSibling;
    if (children && children.classList.contains('tree-children')) {
        const isHidden = children.style.display === 'none';
        children.style.display = isHidden ? 'block' : 'none';
        element.textContent = isHidden ? '▼' : '▶';
    }
}

/**
 * 显示统计卡片
 * @param {object} stats - 统计数据
 * @param {string} containerId - 容器ID
 */
function showStatistics(stats, containerId) {
    const container = document.getElementById(containerId);
    let html = '';
    
    for (const key in stats) {
        const label = getStatLabel(key);
        html += `
            <div class="stat-card">
                <div class="number">${formatNumber(stats[key])}</div>
                <div class="label">${label}</div>
            </div>
        `;
    }
    
    container.innerHTML = html;
}

/**
 * 获取统计标签
 * @param {string} key - 统计键
 * @returns {string} - 标签文本
 */
function getStatLabel(key) {
    const labels = {
        'total': '总井数',
        'evaluated': '参评井数',
        'not_evaluated': '未参评井数',
        'cancelled': '注销井数',
        'new': '新投井数',
        'unit_changed': '单元变化井数',
        'conventional': '常规油井数',
        'shale': '页岩油井数'
    };
    return labels[key] || key;
}

// 导出函数供HTML使用
window.uploadFile = uploadFile;
window.downloadFile = downloadFile;
window.toggleNode = toggleNode;
window.buildTreeHTML = buildTreeHTML;
window.showStatistics = showStatistics;

console.log('main.js加载完成');
