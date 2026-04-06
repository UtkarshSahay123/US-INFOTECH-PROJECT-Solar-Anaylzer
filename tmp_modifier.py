import sys

file_path = r"e:\solar anlyzer\stitch\stitch\user_dashboard.html"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Replace the button
old_btn = '<button class="text-primary/50 text-xs font-bold uppercase tracking-widest cursor-not-allowed">View History</button>'
new_btn = '<button id="viewHistoryBtn" class="text-primary text-xs font-bold uppercase tracking-widest cursor-pointer hover:text-white transition-colors">View History</button>'
content = content.replace(old_btn, new_btn)

# 2. Inject Modal HTML just above <!-- Upload choice modal -->
modal_html = """
<!-- History Modal -->
<div id="historyModal" class="fixed inset-0 bg-black/60 backdrop-blur-sm shadow-2xl z-[100] hidden items-center justify-center">
    <div class="bg-surface border border-primary/20 p-8 rounded-2xl flex flex-col w-full max-w-2xl max-h-[80vh] mx-4 relative overflow-hidden">
        <button id="closeHistoryModal" class="absolute top-4 right-4 text-slate-400 hover:text-white"><span class="material-icons">close</span></button>
        <h3 class="text-xl font-bold text-white mb-6">Your Calculation History</h3>
        
        <div id="historyListContainer" class="flex flex-col gap-4 overflow-y-auto custom-scrollbar flex-1 pr-2">
            <!-- Items injected by JS -->
        </div>
    </div>
</div>

"""
content = content.replace('<!-- Upload choice modal -->', modal_html + '<!-- Upload choice modal -->')

# 3. Augment the existing DOMContentLoaded fetch to store history to window.dashboardHistory
old_fetch = """                    const history = await response.json();
                    if (history && history.length > 0) {
                        renderResults(history[0], true); // Pass true to indicate this is history
                    }"""
new_fetch = """                    const history = await response.json();
                    if (history && history.length > 0) {
                        window.dashboardHistory = history;
                        renderResults(history[0], true); // Pass true to indicate this is history
                    }"""
content = content.replace(old_fetch, new_fetch)

# 4. Append JS history logic before </script>
js_logic = """
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
content = content.replace('</script>', js_logic + '\n</script>')

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("History Logic and UI successfully deployed!")
