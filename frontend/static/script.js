 
function showNotification(message, type = 'info', callback = null) {
    
    const existing = document.getElementById('app-notification');
    if (existing) existing.remove();
    const notification = document.createElement('div');
    notification.id = 'app-notification';
    notification.className = `notification notification-${type}`;
    
    const icon = type === 'success' ? '✓' : 
                 type === 'error' ? '✕' : 
                 type === 'warning' ? '⚠' : 
                 'ℹ';
    
    notification.innerHTML = `
        <span class="notification-icon">${icon}</span>
        <span class="notification-message">${message}</span>
        <button class="notification-close" onclick="this.parentElement.remove()">×</button>
    `;
    
    document.body.appendChild(notification);
    
    // Animate in
    setTimeout(() => notification.classList.add('show'), 10);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => notification.remove(), 300);
    }, 5000);
    
    // Execute callback if provided
    if (callback) callback();
}
 
function showConfirm(message, onConfirm, onCancel = null) {
    // Remove existing modal if any
    const existing = document.getElementById('app-confirm-modal');
    if (existing) existing.remove();
 
    // Create modal
    const modal = document.createElement('div');
    modal.id = 'app-confirm-modal';
    modal.className = 'confirm-modal';
    
    modal.innerHTML = `
        <div class="confirm-overlay" onclick="document.getElementById('app-confirm-modal').remove(); ${onCancel ? 'cancelAction()' : ''}"></div>
        <div class="confirm-box">
            <div class="confirm-icon">⚠</div>
            <div class="confirm-message">${message}</div>
            <div class="confirm-buttons">
                <button class="confirm-btn confirm-cancel" onclick="document.getElementById('app-confirm-modal').remove(); ${onCancel ? 'cancelAction()' : ''}">Cancel</button>
                <button class="confirm-btn confirm-yes" onclick="confirmAction()">Continue</button>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    
    // Set up action handlers
    window.confirmAction = () => {
        modal.remove();
        if (onConfirm) onConfirm();
        delete window.confirmAction;
        delete window.cancelAction;
    };
    
    window.cancelAction = () => {
        modal.remove();
        if (onCancel) onCancel();
        delete window.confirmAction;
        delete window.cancelAction;
    };
    
    // Animate in
    setTimeout(() => modal.classList.add('show'), 10);
}
 
// Add styles dynamically
const notificationStyles = document.createElement('style');
notificationStyles.textContent = `
    .notification {
        position: fixed;
        top: 20px;
        right: 20px;
        background: white;
        padding: 16px 20px;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        display: flex;
        align-items: center;
        gap: 12px;
        max-width: 400px;
        z-index: 10000;
        opacity: 0;
        transform: translateX(400px);
        transition: all 0.3s ease;
    }
    
    .notification.show {
        opacity: 1;
        transform: translateX(0);
    }
    
    .notification-success {
        border-left: 4px solid #4CAF50;
    }
    
    .notification-error {
        border-left: 4px solid #f44336;
    }
    
    .notification-warning {
        border-left: 4px solid #ff9800;
    }
    
    .notification-info {
        border-left: 4px solid #2196F3;
    }
    
    .notification-icon {
        font-size: 20px;
        font-weight: bold;
    }
    
    .notification-success .notification-icon {
        color: #4CAF50;
    }
    
    .notification-error .notification-icon {
        color: #f44336;
    }
    
    .notification-warning .notification-icon {
        color: #ff9800;
    }
    
    .notification-info .notification-icon {
        color: #2196F3;
    }
    
    .notification-message {
        flex: 1;
        color: #333;
        font-size: 14px;
    }
    
    .notification-close {
        background: none;
        border: none;
        font-size: 24px;
        color: #999;
        cursor: pointer;
        padding: 0;
        width: 24px;
        height: 24px;
        line-height: 20px;
    }
    
    .notification-close:hover {
        color: #333;
    }
    
    .confirm-modal {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        z-index: 10001;
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .confirm-modal.show {
        opacity: 1;
    }
    
    .confirm-overlay {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0,0,0,0.5);
    }
    
    .confirm-box {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background: white;
        padding: 30px;
        border-radius: 12px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.3);
        max-width: 400px;
        width: 90%;
        text-align: center;
    }
    
    .confirm-icon {
        font-size: 48px;
        margin-bottom: 15px;
        color: #ff9800;
    }
    
    .confirm-message {
        font-size: 16px;
        color: #333;
        margin-bottom: 25px;
        line-height: 1.5;
        white-space: pre-line;
    }
    
    .confirm-buttons {
        display: flex;
        gap: 10px;
        justify-content: center;
    }
    
    .confirm-btn {
        padding: 10px 24px;
        border: none;
        border-radius: 6px;
        font-size: 14px;
        cursor: pointer;
        transition: all 0.2s;
        font-weight: 500;
    }
    
    .confirm-cancel {
        background: #e0e0e0;
        color: #333;
    }
    
    .confirm-cancel:hover {
        background: #d0d0d0;
    }
    
    .confirm-yes {
        background: #000000;
        color: white;
    }
    
    .confirm-yes:hover {
        background: #5D4037;
    }
    
    @media (max-width: 600px) {
        .notification {
            right: 10px;
            left: 10px;
            max-width: none;
        }
    }
`;
document.head.appendChild(notificationStyles);
 
 
// ============================================
// MAIN APPLICATION CODE
// ============================================
 
document.addEventListener('DOMContentLoaded', () => {
    /* home travel bar */
 
    async function loadHomeTravelBar() {
        const res = await fetch("/travel_goals");
        const data = await res.json();
 
        if (data.length === 0) {
            updateUI(0, 0);
            return;
        }
 
        const goal = data[0];
 
        const homeSaved = goal.saved_amount;
        const homeGoal = goal.target_amount;
        
        const percent = homeGoal > 0 ? Math.min((homeSaved / homeGoal) * 100, 100) : 0;
        const remaining = Math.max(homeGoal - homeSaved, 0);
 
        const homeBar = document.getElementById("homeTravelProgress");
        const homePercent = document.getElementById("homeTravelPercent");
        const homeSavedText = document.getElementById("homeGoalSaved");
        const homeLeftText = document.getElementById("homeGoalLeft");
        const homeRemainingText = document.getElementById("homeGoalRemainingText");
 
        if (homeBar) homeBar.style.width = percent + "%";
        if (homePercent) homePercent.textContent = percent.toFixed(1) + "%";
        if (homeSavedText) homeSavedText.textContent = "$" + homeSaved.toFixed(0);
        if (homeLeftText) homeLeftText.textContent = "$" + remaining.toFixed(0);
        if (homeRemainingText) homeRemainingText.textContent = "$" + remaining.toFixed(0) + " left";
    }
 
    loadHomeTravelBar();
 
 
    /* travel pg */
 
    const goalInput = document.getElementById("goalAmount");
    const contributionInput = document.getElementById("contributionAmount");
    const addBtn = document.getElementById("addBtn");
    const setBtn = document.getElementById("setGoalBtn");
    const resetBtn = document.getElementById("resetGoal");
    const goalMsg = document.getElementById("goalMessage");
    const contributionMsg = document.getElementById("contributionMessage");
 
    let currentGoalId = null;
    let savedGoal = 0;
 
    async function loadTravelGoal() {
        const res = await fetch("/travel_goals");
        const data = await res.json();
 
        if (data.length === 0) {
            currentGoalId = null;
            updateUI(0, 0);
            return;
        }
 
        const goal = data[0];
 
        currentGoalId = goal.id;
        savedGoal = goal.target_amount;
 
        if (goalInput) goalInput.value = savedGoal;
 
        updateUI(goal.saved_amount, goal.target_amount);
    }
 
    if (goalInput) loadTravelGoal();
 
 
    /* set goal */
 
    if (setBtn) {
        setBtn.addEventListener("click", async () => {
 
            const goal = parseFloat(goalInput.value);
 
            if (!goal || goal <= 0) {
                goalMsg.textContent = "Enter a valid goal.";
                goalMsg.style.color = "red";
                return;
            }
 
           if (goal > 10000) {
                showConfirm(
                    "This goal exceeds $10,000. Are you sure you want to continue?",
                    async () => {
                        await saveGoal(goal);
                        goalMsg.textContent = "Goal set.";
                        goalMsg.style.color = "orange";
                    }
                );
                return;
            }
 
            await saveGoal(goal);
        });
    }
 
    async function saveGoal(goal) {
        goalMsg.textContent = "";
 
        await fetch("/travel_goal", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                destination: "My Trip",
                target_amount: goal
            })
        });
 
        loadTravelGoal();
        loadHomeTravelBar();
    }
 
 
    /* add contribution */
 
    if (addBtn) {
        addBtn.addEventListener("click", async () => {
 
            const contribution = parseFloat(contributionInput.value);
 
            if (!contribution || contribution <= 0) {
                contributionMsg.textContent = "Enter a valid contribution.";
                contributionMsg.style.color = "red";
                return;
            }
 
            if (!currentGoalId) {
                contributionMsg.textContent = "Please set a goal first.";
                contributionMsg.style.color = "red";
                return;
            }
 
            if (contribution > savedGoal) {
                contributionMsg.textContent = "Cannot exceed goal amount.";
                contributionMsg.style.color = "red";
                return;
            }
 
            if (contribution > savedGoal / 2) {
                showConfirm(
                    "This contribution is more than 50% of your goal. Continue?",
                    async () => {
                        await saveContribution(contribution);
                        contributionMsg.textContent = "Contribution added.";
                        contributionMsg.style.color = "orange";
                    }
                );
                return;
            }
 
            await saveContribution(contribution);
        });
    }
 
    async function saveContribution(contribution) {
        contributionMsg.textContent = "";
 
        await fetch("/travel_goal/save", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                id: currentGoalId,
                amount: contribution
            })
        });
 
        loadTravelGoal();
        loadHomeTravelBar();
 
        contributionInput.value = "";
    }
 
 
    /* reset goal */
 
    if (resetBtn) {
        resetBtn.addEventListener("click", async () => {
 
            showConfirm(
                "Are you sure you want to reset your travel goal? This action cannot be undone.",
                async () => {
                    await fetch("/travel_goal/reset", {
                        method: "POST"
                    });
 
                    loadTravelGoal();
                    loadHomeTravelBar();
                    showNotification("Travel goal has been reset.", "info");
                }
            );
        });
    }
 
 
    /* budget page */
 
    const categoryTable = document.getElementById("categoryTable");
 
    if (categoryTable) {
        loadCategories();
        loadRecentPurchases();
    }
 
    const recentList = document.getElementById("recentPurchases");
 
    if (recentList) {
        loadRecentPurchases();
    }
 
});
 
 
/* limit */
 
async function setCategoryLimit() {
 
    const category = document.getElementById("limitCategory")?.value;
    const limit = parseFloat(document.getElementById("categoryLimit")?.value);
    const msg = document.getElementById("limitMessage");
 
    if (!category || !limit) {
        msg.textContent = "Please select a category and enter a limit.";
        msg.style.color = "red";
        return;
    }
 
    if (limit <= 0) {
        msg.textContent = "Limit must be greater than 0.";
        msg.style.color = "red";
        return;
    }
 
    if (limit > 1000) {
        showConfirm(
            "This limit is over $1,000. Are you sure you want to set this limit?",
            async () => {
                await saveCategoryLimit(category, limit);
            }
        );
        return;
    }
 
    await saveCategoryLimit(category, limit);
}
 
async function saveCategoryLimit(category, limit) {
    const msg = document.getElementById("limitMessage");
    msg.textContent = "";
 
    await fetch("/limit", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            category: category,
            limit_amount: limit
        })
    });
 
    loadCategories();
    showNotification("Category limit set successfully!", "success");
}
 
/* load category cards*/
async function loadCategories() {
 
    const res = await fetch("/limits");
    const data = await res.json();
 
    const list = document.getElementById("categoryTable");
    if (!list) return;
 
    list.innerHTML = "";
 
    if (data.length === 0) {
        list.innerHTML = `<li class="empty-state">No categories yet.</li>`;
        return;
    }
 
    data.forEach(c => {
 
        const spent = c.limit_amount - c.remaining;
 
        list.innerHTML += `
            <li>
                <span><strong>${c.category}</strong></span>
                <span>Limit: $${c.limit_amount}</span>
                <span>Spent: $${spent}</span>
                <span>Remaining: $${c.remaining}</span>
            </li>
        `;
    });
}
 
 
/* purchases */
 
async function loadRecentPurchases() {
 
    const res = await fetch("/recent_purchases");
    const data = await res.json();
 
    const list = document.getElementById("recentPurchases");
    if (!list) return;
 
    list.innerHTML = "";
 
    if (data.length === 0) {
        list.innerHTML = `<li class="empty-state">No purchases yet.</li>`;
        return;
    }
 
    data.forEach(p => {
 
        list.innerHTML += `
            <li>
                <span><strong>${p.category}</strong></span>
                <span>$${p.amount}</span>
                <span>${new Date(p.date).toLocaleString()}</span>
            </li>
        `;
    });
}
 
/* add purchases*/
async function addPurchase() {
 
    const category = document.getElementById("purchaseCategory").value.toLowerCase();
    const amount = parseFloat(document.getElementById("purchaseAmount").value);
    const msg = document.getElementById("purchaseMessage");
 
    if (!category || !amount) {
        msg.textContent = "Please select a category and enter an amount.";
        msg.style.color = "red";
        return;
    }
 
    if (amount <= 0) {
        msg.textContent = "Amount must be greater than 0.";
        msg.style.color = "red";
        return;
    }
 
    const res = await fetch("/purchase", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            category: category,
            amount: amount
        })
    });
 
    const data = await res.json();
 
    if (data.error) {
        msg.textContent = data.error;
        msg.style.color = "red";
        return;
    }
 
    if (data.warning) {
 
        showConfirm(
            data.warning,
            async () => {
                await fetch("/purchase", {
                    method: "POST",
                    headers: {"Content-Type": "application/json"},
                    body: JSON.stringify({
                        category: category,
                        amount: amount,
                        confirm: true
                    })
                });
 
                msg.textContent = "Purchase added.";
                msg.style.color = "green";
 
                loadRecentPurchases();
                loadCategories();
                showNotification("Purchase added successfully!", "success");
            },
            () => {
                msg.textContent = "Purchase cancelled.";
                msg.style.color = "orange";
            }
        );
        return;
    }
 
    msg.textContent = "Purchase added.";
    msg.style.color = "green";
 
    loadRecentPurchases();
    loadCategories();
    showNotification("Purchase added successfully!", "success");
}
 
/* budget to travel transfer */
async function transferToTravel() {
 
    const msg = document.getElementById("transferMessage");
    const resCheck = await fetch("/limits");
    const limits = await resCheck.json();
 
    let totalRemaining = 0;
 
    limits.forEach(l => {
        totalRemaining += l.remaining;
    });
 
    if (totalRemaining <= 0) {
        msg.textContent = "No remaining budget to transfer.";
        msg.style.color = "red";
        return;
    }
    
    const resGoal = await fetch("/travel_goals");
    const goals = await resGoal.json();
 
    if (goals.length === 0) {
        msg.textContent = "Please set a travel goal first.";
        msg.style.color = "red";
        return;
    }
 
    const goal = goals[0];
    const target = goal.target_amount;
    const saved = goal.saved_amount;
 
    if (saved + totalRemaining > target) {
        showConfirm(
            `This will exceed your goal.\n\nGoal: $${target}\nAfter transfer: $${(saved + totalRemaining).toFixed(2)}\n\nContinue?`,
            async () => {
                await executeTransfer(msg);
            }
        );
    } 
    else {  
        showConfirm(
            `Transfer $${totalRemaining.toFixed(2)} to your travel goal?`,
            async () => {
                await executeTransfer(msg);
            }
        );
    }
   loadTravelGoal();
   loadCategories();
}
 
async function executeTransfer(msg) {
    const res = await fetch("/transfer_to_travel", {
        method: "POST"
    });
 
    const data = await res.json();
 
    if (data.error) {
        msg.textContent = data.error;
        msg.style.color = "red";
        showNotification(data.error, "error");
        return;
    }
 
    msg.textContent = data.message;
    msg.style.color = "green";
 
    const resGoalAfter = await fetch("/travel_goals");
    const goalsAfter = await resGoalAfter.json();
 
    if (goalsAfter.length > 0) {
        const goalAfter = goalsAfter[0];
 
        if (goalAfter.saved_amount > goalAfter.target_amount) {
            msg.textContent += " Goal exceeded!";
            showNotification("Transfer successful! Goal exceeded!", "success");
        } else {
            showNotification("Transfer successful!", "success");
        }
    }
 
    await loadCategories();
    await loadTravelGoal();
}
 
 
/* travel bar */
 
function updateUI(saved, goal) {
 
    const percent = goal > 0 ? Math.min((saved / goal) * 100, 100) : 0;
    const remaining = goal > 0 ? Math.max(goal - saved, 0) : 0;
 
    const progressBar = document.getElementById("travelProgress");
    const percentText = document.getElementById("travelPercent");
    const savedText = document.getElementById("goalSaved");
    const leftText = document.getElementById("goalLeft");
    const remainingBarText = document.getElementById("goalRemainingText");
    const summary = document.getElementById("goalSummary");
    const celebrate = document.getElementById("goalCelebrate");
 
    if (progressBar) progressBar.style.width = percent + "%";
    if (percentText) percentText.textContent = percent.toFixed(1) + "%";
    if (savedText) savedText.textContent = "$" + saved.toFixed(0);
    if (leftText) leftText.textContent = "$" + remaining.toFixed(0);
    if (remainingBarText) remainingBarText.textContent = "$" + remaining.toFixed(0) + " left";
 
    if (summary) {
        summary.textContent =
            `Saved: $${saved.toFixed(2)} / $${goal.toFixed(2)} (${percent.toFixed(1)}%)`;
    }
 
    if (celebrate) {
 
        if (saved > goal) {
            celebrate.textContent = "Goal exceeded!";
        }
        else if (percent >= 100) {
            celebrate.textContent = "Congratulations! You've reached your travel goal!";
        }
        else if (percent >= 75) celebrate.textContent = "Almost there!";
        else if (percent >= 50) celebrate.textContent = "Halfway there!";
        else if (percent >= 25) celebrate.textContent = "Great start!";
        else celebrate.textContent = "";
    }
}
