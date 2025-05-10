chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  if (msg.action === "getSelectedText") {
    sendResponse({ text: window.getSelection().toString() });
  }
});