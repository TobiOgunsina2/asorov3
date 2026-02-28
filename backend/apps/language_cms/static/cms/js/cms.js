// LinguaCMS — client-side interactions

// ── Auto-dismiss toasts ───────────────────────────────────────────────────
document.addEventListener("DOMContentLoaded", () => {
  setTimeout(() => {
    document.querySelectorAll(".message-toast").forEach(el => {
      el.style.transition = "opacity 400ms";
      el.style.opacity = "0";
      setTimeout(() => el.remove(), 400);
    });
  }, 3500);
});

// ── Re-run toast fade after HTMX swaps ───────────────────────────────────
document.body.addEventListener("htmx:afterSwap", () => {
  setTimeout(() => {
    document.querySelectorAll(".message-toast").forEach(el => {
      el.style.transition = "opacity 400ms";
      el.style.opacity = "0";
      setTimeout(() => el.remove(), 400);
    });
  }, 3500);
});

// ── Modal helpers ─────────────────────────────────────────────────────────
function openModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) {
    modal.style.display = "flex";
    document.body.style.overflow = "hidden";
  }
}

function closeModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) {
    modal.style.display = "none";
    document.body.style.overflow = "";
  }
}

// Close modal on overlay click
document.addEventListener("click", (e) => {
  if (e.target.classList.contains("modal-overlay")) {
    e.target.style.display = "none";
    document.body.style.overflow = "";
  }
});

// Close modal on Escape
document.addEventListener("keydown", (e) => {
  if (e.key === "Escape") {
    document.querySelectorAll(".modal-overlay").forEach(m => {
      m.style.display = "none";
    });
    document.body.style.overflow = "";
  }
});

// ── After HTMX form submits (204 response), close modal + refresh list ───
document.body.addEventListener("htmx:responseError", (e) => {
  console.warn("HTMX error", e.detail);
});

document.body.addEventListener("contentChanged", () => {
  // Close any open modals
  document.querySelectorAll(".modal-overlay").forEach(m => {
    m.style.display = "none";
  });
  document.body.style.overflow = "";
});

// ── Word Picker (for Phrase/Sentence forms) ───────────────────────────────
class WordPicker {
  constructor(container) {
    this.container = container;
    this.hiddenInput = container.querySelector("[data-word-ids]");
    this.selectedArea = container.querySelector(".selected-words-area");
    this.chips = container.querySelectorAll(".word-chip");
    this.selected = new Map(); // id → text
    this.searchInput = container.querySelector(".picker-search");

    this.chips.forEach(chip => {
      chip.addEventListener("click", () => this.toggle(chip));
    });

    if (this.searchInput) {
      this.searchInput.addEventListener("input", () => this.filterChips());
    }

    this.render();
  }

  toggle(chip) {
    const id = chip.dataset.wordId;
    const text = chip.dataset.wordText;
    if (this.selected.has(id)) {
      this.selected.delete(id);
      chip.classList.remove("selected");
    } else {
      this.selected.set(id, text);
      chip.classList.add("selected");
    }
    this.render();
  }

  remove(id) {
    this.selected.delete(id);
    const chip = this.container.querySelector(`[data-word-id="${id}"]`);
    if (chip) chip.classList.remove("selected");
    this.render();
  }

  render() {
    this.selectedArea.innerHTML = "";
    if (this.selected.size === 0) {
      this.selectedArea.innerHTML = '<span class="empty-hint">Click words above to add them</span>';
    } else {
      this.selected.forEach((text, id) => {
        const el = document.createElement("span");
        el.className = "selected-chip";
        el.innerHTML = `${text} <button type="button" onclick="wordPickers.get('${this.container.id}').remove('${id}')">×</button>`;
        this.selectedArea.appendChild(el);
      });
    }
    if (this.hiddenInput) {
      this.hiddenInput.value = [...this.selected.keys()].join(",");
    }
  }

  filterChips() {
    const q = this.searchInput.value.toLowerCase();
    this.chips.forEach(chip => {
      const matches = chip.dataset.wordText.toLowerCase().includes(q);
      chip.style.display = matches ? "" : "none";
    });
  }
}

// Initialize all word pickers
const wordPickers = new Map();
document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll("[data-word-picker]").forEach(el => {
    wordPickers.set(el.id, new WordPicker(el));
  });
});

// Re-init after HTMX swaps in new content
document.body.addEventListener("htmx:afterSwap", () => {
  document.querySelectorAll("[data-word-picker]").forEach(el => {
    if (!wordPickers.has(el.id)) {
      wordPickers.set(el.id, new WordPicker(el));
    }
  });
});

// ── Highlight builder for SentenceComponent ──────────────────────────────
function updateHighlightPreview(inputId, previewId) {
  const input = document.getElementById(inputId);
  const preview = document.getElementById(previewId);
  if (!input || !preview) return;
  const sentence = preview.dataset.sentence || "";
  const parts = input.value.split(",").map(p => p.trim().split("-").map(Number));
  let html = sentence;
  // Simple single-range highlight
  if (parts[0] && parts[0].length === 2) {
    const [s, e] = parts[0];
    html = sentence.slice(0, s)
      + `<mark style="background:var(--amber-pale);padding:0 2px;border-radius:2px">`
      + sentence.slice(s, e)
      + `</mark>`
      + sentence.slice(e);
  }
  preview.innerHTML = html;
}
