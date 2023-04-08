const SUPPORTED_SOURCES = [
  "apnews.com/article/",
  "www.bbc.com/news/",
  "www.cnbc.com/",
  "edition.cnn.com/",
  "www.cnn.com/",
  "www.foxnews.com/",
  "www.theguardian.com/",
  "nypost.com/",
  "www.newsweek.com/",
  "www.reuters.com/",
  "www.washingtonexaminer.com/news/"
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

function removeHttp(url) {
  return url.replace(/^https?:\/\//, '');
}

function updateEntries(results) {
  entry1.style.display = "none";
  entry2.style.display = "none";
  entry3.style.display = "none";

  for (let i = 0; i < results.length; i++) {
    const currEntry = entries[i];
    const currResult = results[i];
    currEntry.style.display = "block"

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
    url = removeHttp(tabs[0].url);

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
      await chrome.tabs.query({ active: true, lastFocusedWindow: true }, tabs => {
        url = removeHttp(tabs[0].url);
        if (areaName == url) {
          chrome.storage.local.get(url).then((result) => {
            updateEntries(result)
          });
        }
      });
    })
  }
}

fillInEntries();
