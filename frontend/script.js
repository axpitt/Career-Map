/* =====================================================================
   CareerMap AI — script.js
   ===================================================================== */

// Configuration
const CONFIG = {
    API_URL: window.location.protocol === 'file:' || window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
        ? 'http://localhost:8000/analyze'
        : 'https://careermap-ai-backend.onrender.com/analyze', // Update with your deployed backend URL
    API_KEY: '', // Optional: add X-API-Key here for a private backend. Not secure in public static builds.
    MAX_FILE_SIZE_MB: 10,
    MAX_FILE_SIZE_BYTES: 10 * 1024 * 1024,
};

// ── DOM References ───────────────────────────────────────────────────
const elements = {
    form: document.getElementById("upload-form"),
    fileInput: document.getElementById("resume-file"),
    cityInput: document.getElementById("city-input"),
    dropZone: document.getElementById("drop-zone"),
    fileNameEl: document.getElementById("file-name"),
    analyzeBtn: document.getElementById("analyze-btn"),
    errorBanner: document.getElementById("error-banner"),
    errorMsg: document.getElementById("error-msg"),
    spinnerOverlay: document.getElementById("spinner-overlay"),
    resultsSection: document.getElementById("results-section"),
    // Results elements
    elScore: document.getElementById("res-score"),
    elLevelCard: document.getElementById("level-card"),
    elLevelIcon: document.getElementById("level-icon"),
    elLevelBadge: document.getElementById("level-badge"),
    elStrengths: document.getElementById("list-strengths"),
    elWeaknesses: document.getElementById("list-weaknesses"),
    elCompanies: document.getElementById("list-companies"),
    elUpgradeCo: document.getElementById("list-upgrade-companies"),
    elUpgradeReq: document.getElementById("list-upgrade-req"),
    // Subscription elements
    subscriptionSection: document.getElementById("subscription-section"),
    btnUpgradePro: document.getElementById("btn-upgrade-pro"),
    btnUpgradeEnterprise: document.getElementById("btn-upgrade-enterprise"),
};

// Track subscription state
let hasAnalyzedResume = false;

// ── Drag & Drop ──────────────────────────────────────────────────────
["dragenter", "dragover"].forEach(evt =>
  elements.dropZone.addEventListener(evt, (e) => {
    e.preventDefault();
    elements.dropZone.classList.add("dragover");
  })
);

["dragleave", "drop"].forEach(evt =>
  elements.dropZone.addEventListener(evt, (e) => {
    e.preventDefault();
    elements.dropZone.classList.remove("dragover");
  })
);

elements.dropZone.addEventListener("drop", (e) => {
  const file = e.dataTransfer.files[0];
  if (file) {
    elements.fileInput.files = e.dataTransfer.files;
    handleFileSelected(file);
  }
});

elements.fileInput.addEventListener("change", () => {
  if (elements.fileInput.files.length > 0) {
    handleFileSelected(elements.fileInput.files[0]);
  }
});

function handleFileSelected(file) {
  elements.fileNameEl.textContent = `📄 ${file.name}`;
  elements.fileNameEl.style.display = "block";
  elements.dropZone.classList.add("has-file");
}

// ── Form Submit ──────────────────────────────────────────────────────
elements.form.addEventListener("submit", async (e) => {
  e.preventDefault();
  clearError();
  clearResults();

  // ── Client-side validation ───────────────────────────────────────
  const file = elements.fileInput.files[0];
  const city = elements.cityInput.value.trim();

  if (!file) {
    showError("Please select a PDF resume file to upload.");
    return;
  }

  if (!file.name.toLowerCase().endsWith(".pdf")) {
    showError("Invalid file type. Only PDF files are accepted.");
    return;
  }

  if (file.size > CONFIG.MAX_FILE_SIZE_BYTES) {
    showError(`File is too large. Maximum allowed size is ${CONFIG.MAX_FILE_SIZE_MB} MB.`);
    return;
  }

  if (!city) {
    showError("Please enter your city before analyzing.");
    elements.cityInput.focus();
    return;
  }

  // ── Build FormData ───────────────────────────────────────────────
  const formData = new FormData();
  formData.append("file", file);
  formData.append("city", city);

  // ── Loading state ────────────────────────────────────────────────
  setLoading(true);

  try {
    const response = await fetch(CONFIG.API_URL, {
      method: "POST",
      headers: CONFIG.API_KEY ? { "X-API-Key": CONFIG.API_KEY } : {},
      body: formData,
    });

    let data;
    try {
      data = await response.json();
    } catch {
      throw new Error("Server returned an unreadable response. Please try again.");
    }

    if (!response.ok) {
      const detail = data?.detail || `Server error (HTTP ${response.status}).`;
      throw new Error(detail);
    }

    renderResults(data);

  } catch (err) {
    if (err instanceof TypeError && err.message.includes("fetch")) {
      showError(
        "Cannot connect to the backend. Make sure the server is running and accessible."
      );
    } else {
      showError(err.message || "An unexpected error occurred.");
    }
  } finally {
    setLoading(false);
  }
});

// ── Render Results ───────────────────────────────────────────────────
function renderResults(data) {
  // Score
  elements.elScore.textContent = data.score;

  // Level card class & badge
  const levelKey = data.level.toLowerCase(); // beginner | intermediate | strong
  const levelIcons = { beginner: "🌱", intermediate: "🚀", strong: "⭐" };

  elements.elLevelCard.className = `level-card ${levelKey}`;
  elements.elLevelBadge.className = `level-badge ${levelKey}`;
  elements.elLevelBadge.textContent = data.level;
  elements.elLevelIcon.textContent = levelIcons[levelKey] || "🎯";

  // Lists
  renderList(elements.elStrengths,   data.strengths,                "✅");
  renderList(elements.elWeaknesses,  data.weaknesses,               "⚠️");
  renderList(elements.elCompanies,   data.companies_to_apply,       "🏢");
  renderList(elements.elUpgradeCo,   data.upgrade_target_companies, "🎯");
  renderList(elements.elUpgradeReq,  data.upgrade_requirements,     "📌");

  // Show results
  elements.resultsSection.classList.add("visible");
  elements.resultsSection.scrollIntoView({ behavior: "smooth", block: "start" });

  // Show subscription section after first analysis
  if (!hasAnalyzedResume) {
    hasAnalyzedResume = true;
    setTimeout(() => {
      elements.subscriptionSection.classList.add("visible");
      elements.subscriptionSection.scrollIntoView({ behavior: "smooth", block: "center" });
    }, 500);
  }
}

function renderList(ulEl, items, icon) {
  ulEl.innerHTML = "";
  if (!Array.isArray(items) || items.length === 0) {
    const li = document.createElement("li");
    li.setAttribute("data-icon", "—");
    li.textContent = "No data returned.";
    ulEl.appendChild(li);
    return;
  }
  items.forEach((item) => {
    const li = document.createElement("li");
    li.setAttribute("data-icon", icon);
    li.textContent = item;
    ulEl.appendChild(li);
  });
}

// ── Reset ────────────────────────────────────────────────────────────
document.getElementById("reset-btn").addEventListener("click", () => {
  elements.form.reset();
  elements.fileNameEl.style.display = "none";
  elements.fileNameEl.textContent = "";
  elements.dropZone.classList.remove("has-file");
  clearError();
  clearResults();
  // Hide subscription section on reset
  elements.subscriptionSection.classList.remove("visible");
  hasAnalyzedResume = false;
  window.scrollTo({ top: 0, behavior: "smooth" });
});

// ── Subscription Button Handlers ────────────────────────────────────
elements.btnUpgradePro.addEventListener("click", () => {
  alert("🚀 Upgrade to Pro selected! This would redirect to payment processing.\n\nDemo: In production, this would open Stripe checkout or similar payment flow.");
});

elements.btnUpgradeEnterprise.addEventListener("click", () => {
  alert("👑 Enterprise plan selected! Our team will contact you shortly.\n\nDemo: In production, this would open a contact/sales form.");
});

// ── Helpers ──────────────────────────────────────────────────────────
function setLoading(isLoading) {
  elements.analyzeBtn.disabled = isLoading;
  elements.spinnerOverlay.classList.toggle("visible", isLoading);

  if (isLoading) {
    elements.analyzeBtn.innerHTML = `<span class="btn-spinner"></span> Analyzing…`;
  } else {
    elements.analyzeBtn.innerHTML = `🔍 Analyze My Resume`;
  }
}

function showError(msg) {
  elements.errorMsg.textContent = msg;
  elements.errorBanner.classList.add("visible");
  elements.errorBanner.scrollIntoView({ behavior: "smooth", block: "nearest" });
}

function clearError() {
  elements.errorBanner.classList.remove("visible");
  elements.errorMsg.textContent = "";
}

function clearResults() {
  elements.resultsSection.classList.remove("visible");
  [elements.elStrengths, elements.elWeaknesses, elements.elCompanies, elements.elUpgradeCo, elements.elUpgradeReq].forEach(
    (ul) => (ul.innerHTML = "")
  );
}
