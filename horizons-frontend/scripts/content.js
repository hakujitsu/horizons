// TODO: add links to the matches [] in manifest.json
url = document.location.href;

async function getRecommendations() {
  url = document.location.href;

  // TODO: remove entry from localStorage when the page is unloaded
  addEventListener("beforeunload", (event) => {
    chrome.storage.local.remove(url)
  });

  let json;
  await chrome.storage.local.get("user_id").then((user_id) => {
    json = JSON.stringify({ user_id, url });
  });

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
    chrome.storage.local.set({ url: res })
  });
}

getRecommendations()

const results = [
  {
    title: "Communities face major destruction after large tornadoes tear through the South and Midwest, leaving at least 22 dead",
    source: "CNN",
    url: "https://edition.cnn.com/2023/04/02/us/us-severe-storm-south-midwest-sunday/index.html"
  },
  {
    title: "Finland begins voting in knife-edge election",
    source: "The Guardian",
    url: "https://www.theguardian.com/world/2023/apr/02/finland-begins-voting-in-knife-edge-election"
  },
  {
    title: "US tornadoes: Death toll grows as extreme storms ravage several states",
    source: "BBC",
    url: "https://www.bbc.com/news/world-us-canada-65150138"
  }
]

