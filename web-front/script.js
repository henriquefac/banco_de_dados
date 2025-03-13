const apiUrl = "http://172.17.245.42:8080";
let recordsPerPage;
let searchTime, scanTime;

// Simulação de API
function mockApi(endpoint, data = null) {
  return new Promise((resolve) => {
    setTimeout(() => {
      if (endpoint === "getPages") {
        resolve({
          pages: [
            {
              number: 1,
              records: Array.from(
                { length: data.recordsPerPage },
                (_, i) => `Registro ${i + 1}`
              ),
            },
            {
              number: 892,
              records: Array.from(
                { length: data.recordsPerPage },
                (_, i) => `Registro ${i + 1 + 1000}`
              ),
            },
          ],
        });
      } else if (endpoint === "search") {
        resolve({
          pages: [
            {
              number: Math.floor(Math.random() * 900),
              records: Array.from(
                { length: recordsPerPage },
                (_, i) => `Resultado ${i + 1}`
              ),
            },
          ],
        });
      } else if (endpoint === "tableScan") {
        resolve({
          pages: [
            {
              number: Math.floor(Math.random() * 900),
              records: Array.from(
                { length: recordsPerPage },
                (_, i) => `Scan ${i + 1}`
              ),
            },
          ],
          stats: {
            collisionRate: (Math.random() * 10).toFixed(2),
            overflowRate: (Math.random() * 10).toFixed(2),
            indexCost: Math.floor(Math.random() * 100),
            scanCost: Math.floor(Math.random() * 1000),
          },
        });
      }
    }, 500);
  });
}

document.addEventListener("DOMContentLoaded", () => {
  const params = new URLSearchParams(window.location.search);
  recordsPerPage = params.get("records") || 10;
  if (window.location.pathname.includes("results.html")) {
    fetch(`${apiUrl}/getPages`, {
      method: "GET",
      headers: { 
        "Content-Type": "application/json", 
        "Access-Control-Allow-Origin": "*" 
      },
    })
      .then((response) => response.json())
      .then(data => displayData(data))
      .catch( erro => displayError(erro))
  }
});

function sendData() {
  rpp = parseInt(document.getElementById("recordsPerPage").value);

  fetch(`${apiUrl}/init`, {
    method: "POST",
    headers: { 
      "Content-Type": "application/json", 
      "Access-Control-Allow-Origin": "*" 
    },
    body: JSON.stringify({ rpp }),
  })
    .then((response) => response.json())
    .then((data) => {
      localStorage.setItem("initialData", JSON.stringify(data));
      window.location.href = `results.html`;
    });
}

function backToHomePage() {
  window.location.href = `index.html`;
}

function fetchData(records) {
  let data = JSON.parse(localStorage.getItem("initialData"));
  displayData(data);
}

function displayData(data, item = "") {
  let resultsDiv = document.getElementById("tables-container");
  resultsDiv.innerHTML = "";
  
  if(data.first?.idx == 0) {
    let table = `
    <table>
      <tr>
        <th>Página ${data.first.idx + 1}</th>
      </tr>`;

    data.first.page.forEach((record) => {
      table += `<tr>
          <td>${record}</td>
        </tr>`;
      });
    table += "</table>";

    table += `
    <table>
      <tr>
        <th>Página ${data.last.idx + 1}</th>
      </tr>`;

    data.last.page.forEach((record) => {
      table += `<tr>
        <td>${record}</td>
      </tr>`;
    });
    table += "</table>";
    resultsDiv.innerHTML += table;
    displayError({erro: ""})
  } else if(data?.idx != null) {
    
    let table = `
        <table>
          <tr>
            <th>Página ${data.idx + 1}</th>
          </tr>`;

    data.page.forEach(record => {
      let outlineStyle = record === item ? 'style="border: 2px solid red;"' : "";

      table += `<tr>
        <td ${outlineStyle}>${record}</td>
      </tr>`;
    });

      table += "</table>";
      resultsDiv.innerHTML += table;
      displayError({erro: ""})
  } else {
    displayError(data);
  }
}

function search() {
  let key = document.getElementById("searchKey").value;
  let startTime = performance.now();

  fetch(`${apiUrl}/search?key=${key}`)
    .then((response) => response.json())
    .then((data) => {
      let endTime = performance.now();
      searchTime = endTime - startTime;
      document.getElementById("tableScanBtn").classList.remove("disabled");
      localStorage.setItem("searchTime", JSON.stringify(data.time))
      localStorage.setItem("searchCost", JSON.stringify(data.cost))
      displayData(data, key);
      displayStatistics(data);
    });
}

function tableScan() {
  let key = document.getElementById("searchKey").value;
  let startTime = performance.now();

  fetch(`${apiUrl}/tablescan?key=${key}`)
    .then((response) => response.json())
    .then((data) => {
      let endTime = performance.now();
      scanTime = endTime - startTime;
      localStorage.setItem("tableScanTime", JSON.stringify(data.time))
      localStorage.setItem("tableScanCost", JSON.stringify(data.cost))
      displayData(data, key);
      displayStatistics(data);
    });
}

function displayStatistics(stats) {
  let data = JSON.parse(localStorage.getItem("initialData"));

  let timeSearch = JSON.parse(localStorage.getItem("searchTime"));
  timeSearch = timeSearch != undefined ? timeSearch : "0";
  let costSearch = JSON.parse(localStorage.getItem("searchCost"));
  costSearch = costSearch != undefined ? costSearch + " leituras" : "Ainda não foi feito nenhuma leitura";


  let timeScan = JSON.parse(localStorage.getItem("tableScanTime"));
  timeScan = timeScan != undefined ? timeScan : "0";
  let costScan = JSON.parse(localStorage.getItem("tableScanCost"));
  costScan = costScan != undefined ? costScan + " leituras" : "Ainda não foi feito nenhuma leitura";
  


  let statsDiv = document.getElementById("statistics");

  let diffInTime = Math.abs((1000 * parseFloat(timeSearch)) - (1000 * parseFloat(timeScan)));
  console.log(diffInTime);
  
  statsDiv.innerHTML = `
        <p>Taxa de colisões: ${data.colision_rate}</p>
        <p>Taxa de overflows: ${data.overflow_rate}</p>
        <p>Estimativa de custo da busca por índice: ${costSearch}</p>
        <p>Estimativa de custo do table scan: ${costScan}</p>
        <p>Diferença de tempo entre busca e table scan: ${(
          diffInTime
        ).toFixed(2)}ms</p>
    `;
}

function displayError(erro) {
  if(erro.erro == "" || erro.erro == undefined) return;
  alert(erro.erro)
}