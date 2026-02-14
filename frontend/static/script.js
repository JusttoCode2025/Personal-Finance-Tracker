async function loadExpenses() {
    const res = await fetch("/expenses");
    const data = await res.json();

    const list = document.getElementById("expenseList");
    list.innerHTML = "";

    data.forEach(e => {
        list.innerHTML += `<li>${e.name} - $${e.amount} (${e.frequency})</li>`;
    });
}

async function addExpense() {
    await fetch("/expenses", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            name: name.value,
            amount: amount.value,
            frequency: frequency.value
        })
    });
    loadExpenses();
}

async function setLimit() {
    await fetch("/limit", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ amount: limitInput.value })
    });
    loadLimit();
}

async function loadLimit() {
    const res = await fetch("/limit");
    const data = await res.json();
    remaining.innerText = `Remaining: $${data.remaining}`;
}

async function addPurchase() {
    await fetch("/purchase", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            description: purchaseDesc.value,
            amount: purchaseAmount.value
        })
    });
    loadLimit();
}

loadExpenses();
loadLimit();
