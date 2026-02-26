/**
 * Trek Safety AI - Frontend
 * Calls backend POST /predict-by-location with a single location; shows risk level, confidence, and reasons.
 */

(function () {
  // Backend URL: change if you run the API on a different host/port
  const API_BASE = "http://127.0.0.1:8000";

  const form = document.getElementById("predict-form");
  const resultSection = document.getElementById("result-section");
  const submitBtn = document.getElementById("submit-btn");

  /**
   * Get form payload: only location (place name or coordinates).
   */
  function getFormPayload() {
    return {
      location: (form.location && form.location.value) ? String(form.location.value).trim() : "",
    };
  }

  /**
   * Map risk_level string to CSS class for green / yellow / red theme.
   */
  function riskClass(riskLevel) {
    if (riskLevel === "Safe") return "safe";
    if (riskLevel === "Moderate_Risk") return "moderate";
    if (riskLevel === "High_Risk") return "high";
    return "";
  }

  /**
   * Compute safety score 0-100 from confidence.
   * Safe probability maps to score; higher Safe = higher score.
   */
  function getSafetyScore(confidence) {
    if (!confidence || typeof confidence.Safe !== "number") return 50;
    return Math.round(confidence.Safe * 100);
  }

  /**
   * Get recommendation text based on risk level.
   */
  function getRecommendation(riskLevel) {
    if (riskLevel === "Safe") return "Route conditions look safe. Proceed with normal precautions.";
    if (riskLevel === "Moderate_Risk") return "Some risks detected. Trek carefully and monitor weather.";
    if (riskLevel === "High_Risk") return "High risk detected. Avoid trekking in current conditions.";
    return "Review the factors below before deciding.";
  }

  /**
   * Build HTML for the result card and inject into result-section.
   * Includes risk level, safety score, meter bar, recommendation, confidence, reasons.
   */
  function showResult(data) {
    const cls = riskClass(data.risk_level);
    var score = getSafetyScore(data.confidence);
    var recommendation = getRecommendation(data.risk_level);

    var meterFillClass = cls || "safe";
    var meterHtml =
      "<div class=\"safety-meter-wrap\">" +
      "<div class=\"safety-meter-label\">Safety meter</div>" +
      "<div class=\"safety-meter-track\">" +
      "<div class=\"safety-meter-fill " + meterFillClass + "\" style=\"width:" + score + "%\"></div>" +
      "</div></div>";

    var scoreHtml = "<div class=\"safety-score\">Safety Score: " + score + " / 100</div>";

    var recommendationHtml = "<p class=\"recommendation\">" + escapeHtml(recommendation) + "</p>";

    var confidenceHtml = "";
    if (data.confidence && Object.keys(data.confidence).length > 0) {
      confidenceHtml = "<ul class=\"confidence-list\">";
      for (var key in data.confidence) {
        if (data.confidence.hasOwnProperty(key)) {
          var pct = Math.round(data.confidence[key] * 100);
          confidenceHtml += "<li>" + escapeHtml(key) + ": " + pct + "%</li>";
        }
      }
      confidenceHtml += "</ul>";
    }

    var reasonsHtml = "";
    if (data.reasons && data.reasons.length > 0) {
      reasonsHtml = "<strong>Reasoning</strong><ul class=\"reasons-list\">" +
        data.reasons.map(function (r) { return "<li>" + escapeHtml(r) + "</li>"; }).join("") +
        "</ul>";
    }

    resultSection.innerHTML =
      "<div class=\"result-card " + cls + "\">" +
      "<h3>Predicted Risk Level</h3>" +
      "<div class=\"risk-level\">" + escapeHtml(data.risk_level) + "</div>" +
      scoreHtml +
      meterHtml +
      recommendationHtml +
      confidenceHtml +
      reasonsHtml +
      "</div>";
  }

  /**
   * Show error message in result area.
   */
  function showError(message) {
    resultSection.innerHTML =
      "<div class=\"result-card\">" +
      "<p class=\"error-message\">" + escapeHtml(message) + "</p>" +
      "</div>";
  }

  function escapeHtml(text) {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
  }

  form.addEventListener("submit", async function (e) {
    e.preventDefault();
    submitBtn.disabled = true;
    resultSection.innerHTML = "<p>Checking…</p>";

    const payload = getFormPayload();

    try {
      const res = await fetch(API_BASE + "/predict-by-location", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      const data = await res.json();

      if (!res.ok) {
        var msg = data.detail;
        if (Array.isArray(msg)) msg = msg.map(function (x) { return x.msg || x; }).join("; ");
        else if (typeof msg !== "string") msg = "Request failed. Is the backend running?";
        showError(msg);
        return;
      }
      showResult(data);
    } catch (err) {
      showError("Could not reach the server. Start the backend with: uvicorn backend.app:app --reload");
    } finally {
      submitBtn.disabled = false;
    }
  });
})();
