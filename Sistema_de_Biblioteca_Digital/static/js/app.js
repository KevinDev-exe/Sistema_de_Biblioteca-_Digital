async function fetchChartData(url) {
  const response = await fetch(url);
  return response.json();
}

function buildChart(elementId, type, labels, values, label, colors) {
  const element = document.getElementById(elementId);
  if (!element) return;
  new Chart(element, {
    type,
    data: {
      labels,
      datasets: [{
        label,
        data: values,
        backgroundColor: colors.background,
        borderColor: colors.border,
        borderWidth: 2,
        tension: 0.35
      }]
    },
    options: {
      responsive: true,
      plugins: { legend: { display: type !== "bar" } },
      scales: type === "doughnut" ? {} : { y: { beginAtZero: true, ticks: { precision: 0 } } }
    }
  });
}

async function initDashboardCharts() {
  if (!window.chartEndpoints) return;
  const [prestamos, reservas, categorias, autores] = await Promise.all([
    fetchChartData(window.chartEndpoints.prestamos),
    fetchChartData(window.chartEndpoints.reservas),
    fetchChartData(window.chartEndpoints.categorias),
    fetchChartData(window.chartEndpoints.autores)
  ]);

  buildChart("prestamosMesChart", "line", prestamos.labels, prestamos.values, "Préstamos", {
    background: "rgba(31, 94, 255, .1)",
    border: "#1f5eff"
  });
  buildChart("reservasChart", "bar", reservas.labels, reservas.values, "Reservas", {
    background: "rgba(31, 138, 91, .2)",
    border: "#1f8a5b"
  });
  buildChart("categoriasChart", "doughnut", categorias.labels, categorias.values, "Categorías", {
    background: ["#1f5eff", "#1f8a5b", "#b7791f", "#c24135", "#64748b", "#7c3aed", "#0891b2", "#db2777"],
    border: "#ffffff"
  });
  buildChart("autoresChart", "bar", autores.labels, autores.values, "Préstamos", {
    background: "rgba(124, 58, 237, .2)",
    border: "#7c3aed"
  });
}

