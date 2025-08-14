async function fetchHistory(monitorId) {
  const res = await fetch(`/history/${monitorId}`);
  return await res.json();
}

function renderChart(canvas, series) {
  const ctx = canvas.getContext('2d');
  const labels = series.map(p => new Date(p.t).toLocaleString());
  const data = series.map(p => p.position || null);
  new Chart(ctx, {
    type: 'line',
    data: {
      labels,
      datasets: [{
        label: 'Position (lower is better)',
        data,
        spanGaps: true,
        tension: 0.3
      }]
    },
    options: {
      scales: {
        y: {
          reverse: true,
          suggestedMin: 100,
          suggestedMax: 1,
          title: { display: true, text: 'Google Position' }
        }
      },
      plugins: {
        legend: { display: true }
      }
    }
  });
}

async function initCharts() {
  const canvases = document.querySelectorAll('canvas[data-monitor-id]');
  for (const c of canvases) {
    const id = c.getAttribute('data-monitor-id');
    const { series } = await fetchHistory(id);
    renderChart(c, series);
  }
}

document.addEventListener('DOMContentLoaded', initCharts);