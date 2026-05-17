const data = window.projectData;
let scenarioKey = "base";

function render() {
  const scenario = data.scenarios[scenarioKey];
  document.querySelector("#scenario-name").textContent = scenario.name;
  document.querySelector("#forecast-metrics").innerHTML = scenario.metrics.map(([label, value]) => `<div><span>${label}</span><strong>${value}</strong></div>`).join("");
  document.querySelector("#insights").innerHTML = scenario.insights.map((item) => `<p>${item}</p>`).join("");
  document.querySelector("#recommendations").innerHTML = scenario.recs.map((item, index) => `<p><b>${index + 1}</b> ${item}</p>`).join("");
  document.querySelector("#territories").innerHTML = data.territories.map(([name, status, score, note]) => `
    <article>
      <span>${status}</span>
      <h3>${name}</h3>
      <div class="gauge"><i style="height:${score}%"></i></div>
      <p>${note}</p>
    </article>
  `).join("");
  document.querySelectorAll("[data-scenario]").forEach((button) => {
    button.classList.toggle("active", button.dataset.scenario === scenarioKey);
    button.addEventListener("click", () => {
      scenarioKey = button.dataset.scenario;
      render();
    }, { once: true });
  });
}

render();
