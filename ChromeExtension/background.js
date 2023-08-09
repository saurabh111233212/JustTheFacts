chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
    if (changeInfo.status === 'active') {
      // The tab is now active, so re-inject the content script.
      chrome.tabs.executeScript(tabId, {
        file: 'content.js'
      });
    }
  });