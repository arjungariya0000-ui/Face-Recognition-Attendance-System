// REGISTER BUTTON
document.getElementById("registerBtn")?.addEventListener("click", async () => {
  const name = document.getElementById("nameInput").value.trim();
  if (!name) return alert("Please enter a name");

  const response = await fetch("/api/register", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name }),
  });

  const result = await response.json();
  alert(result.status);
});

// ATTENDANCE BUTTON
document
  .getElementById("attendanceBtn")
  ?.addEventListener("click", async () => {
    const response = await fetch("/api/attendance", {
      method: "POST",
    });

    const result = await response.json();
    alert(result.status);
  });
