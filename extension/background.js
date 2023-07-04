chrome.tabs.onUpdated.addListener(function(tabId, changeInfo, tab) {
  if(changeInfo.status === 'complete' && tab.active) {
     chrome.tabs.get(tabId, function(tab) {
      var url = tab.url;
      //console.log(url);
      send_request(url, tab.id);
    });
  }
});


function send_request(url, tabId){
  const datos = {url: url};
  fetch('http://localhost:8080/get_url', {
  method: "POST",
  body: JSON.stringify(datos),
  headers: {"Content-type": "application/json; charset=UTF-8"}
  })
  .then(response => response.json())
  .then(data => {
    console.log(data.status);
    if(data.status == 1){
      chrome.tabs.sendMessage(tabId, { action: 'phishing' });
      chrome.storage.local.set({
        messageData: {
          showModal: true,
          url: url
        }
      });
    }
    else if(data.status == 0){
      chrome.tabs.sendMessage(tabId, { action: 'legitimate' });
    }
   
  })
  .catch(err => {
      console.log(err)
  });
}

/*chrome.tabs.onUpdated.addListener(function(tabId, changeInfo, tab) {
  if (changeInfo.status === 'complete' && tab.active) {
    chrome.scripting.executeScript({
      target: { tabId: tabId },
      function: () => {
        const bootstrapCSS = document.createElement('link');
        bootstrapCSS.rel = 'stylesheet';
        bootstrapCSS.href = './node_modules/bootstrap/dist/css/bootstrap.min.css';
        document.head.appendChild(bootstrapCSS);
    
        const bootstrapJS = document.createElement('script');
        bootstrapJS.src = './node_modules/bootstrap/dist/js/bootstrap.bundle.min.js';
        document.head.appendChild(bootstrapJS);
      }
    });
  }
});


 chrome.scripting.executeScript({
      target: { tabId: tabId },
      function: () => {
        fetch(chrome.runtime.getURL('modal.html'))
          .then(response => response.text())
          .then(html => {
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, 'text/html');
            const modalContent = doc.getElementById('exampleModal')
            var modal = new bootstrap.Modal(modalContent);
            modal.show();
          
          });
      }
    });


          chrome.scripting.executeScript({
        target: { tabId: tabId },
        function: () => {
          fetch(chrome.runtime.getURL('modal.html'))
            .then(response => response.text())
            .then(html => {
              const parser = new DOMParser();
              const doc = parser.parseFromString(html, 'text/html');
              const modalContent = doc.getElementById('exampleModal')
              var modal = new bootstrap.Modal(modalContent);
              modal.show();
            });
        }
      });
*/

/*chrome.tabs.onActivated.addListener(function(activeInfo) {
  chrome.tabs.get(activeInfo.tabId, function(tab) {
    var url = tab.url;
    console.log(url);
    send_request(url);
  });
});


chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
  if (message.action === 'contentLoaded') {
    setTimeout(function() {
      chrome.tabs.sendMessage(sender.tab.id, { action: 'displayAlert' });
    }, 1500);
  }
});
*/


/*chrome.tabs.onUpdated.addListener(function(tabId, changeInfo, tab) {
  if (changeInfo.status === 'complete' && tab.active) {

    chrome.scripting.insertCSS({
      target: { tabId: tabId },
      files: ['./node_modules/bootstrap/dist/css/bootstrap.min.css'],
    }, () => {
      console.log('CSS de Bootstrap inyectado');
      chrome.scripting.executeScript({
        target: { tabId: tabId },
        files: ['./node_modules/bootstrap/dist/js/bootstrap.bundle.min.js'],
      }, () => {
        console.log('JS de Bootstrap y Modal inyectados');
      });
    });

    chrome.tabs.get(tabId, function(tab) {
      var url = tab.url;
      console.log(url);
      send_request(url, tab.id);
    });
  }
});*/