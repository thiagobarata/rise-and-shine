const timeInput = document.getElementById("alarm-time");
const toggleInput = document.getElementById("alarm-toggle");
const statusMsg = document.getElementById("status-msg");

// Fetch alarm from server and populate UI in LA time
fetch("http://localhost:5050/alarm")
  .then(res => res.json())
  .then(alarm => {
    timeInput.value = getLAFormattedTime(alarm.alarm_time); // show 07:00 if UTC is 14:00
    toggleInput.checked = alarm.enabled;
    statusMsg.textContent = "Alarm loaded from server.";
  })
  .catch(err => {
    console.error("Error fetching alarm:", err);
    statusMsg.textContent = "Failed to load alarm.";
  });

// Update alarm on time or toggle change
timeInput.addEventListener("change", updateAlarm);
toggleInput.addEventListener("change", updateAlarm);

// Converts ISO UTC string → "HH:MM" in LA time
function getLAFormattedTime(isoString) {
  const utcDate = new Date(isoString);
  const laString = utcDate.toLocaleString("en-US", {
    timeZone: "America/Los_Angeles",
    hour12: false,
    hour: "2-digit",
    minute: "2-digit"
  });
  return laString;
}

// Convert LA time to UTC ISO and send to server
function updateAlarm() {
  const [hour, minute] = timeInput.value.split(":").map(Number);

  // Build a Date object with today's date and selected time
  const today = new Date();
  const laDateString = new Date(
    today.getFullYear(),
    today.getMonth(),
    today.getDate(),
    hour,
    minute,
    0,
    0
  ).toLocaleString("en-US", { timeZone: "America/Los_Angeles" });

  // Convert LA-local string to a real Date object
  const laDate = new Date(laDateString);

  // Convert to UTC ISO string for Mongo
  const payload = {
    alarm_time: laDate.toISOString(),
    enabled: toggleInput.checked
  };

  fetch("http://localhost:5050/alarm", {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  })
    .then(res => res.json())
    .then(data => {
      console.log("Alarm updated:", data);
      statusMsg.textContent = "Alarm updated successfully.";
    })
    .catch(err => {
      console.error("Failed to update alarm:", err);
      statusMsg.textContent = "Failed to update alarm.";
    });
}
