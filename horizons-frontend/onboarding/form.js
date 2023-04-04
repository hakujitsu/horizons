const form = document.getElementById("onboarding-form");

async function sendData() {
  await chrome.storage.sync.clear();

  // Bind the FormData object and the form element
  const formData = new FormData(form);
  var object = {};
  formData.forEach((value, key) => object[key] = value);
  var json = JSON.stringify(object);

  const response = await fetch("http://localhost:5000/signup", {
    method: 'POST',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
    body: json,
  });

  response.json().then(data => {
    res = JSON.parse(JSON.stringify(data))
    user_id = res.user_id
    chrome.storage.local.set({ user_id })
  });
  location.href = "../success/index.html"
}

// Add 'submit' event handler
form.addEventListener("submit", (event) => {
  event.preventDefault();
  sendData()
});