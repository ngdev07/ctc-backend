// script.js

document.addEventListener('DOMContentLoaded', function () {

  // ============================================================
  // 1. MODE SOMBRE / CLAIR
  // ============================================================
  const themeToggle = document.getElementById('themeToggle');
  const html = document.documentElement;

  // Récupérer la préférence stockée ou système
  const storedTheme = localStorage.getItem('theme');
  if (storedTheme) {
    html.className = storedTheme;
  } else if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
    html.className = 'dark';
  } else {
    html.className = 'light';
  }

  themeToggle.addEventListener('click', function () {
    if (html.classList.contains('dark')) {
      html.classList.remove('dark');
      html.classList.add('light');
      localStorage.setItem('theme', 'light');
    } else {
      html.classList.remove('light');
      html.classList.add('dark');
      localStorage.setItem('theme', 'dark');
    }
  });

  // ============================================================
  // 2. RENDU DES ENDPOINTS
  // ============================================================
  function renderEndpoints(sectionKey, container) {
    const items = window.endpointsData[sectionKey];
    if (!items) return;
    let html = '';
    items.forEach(item => {
      const methodClass = 'method-' + item.method.toLowerCase();
      const bodyHtml = item.body ? `<pre class="code-block">${JSON.stringify(item.body, null, 2)}</pre>` : '<span class="text-gray-400 dark:text-gray-500 text-sm">Aucun body</span>';
      const responseHtml = item.response ? `<pre class="code-block">${JSON.stringify(item.response, null, 2)}</pre>` : '<span class="text-gray-400 dark:text-gray-500 text-sm">Non spécifié</span>';
      const paramsHtml = item.params ? `<div class="text-sm text-gray-600 dark:text-gray-400"><strong>Paramètres :</strong> ${Object.entries(item.params).map(([k,v]) => `${k} (${v})`).join(', ')}</div>` : '';
      html += `
        <div class="endpoint-item border border-gray-200 dark:border-gray-700 rounded-lg overflow-hidden shadow-sm bg-white dark:bg-gray-800 mb-3">
          <div class="endpoint-header flex flex-wrap items-center gap-3 px-4 py-3 bg-gray-50 dark:bg-gray-700/50 cursor-pointer hover:bg-gray-100 dark:hover:bg-gray-700 transition">
            <span class="method-badge ${methodClass} text-white text-xs font-bold px-2 py-0.5 rounded">${item.method}</span>
            <span class="path font-mono text-sm font-medium text-gray-800 dark:text-gray-200">${item.path}</span>
            <span class="perms ml-auto text-xs bg-gray-200 dark:bg-gray-600 text-gray-700 dark:text-gray-300 px-2 py-0.5 rounded-full">${item.permission}</span>
            <i class="fas fa-chevron-down text-gray-400 dark:text-gray-500 text-xs"></i>
          </div>
          <div class="endpoint-detail closed px-4 border-t border-gray-100 dark:border-gray-700">
            <div class="py-3 space-y-2">
              <p class="text-sm text-gray-600 dark:text-gray-400">${item.description}</p>
              ${paramsHtml}
              <div><span class="text-sm font-medium text-gray-700 dark:text-gray-300">Body :</span> ${bodyHtml}</div>
              <div><span class="text-sm font-medium text-gray-700 dark:text-gray-300">Réponse :</span> ${responseHtml}</div>
              <button class="try-btn text-blue-600 dark:text-blue-400 text-sm font-medium hover:underline" data-method="${item.method}" data-path="${item.path}" data-body='${JSON.stringify(item.body)}'> <i class="fas fa-play"></i> Try it</button>
            </div>
          </div>
        </div>
      `;
    });
    container.innerHTML = html;
  }

  // Remplir toutes les sections
  document.querySelectorAll('.endpoint-group').forEach(group => {
    const section = group.dataset.section;
    renderEndpoints(section, group);
  });

  // Auth
  renderEndpoints('auth', document.getElementById('auth-endpoints'));

  // ============================================================
  // 3. TOGGLE DES DÉTAILS
  // ============================================================
  document.addEventListener('click', function (e) {
    const header = e.target.closest('.endpoint-header');
    if (header) {
      const detail = header.nextElementSibling;
      if (detail && detail.classList.contains('endpoint-detail')) {
        detail.classList.toggle('closed');
        detail.classList.toggle('open');
        const icon = header.querySelector('.fa-chevron-down');
        if (icon) icon.classList.toggle('rotate-180');
      }
    }
  });

  // ============================================================
  // 4. RECHERCHE
  // ============================================================
  const searchInput = document.getElementById('searchInput');
  if (searchInput) {
    searchInput.addEventListener('input', function () {
      const query = this.value.toLowerCase().trim();
      document.querySelectorAll('.endpoint-item').forEach(item => {
        const text = item.textContent.toLowerCase();
        item.style.display = text.includes(query) ? '' : 'none';
      });
    });
  }

  // ============================================================
  // 5. MODAL "TRY IT"
  // ============================================================
  const modal = document.getElementById('tryModal');
  const closeModal = document.getElementById('closeModal');
  const modalContent = document.getElementById('modalContent');

  document.addEventListener('click', function (e) {
    const btn = e.target.closest('.try-btn');
    if (btn) {
      e.preventDefault();
      const method = btn.dataset.method;
      const path = btn.dataset.path;
      const body = JSON.parse(btn.dataset.body || 'null');
      modalContent.innerHTML = `
        <div class="space-y-3 text-gray-900 dark:text-white">
          <div class="flex items-center gap-2">
            <span class="method-badge method-${method.toLowerCase()} text-white text-xs font-bold px-2 py-0.5 rounded">${method}</span>
            <span class="font-mono text-sm">${path}</span>
          </div>
          <div class="bg-gray-50 dark:bg-gray-700 p-3 rounded border border-gray-200 dark:border-gray-600">
            <p class="text-sm font-medium">Requête simulée</p>
            ${body ? `<pre class="code-block text-xs">${JSON.stringify(body, null, 2)}</pre>` : '<span class="text-gray-400 dark:text-gray-500 text-sm">Aucun body</span>'}
          </div>
          <div class="bg-gray-50 dark:bg-gray-700 p-3 rounded border border-gray-200 dark:border-gray-600">
            <p class="text-sm font-medium">Réponse (simulée)</p>
            <pre class="code-block text-xs">{\n  "status": 200,\n  "message": "Succès (simulation)"\n}</pre>
          </div>
          <p class="text-xs text-gray-400 dark:text-gray-500">* Cette fonctionnalité est une démonstration.</p>
        </div>
      `;
      modal.classList.remove('hidden');
    }
  });

  if (closeModal) {
    closeModal.addEventListener('click', function () { modal.classList.add('hidden'); });
  }
  if (modal) {
    modal.addEventListener('click', function (e) {
      if (e.target === modal) modal.classList.add('hidden');
    });
  }

  // ============================================================
  // 6. SIDEBAR MOBILE
  // ============================================================
  const sidebar = document.getElementById('sidebar');
  const menuToggle = document.getElementById('menuToggle');

  if (menuToggle) {
    menuToggle.addEventListener('click', function () {
      sidebar.classList.toggle('-translate-x-full');
      // Pour le rendre visible, on override la classe md:translate-x-0
      // on utilise une classe .open pour forcer l'affichage
      sidebar.classList.toggle('open-mobile');
    });
  }

  // Fermer le sidebar en cliquant à l'extérieur (mobile)
  document.addEventListener('click', function (e) {
    if (window.innerWidth < 768) {
      if (!sidebar.contains(e.target) && !menuToggle.contains(e.target)) {
        sidebar.classList.add('-translate-x-full');
        sidebar.classList.remove('open-mobile');
      }
    }
  });

  // Au redimensionnement, réinitialiser si on passe en desktop
  window.addEventListener('resize', function () {
    if (window.innerWidth >= 768) {
      sidebar.classList.remove('-translate-x-full', 'open-mobile');
    }
  });

  // ============================================================
  // 7. LIEN ACTIF (SCROLL + CLIC)
  // ============================================================
  const links = document.querySelectorAll('#sidebar nav a');

  links.forEach(link => {
    link.addEventListener('click', function () {
      links.forEach(l => l.classList.remove('active'));
      this.classList.add('active');
      if (window.innerWidth < 768) {
        sidebar.classList.add('-translate-x-full');
        sidebar.classList.remove('open-mobile');
      }
    });
  });

  window.addEventListener('scroll', function () {
    let current = '';
    document.querySelectorAll('section[id], div[id]').forEach(sec => {
      const rect = sec.getBoundingClientRect();
      if (rect.top <= 100) current = sec.id;
    });
    links.forEach(link => {
      link.classList.remove('active');
      if (link.getAttribute('href') === '#' + current) link.classList.add('active');
    });
  });

  // Ouvrir le premier endpoint par défaut ? (optionnel)
  // const firstDetail = document.querySelector('.endpoint-detail');
  // if (firstDetail) {
  //   firstDetail.classList.remove('closed');
  //   firstDetail.classList.add('open');
  // }
});