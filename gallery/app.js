// Design Atlas Gallery App
(function() {
  var manifest = null;
  var activeCategory = 'all';
  var searchQuery = '';

  function init() {
    fetch('../manifest.json')
      .then(function(r) { return r.json(); })
      .then(function(data) {
        manifest = data;
        renderStats();
        renderFilters();
        renderGallery();
      })
      .catch(function(err) {
        document.getElementById('gallery').innerHTML = '<p class="loading-msg">Failed to load manifest.json. Run from project root: python3 -m http.server</p>';
      });
  }

  function renderStats() {
    var el = document.getElementById('stats');
    var count = manifest.systems.length;
    var cats = manifest.categories.length;
    el.textContent = count + ' design systems in ' + cats + ' categories';
  }

  function renderFilters() {
    var container = document.getElementById('filterTabs');
    container.innerHTML = '';

    // "All" tab
    container.appendChild(makeTab('All', 'all'));

    // Category tabs
    manifest.categories.forEach(function(cat) {
      var count = manifest.systems.filter(function(s) {
        return s.category === cat.id;
      }).length;
      container.appendChild(makeTab(cat.name + ' (' + count + ')', cat.id));
    });
  }

  function makeTab(label, catId) {
    var btn = document.createElement('button');
    btn.className = 'filter-tab' + (catId === activeCategory ? ' active' : '');
    btn.textContent = label;
    btn.onclick = function() {
      activeCategory = catId;
      renderFilters();
      renderGallery();
    };
    return btn;
  }

  function getFilteredSystems() {
    return manifest.systems.filter(function(s) {
      // Category filter
      if (activeCategory !== 'all' && s.category !== activeCategory) return false;
      // Search filter
      if (searchQuery) {
        var q = searchQuery.toLowerCase();
        var haystack = (s.name + ' ' + s.tags.join(' ') + ' ' + s.category).toLowerCase();
        if (haystack.indexOf(q) === -1) return false;
      }
      return true;
    });
  }

  function renderGallery() {
    var container = document.getElementById('gallery');
    container.innerHTML = '';
    var systems = getFilteredSystems();

    if (systems.length === 0) {
      container.innerHTML = '<p class="loading-msg">No styles found.</p>';
      return;
    }

    systems.forEach(function(s) {
      container.appendChild(makeCard(s));
    });
  }

  function makeCard(s) {
    var card = document.createElement('div');
    card.className = 'card';
    card.onclick = function() { openModal(s); };

    // Preview (palette bands)
    var preview = document.createElement('div');
    preview.className = 'card-preview';
    var palette = s.palette || ['#333'];
    palette.forEach(function(color) {
      var band = document.createElement('div');
      band.className = 'preview-band';
      band.style.background = color;
      if (s.year) band.setAttribute('data-year', s.year);
      preview.appendChild(band);
    });
    card.appendChild(preview);

    // Body
    var body = document.createElement('div');
    body.className = 'card-body';

    var name = document.createElement('div');
    name.className = 'card-name';
    name.textContent = s.name;
    body.appendChild(name);

    // Meta line
    var meta = document.createElement('div');
    meta.className = 'card-meta';

    var catName = getCategoryName(s);
    var catSpan = document.createElement('span');
    catSpan.className = 'card-category';
    catSpan.textContent = catName;
    meta.appendChild(catSpan);

    if (s.source && s.source.author) {
      var dot = document.createElement('span');
      dot.textContent = '\u00b7';
      dot.style.color = 'var(--text-faint)';
      meta.appendChild(dot);

      var author = document.createElement('span');
      author.className = 'card-author';
      author.textContent = s.source.author;
      meta.appendChild(author);
    }
    body.appendChild(meta);

    // Tags
    if (s.tags && s.tags.length > 0) {
      var tags = document.createElement('div');
      tags.className = 'card-tags';
      s.tags.slice(0, 4).forEach(function(tag) {
        var t = document.createElement('span');
        t.className = 'card-tag';
        t.textContent = tag;
        tags.appendChild(t);
      });
      body.appendChild(tags);
    }

    card.appendChild(body);
    return card;
  }

  function getCategoryName(s) {
    var cat = manifest.categories.find(function(c) { return c.id === s.category; });
    return cat ? cat.name : s.category;
  }

  // ===== Modal =====
  function openModal(s) {
    var overlay = document.getElementById('modalOverlay');
    var frame = document.getElementById('modalFrame');
    var info = document.getElementById('modalInfo');

    // Set iframe
    frame.src = s.demo_url || '';

    // Build info panel
    info.innerHTML = '';

    var title = document.createElement('h2');
    title.className = 'modal-title';
    title.textContent = s.name;
    info.appendChild(title);

    var subtitle = document.createElement('p');
    subtitle.className = 'modal-subtitle';
    subtitle.textContent = s.year ? String(s.year) + ' \u00b7 ' + getCategoryName(s) : getCategoryName(s);
    info.appendChild(subtitle);

    // Palette
    if (s.palette && s.palette.length > 0) {
      var palSection = makeSection('Palette');
      var table = document.createElement('table');
      table.className = 'token-table';
      s.palette.forEach(function(color) {
        var tr = document.createElement('tr');
        var td = document.createElement('td');

        var swatch = document.createElement('span');
        swatch.className = 'token-color-swatch';
        swatch.style.background = color;
        td.appendChild(swatch);

        td.appendChild(document.createTextNode(color));
        tr.appendChild(td);
        table.appendChild(tr);
      });
      palSection.appendChild(table);
      info.appendChild(palSection);
    }

    // Tags
    if (s.tags && s.tags.length > 0) {
      var tagSection = makeSection('Tags');
      var tagText = document.createElement('p');
      tagText.style.fontSize = '12px';
      tagText.style.color = 'var(--text-dim)';
      tagText.textContent = s.tags.join(', ');
      tagSection.appendChild(tagText);
      info.appendChild(tagSection);
    }

    // Source
    if (s.source) {
      var srcSection = makeSection('Source');
      var srcInfo = document.createElement('p');
      srcInfo.className = 'modal-source';
      srcInfo.innerHTML = '<strong>' + (s.source.author || 'Unknown') + '</strong>';
      if (s.source.license) {
        srcInfo.innerHTML += ' \u00b7 ' + s.source.license;
      }
      srcInfo.innerHTML += '<br><span style="font-size:11px;color:var(--text-faint)">' + (s.source.type || '') + '</span>';
      srcSection.appendChild(srcInfo);

      if (s.source.repo) {
        var br = document.createElement('br');
        srcSection.appendChild(br);
        var link = document.createElement('a');
        link.className = 'modal-link';
        link.href = s.source.repo;
        link.target = '_blank';
        link.textContent = 'View Repository';
        srcSection.appendChild(link);
      }
      info.appendChild(srcSection);
    }

    // Demo link
    if (s.demo_url) {
      var demoSection = makeSection('Live Demo');
      var demoLink = document.createElement('a');
      demoLink.className = 'modal-link';
      demoLink.href = s.demo_url;
      demoLink.target = '_blank';
      demoLink.textContent = 'Open in new tab';
      demoSection.appendChild(demoLink);
      info.appendChild(demoSection);
    }

    overlay.classList.add('active');
  }

  function makeSection(title) {
    var section = document.createElement('div');
    section.className = 'modal-section';
    var t = document.createElement('p');
    t.className = 'modal-section-title';
    t.textContent = title;
    section.appendChild(t);
    return section;
  }

  function closeModal() {
    document.getElementById('modalOverlay').classList.remove('active');
    document.getElementById('modalFrame').src = '';
  }

  // ===== Event Bindings =====
  document.getElementById('modalClose').onclick = closeModal;
  document.getElementById('modalOverlay').onclick = function(e) {
    if (e.target === this) closeModal();
  };
  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') closeModal();
  });

  // Search
  document.getElementById('searchBox').oninput = function(e) {
    searchQuery = e.target.value;
    renderGallery();
  };

  // Init
  init();
})();