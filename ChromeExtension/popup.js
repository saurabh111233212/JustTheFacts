document.addEventListener('DOMContentLoaded', function() {
    var convertButton = document.getElementById('factsButton');
  
    convertButton.addEventListener('click', function() {
      chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
        console.log(tabs);
        chrome.tabs.sendMessage(tabs[0].id, { action: 'getFacts' });
      });
    });
  });