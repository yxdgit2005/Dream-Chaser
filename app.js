
/**
 * 每日感悟 - 核心逻辑
 * 功能：CRUD操作，LocalStorage持久化，UI交互
 */
const app = {
    data: [],
    currentEditId: null,
    deleteTargetId: null,
    selectedMood: '',

    // 初始化
    init() {
        this.loadData();
        this.renderList();
        
        // 设置默认日期为今天
        const today = new Date().toISOString().split('T');
        document.getElementById('edit-date').value = today;
    },

    // 从 LocalStorage 加载数据
    loadData() {
        const stored = localStorage.getItem('daily_thoughts_data');
        if (stored) {
            try {
                this.data = JSON.parse(stored);
                // 按日期倒序排序
                this.data.sort((a, b) => new Date(b.date) - new Date(a.date));
            } catch (e) {
                console.error("数据解析失败", e);
                this.data = [];
            }
        }
    },

    // 保存数据到 LocalStorage
    saveDataToStorage() {
        localStorage.setItem('daily_thoughts_data', JSON.stringify(this.data));
    },

    // 渲染日记列表
    renderList() {
        const container = document.getElementById('diary-list-container');
        const emptyState = document.getElementById('empty-state');
        
        // 清除现有列表项（保留空状态元素）
        Array.from(container.children).forEach(child => {
            if (child.id !== 'empty-state') container.removeChild(child);
        });

        if (this.data.length === 0) {
            emptyState.classList.remove('hidden');
            return;
        } else {
            emptyState.classList.add('hidden');
        }

        this.data.forEach(item => {
            const card = document.createElement('div');
            card.className = 'bg-white p-4 rounded-xl shadow-sm border border-gray-100 fade-in relative group';
            
            // 情绪颜色映射
            let moodColor = 'bg-gray-100 text-gray-500';
            let moodIcon = 'fa-circle';
            if (item.mood === 'happy') { moodColor = 'bg-yellow-100 text-yellow-600'; moodIcon = 'fa-face-smile'; }
            if (item.mood === 'calm') { moodColor = 'bg-blue-100 text-blue-600'; moodIcon = 'fa-face-meh'; }
            if (item.mood === 'sad') { moodColor = 'bg-gray-200 text-gray-600'; moodIcon = 'fa-face-frown'; }
            if (item.mood === 'excited') { moodColor = 'bg-red-100 text-red-600'; moodIcon = 'fa-face-grin-stars'; }

            card.innerHTML = `
                <div class="flex justify-between items-start mb-2">
                    <div class="flex items-center gap-2">
                        <span class="${moodColor} w-8 h-8 rounded-full flex items-center justify-center text-sm">
                            <i class="fa-solid ${moodIcon}"></i>
                        </span>
                        <div>
                            <h3 class="font-bold text-gray-800 text-lg leading-tight">${this.escapeHtml(item.title || '无标题')}</h3>
                            <p class="text-xs text-gray-400 mt-1">${item.date}</p>
                        </div>
                    </div>
                    <div class="flex gap-2 opacity-0 group-hover:opacity-100 transition-opacity duration-200">
                        <button onclick="app.editDiary('${item.id}')" class="text-gray-400 hover:text-primary p-1">
                            <i class="fa-solid fa-pen"></i>
                        </button>
                        <button onclick="app.promptDelete('${item.id}')" class="text-gray-400 hover:text-red-500 p-1">
                            <i class="fa-solid fa-trash"></i>
                        </button>
                    </div>
                </div>
                <p class="text-gray-600 text-sm leading-relaxed whitespace-pre-wrap">${this.escapeHtml(item.content)}</p>
            `;
            
            // 移动端点击卡片也可编辑（除了按钮区域）
            card.addEventListener('click', (e) => {
                if(!e.target.closest('button')) {
                    this.editDiary(item.id);
                }
            });

            container.appendChild(card);
        });
    },

    // 打开编辑器（新建模式）
    openEditor() {
        this.currentEditId = null;
        this.selectedMood = '';
        document.getElementById('modal-title').innerText = '新日记';
        document.getElementById('edit-title').value = '';
        document.getElementById('edit-content').value = '';
        document.getElementById('edit-date').value = new Date().toISOString().split('T');
        this.resetMoodButtons();
        
        const modal = document.getElementById('editor-modal');
        modal.classList.remove('hidden');
        // 聚焦标题
        setTimeout(() => document.getElementById('edit-title').focus(), 100);
    },

    // 打开编辑器（编辑模式）
    editDiary(id) {
        const item = this.data.find(d => d.id === id);
        if (!item) return;

        this.currentEditId = id;
        this.selectedMood = item.mood || '';
        document.getElementById('modal-title').innerText = '编辑日记';
        document.getElementById('edit-title').value = item.title;
        document.getElementById('edit-content').value = item.content;
        document.getElementById('edit-date').value = item.date;
        
        this.highlightMoodButton(this.selectedMood);

        const modal = document.getElementById('editor-modal');
        modal.classList.remove('hidden');
    },

    // 关闭编辑器
    closeEditor() {
        document.getElementById('editor-modal').classList.add('hidden');
    },

    // 保存日记
    saveDiary() {
        const title = document.getElementById('edit-title').value.trim();
        const content = document.getElementById('edit-content').value.trim();
        const date = document.getElementById('edit-date').value;

        if (!content && !title) {
            alert('请至少输入标题或内容');
            return;
        }

        if (this.currentEditId) {
            // 更新现有
            const index = this.data.findIndex(d => d.id === this.currentEditId);
            if (index !== -1) {
                this.data[index] = {
                    ...this.data[index],
                    title,
                    content,
                    date,
                    mood: this.selectedMood,
                    updatedAt: new Date().toISOString()
                };
            }
        } else {
            // 创建新的
            const newDiary = {
                id: Date.now().toString(),
                title,
                content,
                date,
                mood: this.selectedMood,
                createdAt: new Date().toISOString()
            };
            this.data.unshift(newDiary); // 添加到开头
        }

        // 重新排序并保存
        this.data.sort((a, b) => new Date(b.date) - new Date(a.date));
        this.saveDataToStorage();
        this.renderList();
        this.closeEditor();
    },

    // 提示删除
    promptDelete(id) {
        this.deleteTargetId = id;
        document.getElementById('delete-confirm-modal').classList.remove('hidden');
    },

    // 取消删除
    cancelDelete() {
        this.deleteTargetId = null;
        document.getElementById('delete-confirm-modal').classList.add('hidden');
    },

    // 确认删除
    confirmDelete() {
        if (this.deleteTargetId) {
            this.data = this.data.filter(d => d.id !== this.deleteTargetId);
            this.saveDataToStorage();
            this.renderList();
            this.cancelDelete();
        }
    },

    // 选择情绪
    selectMood(mood) {
        this.selectedMood = mood;
        this.highlightMoodButton(mood);
    },

    // 高亮情绪按钮
    highlightMoodButton(mood) {
        this.resetMoodButtons();
        if (!mood) return;
        
        const buttons = document.querySelectorAll('.mood-btn');
        buttons.forEach(btn => {
            if (btn.onclick.toString().includes(mood)) {
                btn.classList.add('ring-2', 'ring-offset-1', 'ring-primary');
                if(mood === 'happy') btn.classList.add('ring-yellow-400');
                if(mood === 'calm') btn.classList.add('ring-blue-400');
                if(mood === 'sad') btn.classList.add('ring-gray-400');
                if(mood === 'excited') btn.classList.add('ring-red-400');
            }
        });
    },

    resetMoodButtons() {
        const buttons = document.querySelectorAll('.mood-btn');
        buttons.forEach(btn => {
            btn.classList.remove('ring-2', 'ring-offset-1', 'ring-primary', 'ring-yellow-400', 'ring-blue-400', 'ring-gray-400', 'ring-red-400');
        });
    },

    // 切换设置面板
    toggleSettings() {
        const modal = document.getElementById('settings-modal');
        modal.classList.toggle('hidden');
    },

    // 导出数据
    exportData() {
        const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(this.data, null, 2));
        const downloadAnchorNode = document.createElement('a');
        downloadAnchorNode.setAttribute("href", dataStr);
        downloadAnchorNode.setAttribute("download", "my_diary_backup.json");
        document.body.appendChild(downloadAnchorNode);
        downloadAnchorNode.click();
        downloadAnchorNode.remove();
    },

    // 清空所有数据
    clearAllData() {
        if(confirm('确定要清空所有日记吗？此操作不可逆。')) {
            this.data = [];
            this.saveDataToStorage();
            this.renderList();
            this.toggleSettings();
        }
    },

    // HTML转义防止XSS
    escapeHtml(text) {
        if (!text) return '';
        return text
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }
};

// 启动应用
document.addEventListener('DOMContentLoaded', () => {
    app.init();
});
