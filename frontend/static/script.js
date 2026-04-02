document.addEventListener('DOMContentLoaded', () => {

    /* login */

    const submitBtn = document.getElementById('submit-btn');

    if (submitBtn) {
        submitBtn.addEventListener('click', async () => {

            const emailInput = document.querySelector('#email');
            const passwordInput = document.querySelector('#password');

            const validEmail = "group1@gmail.com";
            const validPassword = "group1";

            /* Need popups*/
            if (emailInput.value === validEmail && passwordInput.value === validPassword) {
                await showAlert("✨ Success! You are now logged in.", "success");
                window.location.href = "/home";
            } else {
                await showAlert("❌ Error: Invalid email or password.", "error");
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
/* popup */
           if (goal > 10000) {
                const confirmGoal = await showConfirm("This goal exceeds $10,000. Are you sure?");
                if (!confirmGoal) return;
               goalMsg.textContent = "Goal set.";
               goalMsg.style.color = "orange";
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
/* Needs popup*/
            if (contribution > savedGoal / 2) {
                const confirmContribution = await showConfirm("This contribution is more than 50% of your goal. Continue?");
                
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
/* needs popup*/
            const confirmReset = await showConfirm("Are you sure you want to reset your travel goal?");
            if (!confirmReset) return;

            await fetch("/travel_goal/reset", {
                method: "POST"
            });

            loadTravelGoal();
            loadHomeTravelBar();
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


/* =pop ups */

function showAlert(message, type = "default") {
    return new Promise((resolve) => {
        const modal = document.getElementById("customModal");
        const msg = document.getElementById("modalMessage");
        const box = document.querySelector(".modal-content");

        msg.textContent = message;

        box.style.borderTop = "5px solid #7a4a3b";

        if (type === "success") box.style.borderTop = "5px solid #2E7D32";
        if (type === "error") box.style.borderTop = "5px solid #c62828";
        if (type === "warning") box.style.borderTop = "5px solid #ef6c00";

        modal.classList.remove("hidden");

        document.getElementById("modalConfirmBtn").onclick = () => {
            modal.classList.add("hidden");
            resolve(true);
        };
    });
}

function showConfirm(message) {
    return new Promise((resolve) => {
        const modal = document.getElementById("customModal");
        const msg = document.getElementById("modalMessage");
        const cancelBtn = document.getElementById("modalCancelBtn");

        msg.textContent = message;
        cancelBtn.classList.remove("hidden");

        modal.classList.remove("hidden");

        document.getElementById("modalConfirmBtn").onclick = () => {
            modal.classList.add("hidden");
            cancelBtn.classList.add("hidden");
            resolve(true);
        };

        cancelBtn.onclick = () => {
            modal.classList.add("hidden");
            cancelBtn.classList.add("hidden");
            resolve(false);
        };
    });
}
