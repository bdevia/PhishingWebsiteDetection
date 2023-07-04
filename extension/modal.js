chrome.storage.local.get('messageData', function(result) {
  var data = result.messageData;
  if (data && data.showModal) {
    // Acceder a los datos adicionales
    console.log(data.url);
    var modalElement = document.getElementById('exampleModal');
    var modal = new bootstrap.Modal(modalElement);
    modal.show();
    
    // Limpiar el estado del mensaje y otros datos en chrome.storage.local
    //chrome.storage.local.remove('messageData');
  }
});

document.addEventListener("DOMContentLoaded", function() {
  var seguroButton = document.getElementById('seguro');
  seguroButton.addEventListener('click', function() {

    chrome.storage.local.get('messageData', function(result) {
      var data = result.messageData;
      if (data && data.showModal) {
        // Acceder a los datos adicionales
        const datos = {url: data.url};
        fetch('http://localhost:8080/save_url', {
          method: "POST",
          body: JSON.stringify(datos),
          headers: {"Content-type": "application/json; charset=UTF-8"}
          })
          .then(response => response.json())
          .then(data => {
            console.log(data);
            if( data.status == 'OK'){
              alert("Sitio guardado como legitimo");
            }
          })
          .catch(err => {
              console.log(err)
          });
      }
    });
  });
});

document.addEventListener("DOMContentLoaded", function() {
  var seguroButton = document.getElementById('cerrar');
  seguroButton.addEventListener('click', function() {
    chrome.storage.local.remove('messageData');
  });
});