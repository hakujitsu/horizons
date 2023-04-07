// TODO: add links to the matches [] in manifest.json
async function getRecommendations() {
  url = document.location.href;

  // TODO: remove entry from localStorage when the page is unloaded
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

    // TODO: clean up response over here and check that it is stored in storage.local correctly
    response.json().then(data => {
      res = JSON.parse(JSON.stringify(data))
      recs = res.recommendations
      console.log(recs)
      var v1 = 'k1';
      let obj= {};
      obj[url] = recs;
      chrome.storage.local.set(obj)
    });
  });
}

getRecommendations()
