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

  function getSourceInfo(s) {
    var repo = (s.source && s.source.repo) || 'unknown';
    var src = manifest.sources.find(function(x) { return x.repo === repo; });
    if (src) return src;
    // Fallback: build from system data
    return {
      name: repo !== 'unknown' ? repo.split('/').pop() : 'Unknown',
      author: (s.source && s.source.author) || '',
      type: (s.source && s.source.type) || '',
      license: (s.source && s.source.license) || '',
      repo: repo,
      description: ''
    };
  }

  function renderGallery() {
    var container = document.getElementById('gallery');
    container.innerHTML = '';
    var systems = getFilteredSystems();

    if (systems.length === 0) {
      container.innerHTML = '<p class="loading-msg">No styles found.</p>';
      return;
    }

    // Group by source repo (preserve first-appearance order)
    var groups = [];
    var groupMap = {};
    systems.forEach(function(s) {
      var repo = (s.source && s.source.repo) || 'unknown';
      if (!groupMap[repo]) {
        groupMap[repo] = [];
        groups.push(repo);
      }
      groupMap[repo].push(s);
    });

    // Render each source group
    groups.forEach(function(repo) {
      var groupSystems = groupMap[repo];
      var srcInfo = getSourceInfo(groupSystems[0]);
      container.appendChild(makeSourceHeader(srcInfo, groupSystems.length));
      
      var grid = document.createElement('div');
      grid.className = 'card-grid';
      groupSystems.forEach(function(s) {
        grid.appendChild(makeCard(s));
      });
      container.appendChild(grid);
    });
  }

  function makeSourceHeader(src, count) {
    var header = document.createElement('div');
    header.className = 'source-header';

    var left = document.createElement('div');
    left.className = 'source-header-left';

    var name = document.createElement('h2');
    name.className = 'source-name';
    name.textContent = src.name;
    left.appendChild(name);

    if (src.description) {
      var desc = document.createElement('p');
      desc.className = 'source-desc';
      desc.textContent = src.description;
      left.appendChild(desc);
    }

    var meta = document.createElement('div');
    meta.className = 'source-meta';
    
    if (src.author) {
      var author = document.createElement('span');
      author.textContent = src.author;
      meta.appendChild(author);
    }
    if (src.type) {
      var sep = document.createElement('span');
      sep.textContent = '\u00b7';
      sep.className = 'source-meta-sep';
      meta.appendChild(sep);
      var typeBadge = document.createElement('span');
      typeBadge.className = 'source-type-badge';
      typeBadge.textContent = src.type;
      meta.appendChild(typeBadge);
    }
    if (src.license) {
      var sep2 = document.createElement('span');
      sep2.textContent = '\u00b7';
      sep2.className = 'source-meta-sep';
      meta.appendChild(sep2);
      var lic = document.createElement('span');
      lic.textContent = src.license;
      meta.appendChild(lic);
    }
    var sep3 = document.createElement('span');
    sep3.textContent = '\u00b7';
    sep3.className = 'source-meta-sep';
    meta.appendChild(sep3);
    var countEl = document.createElement('span');
    countEl.textContent = count + ' styles';
    meta.appendChild(countEl);

    left.appendChild(meta);
    header.appendChild(left);

    if (src.repo && src.repo !== 'unknown') {
      var link = document.createElement('a');
      link.className = 'source-link';
      link.href = src.repo;
      link.target = '_blank';
      link.textContent = 'GitHub \u2197';
      header.appendChild(link);
    }

    return header;
  }

  function makeCard(s) {
    var card = document.createElement('div');
    card.className = 'card';
    card.onclick = function() { openModal(s); };

    // Preview (screenshot or palette fallback)
    var preview = document.createElement('div');
    preview.className = 'card-preview';
    if (s.preview) {
      var img = document.createElement('img');
      img.className = 'preview-img';
      img.src = '../' + s.preview;
      img.alt = s.name;
      img.loading = 'lazy';
      preview.appendChild(img);
    } else {
      var palette = s.palette || ['#333'];
      palette.forEach(function(color) {
        var band = document.createElement('div');
        band.className = 'preview-band';
        band.style.background = color;
        preview.appendChild(band);
      });
    }
    card.appendChild(preview);

    // Body
    var body = document.createElement('div');
    body.className = 'card-body';

    var name = document.createElement('div');
    name.className = 'card-name';
    name.textContent = s.name;
    body.appendChild(name);

    // One-liner description
    if (s.one_liner) {
      var desc = document.createElement('p');
      desc.className = 'card-desc';
      desc.textContent = s.one_liner;
      body.appendChild(desc);
    }

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

    // One-liner
    if (s.one_liner) {
      var tagline = document.createElement('p');
      tagline.className = 'modal-tagline';
      tagline.textContent = s.one_liner;
      info.appendChild(tagline);
    }

    // Best for
    if (s.best_for) {
      var bestSection = makeSection('Best For');
      var bestText = document.createElement('p');
      bestText.className = 'modal-best-for';
      bestText.textContent = s.best_for;
      bestSection.appendChild(bestText);
      info.appendChild(bestSection);
    }

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

    // ===== Agent Integration Guide =====
    info.appendChild(makeAgentGuide(s));

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

  // ===== Agent Integration =====
  function getBaseUrl() {
    var path = window.location.pathname;
    var idx = path.lastIndexOf('/gallery/');
    if (idx !== -1) return window.location.origin + path.substring(0, idx);
    return window.location.origin;
  }

  function generateSkillMd(baseUrl) {
    return [
      '---',
      'name: design-atlas',
      'description: Design Atlas 设计风格知识库——AI Agent 可搜索、引用和应用的设计风格集合',
      'type: knowledge-base',
      'cost: low',
      '---',
      '',
      '# Design Atlas — 设计风格知识库',
      '',
      'Design Atlas 是一个收录了 **59 个设计系统**（来自 7 个来源）的设计风格聚合库。',
      '包含从 Mac System 7 到赛博朋克 2077 的完整视觉指引。',
      '',
      '## 数据地址（线上）',
      '',
      'Base URL: `' + baseUrl + '`',
      '',
      '```',
      baseUrl + '/',
      '├── manifest.json              ← 全局索引',
      '├── systems/',
      '│   └── {id}/',
      '│       ├── STYLE.md           ← 设计语言 + Do/Don\'t',
      '│       └── tokens.css         ← CSS 变量',
      '└── gallery/                   ← 在线预览',
      '```',
      '',
      '## 工作流程',
      '',
      '当被要求"根据某个风格做 UI"时：',
      '',
      '1. **获取索引** → fetch `' + baseUrl + '/manifest.json`，搜索 category、tags、name',
      '2. **获取设计指引** → fetch `' + baseUrl + '/systems/{id}/STYLE.md`',
      '3. **获取 CSS Token** → fetch `' + baseUrl + '/systems/{id}/tokens.css`',
      '4. **应用** → 将 CSS 变量注入 :root，严格遵循 STYLE.md 的 Do/Don\'t',
      '',
      '## tags 标签体系',
      '',
      'manifest.json 中每个风格有 tags 数组，支持多维筛选：',
      '',
      '- **mood**：minimal, bold, playful, dark, warm, futuristic, nostalgic, elegant, raw',
      '- **palette**：monochrome, duotone, neon, primary-colors, pastel, earth-tone, 8bit',
      '- **typography**：serif, sans, pixel, mono, script, display',
      '- **era**：1970s, 1980s, 1990s, 2000s, 2010s, 2020s',
      '- **best_for**：app-ui, game-ui, data-viz, landing-page, portfolio, blog, tool, poster',
      ''
    ].join('\n');
  }

  function makeAgentGuide(s) {
    var section = document.createElement('div');
    section.className = 'agent-guide';

    var title = document.createElement('p');
    title.className = 'agent-guide-title';
    title.textContent = 'Use with AI Agent';
    section.appendChild(title);

    var intro = document.createElement('p');
    intro.className = 'agent-guide-intro';
    intro.textContent = '让你的 AI Agent（Claude / Cursor / Copilot 等）自动应用这个设计风格';
    section.appendChild(intro);

    // Step 1
    var step1 = document.createElement('div');
    step1.className = 'agent-step';

    var step1Label = document.createElement('p');
    step1Label.className = 'agent-step-num';
    step1Label.textContent = 'Step 1';
    step1.appendChild(step1Label);

    var step1Desc = document.createElement('p');
    step1Desc.className = 'agent-step-desc';
    step1Desc.textContent = '下载 SKILL.md，放到你项目根目录下（Agent 会自动读取）：';
    step1.appendChild(step1Desc);

    var downloadBtn = document.createElement('button');
    downloadBtn.className = 'agent-download-btn';
    downloadBtn.textContent = '⬇ 下载 SKILL.md';
    downloadBtn.onclick = function() {
      var md = generateSkillMd(getBaseUrl());
      var blob = new Blob([md], { type: 'text/markdown' });
      var url = URL.createObjectURL(blob);
      var a = document.createElement('a');
      a.href = url;
      a.download = 'SKILL.md';
      a.click();
      URL.revokeObjectURL(url);
      downloadBtn.textContent = '✓ 已下载';
      setTimeout(function() { downloadBtn.textContent = '⬇ 下载 SKILL.md'; }, 2000);
    };
    step1.appendChild(downloadBtn);
    section.appendChild(step1);

    var divider = document.createElement('div');
    divider.className = 'agent-divider';
    section.appendChild(divider);

    // Step 2
    var step2 = document.createElement('div');
    step2.className = 'agent-step';

    var step2Label = document.createElement('p');
    step2Label.className = 'agent-step-num';
    step2Label.textContent = 'Step 2';
    step2.appendChild(step2Label);

    var step2Desc = document.createElement('p');
    step2Desc.className = 'agent-step-desc';
    step2Desc.textContent = '安装完成后，复制以下提示词发给你的 Agent：';
    step2.appendChild(step2Desc);

    var promptText = '我已经安装了 design-atlas skill。\n' +
      '请帮我使用其中的 "' + s.name + '" 风格（ID: ' + s.id + '），\n' +
      '读取对应的 STYLE.md 和 tokens.css，\n' +
      '按照其设计规范帮我实现界面。';

    var codeWrap = document.createElement('div');
    codeWrap.className = 'agent-code-wrap';

    var code = document.createElement('pre');
    code.className = 'agent-code';
    code.textContent = promptText;
    codeWrap.appendChild(code);

    var copyBtn = document.createElement('button');
    copyBtn.className = 'agent-copy-btn';
    copyBtn.textContent = '复制';
    copyBtn.onclick = function() {
      navigator.clipboard.writeText(promptText).then(function() {
        copyBtn.textContent = '✓ 已复制';
        copyBtn.classList.add('copied');
        setTimeout(function() {
          copyBtn.textContent = '复制';
          copyBtn.classList.remove('copied');
        }, 2000);
      });
    };
    codeWrap.appendChild(copyBtn);
    step2.appendChild(codeWrap);
    section.appendChild(step2);

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