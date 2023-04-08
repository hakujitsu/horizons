async function getRecommendations() {
  let url = document.location.href;

  addEventListener("beforeunload", (event) => {
    chrome.storage.local.remove(url)
  });

  await chrome.storage.local.get("user_id").then(async (user_id) => {
    json = JSON.stringify({ user_id, url });

    const response = await fetch("http://localhost:5000/scrape", {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      body: json,
    });

    response.json().then(data => {
      res = JSON.parse(JSON.stringify(data))
      let obj= {};
      obj[url] = res.recommendations;
      chrome.storage.local.set(obj)
    });
  });
}

getRecommendations()
