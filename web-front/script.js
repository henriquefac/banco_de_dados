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
      .then(data => {
        displayData(data)
      })
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
      console.log(data);
      
      localStorage.setItem("initialData", JSON.stringify(data));
      window.location.href = `results.html?records=${recordsPerPage}`;
    });
}

function fetchData(records) {
  let data = JSON.parse(localStorage.getItem("initialData"));
  displayData(data);
}

function displayData(data) {
  let resultsDiv = document.getElementById("tables-container");
  resultsDiv.innerHTML = "";
  
  if(data.first?.idx == 0) {
    let table = `
    <table>
      <tr>
        <th>Página: ${data.first.idx + 1}</th>
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
        <th>Página: ${data.last.idx + 1}</th>
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
            <th>${data.idx + 1}</th>
          </tr>`;

    data.page.forEach(record => {
      table += `<tr>
        <td>${record}</td>
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
      displayData(data);
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
      displayData(data);
      displayStatistics(data);
    });
}

function displayStatistics(stats) {
  let data = JSON.parse(localStorage.getItem("initialData"));
  let statsDiv = document.getElementById("statistics");
  statsDiv.innerHTML = `
        <p>Taxa de colisões: ${data.colision_rate}</p>
        <p>Taxa de overflows: ${data.overflow_rate}</p>
        <p>Estimativa de custo da busca por índice: ${
          stats.cost
        } leituras</p>
        <p>Estimativa de custo do table scan: ${stats.cost} leituras</p>
        <p>Diferença de tempo entre busca e table scan: ${(
          scanTime - searchTime
        ).toFixed(2)}ms</p>
    `;
}

function displayError(erro) {
  let error = document.getElementById("erro");

  error.innerHTML = `<p>${erro.erro}</p>`
}