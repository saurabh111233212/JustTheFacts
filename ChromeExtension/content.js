chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
  if (request.action === 'getFacts') {
    document.documentElement.style.filter = 'grayscale(100%)';
    sendResponse({ message: 'Website converted to black and white.' });
    console.log('Website converted to black and white.');
    return true
  } else {
    sendResponse({ message: 'Invalid action requested.' });
    return false
  }
});