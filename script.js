// Fetches the rankings from the Flask API and fills in the page.

(function () {
  "use strict";

  function el(tag, text, className) {
    var node = document.createElement(tag);
    if (text !== undefined) {
      node.textContent = text;
    }
    if (className) {
      node.className = className;
    }
    return node;
  }

  function showError(statusId, message) {
    var node = document.getElementById(statusId);
    node.textContent = message;
    node.classList.add("error");
  }

  function renderRankings(rankings) {
    var tbody = document.querySelector("#rankings-table tbody");
    tbody.innerHTML = "";

    rankings.forEach(function (row) {
      var tr = document.createElement("tr");
      tr.appendChild(el("td", String(row.rank), "num"));
      tr.appendChild(el("td", row.team));
      tr.appendChild(el("td", row.record, "num"));
      tr.appendChild(el("td", row.rating.toFixed(4), "num"));
      tbody.appendChild(tr);
    });

    document.getElementById("status").hidden = true;
    document.getElementById("rankings-table").hidden = false;
  }

  function formatB(value) {
    return value.toFixed(1);
  }

  function renderMatrix(teams, matrix, b) {
    var table = document.getElementById("matrix-table");
    table.innerHTML = "";

    var thead = document.createElement("thead");
    var headRow = document.createElement("tr");
    headRow.appendChild(el("th", ""));
    teams.forEach(function (team) {
      headRow.appendChild(el("th", team));
    });
    headRow.appendChild(el("th", "b", "b-col"));
    thead.appendChild(headRow);
    table.appendChild(thead);

    var tbody = document.createElement("tbody");
    matrix.forEach(function (rowValues, i) {
      var tr = document.createElement("tr");
      tr.appendChild(el("td", teams[i]));
      rowValues.forEach(function (value, j) {
        tr.appendChild(el("td", String(value), i === j ? "diag" : ""));
      });
      tr.appendChild(el("td", formatB(b[i]), "b-col"));
      tbody.appendChild(tr);
    });
    table.appendChild(tbody);

    document.getElementById("matrix-status").hidden = true;
    document.getElementById("matrix-wrap").hidden = false;
  }

  function renderChecks(checks) {
    var text =
      "Check: the residual ||Cr − b|| is " +
      checks.residual_norm.toExponential(2) +
      " (effectively zero), and the ratings sum to " +
      checks.sum_of_ratings +
      ", matching n/2 = " +
      checks.expected_sum +
      ".";
    document.getElementById("checks").textContent = text;
  }

  function renderGames(games) {
    var list = document.getElementById("games-list");
    list.innerHTML = "";
    games.forEach(function (game) {
      list.appendChild(el("li", game.winner + " defeated " + game.loser));
    });
    document.getElementById("games-details").hidden = false;
  }

  fetch("/api/rankings")
    .then(function (response) {
      if (!response.ok) {
        throw new Error("Server returned status " + response.status);
      }
      return response.json();
    })
    .then(function (data) {
      renderRankings(data.rankings);
      renderMatrix(data.teams, data.matrix, data.b);
      renderChecks(data.checks);
      renderGames(data.games);
    })
    .catch(function (error) {
      showError("status", "Could not load rankings: " + error.message);
      showError("matrix-status", "Could not load the system.");
    });
})();
