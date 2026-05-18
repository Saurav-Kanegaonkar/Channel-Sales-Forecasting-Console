const data = window.forecastingConsoleData;
const state = {
  view: "executive",
  region: "All regions",
  channel: "All channels",
};

const root = document.querySelector("#viewRoot");
const regionFilter = document.querySelector("#regionFilter");
const channelFilter = document.querySelector("#channelFilter");
const tabs = document.querySelectorAll(".tab");

const formatMoney = (value) =>
  new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    maximumFractionDigits: 0,
  }).format(value);

const formatNumber = (value) => new Intl.NumberFormat("en-US").format(value);

function optionList(select, values) {
  select.innerHTML = values.map((value) => `<option value="${value}">${value}</option>`).join("");
}

function filteredQueue() {
  return data.priorityQueue.filter((row) => {
    const regionMatch = state.region === "All regions" || row.region === state.region;
    const channelMatch = state.channel === "All channels" || row.channel_type === state.channel;
    return regionMatch && channelMatch;
  });
}

function tierClass(tier) {
  return `tier-${tier.toLowerCase()}`;
}

function kpis(items) {
  return `
    <section class="kpi-grid">
      ${items
        .map(
          (item) => `
            <article class="kpi-card">
              <span>${item.label}</span>
              <strong>${item.value}</strong>
              <em>${item.note}</em>
            </article>
          `
        )
        .join("")}
    </section>
  `;
}

function renderTrend() {
  const maxValue = Math.max(...data.trend.flatMap((row) => [row.actual, row.forecast]));
  return `
    <div class="chart">
      ${data.trend
        .map((row) => {
          const actualWidth = Math.max(4, (row.actual / maxValue) * 100);
          const forecastWidth = Math.max(4, (row.forecast / maxValue) * 100);
          return `
            <div class="bar-row">
              <span>${row.month}</span>
              <div class="bar-track">
                <i class="bar actual" style="width:${actualWidth}%"></i>
                <i class="bar forecast" style="width:${forecastWidth}%"></i>
              </div>
              <b>${formatNumber(row.actual)}</b>
            </div>
          `;
        })
        .join("")}
    </div>
    <div class="legend">
      <span><i class="actual-dot"></i>Actual units</span>
      <span><i class="forecast-dot"></i>Submitted forecast</span>
    </div>
  `;
}

function renderExecutive() {
  const top = filteredQueue()[0] || data.priorityQueue[0];
  root.innerHTML = `
    ${kpis([
      { label: "Sales modeled", value: formatMoney(data.summary.totalSales), note: `${formatNumber(data.summary.totalUnits)} units` },
      { label: "Forecast accuracy", value: `${data.summary.forecastAccuracy}%`, note: "actual versus submitted" },
      { label: "Open incentive exposure", value: formatMoney(data.summary.openCompExposure), note: "requires payout review" },
      { label: "Data trust score", value: `${data.summary.dataTrust}%`, note: `${data.summary.dealerCount} channel partners` },
    ])}
    <section class="layout-two">
      <article class="panel">
        <p class="section-label">Forecast performance</p>
        <h2>Monthly unit forecast versus actual demand</h2>
        ${renderTrend()}
      </article>
      <article class="panel">
        <p class="section-label">Leadership action</p>
        <h2>${top.dealer_name}</h2>
        <div class="action-stack">
          <div class="action-item">
            <strong>${top.recommended_action}</strong>
            <p>${top.region} ${top.channel_type.toLowerCase()} partner with a ${top.priority_score} priority score and ${top.forecast_variance_pct}% forecast variance.</p>
          </div>
          <div class="action-item">
            <strong>Promotion ROI</strong>
            <p>${top.promo_roi}x expected return with ${top.inventory_days} inventory days and ${formatMoney(top.open_comp_exposure)} open compensation exposure.</p>
          </div>
          <div class="action-item">
            <strong>Executive narrative</strong>
            <p>Focus the monthly readout on where forecast miss, incentive risk, and coverage pressure overlap.</p>
          </div>
        </div>
      </article>
    </section>
  `;
}

function renderDealerQueue() {
  const rows = filteredQueue();
  root.innerHTML = `
    ${kpis([
      { label: "Filtered partners", value: rows.length, note: "ranked dealer actions" },
      { label: "Average priority", value: rows.length ? (rows.reduce((sum, row) => sum + Number(row.priority_score), 0) / rows.length).toFixed(1) : "0.0", note: "model score" },
      { label: "Open exposure", value: formatMoney(rows.reduce((sum, row) => sum + Number(row.open_comp_exposure), 0)), note: "incentive risk" },
      { label: "Average quality", value: rows.length ? `${(rows.reduce((sum, row) => sum + Number(row.data_quality_score), 0) / rows.length).toFixed(1)}%` : "0.0%", note: "source trust" },
    ])}
    <section class="queue-grid">
      <div class="queue-row header">
        <span>Dealer</span>
        <span>Tier</span>
        <span>Score</span>
        <span>Forecast</span>
        <span>Inventory</span>
        <span>Recommended action</span>
      </div>
      ${rows
        .map(
          (row) => `
            <article class="queue-row">
              <div class="dealer-name">
                <strong>${row.dealer_name}</strong>
                <span>${row.region} | ${row.channel_type}</span>
              </div>
              <span class="tier-pill ${tierClass(row.risk_tier)}">${row.risk_tier}</span>
              <span class="score-pill">${row.priority_score}</span>
              <span class="metric-cell"><strong>${row.forecast_variance_pct}%</strong> variance</span>
              <span class="metric-cell"><strong>${row.inventory_days}</strong> days</span>
              <span>${row.recommended_action}</span>
            </article>
          `
        )
        .join("")}
    </section>
  `;
}

function renderTerritory() {
  root.innerHTML = `
    ${kpis([
      { label: "Promotion ROI", value: `${data.summary.avgPromoRoi}x`, note: "synthetic campaign mix" },
      { label: "Priority partners", value: data.summary.priorityCount, note: "watch or critical" },
      { label: "Open exposure", value: formatMoney(data.summary.openCompExposure), note: "compensation model" },
      { label: "Forecast accuracy", value: `${data.summary.forecastAccuracy}%`, note: "portfolio level" },
    ])}
    <section class="region-grid">
      ${data.regions
        .map(
          (row) => `
            <article class="region-card">
              <h3>${row.region}</h3>
              <div class="stat-list">
                <div><span>Avg score</span><strong>${row.avgScore}</strong></div>
                <div><span>Forecast variance</span><strong>${row.forecastVariance}%</strong></div>
                <div><span>Promo ROI</span><strong>${row.promoRoi}x</strong></div>
                <div><span>High coverage weeks</span><strong>${row.coverageRiskWeeks}</strong></div>
                <div><span>Open exposure</span><strong>${formatMoney(row.openCompExposure)}</strong></div>
              </div>
              <p>${row.action}</p>
            </article>
          `
        )
        .join("")}
    </section>
  `;
}

function renderQuality() {
  root.innerHTML = `
    <section class="layout-two">
      <article class="panel">
        <p class="section-label">Data trust</p>
        <h2>Reconciliation checks for executive reporting</h2>
        <div class="quality-list">
          ${data.qualityChecks
            .map(
              (row) => `
                <div class="quality-row">
                  <strong>${row.check}</strong>
                  <span class="result-pill result-${row.result.toLowerCase()}">${row.result}</span>
                  <p>${row.detail}</p>
                </div>
              `
            )
            .join("")}
        </div>
      </article>
      <article class="panel">
        <p class="section-label">Channel health</p>
        <h2>Accuracy and inventory by channel</h2>
        <section class="channel-grid">
          ${data.channels
            .map(
              (row) => `
                <article class="channel-card">
                  <h3>${row.channel}</h3>
                  <div class="stat-list">
                    <div><span>Avg score</span><strong>${row.avgScore}</strong></div>
                    <div><span>Accuracy</span><strong>${row.accuracy}%</strong></div>
                    <div><span>Inventory</span><strong>${row.inventoryDays} days</strong></div>
                    <div><span>Quality</span><strong>${row.dataQuality}%</strong></div>
                  </div>
                </article>
              `
            )
            .join("")}
        </section>
      </article>
    </section>
  `;
}

function render() {
  if (state.view === "executive") renderExecutive();
  if (state.view === "dealers") renderDealerQueue();
  if (state.view === "territory") renderTerritory();
  if (state.view === "quality") renderQuality();
}

optionList(regionFilter, data.filters.regions);
optionList(channelFilter, data.filters.channels);

regionFilter.addEventListener("change", (event) => {
  state.region = event.target.value;
  render();
});

channelFilter.addEventListener("change", (event) => {
  state.channel = event.target.value;
  render();
});

tabs.forEach((tab) => {
  tab.addEventListener("click", () => {
    tabs.forEach((item) => item.classList.remove("active"));
    tab.classList.add("active");
    state.view = tab.dataset.view;
    render();
  });
});

render();
