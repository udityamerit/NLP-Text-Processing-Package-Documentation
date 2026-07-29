/* ==========================================================================
   NLP Text Preprocessing Documentation — App Logic
   Aligned to DESIGN.md spec. Premium enhancements included.
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {

    // =========================================================================
    // 1. THEME TOGGLE — Light / Dark mode with localStorage persistence
    // =========================================================================
    const themeBtn  = document.getElementById('theme-toggle-btn');
    const themeIcon = document.getElementById('theme-icon');

    const savedTheme   = localStorage.getItem('docs-theme');
    let   currentTheme = savedTheme || 'light';

    function applyTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        if (themeIcon) {
            themeIcon.textContent = theme === 'dark' ? '☀️' : '🌙';
        }
        localStorage.setItem('docs-theme', theme);
    }

    applyTheme(currentTheme);

    if (themeBtn) {
        themeBtn.addEventListener('click', () => {
            currentTheme = currentTheme === 'light' ? 'dark' : 'light';
            applyTheme(currentTheme);
        });
    }

    // =========================================================================
    // 2. MOBILE SIDEBAR TOGGLE — hamburger menu
    // =========================================================================
    const mobileBtn = document.getElementById('mobile-menu-btn');
    const sidebar   = document.getElementById('sidebar');
    const overlay   = document.getElementById('sidebar-overlay');

    function openSidebar() {
        if (sidebar && overlay) {
            sidebar.classList.add('open');
            overlay.classList.add('active');
            overlay.setAttribute('aria-hidden', 'false');
            document.body.style.overflow = 'hidden';
            if (mobileBtn) mobileBtn.setAttribute('aria-expanded', 'true');
        }
    }

    function closeSidebar() {
        if (sidebar && overlay) {
            sidebar.classList.remove('open');
            overlay.classList.remove('active');
            overlay.setAttribute('aria-hidden', 'true');
            document.body.style.overflow = '';
            if (mobileBtn) mobileBtn.setAttribute('aria-expanded', 'false');
        }
    }

    function toggleSidebar() {
        sidebar && sidebar.classList.contains('open') ? closeSidebar() : openSidebar();
    }

    if (mobileBtn) mobileBtn.addEventListener('click', toggleSidebar);
    if (overlay)   overlay.addEventListener('click', closeSidebar);

    // Close sidebar on Escape key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && sidebar && sidebar.classList.contains('open')) {
            closeSidebar();
            if (mobileBtn) mobileBtn.focus();
        }
    });

    // =========================================================================
    // 3. ACTIVE SIDEBAR LINK — highlight based on current URL
    // =========================================================================
    const currentPath = window.location.pathname;
    const navLinks    = document.querySelectorAll('.sidebar-link');

    navLinks.forEach(link => {
        const linkPath = link.getAttribute('href');
        if (!linkPath || linkPath.startsWith('#')) return;

        // Don't override links that were marked active in HTML for anchor sub-links
        if (linkPath.includes('.html') && currentPath.endsWith(linkPath)) {
            link.classList.add('active');
        } else if (
            linkPath === 'index.html' &&
            (currentPath.endsWith('/') || currentPath.endsWith('index.html'))
        ) {
            link.classList.add('active');
        } else if (linkPath.includes('.html')) {
            link.classList.remove('active');
        }
    });

    // =========================================================================
    // 4. CODE BLOCK UPGRADE — Highlight.js + VS Code–style header & copy button
    //    Wraps every <pre> (outside .install-panel) in a .code-block-wrapper
    //    and injects a header bar with: traffic-light dots, language badge, copy btn.
    // =========================================================================

    if (window.hljs) {
        try {
            hljs.highlightAll();
        } catch (e) {
            console.warn('Highlight.js initialization warning:', e);
        }
    }

    // Map language classes → display labels
    const LANG_LABELS = {
        'language-python': 'Python',
        'python':          'Python',
        'language-bash':   'Bash',
        'bash':            'Bash',
        'language-sh':     'Shell',
        'sh':              'Shell',
        'language-js':     'JavaScript',
        'javascript':      'JavaScript',
        'language-css':    'CSS',
        'css':             'CSS',
        'language-html':   'HTML',
        'html':            'HTML',
        'language-json':   'JSON',
        'json':            'JSON',
        'language-yaml':   'YAML',
        'yaml':            'YAML',
        'language-sql':    'SQL',
        'sql':             'SQL',
    };

    const COPY_ICON = `<svg width="12" height="12" viewBox="0 0 24 24" fill="none"
        stroke="currentColor" stroke-width="2" aria-hidden="true">
        <rect x="9" y="9" width="13" height="13" rx="2"/>
        <path d="M5 15H4a2 2 0 01-2-2V4a2 2 0 012-2h9a2 2 0 012 2v1"/>
    </svg>`;

    document.querySelectorAll('pre').forEach(pre => {
        // Skip install panel — has its own terminal UI
        if (pre.closest('.install-panel') || pre.closest('.code-block-wrapper')) return;

        // Detect language from child <code> class
        const codeEl   = pre.querySelector('code');
        let langLabel  = 'Code';
        if (codeEl) {
            const classes = [...codeEl.classList];
            const langClass = classes.find(c => c.startsWith('language-') || LANG_LABELS[c]);
            if (langClass) {
                langLabel = LANG_LABELS[langClass] || langClass.replace('language-', '').toUpperCase();
            }
        }

        // Build wrapper
        const wrapper = document.createElement('div');
        wrapper.className = 'code-block-wrapper';

        // Build header
        const header = document.createElement('div');
        header.className = 'code-block-header';
        header.setAttribute('aria-hidden', 'true');

        const headerLeft = document.createElement('div');
        headerLeft.className = 'code-block-header-left';
        headerLeft.innerHTML = `
            <div class="code-dots">
                <span class="code-dot code-dot-red"></span>
                <span class="code-dot code-dot-yellow"></span>
                <span class="code-dot code-dot-green"></span>
            </div>
            <span class="code-lang-badge">${langLabel}</span>`;

        // Copy button
        const copyBtn = document.createElement('button');
        copyBtn.type      = 'button';
        copyBtn.className = 'code-copy-btn';
        copyBtn.setAttribute('aria-label', `Copy ${langLabel} code`);
        copyBtn.innerHTML = `${COPY_ICON} Copy`;

        copyBtn.addEventListener('click', () => {
            const text = (codeEl ? codeEl.innerText : pre.innerText).trim();
            navigator.clipboard.writeText(text).then(() => {
                copyBtn.classList.add('copied');
                copyBtn.innerHTML = `<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" aria-hidden="true"><polyline points="20 6 9 17 4 12"/></svg> Copied!`;
                setTimeout(() => {
                    copyBtn.classList.remove('copied');
                    copyBtn.innerHTML = `${COPY_ICON} Copy`;
                }, 2000);
            }).catch(() => {
                copyBtn.innerHTML = 'Failed';
                setTimeout(() => { copyBtn.innerHTML = `${COPY_ICON} Copy`; }, 2000);
            });
        });

        header.appendChild(headerLeft);
        header.appendChild(copyBtn);

        // Wrap the pre: insert wrapper before pre, move pre inside
        pre.parentNode.insertBefore(wrapper, pre);
        wrapper.appendChild(header);
        wrapper.appendChild(pre);

        // Remove any old absolute-positioned copy buttons that app previously added
        pre.style.paddingRight = '';
        const oldBtn = pre.querySelector('.btn-copy');
        if (oldBtn) oldBtn.remove();
    });


    // =========================================================================
    // 5. SCROLL PROGRESS BAR (Premium Enhancement)
    //    Thin cyan-to-emerald gradient bar at the very top of the viewport.
    // =========================================================================
    const progressBar = document.getElementById('scroll-progress');

    if (progressBar) {
        const updateProgress = () => {
            const scrollTop    = window.scrollY || document.documentElement.scrollTop;
            const docHeight    = document.documentElement.scrollHeight - window.innerHeight;
            const pct          = docHeight > 0 ? (scrollTop / docHeight) * 100 : 0;
            progressBar.style.width = `${Math.min(pct, 100)}%`;
        };

        window.addEventListener('scroll', updateProgress, { passive: true });
        updateProgress(); // Initialize on load
    }

    // =========================================================================
    // 6. COUNT-UP ANIMATION for stat values (Premium Enhancement)
    //    Triggers once when the stats row enters the viewport.
    // =========================================================================
    const statVals = document.querySelectorAll('.stat-val[data-count]');

    if (statVals.length > 0 && 'IntersectionObserver' in window) {
        // Respect prefers-reduced-motion
        const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

        const countUp = (el, target, suffix) => {
            if (prefersReducedMotion) {
                el.textContent = target + suffix;
                return;
            }

            const duration = 1200; // ms
            const steps    = 40;
            const increment = target / steps;
            let   current  = 0;
            let   step     = 0;

            const timer = setInterval(() => {
                step++;
                current = Math.min(Math.round(increment * step), target);
                el.textContent = current + suffix;
                if (step >= steps) clearInterval(timer);
            }, duration / steps);
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting && !entry.target.dataset.animated) {
                    entry.target.dataset.animated = 'true';
                    const target = parseInt(entry.target.dataset.count, 10);
                    const suffix = entry.target.dataset.suffix || '';
                    countUp(entry.target, target, suffix);
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.5 });

        statVals.forEach(el => observer.observe(el));
    }

    // =========================================================================
    // 7. SMOOTH ANCHOR SCROLL for sidebar sub-links
    // =========================================================================
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const targetId = this.getAttribute('href').slice(1);
            const target   = document.getElementById(targetId);
            if (target) {
                e.preventDefault();
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
                // Close mobile sidebar if open
                closeSidebar();
            }
        });
    });

});

// =============================================================================
// OS TAB SWITCHER — Installation Hub
// =============================================================================
function switchInstallOS(os) {
    // 1. Update tab active state + ARIA
    document.querySelectorAll('.install-tab').forEach(tab => {
        const isActive = tab.dataset.os === os;
        tab.classList.toggle('active', isActive);
        tab.setAttribute('aria-selected', isActive.toString());
    });

    // 2. Gather DOM elements
    const commandEl  = document.getElementById('install-command');
    const labelEl    = document.getElementById('terminal-label');
    const promptEl   = document.getElementById('install-prompt');
    const subtextEl  = document.getElementById('install-subtext');
    const copyBtn    = document.getElementById('copy-install-btn');

    // 3. Define OS-specific commands
    const configs = {
        windows: {
            label:   'Windows PowerShell',
            prompt:  'PS C:\\>',
            command: 'python -m venv venv\n.\\venv\\Scripts\\activate\npip install nlp-text-preprocessing',
            hint:    'Recommended for Windows PowerShell.'
        },
        mac: {
            label:   'macOS Terminal',
            prompt:  'user@mac %',
            command: 'python3 -m venv venv\nsource venv/bin/activate\npip3 install nlp-text-preprocessing',
            hint:    'Standard installation for macOS environments.'
        },
        linux: {
            label:   'Linux Shell',
            prompt:  '$',
            command: 'python3 -m venv venv\nsource venv/bin/activate\npip install nlp-text-preprocessing',
            hint:    'Compatible with Ubuntu, Debian, CentOS, and other distributions.'
        },
        conda: {
            label:   'Conda Environment',
            prompt:  '(base) $',
            command: 'conda create -n nlp_env python=3.9\nconda activate nlp_env\npip install nlp-text-preprocessing',
            hint:    'For Anaconda / Miniconda users. Python 3.8+ recommended.'
        }
    };

    const cfg = configs[os];
    if (!cfg) return;

    // 4. Apply content
    if (labelEl)   labelEl.textContent  = cfg.label;
    if (promptEl)  promptEl.textContent = cfg.prompt;
    if (subtextEl) subtextEl.textContent = cfg.hint;

    // Render command with line breaks
    if (commandEl) {
        commandEl.innerHTML = cfg.command
            .split('\n')
            .map(line => `<span>${escapeHtml(line)}</span>`)
            .join('<br>');
    }

    // 5. Update copy button handler
    if (copyBtn) {
        copyBtn.onclick = () => {
            navigator.clipboard.writeText(cfg.command).then(() => {
                const originalHtml = copyBtn.innerHTML;
                copyBtn.innerHTML  = '<span style="color: var(--accent-emerald)">✓ Copied!</span>';
                setTimeout(() => { copyBtn.innerHTML = originalHtml; }, 2000);
            });
        };
    }
}

// Helper: escape HTML entities for safe innerHTML injection
function escapeHtml(str) {
    return str
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;');
}

// =============================================================================
// API REFERENCE CODE MODAL POPUP SYSTEM
// =============================================================================
const API_EXAMPLES = {
    word_count: {
        title: 'word_count(x)',
        badge: 'General Feature Extraction — int',
        desc: 'Calculates total whitespace-separated words in the input text string. Returns 0 for empty string or NaN inputs.',
        code: `import nlp_text_preprocessing as tp

text = "Natural Language Processing makes text cleaning effortless!"
count = tp.word_count(text)

print(f"Word Count: {count}")
# Output: Word Count: 7`
    },
    char_count: {
        title: 'char_count(x)',
        badge: 'General Feature Extraction — int',
        desc: 'Counts total characters in text, excluding space characters.',
        code: `import nlp_text_preprocessing as tp

text = "Hello World!"
length = tp.char_count(text)

print(f"Character Count: {length}")
# Output: Character Count: 11`
    },
    avg_word_len: {
        title: 'avg_word_len(x)',
        badge: 'General Feature Extraction — float',
        desc: 'Computes average word length in characters. Returns 0.0 for empty or whitespace-only inputs.',
        code: `import nlp_text_preprocessing as tp

text = "Python data science"
avg_len = tp.avg_word_len(text)

print(f"Average Word Length: {avg_len:.2f}")
# Output: Average Word Length: 6.00`
    },
    stop_words_count: {
        title: 'stop_words_count(x)',
        badge: 'General Feature Extraction — int',
        desc: 'Counts total English stop words in input text (case-insensitive).',
        code: `import nlp_text_preprocessing as tp

text = "This is a sample sentence with some stop words"
num_stopwords = tp.stop_words_count(text)

print(f"Stop Words Count: {num_stopwords}")
# Output: Stop Words Count: 6`
    },
    sentence_count: {
        title: 'sentence_count(x)',
        badge: 'General Feature Extraction — int',
        desc: 'Counts total sentences using punctuation delimiters (. ! ?).',
        code: `import nlp_text_preprocessing as tp

text = "First sentence. Second sentence! Is this the third?"
sentences = tp.sentence_count(text)

print(f"Sentence Count: {sentences}")
# Output: Sentence Count: 3`
    },
    avg_sentence_len: {
        title: 'avg_sentence_len(x)',
        badge: 'General Feature Extraction — float',
        desc: 'Calculates average sentence length measured in words per sentence.',
        code: `import nlp_text_preprocessing as tp

text = "Machine learning is fascinating. Text preprocessing is vital."
avg_sent = tp.avg_sentence_len(text)

print(f"Average Sentence Length: {avg_sent}")
# Output: Average Sentence Length: 4.0`
    },
    text_stats_batch: {
        title: 'text_stats_batch(df, col)',
        badge: 'General Feature Extraction — DataFrame',
        desc: 'Computes word_count, char_count, avg_word_len, sentence_count, and stop_words_count in a single pass over a DataFrame column.',
        code: `import pandas as pd
import nlp_text_preprocessing as tp

df = pd.DataFrame({'reviews': [
    "Great product quality!",
    "Terrible customer service."
]})

features = tp.text_stats_batch(df, col='reviews')
print(features)
# Returns DataFrame with columns: [word_count, char_count, avg_word_len, ...]`
    },
    to_lower_case: {
        title: 'to_lower_case(x)',
        badge: 'Text Cleaning — str',
        desc: 'Converts input text to lowercase safely without crashing on null values.',
        code: `import nlp_text_preprocessing as tp

text = "NLP Text Preprocessing Library v1.0"
lowered = tp.to_lower_case(text)

print(lowered)
# Output: nlp text preprocessing library v1.0`
    },
    contraction_to_expansion: {
        title: 'contraction_to_expansion(x)',
        badge: 'Text Cleaning — str',
        desc: 'Expands English contractions (e.g. "don\'t" -> "do not", "I\'m" -> "I am").',
        code: `import nlp_text_preprocessing as tp

text = "I'm sure it'll work and won't fail!"
expanded = tp.contraction_to_expansion(text)

print(expanded)
# Output: I am sure it will work and will not fail!`
    },
    remove_emails: {
        title: 'remove_emails(x)',
        badge: 'Text Cleaning — str',
        desc: 'Strips email addresses matching standard RFC 5322 patterns.',
        code: `import nlp_text_preprocessing as tp

text = "Contact support@example.com for help or admin@domain.org."
clean = tp.remove_emails(text)

print(clean)
# Output: Contact  for help or .`
    },
    remove_urls: {
        title: 'remove_urls(x)',
        badge: 'Text Cleaning — str',
        desc: 'Removes HTTP, HTTPS, FTP links and www web domain URLs.',
        code: `import nlp_text_preprocessing as tp

text = "Check out https://pypi.org/project/nlp-text-preprocessing/ today!"
clean = tp.remove_urls(text)

print(clean)
# Output: Check out  today!`
    },
    remove_html_tag: {
        title: 'remove_html_tag(x)',
        badge: 'Text Cleaning — str',
        desc: 'Strips HTML, XML tags, and inline markup using BeautifulSoup parser.',
        code: `import nlp_text_preprocessing as tp

raw_html = "<div class='main'><h1>Title</h1><p>Sample paragraph.</p></div>"
clean = tp.remove_html_tag(raw_html)

print(clean)
# Output: TitleSample paragraph.`
    },
    remove_accented_chars: {
        title: 'remove_accented_chars(x)',
        badge: 'Text Cleaning — str',
        desc: 'Normalizes unicode accented characters (NFKD decomposition -> ASCII).',
        code: `import nlp_text_preprocessing as tp

accented = "Café, résumé, and mañana."
normalized = tp.remove_accented_chars(accented)

print(normalized)
# Output: Cafe, resume, and manana.`
    },
    clean_text: {
        title: 'clean_text(text)',
        badge: 'Text Cleaning — str',
        desc: 'Runs the default end-to-end cleaning pipeline: lowercase, expand contractions, remove URLs/emails/HTML, remove special characters & extra spaces.',
        code: `import nlp_text_preprocessing as tp

raw_text = "<b>Hello WORLD!</b> Contact test@email.com at https://test.com"
cleaned = tp.clean_text(raw_text)

print(cleaned)
# Output: hello world contact at`
    },
    convert_to_base: {
        title: 'convert_to_base(x)',
        badge: 'Linguistic Processing — str',
        desc: 'Lemmatizes verbs and nouns into base forms using spaCy while preserving word order.',
        code: `import nlp_text_preprocessing as tp

text = "The running dogs were barking loudly at passing cars."
base = tp.convert_to_base(text)

print(base)
# Output: The run dog be bark loudly at pass car.`
    },
    extract_ner: {
        title: 'extract_ner(x)',
        badge: 'Linguistic Processing — list[tuple]',
        desc: 'Extracts Named Entities (PERSON, ORG, GPE, DATE, etc.) as a list of (entity, label) tuples.',
        code: `import nlp_text_preprocessing as tp

text = "Elon Musk visited Tesla headquarters in Austin, Texas."
entities = tp.extract_ner(text)

print(entities)
# Output: [('Elon Musk', 'PERSON'), ('Tesla', 'ORG'), ('Austin', 'GPE'), ('Texas', 'GPE')]`
    },
    extract_pos: {
        title: 'extract_pos(x)',
        badge: 'Linguistic Processing — list[tuple]',
        desc: 'Returns Part-Of-Speech (POS) tags for each token in the text.',
        code: `import nlp_text_preprocessing as tp

text = "Python enables rapid NLP development."
pos_tags = tp.extract_pos(text)

print(pos_tags)
# Output: [('Python', 'PROPN'), ('enables', 'VERB'), ('rapid', 'ADJ'), ('NLP', 'PROPN'), ('development', 'NOUN')]`
    }
};

document.addEventListener('DOMContentLoaded', () => {
    const modalOverlay = document.getElementById('api-modal-overlay');
    const modalClose   = document.getElementById('api-modal-close');
    const modalTitle   = document.getElementById('modal-func-title');
    const modalBadge   = document.getElementById('modal-func-badge');
    const modalDesc    = document.getElementById('modal-func-desc');
    const modalCode    = document.getElementById('modal-func-code');
    const modalCopyBtn = document.getElementById('modal-copy-btn');

    if (!modalOverlay) return;

    let currentCodeText = '';

    // Delegate clicks on function buttons
    document.addEventListener('click', (e) => {
        const btn = e.target.closest('.func-trigger-btn');
        if (!btn) return;

        const funcKey = btn.dataset.func;
        const data = API_EXAMPLES[funcKey];

        if (data) {
            modalTitle.textContent = data.title;
            modalBadge.textContent = data.badge;
            modalDesc.textContent  = data.desc;
            currentCodeText        = data.code;

            modalCode.textContent = data.code;
            if (window.hljs) {
                delete modalCode.dataset.highlighted;
                hljs.highlightElement(modalCode);
            }

            modalOverlay.classList.add('active');
            modalOverlay.setAttribute('aria-hidden', 'false');
            document.body.style.overflow = 'hidden'; // Prevent background scroll
        }
    });

    const closeModal = () => {
        modalOverlay.classList.remove('active');
        modalOverlay.setAttribute('aria-hidden', 'true');
        document.body.style.overflow = '';
    };

    if (modalClose) {
        modalClose.addEventListener('click', closeModal);
    }

    modalOverlay.addEventListener('click', (e) => {
        if (e.target === modalOverlay) closeModal();
    });

    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && modalOverlay.classList.contains('active')) {
            closeModal();
        }
    });

    if (modalCopyBtn) {
        modalCopyBtn.addEventListener('click', () => {
            if (!currentCodeText) return;
            navigator.clipboard.writeText(currentCodeText).then(() => {
                const originalHtml = modalCopyBtn.innerHTML;
                modalCopyBtn.innerHTML = '<span style="color: var(--accent-emerald)">✓ Copied!</span>';
                setTimeout(() => { modalCopyBtn.innerHTML = originalHtml; }, 2000);
            });
        });
    }
});
