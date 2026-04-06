import sys

file_path = r"e:\solar anlyzer\stitch\stitch\user_dashboard.html"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# The string that got duplicated:
duplicate_str = """
    const viewHistoryBtn = document.getElementById('viewHistoryBtn');
    const historyModal = document.getElementById('historyModal');
    const closeHistoryModal = document.getElementById('closeHistoryModal');
    const historyListContainer = document.getElementById('historyListContainer');

    if(viewHistoryBtn) {
        viewHistoryBtn.addEventListener('click', () => {
            historyModal.classList.remove('hidden');
            historyModal.classList.add('flex');
            
            if(!window.dashboardHistory || window.dashboardHistory.length === 0) {
                historyListContainer.innerHTML = '<p class="text-slate-400">No saved history found.</p>';
                return;
            }
            
            historyListContainer.innerHTML = '';
            window.dashboardHistory.forEach((item, index) => {
                const d = new Date(item.createdAt);
                historyListContainer.innerHTML += `
                    <div class="bg-surface-bright/50 border border-primary/20 p-4 rounded-xl flex items-center justify-between hover:border-primary/50 cursor-pointer transition-colors" onclick="loadHistoryItem(${index})">
                        <div>
                            <p class="text-sm font-bold text-white">${d.toLocaleDateString()} ${d.toLocaleTimeString()}</p>
                            <p class="text-xs text-slate-400">${item.detectedAreaM2.toFixed(1)} m² &bull; ${item.systemCapacityKw.toFixed(2)} kW</p>
                        </div>
                        <div class="text-right">
                            <p class="text-eco-green font-bold">$${item.monthlyProfitUsd.toFixed(2)}</p>
                            <p class="text-[10px] text-primary/70 uppercase">Profit/Mo</p>
                        </div>
                    </div>
                `;
            });
        });
    }

    if(closeHistoryModal) {
        closeHistoryModal.addEventListener('click', () => {
            historyModal.classList.add('hidden');
            historyModal.classList.remove('flex');
        });
    }

    window.loadHistoryItem = function(index) {
        if(window.dashboardHistory && window.dashboardHistory[index]) {
            renderResults(window.dashboardHistory[index], true);
            historyModal.classList.add('hidden');
            historyModal.classList.remove('flex');
        }
    }
"""

# replace the first two occurrences with empty string, leaving the 3rd one at the bottom.
content = content.replace(duplicate_str, "", 2)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Duplicates removed!")
