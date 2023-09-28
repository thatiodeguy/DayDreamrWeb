## static/js/actions.js

// Global variables
const API_URL = "http://localhost:5000";

// User actions
const createUser = async (name, email, password) => {
  try {
    const response = await fetch(`${API_URL}/users`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ name, email, password }),
    });
    const data = await response.json();
    return data.id;
  } catch (error) {
    console.error("Error creating user:", error);
    return null;
  }
};

const createGoal = async (userId, name, deadline) => {
  try {
    const response = await fetch(`${API_URL}/users/${userId}/goals`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ name, deadline }),
    });
    const data = await response.json();
    return data.id;
  } catch (error) {
    console.error("Error creating goal:", error);
    return null;
  }
};

const getGoal = async (userId, goalId) => {
  try {
    const response = await fetch(`${API_URL}/users/${userId}/goals/${goalId}`);
    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Error getting goal:", error);
    return null;
  }
};

const deleteGoal = async (userId, goalId) => {
  try {
    const response = await fetch(`${API_URL}/users/${userId}/goals/${goalId}`, {
      method: "DELETE",
    });
    const data = await response.json();
    return data.message;
  } catch (error) {
    console.error("Error deleting goal:", error);
    return null;
  }
};

// UI functions
const displayMessage = (message) => {
  const messageElement = document.getElementById("message");
  messageElement.textContent = message;
};

const createUserForm = document.getElementById("createUserForm");
createUserForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const name = document.getElementById("nameInput").value;
  const email = document.getElementById("emailInput").value;
  const password = document.getElementById("passwordInput").value;
  const userId = await createUser(name, email, password);
  if (userId) {
    displayMessage(`User created with ID: ${userId}`);
  } else {
    displayMessage("Error creating user");
  }
});

const createGoalForm = document.getElementById("createGoalForm");
createGoalForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const userId = document.getElementById("userIdInput").value;
  const name = document.getElementById("goalNameInput").value;
  const deadline = document.getElementById("goalDeadlineInput").value;
  const goalId = await createGoal(userId, name, deadline);
  if (goalId) {
    displayMessage(`Goal created with ID: ${goalId}`);
  } else {
    displayMessage("Error creating goal");
  }
});

const getGoalForm = document.getElementById("getGoalForm");
getGoalForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const userId = document.getElementById("userIdInput").value;
  const goalId = document.getElementById("goalIdInput").value;
  const goal = await getGoal(userId, goalId);
  if (goal) {
    displayMessage(`Goal: ${JSON.stringify(goal)}`);
  } else {
    displayMessage("Error getting goal");
  }
});

const deleteGoalForm = document.getElementById("deleteGoalForm");
deleteGoalForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const userId = document.getElementById("userIdInput").value;
  const goalId = document.getElementById("goalIdInput").value;
  const message = await deleteGoal(userId, goalId);
  if (message) {
    displayMessage(message);
  } else {
    displayMessage("Error deleting goal");
  }
});
