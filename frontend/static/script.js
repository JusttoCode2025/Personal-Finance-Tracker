// ============================================
// POPUP / NOTIFICATION SYSTEM (added feature)


function showNotification(message, type = 'info', callback = null) {
    const existing = document.getElementById('app-notification');
    if (existing) existing.remove();

    const notification = document.createElement('div');
    notification.id = 'app-notification';
    notification.className = `notification notification-${type}`;
    
    notification.innerHTML = `
        <span>${message}</span>
        <button onclick="this.parentElement.remove()">×</button>
    `;
    
    document.body.appendChild(notification);

    setTimeout(() => notification.remove(), 4000);

    if (callback) callback();
}

function showConfirm(message, onConfirm) {
    const confirmBox = document.createElement('div');
    confirmBox.innerHTML = `
        <div style="position:fixed; top:0; left:0; right:0; bottom:0; background:rgba(0,0,0,0.5); display:flex; align-items:center; justify-content:center;">
            <div style="background:white; padding:20px; border-radius:10px; text-align:center;">
                <p>${message}</p>
                <button id="yesBtn">Yes</button>
                <button id="noBtn">Cancel</button>
            </div>
        </div>
    `;

    document.body.appendChild(confirmBox);

    confirmBox.querySelector("#yesBtn").onclick = () => {
        confirmBox.remove();
        onConfirm();
    };

    confirmBox.querySelector("#noBtn").onclick = () => {
        confirmBox.remove();
    };
}


document.addEventListener('DOMContentLoaded', () => {

    /* login */

    const submitBtn = document.getElementById('submit-btn');

    if (submitBtn) {
        submitBtn.addEventListener('click', () => {

            const emailInput = document.querySelector('#email');
            const passwordInput = document.querySelector('#password');

            const validEmail = "group1@gmail.com";
            const validPassword = "group1";

            if (emailInput.value === validEmail && passwordInput.value === validPassword) {
                showNotification("Success! You are now logged in.", "success");
                window.location.href = "/home";
            } else {
                showNotification("Invalid email or password.", "error");
            }
        });
    }

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
                showConfirm("This goal exceeds $10,000. Are you sure?", async () => {
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
});
return;
              
            }

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
        });
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
                const confirmContribution = confirm("This contribution is more than 50% of your goal. Continue?");
                if (!confirmContribution) return;
                contributionMsg.textContent = "Contribution added.";
                contributionMsg.style.color = "orange";
            }

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
        });
    }


    /* reset goal */

    if (resetBtn) {
        resetBtn.addEventListener("click", async () => {

           showConfirm("Are you sure you want to reset your travel goal?", async () => {
    await fetch("/travel_goal/reset", {
        method: "POST"
    });

    loadTravelGoal();
    loadHomeTravelBar();
    });
    return;
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
        const confirmLimit = confirm("This limit is over $1,000. Are you sure?");
        if (!confirmLimit) return;
    }

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
}

/* load category cards*/
async function loadCategories() {

    const res = await fetch("/limits");
    const data = await res.json();

    const list = document.getElementById("categoryTable");
    if (!list) return;

    list.innerHTML = "";

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

        const confirmSpend = confirm(data.warning + "\n\nContinue anyway?");

        if (!confirmSpend) {
            msg.textContent = "Purchase cancelled.";
            msg.style.color = "orange";
            return;
        }

        await fetch("/purchase", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                category: category,
                amount: amount,
                confirm: true
            })
        });
    }

    msg.textContent = "Purchase added.";
    msg.style.color = "green";

    loadRecentPurchases();
    loadCategories();
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
        const confirmOver = confirm(
            `This will exceed your goal.\n\nGoal: $${target}\nAfter transfer: $${(saved + totalRemaining).toFixed(2)}\n\nContinue?`
        );
        if (!confirmOver) return;
    } 
    else {  
        const confirmTransfer = confirm(
            `Transfer $${totalRemaining.toFixed(2)} to your travel goal?`
        );
        if (!confirmTransfer) return;
    }
    const res = await fetch("/transfer_to_travel", {
        method: "POST"
    });

    const data = await res.json();

    if (data.error) {
        msg.textContent = data.error;
        msg.style.color = "red";
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
    }
}

    loadTravelGoal();
    loadCategories();
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
