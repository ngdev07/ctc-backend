document.addEventListener('DOMContentLoaded', function () {

  // === VÉRIFICATION DES DONNÉES ===
  console.log('=== DÉMARRAGE SCRIPT ===');
  
  if (typeof endpointsData === 'undefined') {
    console.error('❌ endpointsData non défini !');
    // Créer des données de secours pour éviter une page vide
    window.endpointsData = {
      auth: [
        { method: 'GET', path: '/api/test/', description: 'Données non chargées (fallback)', permission: 'PUBLIC', params: null, body: null, response: { message: 'Vérifiez le contexte Django' } }
      ]
    };
    document.body.insertAdjacentHTML('afterbegin', '<div style="background:orange;color:#000;padding:10px;text-align:center;">⚠️ Données non chargées – utilisation de fallback</div>');
  } else {
    console.log('✅ endpointsData chargé, clés :', Object.keys(endpointsData));
  }

  // === FONCTION DE RENDU ===
  function renderEndpoints(sectionKey, container) {
    if (!container) {
      console.warn('⚠️ Conteneur manquant pour', sectionKey);
      return;
    }
    const items = window.endpointsData[sectionKey];
    if (!items || !Array.isArray(items) || items.length === 0) {
      console.warn(`⚠️ Aucun endpoint pour ${sectionKey}`);
      container.innerHTML = `<p class="text-gray-400 dark:text-gray-500 text-sm">Aucun endpoint pour cette section.</p>`;
      return;
    }
    console.log(`✅ Rendu de ${items.length} endpoints pour ${sectionKey}`);

    let html = '';
    items.forEach(item => {
      const methodClass = 'method-' + (item.method || 'get').toLowerCase();
      const bodyHtml = item.body ? `<pre class="code-block">${JSON.stringify(item.body, null, 2)}</pre>` : '<span class="text-gray-400 dark:text-gray-500 text-sm">Aucun body</span>';
      const responseHtml = item.response ? `<pre class="code-block">${JSON.stringify(item.response, null, 2)}</pre>` : '<span class="text-gray-400 dark:text-gray-500 text-sm">Non spécifié</span>';
      const paramsHtml = item.params && Object.keys(item.params).length ? 
        `<div class="text-sm text-gray-600 dark:text-gray-400"><strong>Paramètres :</strong> ${Object.entries(item.params).map(([k,v]) => `${k} (${v})`).join(', ')}</div>` : '';

      html += `
        <div class="endpoint-item border border-gray-200 dark:border-gray-700 rounded-lg overflow-hidden shadow-sm bg-white dark:bg-gray-800 mb-3">
          <div class="endpoint-header flex flex-wrap items-center gap-3 px-4 py-3 bg-gray-50 dark:bg-gray-700/50 cursor-pointer hover:bg-gray-100 dark:hover:bg-gray-700 transition">
            <span class="method-badge ${methodClass} text-white text-xs font-bold px-2 py-0.5 rounded">${item.method || 'GET'}</span>
            <span class="path font-mono text-sm font-medium text-gray-800 dark:text-gray-200">${item.path || '/'}</span>
            <span class="perms ml-auto text-xs bg-gray-200 dark:bg-gray-600 text-gray-700 dark:text-gray-300 px-2 py-0.5 rounded-full">${item.permission || 'PUBLIC'}</span>
            <i class="fas fa-chevron-down text-gray-400 dark:text-gray-500 text-xs"></i>
          </div>
          <div class="endpoint-detail closed px-4 border-t border-gray-100 dark:border-gray-700">
            <div class="py-3 space-y-2">
              <p class="text-sm text-gray-600 dark:text-gray-400">${item.description || ''}</p>
              ${paramsHtml}
              <div><span class="text-sm font-medium text-gray-700 dark:text-gray-300">Body :</span> ${bodyHtml}</div>
              <div><span class="text-sm font-medium text-gray-700 dark:text-gray-300">Réponse :</span> ${responseHtml}</div>
              <button class="try-btn text-blue-600 dark:text-blue-400 text-sm font-medium hover:underline" data-method="${item.method || 'GET'}" data-path="${item.path || '/'}" data-body='${JSON.stringify(item.body || null)}'> <i class="fas fa-play"></i> Try it</button>
            </div>
          </div>
        </div>
      `;
    });
    container.innerHTML = html;
  }

  // === LANCER LE RENDU POUR CHAQUE GROUPE ===
  document.querySelectorAll('.endpoint-group').forEach(group => {
    const section = group.dataset.section;
    if (section) {
      renderEndpoints(section, group);
    } else {
      console.warn('⚠️ Groupe sans data-section', group);
    }
  });

  // Section Auth spéciale
  const authContainer = document.getElementById('auth-endpoints');
  if (authContainer) {
    renderEndpoints('auth', authContainer);
  }

  // === TOGGLE DES DÉTAILS ===
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

  // === RECHERCHE ===
  const searchInput = document.getElementById('searchInput');
  if (searchInput) {
    searchInput.addEventListener('input', function () {
      const query = this.value.toLowerCase().trim();
      document.querySelectorAll('.endpoint-item').forEach(item => {
        item.style.display = item.textContent.toLowerCase().includes(query) ? '' : 'none';
      });
    });
  }

  // === MODAL TRY IT ===
  const modal = document.getElementById('tryModal');
  const closeModal = document.getElementById('closeModal');
  const modalContent = document.getElementById('modalContent');

  if (modal && closeModal && modalContent) {
    document.addEventListener('click', function (e) {
      const btn = e.target.closest('.try-btn');
      if (btn) {
        e.preventDefault();
        const method = btn.dataset.method || 'GET';
        const path = btn.dataset.path || '/';
        let body;
        try { body = JSON.parse(btn.dataset.body || 'null'); } catch { body = null; }
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
            <p class="text-xs text-gray-400 dark:text-gray-500">* Fonctionnalité de démonstration.</p>
          </div>
        `;
        modal.classList.remove('hidden');
      }
    });

    closeModal.addEventListener('click', function () { modal.classList.add('hidden'); });
    modal.addEventListener('click', function (e) { if (e.target === modal) modal.classList.add('hidden'); });
  }

  // === MODE SOMBRE ===
  const themeToggle = document.getElementById('themeToggle');
  const html = document.documentElement;
  const storedTheme = localStorage.getItem('theme') || 
    (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
  html.className = storedTheme;

  if (themeToggle) {
    themeToggle.addEventListener('click', function () {
      const isDark = html.classList.toggle('dark');
      html.classList.toggle('light', !isDark);
      localStorage.setItem('theme', isDark ? 'dark' : 'light');
    });
  }

  // === SIDEBAR MOBILE ===
  const sidebar = document.getElementById('sidebar');
  const menuToggle = document.getElementById('menuToggle');
  if (menuToggle && sidebar) {
    menuToggle.addEventListener('click', function () {
      sidebar.classList.toggle('-translate-x-full');
      sidebar.classList.toggle('open-mobile');
    });
    document.addEventListener('click', function (e) {
      if (window.innerWidth < 768 && !sidebar.contains(e.target) && !menuToggle.contains(e.target)) {
        sidebar.classList.add('-translate-x-full');
        sidebar.classList.remove('open-mobile');
      }
    });
    window.addEventListener('resize', function () {
      if (window.innerWidth >= 768) {
        sidebar.classList.remove('-translate-x-full', 'open-mobile');
      }
    });
  }

  // === LIENS ACTIFS ===
  const links = document.querySelectorAll('#sidebar nav a');
  links.forEach(link => {
    link.addEventListener('click', function () {
      links.forEach(l => l.classList.remove('active'));
      this.classList.add('active');
      if (window.innerWidth < 768 && sidebar) {
        sidebar.classList.add('-translate-x-full');
        sidebar.classList.remove('open-mobile');
      }
    });
  });

  window.addEventListener('scroll', function () {
    let current = '';
    document.querySelectorAll('section[id], div[id]').forEach(sec => {
      if (sec.getBoundingClientRect().top <= 100) current = sec.id;
    });
    links.forEach(link => {
      link.classList.remove('active');
      if (link.getAttribute('href') === '#' + current) link.classList.add('active');
    });
  });

  console.log('✅ Script terminé');
});