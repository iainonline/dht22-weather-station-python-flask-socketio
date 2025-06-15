var temperatureHistoryDiv = document.getElementById("temperature-history");
var humidityHistoryDiv = document.getElementById("humidity-history");

var temperatureGaugeDiv = document.getElementById("temperature-gauge");
var humidityGaugeDiv = document.getElementById("humidity-gauge");

var graphConfig = {
  displayModeBar: false,
  responsive: true,
};

// History Data
var temperatureTrace = {
  x: [],
  y: [],
  name: "Temperature",
  mode: "lines+markers",
  type: "line",
};
var humidityTrace = {
  x: [],
  y: [],
  name: "Humidity",
  mode: "lines+markers",
  type: "line",
};

var temperatureLayout = {
  autosize: true,
  title: {
    text: "Temperature",
  },
  font: {
    size: 14,
    color: "#7f7f7f",
  },
  colorway: ["#B22222"],
  //   width: 450,
  //   height: 260,
  margin: { t: 30, b: 20, l: 30, r: 20, pad: 0 },
};
var humidityLayout = {
  autosize: true,
  title: {
    text: "Humidity",
  },
  font: {
    size: 14,
    color: "#7f7f7f",
  },
  colorway: ["#00008B"],
  //   width: 450,
  //   height: 260,
  margin: { t: 30, b: 20, l: 30, r: 20, pad: 0 },
};
var config = { responsive: true };

Plotly.newPlot(
  temperatureHistoryDiv,
  [temperatureTrace],
  temperatureLayout,
  graphConfig
);
Plotly.newPlot(
  humidityHistoryDiv,
  [humidityTrace],
  humidityLayout,
  graphConfig
);

// Gauge Data
var temperatureData = [
  {
    domain: { x: [0, 1], y: [0, 1] },
    value: 0,
    title: { text: "Temperature" },
    type: "indicator",
    mode: "gauge+number+delta",
    delta: { reference: 30 },
    gauge: {
      axis: { range: [null, 50] },
      steps: [
        { range: [0, 20], color: "lightgray" },
        { range: [20, 30], color: "gray" },
      ],
      threshold: {
        line: { color: "red", width: 4 },
        thickness: 0.75,
        value: 30,
      },
    },
  },
];

var humidityData = [
  {
    domain: { x: [0, 1], y: [0, 1] },
    value: 0,
    title: { text: "Humidity" },
    type: "indicator",
    mode: "gauge+number+delta",
    delta: { reference: 50 },
    gauge: {
      axis: { range: [null, 100] },
      steps: [
        { range: [0, 20], color: "lightgray" },
        { range: [20, 30], color: "gray" },
      ],
      threshold: {
        line: { color: "red", width: 4 },
        thickness: 0.75,
        value: 30,
      },
    },
  },
];

var layout = { width: 350, height: 250, margin: { t: 0, b: 0, l: 0, r: 0 } };

Plotly.newPlot(temperatureGaugeDiv, temperatureData, layout, graphConfig);
Plotly.newPlot(humidityGaugeDiv, humidityData, layout, graphConfig);

// Temperature
let newTempXArray = [];
let newTempYArray = [];
// Humidity
let newHumidityXArray = [];
let newHumidityYArray = [];

// The maximum number of data points displayed on our scatter/line graph
let MAX_GRAPH_POINTS = 10000;
let ctr = 0;

function updateBoxes(temperature, humidity) {
  let temperatureDiv = document.getElementById("temperature");
  let humidityDiv = document.getElementById("humidity");

  temperatureDiv.innerHTML = temperature + " f";
  humidityDiv.innerHTML = humidity + " %";
}

function updateGauge(temperature, humidity) {
  var temperature_update = {
    value: temperature,
  };
  var humidity_update = {
    value: humidity,
  };

  Plotly.update(temperatureGaugeDiv, temperature_update);
  Plotly.update(humidityGaugeDiv, humidity_update);
}

function updateCharts(lineChartDiv, xArray, yArray, sensorRead) {
  var today = new Date();
  var time =
    today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
  if (xArray.length >= MAX_GRAPH_POINTS) {
    xArray.shift();
  }
  if (yArray.length >= MAX_GRAPH_POINTS) {
    yArray.shift();
  }
  xArray.push(ctr++);
  yArray.push(sensorRead);

  var data_update = {
    x: [xArray],
    y: [yArray],
  };

  Plotly.update(lineChartDiv, data_update);
}

function updateSensorReadings(jsonResponse) {
  let temperature = jsonResponse.temperature.toFixed(2);
  let humidity = jsonResponse.humidity.toFixed(2);

  updateBoxes(temperature, humidity);

  updateGauge(temperature, humidity);

  // Update Temperature Line Chart
  updateCharts(
    temperatureHistoryDiv,
    newTempXArray,
    newTempYArray,
    temperature
  );
  // Update Humidity Line Chart
  updateCharts(
    humidityHistoryDiv,
    newHumidityXArray,
    newHumidityYArray,
    humidity
  );

  // Assuming you receive 'data' from the backend
  document.getElementById('timestamp').textContent = 'Last updated: ' + jsonResponse.timestamp;

  // When you receive new data (jsonResponse):
  temperatureTrace.x.push(jsonResponse.timestamp); // Use timestamp for x
  temperatureTrace.y.push(jsonResponse.temperature);

  humidityTrace.x.push(jsonResponse.timestamp); // Use timestamp for x
  humidityTrace.y.push(jsonResponse.humidity);

  // Then update/redraw the charts:
  Plotly.update(temperatureHistoryDiv, { x: [temperatureTrace.x], y: [temperatureTrace.y] });
  Plotly.update(humidityHistoryDiv, { x: [humidityTrace.x], y: [humidityTrace.y] });
}
/*
  SocketIO Code
*/
//   var socket = io.connect("http://" + document.domain + ":" + location.port);
var socket = io.connect();

//receive details from server
socket.on("updateSensorData", function (msg) {
  var sensorReadings = JSON.parse(msg);
  updateSensorReadings(sensorReadings);
});

// Example: receiving data from backend
const weatherData = [
  { temperature: 72, humidity: 50, timestamp: "2025-06-14T12:34:56" }
];

// Prepare data for Chart.js
const tempData = weatherData.map(d => ({ x: d.timestamp, y: d.temperature }));

// Initialize chart after DOM is ready and data is loaded
const ctx = document.getElementById('weatherChart').getContext('2d');
const chart = new Chart(ctx, {
  type: 'line',
  data: {
    datasets: [{
      label: 'Temperature (°F)',
      data: tempData,
      borderColor: 'red'
    }]
  },
  options: {
    scales: {
      x: {
        type: 'time',
        time: {
          tooltipFormat: 'MMM d, yyyy HH:mm:ss',
          displayFormats: { minute: 'HH:mm', hour: 'HH:mm' }
        }
      }
    }
  }
});

const MAX_POINTS = (60*60*72);

socket.on('weather_update', function(data) {
    tempData.push({ x: data.timestamp, y: data.temperature });
    if (tempData.length > MAX_POINTS) {
        tempData.shift(); // Remove the oldest point
    }
    chart.update();
});
