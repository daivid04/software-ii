import { showNotification } from "./utils/notification.js";
import { obtainToken } from "./utils/store/manager-key.js";

function loginActions() {
  const form = document.querySelector(".form-login");
  const userInput = document.getElementById("user-email");
  const passwordInput = document.getElementById("user-key");
  const errorMsg = document.getElementById('errorMsg');


  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const data = await obtainToken(userInput.value, passwordInput.value);

    if (!data) {
      errorMsg.classList.remove("hidden");
    } else {
      errorMsg.classList.add("hidden");
      const token = data.session.access_token;
      const user = data.user;
      localStorage.setItem('supabase_token', token);
      window.location.href = "index.html";
    }

  });
}

document.addEventListener('DOMContentLoaded', loginActions);