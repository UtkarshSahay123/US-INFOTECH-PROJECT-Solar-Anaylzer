import sys

file_path = r"e:\solar anlyzer\stitch\stitch\user_dashboard.html"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Replace the history tile HTML construction
old_loop_content = """                        <div class="text-right">
                            <p class="text-eco-green font-bold">$${item.monthlyProfitUsd.toFixed(2)}</p>
                            <p class="text-[10px] text-primary/70 uppercase">Profit/Mo</p>
                        </div>
                    </div>"""
new_loop_content = """                        <div class="text-right flex items-center gap-4">
                            <div>
                                <p class="text-eco-green font-bold">$${item.monthlyProfitUsd.toFixed(2)}</p>
                                <p class="text-[10px] text-primary/70 uppercase">Profit/Mo</p>
                            </div>
                            <button onclick="window.deleteHistoryItem(${item.id}, event)" class="text-slate-500 hover:text-red-500 p-2 rounded-full hover:bg-red-500/10 transition-colors">
                                <span class="material-icons text-sm">delete</span>
                            </button>
                        </div>
                    </div>"""
content = content.replace(old_loop_content, new_loop_content)

# Add the frontend `deleteHistoryItem` JS function
js_delete_logic = """
    window.deleteHistoryItem = async function(id, event) {
        event.stopPropagation(); // prevent modal from closing or loading item
        const token = localStorage.getItem('token');
        if (token) {
            try {
                const res = await fetch(`http://localhost:8080/api/dashboard/history/${id}`, {
                    method: 'DELETE',
                    headers: { 'Authorization': 'Bearer ' + token }
                });
                if (res.ok) {
                    // Update the array and re-render the modal seamlessly
                    window.dashboardHistory = window.dashboardHistory.filter(item => item.id !== id);
                    if(window.dashboardHistory.length === 0) {
                        historyListContainer.innerHTML = '<p class="text-slate-400">No saved history found.</p>';
                        return;
                    }
                    
                    historyListContainer.innerHTML = '';
                    window.dashboardHistory.forEach((item, index) => {
                        const d = new Date(item.createdAt);
                        const noteSnippet = item.userComment ? `<p class="text-[10px] text-primary/80 truncate max-w-[200px] mt-1 bg-primary/10 px-2 py-0.5 rounded italic">"${item.userComment}"</p>` : '';
                        historyListContainer.innerHTML += `
                            <div class="bg-surface-bright/50 border border-primary/20 p-4 rounded-xl flex items-center justify-between hover:border-primary/50 cursor-pointer transition-colors" onclick="loadHistoryItem(${index})">
                                <div>
                                    <p class="text-sm font-bold text-white">${d.toLocaleDateString()} ${d.toLocaleTimeString()}</p>
                                    <p class="text-xs text-slate-400">${item.detectedAreaM2.toFixed(1)} m² &bull; ${item.systemCapacityKw.toFixed(2)} kW</p>
                                    ${noteSnippet}
                                </div>
                                <div class="text-right flex items-center gap-4">
                                    <div>
                                        <p class="text-eco-green font-bold">$${item.monthlyProfitUsd.toFixed(2)}</p>
                                        <p class="text-[10px] text-primary/70 uppercase">Profit/Mo</p>
                                    </div>
                                    <button onclick="window.deleteHistoryItem(${item.id}, event)" class="text-slate-500 hover:text-red-500 p-2 rounded-full hover:bg-red-500/10 transition-colors">
                                        <span class="material-icons text-sm">delete</span>
                                    </button>
                                </div>
                            </div>
                        `;
                    });
                } else {
                    alert("Failed to delete item from database.");
                }
            } catch(e) {
                alert("Network error: Failed to delete.");
            }
        }
    }
</script>
"""
content = content.replace("</script>", js_delete_logic, 1)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Dashboard delete operations wired!")
