const API_URL = "http://localhost:5000";

async function calculate() {
    const num1 = parseFloat(document.getElementById("num1").value);
    const num2 = parseFloat(document.getElementById("num2").value);
    const operator = document.getElementById("operator").value;

    const res = await fetch(`${API_URL}/calculate`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ num1, num2, operator })
    });

    const data = await res.json();
    document.getElementById("result").innerText = `Result: ${data.result}`;
    loadHistory();
}

async function loadHistory() {
    const res = await fetch(`${API_URL}/history`);
    const history = await res.json();
    const historyList = document.getElementById("history");
    historyList.innerHTML = "";
    history.forEach(item => {
        const li = document.createElement("li");
        li.innerText = `${item.num1} ${item.operator} ${item.num2} = ${item.result}`;
        historyList.appendChild(li);
    });
}

window.onload = loadHistory;