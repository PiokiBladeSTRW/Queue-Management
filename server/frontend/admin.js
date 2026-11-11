const API_BASE = "http://localhost:8000";

const tableBody = document.getElementById("queue-table-body");
const currentToken = document.getElementById("current-token");
const customerName = document.getElementById("customer-name");

//let activeTokenId = null;

// Display Queue
async function fetchQueue() {
    try {
        const response = await fetch(`${API_BASE}/view`);
        const tokens = await response.json();

        tableBody.innerHTML ="";
        if(tokens.lenth == 0) {
            tableBody.innerHTML = `<tr><td colspan="4" style="text-align: center;"> Queue is empty</td></tr>`;
            return;
        }
        
        tokens.forEach(token => {
            const row = document.createElement("tr");
            row.innerHTML = `
                <td class="token"> ${token.id} </td>
                <td>${token.disp_id}</td>
                <td>${token.name}</td>
                </td>`;
            tableBody.appendChild(row);
        });
    } catch (error) {
        console.error("Error Fetching Queue: ", error);
    }
}

// Generate Token
document.getElementById("add-token-form").addEventListener("submit", async (e) => {
    e.preventDefault();

    const name = document.getElementById("input-name").value.trim();

    const payload = {};
    if(name !== "") {
        payload.user_name = name;
    }

    try {

        await fetch(`${API_BASE}/create-token`, {
            method: "POST",
            headers: { "Content-Type" : "application/json"},
            body: JSON.stringify(payload)
        });

        document.getElementById("add-token-form").reset();
        fetchQueue();

    } catch (error) {
        console.error("Error adding token:", error);
    }  
})

// Call Next
document.getElementById("btn-next").addEventListener("click", async() => {
    try {
        const response = await fetch(`${API_BASE}/exit-token`, {
            method: "POST"
        });

        if(response.ok) {
            const data = await response.json();
            currentToken.innerText = `${data.id} : ${data.disp_id}`;
            customerName.innerText = `${data.user_name}`;
            fetchQueue();
        } else {
            alert("Queue is empty!");
        }

    } catch (error) {
        console.error("Error Calling next:", error);
    }
})

fetchQueue();