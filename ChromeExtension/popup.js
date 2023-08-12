// when the popup is opened, setup the button 
document.addEventListener('DOMContentLoaded', function() {
  var getFactsButton = document.getElementById('factsButton');
    // check local storage for facts
    chrome.tabs.query({ active: true, currentWindow: true }, async function(tabs) {
      const currentTabId = tabs[0].id;
      const storageKey = "factsData_" + currentTabId + "_" + tabs[0].url;
      var result = await chrome.storage.local.get([storageKey]);
      var value = result[storageKey];
      if (value && value.facts) {
        const savedFacts = value.facts;
        const topics = value.topics;
        changeUIWithFacts(savedFacts, currentTabId, tabs[0].url, topics)
      } else if(value && value.loading) {
        var loadingElement = document.createElement("p")
        loadingElement.textContent = "Loading..."
        document.body.appendChild(loadingElement)
        getFactsButton.style.display = "none"
      }
    });

    // add event listener to button
    getFactsButton.addEventListener('click', function() {
      // hide the button
      getFactsButton.style.display = "none"
      // add a loading screen
      var loadingElement = document.createElement("p")
      loadingElement.textContent = "Loading..."
      document.body.appendChild(loadingElement)
      chrome.tabs.query({ active: true, currentWindow: true }, async function(tabs) {
        // send message to background script
        storageKey = "factsData_" + tabs[0].id + "_" + tabs[0].url;
        chrome.storage.local.set({ [storageKey]: {loading: true} }, function() {});
        chrome.runtime.sendMessage({url: tabs[0].url, tabId: tabs[0].id})
      });
    });
  });

// handle the response from the background script when it gives facts
chrome.runtime.onMessage.addListener(function(data, sender, sendResponse) {
  if (data.intent == "newFacts") {
    const facts = data.facts
    const currentTabId = data.tabId
    const topics = data.topics
    const url = data.url
    changeUIWithFacts(facts, currentTabId, url, topics)
    return false
  } else {
    console.log("Unknown intent.", data)
  }
});


const changeUIWithFacts = async (facts, tabId, url, topics) => {
  if (document.getElementById("factsButton")) {
    document.getElementById("factsButton").remove()
  }
  var paragraphs = document.querySelectorAll("p");
  paragraphs.forEach(function(paragraph) {
    paragraph.remove();
  });

  if (facts == undefined) {
    var stringElement = document.createElement("p")
    stringElement.textContent = "Timed out getting facts :( Please try again."
    document.body.appendChild(stringElement)
    return
  }

  // create <ul> for topic buttons
  var topicList = document.createElement("ul")
  topicList.id = "topicList"

  // create a button for displaying topics
  if (topics) {
    // add the button that opens a new tab to the topic
    for (var topic of topics) {
      var topicButton = document.createElement("button")
      topicButton.textContent = "See other facts about " + topic
      var topicWords = topic.split(" ")
      var topicUrl = "https://just-the-facts.allen.ai/components?topic=" + topicWords.join("%20")
      topicButton.addEventListener('click', function() {
        chrome.tabs.create({ url: topicUrl });
      });
      // add this button to the topicList
      var topicListItem = document.createElement("li")
      topicListItem.appendChild(topicButton)
      topicList.appendChild(topicListItem)
    }
  }

  // create a button to send to https://just-the-facts.allen.ai/
  var interfaceButton = document.createElement("button")
  interfaceButton.textContent = "Explore all topics"
  interfaceButton.addEventListener('click', function() {
    chrome.tabs.create({ url: "https://just-the-facts.allen.ai/" });
  });
  // add this button to the topicList
  var interfaceListItem = document.createElement("li")
  interfaceListItem.appendChild(interfaceButton)
  topicList.appendChild(interfaceListItem)

  document.body.appendChild(topicList)


  var list = document.createElement("ol")
  // loop over facts and add them to the list
  for (const i in facts) {
    var listItem = document.createElement("li")
    listItem.textContent = facts[i].text
    list.appendChild(listItem)
  }

  if (facts.length != 0) {
    document.body.appendChild(list)
  } else {
    var stringElement = document.createElement("p")
    stringElement.textContent = "No facts found."
    document.body.appendChild(stringElement)
  } 
}