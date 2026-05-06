function getCookie(name) {
  const cookies = document.cookie ? document.cookie.split(";") : [];

  for (const cookie of cookies) {
    const trimmed = cookie.trim();
    if (trimmed.startsWith(`${name}=`)) {
      return decodeURIComponent(trimmed.substring(name.length + 1));
    }
  }

  return null;
}

function renderStatusChart(canvasId, labelsId, valuesId) {
  const canvas = document.getElementById(canvasId);
  if (!canvas || typeof Chart === "undefined") {
    return;
  }

  const labels = JSON.parse(document.getElementById(labelsId).textContent);
  const values = JSON.parse(document.getElementById(valuesId).textContent);

  new Chart(canvas, {
    type: "doughnut",
    data: {
      labels,
      datasets: [{
        data: values,
        backgroundColor: ["#2563eb", "#f59e0b", "#64748b", "#16a34a"],
      }],
    },
    options: {
      plugins: {
        legend: {
          position: "bottom",
        },
      },
    },
  });
}

document.addEventListener("change", async (event) => {
  const select = event.target.closest(".status-select");
  if (!select) {
    return;
  }

  const body = new URLSearchParams({ status: select.value });
  const response = await fetch(select.dataset.url, {
    method: "POST",
    headers: {
      "X-CSRFToken": getCookie("csrftoken"),
      "X-Requested-With": "XMLHttpRequest",
    },
    body,
  });

  if (!response.ok) {
    alert("Nao foi possivel atualizar o status.");
  }
});

document.addEventListener("click", async (event) => {
  const button = event.target.closest(".detail-button");
  if (!button) {
    return;
  }

  const response = await fetch(button.dataset.url, {
    headers: { "X-Requested-With": "XMLHttpRequest" },
  });
  const data = await response.json();
  const body = document.getElementById("detailsModalBody");

  body.innerHTML = `
    <dl class="row mb-0">
      <dt class="col-sm-4">Numero</dt><dd class="col-sm-8">${data.numero}</dd>
      <dt class="col-sm-4">Cliente</dt><dd class="col-sm-8">${data.cliente}</dd>
      <dt class="col-sm-4">Tribunal</dt><dd class="col-sm-8">${data.tribunal}</dd>
      <dt class="col-sm-4">Vara</dt><dd class="col-sm-8">${data.vara}</dd>
      <dt class="col-sm-4">Status</dt><dd class="col-sm-8">${data.status}</dd>
      <dt class="col-sm-4">Responsavel</dt><dd class="col-sm-8">${data.responsavel || "-"}</dd>
    </dl>
  `;

  bootstrap.Modal.getOrCreateInstance(document.getElementById("detailsModal")).show();
});

document.addEventListener("submit", async (event) => {
  const form = event.target.closest(".ajax-movimentacao-form");
  if (!form) {
    return;
  }

  event.preventDefault();
  const response = await fetch(form.action, {
    method: "POST",
    headers: { "X-Requested-With": "XMLHttpRequest" },
    body: new FormData(form),
  });

  if (!response.ok) {
    alert("Nao foi possivel salvar a movimentacao.");
    return;
  }

  const data = await response.json();
  const list = document.getElementById("movimentacoesList");
  const item = document.createElement("div");
  item.className = "list-group-item px-0";
  item.innerHTML = `
    <strong>${data.movimentacao.titulo}</strong>
    <div class="small text-secondary">${data.movimentacao.data_evento}</div>
  `;
  list.prepend(item);
  form.reset();
  bootstrap.Modal.getInstance(document.getElementById("movimentacaoModal")).hide();
});
