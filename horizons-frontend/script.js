// const results = [
//   {
//     title: "Communities face major destruction after large tornadoes tear through the South and Midwest, leaving at least 22 dead",
//     source: "CNN",
//     url: "https://edition.cnn.com/2023/04/02/us/us-severe-storm-south-midwest-sunday/index.html"
//   },
//   {
//     title: "Finland begins voting in knife-edge election",
//     source: "The Guardian",
//     url: "https://www.theguardian.com/world/2023/apr/02/finland-begins-voting-in-knife-edge-election"
//   },
//   {
//     title: "US tornadoes: Death toll grows as extreme storms ravage several states",
//     source: "BBC",
//     url: "https://www.bbc.com/news/world-us-canada-65150138"
//   }
// ]

// TODO: fix http / https bug
const SUPPORTED_SOURCES = [
  "https://apnews.com/article/",
  "https://www.bbc.com/news/",
  "https://www.cnbc.com/",
  "http://edition.cnn.com/",
  "https://edition.cnn.com/",
  "https://www.cnn.com/",
  "https://www.foxnews.com/",
  "https://www.theguardian.com/",
  "https://nypost.com/",
  "https://www.newsweek.com/",
  "https://www.reuters.com/",
  "https://www.washingtonexaminer.com/news/"
]

const contents = document.querySelector("#contents");
const loadingDiv = document.querySelector("#loading");
const errorDiv = document.querySelector("#error");

const entry1 = document.querySelector("#entry-1");
const entry2 = document.querySelector("#entry-2");
const entry3 = document.querySelector("#entry-3");

const entries = [entry1, entry2, entry3];

function setError() {
  contents.style.display = "none";
  errorDiv.style.display = "block";
  loadingDiv.style.display = "none";
}

function setLoading() {
  contents.style.display = "none";
  errorDiv.style.display = "none";
  loadingDiv.style.display = "block";
}

function setEntries() {
  contents.style.display = "block";
  loadingDiv.style.display = "none";
  errorDiv.style.display = "none";
}

function updateEntries(results) {
  for (let i = 0; i < 3; i++) {
    const currEntry = entries[i];
    const currResult = results[i];

    currEntry.querySelector("div.title").innerHTML = currResult.title;
    currEntry.querySelector("div.source").innerHTML = currResult.source;
    currEntry.addEventListener('click', function (e) {
      chrome.tabs.create({
        url: currResult.url
      });
    });
    setEntries()
  }
}


function isSupportedSource(url) {
  for (const source of SUPPORTED_SOURCES) {
    if (url.includes(source)) {
      return true
    }
  }
  return false
}

async function fillInEntries() {
  setLoading()

  await chrome.tabs.query({ active: true, lastFocusedWindow: true }, tabs => {
    url = tabs[0].url;

    if (!isSupportedSource(url)) {
      setError()
      return
    }

    chrome.storage.local.get(url).then((result) => {
      updateEntries(result[url])
    });
  });

  if (loadingDiv.style.display == "block") {
    chrome.storage.onChanged.addListener(async (changes, areaName) => {
      console.log("storage changed")
      await chrome.tabs.query({ active: true, lastFocusedWindow: true }, tabs => {
        url = tabs[0].url;
        if (areaName == url) {
          chrome.storage.local.get(url).then((result) => {
            console.log(result)
            updateEntries(result)
          });
        }
      });
    })
  }
}

fillInEntries();
