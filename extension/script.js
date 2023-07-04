//chrome.runtime.sendMessage({ action: 'contentLoaded' });

chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
  if (message.action === 'phishing') {
    alert("Phishing WebSite: El sitio web se ha detectado como un sitio no legitimo!. Cuida tu informacion personal. ")
  }
  else if(message.action === 'legitimate'){
    alert("Phishing WebSite: El sitio web es seguro.");
  }
});
 