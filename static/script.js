const form = document.getElementById("leadForm");

form.addEventListener("submit", async (e) => {

    e.preventDefault();

    const status = document.getElementById("status");
    const button = document.getElementById("submitBtn");
    const btnText = button.querySelector(".btn-text");
    const btnArrow = button.querySelector(".btn-arrow");

    status.className = "";
    status.innerHTML = "";

    button.disabled = true;
    btnText.innerText = "Generating…";
    btnArrow.innerText = "⟳";

    const data = {
        name: document.getElementById("name").value,
        email: document.getElementById("email").value,
        company: document.getElementById("company").value,
        website: document.getElementById("website").value
    };

    try {

        const response = await fetch("/submit", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        status.className = "success";
        status.innerHTML = `
            ✓ Audit request received.<br>
            Your AI growth report is being generated and will arrive in your inbox shortly.
        `;

        form.reset();

    } catch (error) {

        status.className = "error";
        status.innerHTML = `
            Something went wrong. Please try again or contact us directly.
        `;
    }

    button.disabled = false;
    btnText.innerText = "Generate My Audit";
    btnArrow.innerText = "↗";
});