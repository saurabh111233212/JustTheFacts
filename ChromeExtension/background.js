chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
    if (changeInfo.status === 'active') {
      // The tab is now active, so re-inject the content script.
      chrome.tabs.executeScript(tabId, {
        file: 'content.js'
      });
    }

    //reset the local storage if the url changes
    if (changeInfo.url) {
      const storageKey = "factsData_" + tabId + "_" + changeInfo.url;
      chrome.storage.local.remove(storageKey, function() {
      });
    }
  });

// when popup.js requests facts (button) get facts and send back to popup.js
chrome.runtime.onMessage.addListener(async function(params, sender, sendResponse) {
  const tabId = params.tabId;
  const currUrl = params.url;
  const storageKey = "factsData_" + tabId + "_" + currUrl;
  // this isn't working and I don't know why
  if (params.reset) {
    chrome.storage.local.remove(storageKey, function() {
      console.log("Resetting facts data.")
      chrome.action.setPopup({ popup: 'popup.html'}, function() {
         console.log("Resetting popup.")
       });
    });
    return true
  } else {
    // check to see if these facts are cached
    var result = await chrome.storage.local.get([storageKey]);
    var value = result[storageKey];
    if (value && value.facts) {
      var savedFacts = value.facts;
      var topics = value.topics;
      chrome.runtime.sendMessage({facts: savedFacts, tabId: tabId, intent: "newFacts", url: params.url, topics: topics})
      console.log("Facts data retrieved from storage.")
      return true
    } else {
      // if not, call the API
      const apiUrl = "http://just-the-facts.apps.allenai.org/api/get-facts";
      const url = params.url;
      const urlparams = new URLSearchParams({ url: url, method: "gpt-4"});
      var resp = await fetch(`${apiUrl}?${urlparams}`)
      resp = await resp.json()
      const facts = resp.facts
      var topics = []

      // get topics
      const topicListUrl = "http://just-the-facts.apps.allenai.org/api/topics-from-url" // TODO
      var urlParams = new URLSearchParams({ url: url});
      var resp = await fetch(`${topicListUrl}?${urlParams}`)
      resp = await resp.json()
      console.log(resp)
      topics = resp

      chrome.storage.local.set({ [storageKey]: {"facts": facts, "loading": false, "topics": topics} }, function() {});
      //send back to popup.js
      chrome.runtime.sendMessage({facts: facts, tabId: tabId, intent: "newFacts", url: url, "topics": topics})
      console.log("Facts data retrieved from API.")
      return true
    }
  }
});