(function () {
  const DATA_URL = "../data/references.yaml";

  function parseSimpleYaml(text) {
    const lines = text.split(/\r?\n/);
    const items = [];
    let current = null;

    for (const rawLine of lines) {
      const line = rawLine.replace(/\t/g, "  ");
      if (/^\s*-\s+id:/.test(line)) {
        if (current) items.push(current);
        current = {};
        const value = line.replace(/^\s*-\s+id:\s*/, "").trim();
        current.id = stripQuotes(value);
        continue;
      }
      if (!current) continue;
      const match = line.match(/^\s+([a-z_]+):\s*(.*)$/);
      if (!match) continue;
      const [, key, value] = match;
      current[key] = stripQuotes(value.trim());
    }

    if (current) items.push(current);
    return items;
  }

  function stripQuotes(value) {
    if (!value) return "";
    if ((value.startsWith('"') && value.endsWith('"')) || (value.startsWith("'") && value.endsWith("'"))) {
      return value.slice(1, -1);
    }
    return value;
  }

  function escapeHtml(text) {
    return String(text || "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#39;");
  }

  function referenceLabel(ref) {
    const author = shortAuthor(ref.authors) || ref.title || "Referens";
    const title = ref.title || "Studie";
    const year = ref.year ? ` (${ref.year})` : "";
    const summary = ref.short || ref.summary || "";
    return `${author} / ${title}${year} — ${summary}`;
  }

  function shortAuthor(authors) {
    if (!authors) return "";
    if (/et al\./i.test(authors)) return authors;
    const first = authors.split(/[;,]/)[0].trim();
    if (!first) return "";
    if (first.includes(" ")) {
      const parts = first.split(/\s+/);
      return parts[parts.length - 1];
    }
    return first;
  }

  function detailedExplanation(ref) {
    const long = (ref.abstract || "").trim();
    const short = (ref.summary || ref.short || "").trim();
    if (long && long !== short) return long;
    if (long) return long;
    return short;
  }

  function applyInlineFootnoteTitles(refMap) {
    const links = document.querySelectorAll("a[data-ref]");
    links.forEach((link) => {
      const ref = refMap.get(link.dataset.ref);
      if (!ref) return;
      link.setAttribute("href", `../vetenskap/index.html#${ref.id}`);
      if (!link.getAttribute("title")) {
        link.setAttribute("title", ref.short || ref.summary || ref.title);
      }
      link.classList.add("footnote-ref");
    });
  }

  function renderFootnotes(refMap) {
    if (document.body.dataset.referencesMode === "library") return;

    const main = document.querySelector("main.container");
    if (!main) return;
    const prose = main.querySelector(".prose-page") || main.querySelector(".content-stack > .content-card:first-child");
    if (!prose) return;

    const oldRefs = prose.querySelector("section.references");
    if (oldRefs) oldRefs.remove();
    prose.querySelectorAll(".section-footnotes").forEach((node) => node.remove());
    [...main.querySelectorAll(".content-stack > .content-card")].forEach((card) => {
      const heading = card.querySelector("h2");
      if (heading && heading.textContent.trim() === "Referenser") {
        card.remove();
      }
    });

    const sections = [];
    let current = { nodes: [], refs: [] };

    [...prose.children].forEach((node) => {
      if (node.classList && node.classList.contains("section-footnotes")) return;
      if (node.tagName === "H2") {
        if (current.nodes.length || current.refs.length) sections.push(current);
        current = { heading: node, nodes: [node], refs: [] };
        return;
      }
      current.nodes.push(node);
      const refs = [...node.querySelectorAll("a[data-ref]")].map((link) => link.dataset.ref).filter(Boolean);
      refs.forEach((id) => {
        if (!current.refs.includes(id)) current.refs.push(id);
      });
    });
    if (current.nodes.length || current.refs.length) sections.push(current);

    sections.forEach((section) => {
      if (!section.refs.length) return;

      const aside = document.createElement("aside");
      aside.className = "section-footnotes";
      aside.setAttribute("aria-label", "Fotnoter");
      const wrapper = document.createElement("div");
      wrapper.className = "section-footnotes-items";
      wrapper.innerHTML = section.refs.map((id, idx) => {
        const ref = refMap.get(id);
        if (!ref) return "";
        return `<p id="footnote-${escapeHtml(id)}"><a href="../vetenskap/index.html#${escapeHtml(id)}" data-ref="${escapeHtml(id)}" title="${escapeHtml(ref.short || ref.summary || ref.title)}"><span class="footnote-number">[${idx + 1}]</span> <span class="footnote-text">${escapeHtml(referenceLabel(ref))}</span></a></p>`;
      }).join("");
      aside.appendChild(wrapper);

      let insertAfter = null;
      for (let i = section.nodes.length - 1; i >= 0; i--) {
        const node = section.nodes[i];
        if (node.tagName !== "HR") {
          insertAfter = node;
          break;
        }
      }
      if (insertAfter) insertAfter.insertAdjacentElement("afterend", aside);
    });
  }

  function renderReferenceLibrary(refs) {
    const host = document.querySelector("[data-reference-library]");
    if (!host) return;

    const categoryOrder = ["Risk", "Mätvärden", "Diagnoser", "Livsstil", "Läkemedel", "Longevity"];

    const grouped = new Map();
    refs.forEach((ref) => {
      const key = ref.category || "Övrigt";
      if (!grouped.has(key)) grouped.set(key, []);
      grouped.get(key).push(ref);
    });

    const renderCard = (ref) => {
      const doiUrl = ref.doi ? (ref.doi.startsWith("http") ? ref.doi : `https://doi.org/${ref.doi}`) : "";
      const metaParts = [];
      if (ref.authors) metaParts.push(escapeHtml(ref.authors));
      if (ref.journal || ref.year) {
        const journalYear = [ref.journal, ref.year ? `(${ref.year})` : ""].filter(Boolean).join(" ");
        if (journalYear) metaParts.push(escapeHtml(journalYear));
      }
      if (doiUrl) {
        metaParts.push(`<a href="${escapeHtml(doiUrl)}" target="_blank" rel="noopener noreferrer">DOI</a>`);
      }
      const metaLine = metaParts.length ? `<p class="reference-meta-line">${metaParts.join(" · ")}</p>` : "";

      return `
        <details class="reference-card" id="${escapeHtml(ref.id)}" data-ref-card>
          <summary class="reference-summary">
            <div class="reference-header">
              <h2>${escapeHtml(ref.title)}</h2>
            </div>
            <p class="reference-short">${escapeHtml(ref.short || ref.summary || "")}</p>
            <span class="reference-toggle">Visa mer</span>
          </summary>
          <div class="reference-body">
            <p class="reference-long">${escapeHtml(detailedExplanation(ref))}</p>
            ${metaLine}
          </div>
        </details>
      `;
    };

    const sections = [...grouped.keys()]
      .sort((a, b) => {
        const ai = categoryOrder.indexOf(a);
        const bi = categoryOrder.indexOf(b);
        if (ai === -1 && bi === -1) return a.localeCompare(b, "sv");
        if (ai === -1) return 1;
        if (bi === -1) return -1;
        return ai - bi;
      })
      .map((category) => {
        const cards = grouped.get(category).map(renderCard).join("");
        return `
          <section class="reference-group" aria-labelledby="group-${escapeHtml(category)}">
            <div class="reference-group-header">
              <h2 id="group-${escapeHtml(category)}">${escapeHtml(category)}</h2>
            </div>
            <div class="reference-group-cards">
              ${cards}
            </div>
          </section>
        `;
      })
      .join("");

    host.innerHTML = sections;

    host.querySelectorAll("[data-ref-card]").forEach((card) => {
      const toggle = card.querySelector(".reference-toggle");
      if (!toggle) return;
      const sync = () => {
        toggle.textContent = card.open ? "Visa mindre" : "Visa mer";
      };
      sync();
      card.addEventListener("toggle", sync);
    });

    const focusHashTarget = () => {
      const hash = window.location.hash.replace(/^#/, "");
      host.querySelectorAll(".is-targeted").forEach((node) => node.classList.remove("is-targeted"));
      if (!hash) return;
      const target = document.getElementById(hash);
      if (target && target.matches("[data-ref-card]")) {
        target.open = true;
        target.classList.add("is-targeted");
        setTimeout(() => {
          target.scrollIntoView({ behavior: "smooth", block: "center" });
        }, 60);
      }
    };

    focusHashTarget();
    window.addEventListener("hashchange", focusHashTarget);
  }

  function renderAll(refs) {
    const refMap = new Map(refs.map((ref) => [ref.id, ref]));
    applyInlineFootnoteTitles(refMap);
    renderFootnotes(refMap);
    renderReferenceLibrary(refs);
  }

  if (Array.isArray(window.__REFERENCE_DATA__) && window.__REFERENCE_DATA__.length) {
    renderAll(window.__REFERENCE_DATA__);
    return;
  }

  fetch(DATA_URL)
    .then((response) => response.text())
    .then((yaml) => {
      const refs = parseSimpleYaml(yaml);
      renderAll(refs);
    })
    .catch((error) => {
      console.error("Kunde inte läsa referensdata:", error);
    });
})();
