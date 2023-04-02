// TODO: retrieve results from localStorage
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

const entry1 = document.querySelector("#entry-1");
const entry2 = document.querySelector("#entry-2");
const entry3 = document.querySelector("#entry-3");

const entries = [entry1, entry2, entry3];

function fillInEntries() {
  for (let i = 0; i < 3; i++) {
    const currEntry = entries[i];
    const currResult = results[i];

    currEntry.querySelector("div.title").innerHTML = currResult.title;
    currEntry.querySelector("div.source").innerHTML = currResult.source;
    currEntry.querySelector("a.link").href = currResult.url;
  }
}

fillInEntries();
