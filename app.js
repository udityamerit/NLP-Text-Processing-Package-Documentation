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

    function applyTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        if (themeIcon) {
            themeIcon.textContent = theme === 'dark' ? '☀️' : '🌙';
        }
        localStorage.setItem('docs-theme', theme);
    }

    // Sync icon with currently active theme
    const activeTheme = document.documentElement.getAttribute('data-theme') || 'light';
    applyTheme(activeTheme);

    if (themeBtn) {
        themeBtn.addEventListener('click', () => {
            const current = document.documentElement.getAttribute('data-theme') === 'dark' ? 'dark' : 'light';
            const nextTheme = current === 'dark' ? 'light' : 'dark';
            applyTheme(nextTheme);
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
    "word_count": {
        "title": "word_count(x)",
        "badge": "Feature Extraction \u2014 int",
        "desc": "Calculates total whitespace-separated word count in input text string.",
        "code": "import nlp_text_preprocessing as tp\n\ntext = \"Natural Language Processing makes text cleaning effortless and reliable!\"\ncount = tp.word_count(text)\n\nprint(f\"Word Count: {count}\")\n# Output: Word Count: 8"
    },
    "char_count": {
        "title": "char_count(x)",
        "badge": "Feature Extraction \u2014 int",
        "desc": "Counts total characters in input text, excluding whitespace characters.",
        "code": "import nlp_text_preprocessing as tp\n\ntext = \"Hello World!\"\nlength = tp.char_count(text)\n\nprint(f\"Character Count: {length}\")\n# Output: Character Count: 11"
    },
    "avg_word_len": {
        "title": "avg_word_len(x)",
        "badge": "Feature Extraction \u2014 float",
        "desc": "Computes average word length in characters. Returns 0.0 for empty text.",
        "code": "import nlp_text_preprocessing as tp\n\ntext = \"Python data science\"\navg_len = tp.avg_word_len(text)\n\nprint(f\"Average Word Length: {avg_len:.2f}\")\n# Output: Average Word Length: 6.00"
    },
    "stop_words_count": {
        "title": "stop_words_count(x)",
        "badge": "Feature Extraction \u2014 int",
        "desc": "Counts total English stop words in input text (case-insensitive).",
        "code": "import nlp_text_preprocessing as tp\n\ntext = \"This is a sample sentence with some stop words\"\nnum_stopwords = tp.stop_words_count(text)\n\nprint(f\"Stop Words Count: {num_stopwords}\")\n# Output: Stop Words Count: 6"
    },
    "hashtags_count": {
        "title": "hashtags_count(x)",
        "badge": "Feature Extraction \u2014 int",
        "desc": "Returns count of social media hashtags (#tag) in text.",
        "code": "import nlp_text_preprocessing as tp\n\ntext = \"Loving #Python and #NLP! Check #MachineLearning.\"\ntags = tp.hashtags_count(text)\n\nprint(f\"Hashtags Count: {tags}\")\n# Output: Hashtags Count: 3"
    },
    "mentions_count": {
        "title": "mentions_count(x)",
        "badge": "Feature Extraction \u2014 int",
        "desc": "Returns count of social media user mentions (@user) in text.",
        "code": "import nlp_text_preprocessing as tp\n\ntext = \"Thanks @openai and @huggingface for great tools!\"\nmentions = tp.mentions_count(text)\n\nprint(f\"Mentions Count: {mentions}\")\n# Output: Mentions Count: 2"
    },
    "numerics_count": {
        "title": "numerics_count(x)",
        "badge": "Feature Extraction \u2014 int",
        "desc": "Returns total count of standalone numeric tokens in text.",
        "code": "import nlp_text_preprocessing as tp\n\ntext = \"Ordered 3 items for 150 dollars on 2026-07-30.\"\nnums = tp.numerics_count(text)\n\nprint(f\"Numeric Tokens Count: {nums}\")\n# Output: Numeric Tokens Count: 4"
    },
    "upper_case_count": {
        "title": "upper_case_count(x)",
        "badge": "Feature Extraction \u2014 int",
        "desc": "Returns count of words written entirely in uppercase.",
        "code": "import nlp_text_preprocessing as tp\n\ntext = \"URGENT ALERT: Please respond ASAP to the HR department.\"\nuppercase_words = tp.upper_case_count(text)\n\nprint(f\"Uppercase Words Count: {uppercase_words}\")\n# Output: Uppercase Words Count: 4"
    },
    "sentence_count": {
        "title": "sentence_count(x)",
        "badge": "Feature Extraction \u2014 int",
        "desc": "Counts total sentences using sentence terminal punctuation (. ! ?).",
        "code": "import nlp_text_preprocessing as tp\n\ntext = \"First sentence. Second sentence! Is this the third?\"\nsentences = tp.sentence_count(text)\n\nprint(f\"Sentence Count: {sentences}\")\n# Output: Sentence Count: 3"
    },
    "avg_sentence_len": {
        "title": "avg_sentence_len(x)",
        "badge": "Feature Extraction \u2014 float",
        "desc": "Calculates average sentence length in words per sentence.",
        "code": "import nlp_text_preprocessing as tp\n\ntext = \"Machine learning is fascinating. Text preprocessing is vital.\"\navg_sent = tp.avg_sentence_len(text)\n\nprint(f\"Average Sentence Length: {avg_sent}\")\n# Output: Average Sentence Length: 4.0"
    },
    "punctuation_density": {
        "title": "punctuation_density(x)",
        "badge": "Feature Extraction \u2014 float",
        "desc": "Returns proportion of punctuation characters relative to total text length.",
        "code": "import nlp_text_preprocessing as tp\n\ntext = \"Hello!!! What's happening???\"\ndensity = tp.punctuation_density(text)\n\nprint(f\"Punctuation Density: {density:.4f}\")\n# Output: Punctuation Density: 0.2500"
    },
    "capital_ratio": {
        "title": "capital_ratio(x)",
        "badge": "Feature Extraction \u2014 float",
        "desc": "Returns proportion of uppercase words relative to total word count.",
        "code": "import nlp_text_preprocessing as tp\n\ntext = \"GREAT news for ALL developers\"\nratio = tp.capital_ratio(text)\n\nprint(f\"Capital Ratio: {ratio:.2f}\")\n# Output: Capital Ratio: 0.40"
    },
    "unique_word_ratio": {
        "title": "unique_word_ratio(x)",
        "badge": "Feature Extraction \u2014 float",
        "desc": "Calculates vocabulary richness as the ratio of unique words to total words.",
        "code": "import nlp_text_preprocessing as tp\n\ntext = \"the quick brown fox jumps over the lazy dog\"\nratio = tp.unique_word_ratio(text)\n\nprint(f\"Unique Word Ratio: {ratio:.2f}\")\n# Output: Unique Word Ratio: 0.89"
    },
    "readability_score": {
        "title": "readability_score(x)",
        "badge": "Feature Extraction \u2014 float",
        "desc": "Calculates Flesch Reading Ease score to measure text readability.",
        "code": "import nlp_text_preprocessing as tp\n\ntext = \"The quick brown fox jumps over the lazy dog. Simple text is easy to read.\"\nscore = tp.readability_score(text)\n\nprint(f\"Readability Score: {score:.2f}\")\n# Output: Readability Score: 87.42"
    },
    "text_stats": {
        "title": "text_stats(x)",
        "badge": "Feature Extraction \u2014 dict",
        "desc": "Returns a comprehensive dictionary containing all summary feature statistics.",
        "code": "import nlp_text_preprocessing as tp\n\ntext = \"Supercharge your NLP pipeline with nlp-text-preprocessing!\"\nstats = tp.text_stats(text)\n\nprint(stats)\n# Output: {'word_count': 7, 'char_count': 51, 'avg_word_len': 7.28, 'stop_words_count': 2, ...}"
    },
    "text_stats_batch": {
        "title": "text_stats_batch(df, column)",
        "badge": "Feature Extraction \u2014 DataFrame",
        "desc": "Computes word_count, char_count, avg_word_len, sentence_count, and stop_words_count in a single pass over a DataFrame column.",
        "code": "import pandas as pd\nimport nlp_text_preprocessing as tp\n\ndf = pd.DataFrame({'reviews': [\n    \"Great product quality!\",\n    \"Terrible customer service.\"\n]})\n\nfeatures = tp.text_stats_batch(df, column='reviews')\nprint(features)\n# Returns DataFrame with columns: [word_count, char_count, avg_word_len, ...]"
    },
    "to_lower_case": {
        "title": "to_lower_case(x)",
        "badge": "Text Cleaning \u2014 str",
        "desc": "Converts input text to lowercase safely without crashing on null values.",
        "code": "import nlp_text_preprocessing as tp\n\ntext = \"NLP Text Preprocessing Library v1.0\"\nlowered = tp.to_lower_case(text)\n\nprint(lowered)\n# Output: nlp text preprocessing library v1.0"
    },
    "contraction_to_expansion": {
        "title": "contraction_to_expansion(x)",
        "badge": "Text Cleaning \u2014 str",
        "desc": "Expands English contractions (e.g. \"don't\" -> \"do not\", \"I'm\" -> \"I am\").",
        "code": "import nlp_text_preprocessing as tp\n\ntext = \"I'm sure it'll work and won't fail!\"\nexpanded = tp.contraction_to_expansion(text)\n\nprint(expanded)\n# Output: I am sure it will work and will not fail!"
    },
    "remove_emails": {
        "title": "remove_emails(x)",
        "badge": "Text Cleaning \u2014 str",
        "desc": "Strips email addresses matching standard RFC 5322 patterns.",
        "code": "import nlp_text_preprocessing as tp\n\ntext = \"Contact support@example.com for help or admin@domain.org.\"\nclean = tp.remove_emails(text)\n\nprint(clean)\n# Output: Contact  for help or ."
    },
    "count_emails": {
        "title": "count_emails(x)",
        "badge": "Text Cleaning \u2014 int",
        "desc": "Returns total count of email addresses present in input text.",
        "code": "import nlp_text_preprocessing as tp\n\ntext = \"Reach user1@test.com or user2@test.com\"\ncount = tp.count_emails(text)\n\nprint(f\"Emails found: {count}\")\n# Output: Emails found: 2"
    },
    "count_urls": {
        "title": "count_urls(x)",
        "badge": "Text Cleaning \u2014 int",
        "desc": "Returns total count of HTTP/HTTPS/FTP web URLs present in input text.",
        "code": "import nlp_text_preprocessing as tp\n\ntext = \"Visit https://google.com or http://github.com for info\"\ncount = tp.count_urls(text)\n\nprint(f\"URLs found: {count}\")\n# Output: URLs found: 2"
    },
    "remove_urls": {
        "title": "remove_urls(x)",
        "badge": "Text Cleaning \u2014 str",
        "desc": "Removes HTTP, HTTPS, FTP links and www web domain URLs.",
        "code": "import nlp_text_preprocessing as tp\n\ntext = \"Check out https://pypi.org/project/nlp-text-preprocessing/ today!\"\nclean = tp.remove_urls(text)\n\nprint(clean)\n# Output: Check out  today!"
    },
    "count_rt": {
        "title": "count_rt(x)",
        "badge": "Text Cleaning \u2014 int",
        "desc": "Returns count of retweet markers (RT @user) in social media text.",
        "code": "import nlp_text_preprocessing as tp\n\ntext = \"RT @elonmusk Great progress on rocket tests!\"\ncount = tp.count_rt(text)\n\nprint(f\"RT Markers: {count}\")\n# Output: RT Markers: 1"
    },
    "remove_rt": {
        "title": "remove_rt(x)",
        "badge": "Text Cleaning \u2014 str",
        "desc": "Strips retweet markers (RT @user) from social media text.",
        "code": "import nlp_text_preprocessing as tp\n\ntext = \"RT @elonmusk Great progress on rocket tests!\"\nclean = tp.remove_rt(text)\n\nprint(clean)\n# Output: Great progress on rocket tests!"
    },
    "remove_html_tag": {
        "title": "remove_html_tag(x)",
        "badge": "Text Cleaning \u2014 str",
        "desc": "Strips HTML, XML tags, and inline markup using BeautifulSoup parser.",
        "code": "import nlp_text_preprocessing as tp\n\nraw_html = \"<div class='main'><h1>Title</h1><p>Sample paragraph.</p></div>\"\nclean = tp.remove_html_tag(raw_html)\n\nprint(clean)\n# Output: TitleSample paragraph."
    },
    "remove_accented_chars": {
        "title": "remove_accented_chars(x)",
        "badge": "Text Cleaning \u2014 str",
        "desc": "Normalizes unicode accented characters (NFKD decomposition -> ASCII).",
        "code": "import nlp_text_preprocessing as tp\n\naccented = \"Caf\u00e9, r\u00e9sum\u00e9, and ma\u00f1ana.\"\nnormalized = tp.remove_accented_chars(accented)\n\nprint(normalized)\n# Output: Cafe, resume, and manana."
    },
    "remove_mentions": {
        "title": "remove_mentions(x)",
        "badge": "Text Cleaning \u2014 str",
        "desc": "Removes user mentions (@user) from social media text.",
        "code": "import nlp_text_preprocessing as tp\n\ntext = \"Shoutout to @user1 and @user2 for the support!\"\nclean = tp.remove_mentions(text)\n\nprint(clean)\n# Output: Shoutout to  and  for the support!"
    },
    "remove_special_chars": {
        "title": "remove_special_chars(x)",
        "badge": "Text Cleaning \u2014 str",
        "desc": "Removes special characters and punctuation symbols from input text.",
        "code": "import nlp_text_preprocessing as tp\n\ntext = \"Hello, World! @2026 #NLP$%^\"\nclean = tp.remove_special_chars(text)\n\nprint(clean)\n# Output: Hello World 2026 NLP"
    },
    "remove_repeated_chars": {
        "title": "remove_repeated_chars(x)",
        "badge": "Text Cleaning \u2014 str",
        "desc": "Truncates character repetitions beyond 2 consecutive occurrences (e.g. \"coooool\" -> \"cool\").",
        "code": "import nlp_text_preprocessing as tp\n\ntext = \"This is sooooo coooool!!!\"\nclean = tp.remove_repeated_chars(text)\n\nprint(clean)\n# Output: This is soo cool!!"
    },
    "remove_stop_words": {
        "title": "remove_stop_words(x)",
        "badge": "Text Cleaning \u2014 str",
        "desc": "Removes English stop words from input text (case-insensitive).",
        "code": "import nlp_text_preprocessing as tp\n\ntext = \"This is a simple sentence for testing stop words removal\"\nclean = tp.remove_stop_words(text)\n\nprint(clean)\n# Output: simple sentence testing stop words removal"
    },
    "remove_emojis": {
        "title": "remove_emojis(x)",
        "badge": "Text Cleaning \u2014 str",
        "desc": "Strips all emoji symbols and unicode pictographs from input text.",
        "code": "import nlp_text_preprocessing as tp\n\ntext = \"Great job! \ud83d\udd25\ud83c\udf89\ud83d\udc4d Keep it up! \u2764\ufe0f\"\nclean = tp.remove_emojis(text)\n\nprint(clean)\n# Output: Great job!  Keep it up! "
    },
    "extract_emojis": {
        "title": "extract_emojis(x)",
        "badge": "Text Cleaning \u2014 list",
        "desc": "Extracts a list of emoji characters present in input text.",
        "code": "import nlp_text_preprocessing as tp\n\ntext = \"Loving this project! \ud83d\udd25\u2764\ufe0f\ud83c\udf89\"\nemojis = tp.extract_emojis(text)\n\nprint(emojis)\n# Output: ['\ud83d\udd25', '\u2764\ufe0f', '\ud83c\udf89']"
    },
    "emoji_to_text": {
        "title": "emoji_to_text(x)",
        "badge": "Text Cleaning \u2014 str",
        "desc": "Converts emojis in input text to descriptive word representations (e.g. \"\ud83d\udd25\" -> \"fire\").",
        "code": "import nlp_text_preprocessing as tp\n\ntext = \"This product is \ud83d\udd25 and \u2764\ufe0f!\"\nconverted = tp.emoji_to_text(text)\n\nprint(converted)\n# Output: This product is fire and red_heart!"
    },
    "remove_phone_numbers": {
        "title": "remove_phone_numbers(x)",
        "badge": "Text Cleaning \u2014 str",
        "desc": "Strips phone numbers in standard international or domestic formats.",
        "code": "import nlp_text_preprocessing as tp\n\ntext = \"Call us at +1-800-555-0199 or 555-123-4567 for inquiries.\"\nclean = tp.remove_phone_numbers(text)\n\nprint(clean)\n# Output: Call us at  or  for inquiries."
    },
    "count_phone_numbers": {
        "title": "count_phone_numbers(x)",
        "badge": "Text Cleaning \u2014 int",
        "desc": "Counts phone numbers present in input text.",
        "code": "import nlp_text_preprocessing as tp\n\ntext = \"Call 800-555-0199 or 987-654-3210\"\ncount = tp.count_phone_numbers(text)\n\nprint(f\"Phone numbers count: {count}\")\n# Output: Phone numbers count: 2"
    },
    "mask_pii": {
        "title": "mask_pii(x)",
        "badge": "Text Cleaning \u2014 str",
        "desc": "Redacts emails, phone numbers, and card/ID numbers with [REDACTED].",
        "code": "import nlp_text_preprocessing as tp\n\ntext = \"My email is john@example.com and phone is 555-0199.\"\nmasked = tp.mask_pii(text)\n\nprint(masked)\n# Output: My email is [REDACTED] and phone is [REDACTED]."
    },
    "remove_extra_whitespace": {
        "title": "remove_extra_whitespace(x)",
        "badge": "Text Cleaning \u2014 str",
        "desc": "Collapses consecutive spaces, tabs, and newlines into a single space.",
        "code": "import nlp_text_preprocessing as tp\n\ntext = \"Too   many   spaces \\n and \\t tabs here.\"\nclean = tp.remove_extra_whitespace(text)\n\nprint(clean)\n# Output: Too many spaces and tabs here."
    },
    "expand_hashtags": {
        "title": "expand_hashtags(x)",
        "badge": "Text Cleaning \u2014 str",
        "desc": "Splits camelCase or PascalCase hashtags into separate words (#MachineLearning -> Machine Learning).",
        "code": "import nlp_text_preprocessing as tp\n\ntext = \"Explore #NaturalLanguageProcessing and #DeepLearning today!\"\nexpanded = tp.expand_hashtags(text)\n\nprint(expanded)\n# Output: Explore Natural Language Processing and Deep Learning today!"
    },
    "normalize_unicode_punctuation": {
        "title": "normalize_unicode_punctuation(x)",
        "badge": "Text Cleaning \u2014 str",
        "desc": "Replaces smart quotes (\u201c \u201d \u2018 \u2019), em-dashes (\u2014), and ellipsis (\u2026) with ASCII equivalents.",
        "code": "import nlp_text_preprocessing as tp\n\ntext = \"\u201cSmart quotes\u201d and em\u2014dashes\u2026\"\nnormalized = tp.normalize_unicode_punctuation(text)\n\nprint(normalized)\n# Output: \"Smart quotes\" and em-dashes..."
    },
    "remove_numbers": {
        "title": "remove_numbers(x)",
        "badge": "Text Cleaning \u2014 str",
        "desc": "Strips all numeric digits from input text.",
        "code": "import nlp_text_preprocessing as tp\n\ntext = \"The price was 100 dollars in 2026.\"\nclean = tp.remove_numbers(text)\n\nprint(clean)\n# Output: The price was  dollars in ."
    },
    "remove_currency_symbols": {
        "title": "remove_currency_symbols(x)",
        "badge": "Text Cleaning \u2014 str",
        "desc": "Strips common currency symbols ($, \u20ac, \u20b9, \u00a3, \u00a5) from text.",
        "code": "import nlp_text_preprocessing as tp\n\ntext = \"Prices: $50, \u20ac45, \u20b93500, \u00a340, \u00a56000\"\nclean = tp.remove_currency_symbols(text)\n\nprint(clean)\n# Output: Prices: 50, 45, 3500, 40, 6000"
    },
    "normalize_whitespace_and_casing": {
        "title": "normalize_whitespace_and_casing(x)",
        "badge": "Text Cleaning \u2014 str",
        "desc": "Canonical combination of lowercasing and extra whitespace collapse.",
        "code": "import nlp_text_preprocessing as tp\n\ntext = \"   TEXT   WITH  EXTRA   SPACES   \"\nclean = tp.normalize_whitespace_and_casing(text)\n\nprint(clean)\n# Output: text with extra spaces"
    },
    "clean_text": {
        "title": "clean_text(text)",
        "badge": "Text Cleaning \u2014 str",
        "desc": "Runs the default end-to-end cleaning pipeline: lowercase, expand contractions, remove URLs/emails/HTML, remove special characters & extra spaces.",
        "code": "import nlp_text_preprocessing as tp\n\nraw_text = \"<b>Hello WORLD!</b> Contact test@email.com at https://test.com\"\ncleaned = tp.clean_text(raw_text)\n\nprint(cleaned)\n# Output: hello world contact at"
    },
    "convert_to_base": {
        "title": "convert_to_base(x)",
        "badge": "Linguistic Processing \u2014 str",
        "desc": "Lemmatizes verbs and nouns into base forms using spaCy while preserving word order.",
        "code": "import nlp_text_preprocessing as tp\n\ntext = \"The running dogs were barking loudly at passing cars.\"\nbase = tp.convert_to_base(text)\n\nprint(base)\n# Output: The run dog be bark loudly at pass car."
    },
    "lemmatize": {
        "title": "lemmatize(x)",
        "badge": "Linguistic Processing \u2014 str",
        "desc": "Lemmatizes all tokens in input text to dictionary lemmas using spaCy.",
        "code": "import nlp_text_preprocessing as tp\n\ntext = \"Better studies are producing remarkable findings.\"\nlemmas = tp.lemmatize(text)\n\nprint(lemmas)\n# Output: well study be produce remarkable finding"
    },
    "extract_entities": {
        "title": "extract_entities(x)",
        "badge": "Linguistic Processing \u2014 list[tuple]",
        "desc": "Extracts Named Entities (PERSON, ORG, GPE, DATE, etc.) as (entity, label) tuples.",
        "code": "import nlp_text_preprocessing as tp\n\ntext = \"Elon Musk visited Tesla headquarters in Austin, Texas.\"\nentities = tp.extract_entities(text)\n\nprint(entities)\n# Output: [('Elon Musk', 'PERSON'), ('Tesla', 'ORG'), ('Austin', 'GPE'), ('Texas', 'GPE')]"
    },
    "extract_pos_tags": {
        "title": "extract_pos_tags(x)",
        "badge": "Linguistic Processing \u2014 list[tuple]",
        "desc": "Returns Part-Of-Speech (POS) tags for each token in the text.",
        "code": "import nlp_text_preprocessing as tp\n\ntext = \"Python enables rapid NLP development.\"\npos_tags = tp.extract_pos_tags(text)\n\nprint(pos_tags)\n# Output: [('Python', 'PROPN', 'NNP'), ('enables', 'VERB', 'VBZ'), ('rapid', 'ADJ', 'JJ')]"
    },
    "get_dependency_tree": {
        "title": "get_dependency_tree(x)",
        "badge": "Linguistic Processing \u2014 list[dict]",
        "desc": "Extracts grammatical dependency parse tree tokens, dependency relations, and head tokens.",
        "code": "import nlp_text_preprocessing as tp\n\ntext = \"The dog chased the cat.\"\ntree = tp.get_dependency_tree(text)\n\nprint(tree)\n# Output: [{'text': 'dog', 'dep': 'nsubj', 'head': 'chased'}, ...]"
    },
    "detect_language": {
        "title": "detect_language(x)",
        "badge": "Linguistic Processing \u2014 str",
        "desc": "Detects ISO language code (e.g. \"en\", \"es\", \"fr\") of text using TextBlob.",
        "code": "import nlp_text_preprocessing as tp\n\ntext = \"Bonjour tout le monde\"\nlang = tp.detect_language(text)\n\nprint(f\"Language Code: {lang}\")\n# Output: Language Code: fr"
    },
    "keyword_extraction": {
        "title": "keyword_extraction(x, top_n=5)",
        "badge": "Linguistic Processing \u2014 list[tuple]",
        "desc": "Extracts top_n keyword tokens based on term frequency.",
        "code": "import nlp_text_preprocessing as tp\n\ntext = \"NLP and text processing libraries make NLP applications powerful.\"\nkeywords = tp.keyword_extraction(text, top_n=3)\n\nprint(keywords)\n# Output: [('nlp', 2), ('text', 1), ('processing', 1)]"
    },
    "text_similarity": {
        "title": "text_similarity(x1, x2)",
        "badge": "Linguistic Processing \u2014 float",
        "desc": "Calculates Jaccard token similarity index between two texts (0.0 to 1.0).",
        "code": "import nlp_text_preprocessing as tp\n\nt1 = \"python machine learning\"\nt2 = \"python deep learning algorithms\"\nsim = tp.text_similarity(t1, t2)\n\nprint(f\"Similarity Score: {sim:.2f}\")\n# Output: Similarity Score: 0.50"
    },
    "get_synonyms": {
        "title": "get_synonyms(word)",
        "badge": "Linguistic Processing \u2014 list[str]",
        "desc": "Retrieves synonym list for target word via NLTK WordNet synsets.",
        "code": "import nlp_text_preprocessing as tp\n\nsyns = tp.get_synonyms(\"happy\")\nprint(syns[:5])\n# Output: ['happy', 'felicitous', 'glad', 'cheerful']"
    },
    "get_antonyms": {
        "title": "get_antonyms(word)",
        "badge": "Linguistic Processing \u2014 list[str]",
        "desc": "Retrieves antonym list for target word via NLTK WordNet synsets.",
        "code": "import nlp_text_preprocessing as tp\n\nants = tp.get_antonyms(\"happy\")\nprint(ants)\n# Output: ['unhappy']"
    },
    "chunk_noun_phrases": {
        "title": "chunk_noun_phrases(x)",
        "badge": "Linguistic Processing \u2014 list[dict]",
        "desc": "Extracts noun phrase chunks with start/end character offsets using spaCy.",
        "code": "import nlp_text_preprocessing as tp\n\ntext = \"The autonomous vehicle navigated the busy intersection.\"\nchunks = tp.chunk_noun_phrases(text)\n\nprint(chunks)\n# Output: [{'text': 'The autonomous vehicle', 'start': 0, 'end': 22}, ...]"
    },
    "get_wordcloud": {
        "title": "get_wordcloud(x, save_path=None, show=True)",
        "badge": "Linguistic Processing \u2014 WordCloud",
        "desc": "Generates, displays, or saves a WordCloud visualization object for input text.",
        "code": "import nlp_text_preprocessing as tp\n\ntext = \"Python data science machine learning text processing NLP AI\"\nwc = tp.get_wordcloud(text, save_path=\"wordcloud.png\", show=False)\n\nprint(type(wc))\n# Output: <class 'wordcloud.wordcloud.WordCloud'>"
    },
    "correct_spelling": {
        "title": "correct_spelling(x)",
        "badge": "Linguistic Processing \u2014 str",
        "desc": "Corrects spelling errors in text using TextBlob probabilistic spellchecker.",
        "code": "import nlp_text_preprocessing as tp\n\ntext = \"I have good speling and clean code.\"\ncorrected = tp.correct_spelling(text)\n\nprint(corrected)\n# Output: I have good spelling and clean code."
    },
    "get_noun_phrase": {
        "title": "get_noun_phrase(x)",
        "badge": "Linguistic Processing \u2014 list[str]",
        "desc": "Extracts noun phrase strings from text using TextBlob.",
        "code": "import nlp_text_preprocessing as tp\n\ntext = \"Python provides great text processing tools.\"\nphrases = tp.get_noun_phrase(text)\n\nprint(phrases)\n# Output: ['python', 'great text processing tools']"
    },
    "n_grams": {
        "title": "n_grams(x, n=2)",
        "badge": "Linguistic Processing \u2014 list[tuple]",
        "desc": "Generates word N-Grams (bigrams, trigrams, etc.) from input text.",
        "code": "import nlp_text_preprocessing as tp\n\ntext = \"natural language processing\"\nbigrams = tp.n_grams(text, n=2)\n\nprint(bigrams)\n# Output: [('natural', 'language'), ('language', 'processing')]"
    },
    "singularize_words": {
        "title": "singularize_words(x)",
        "badge": "Linguistic Processing \u2014 str",
        "desc": "Converts plural nouns to singular form.",
        "code": "import nlp_text_preprocessing as tp\n\ntext = \"The dogs chased the cats.\"\nsingular = tp.singularize_words(text)\n\nprint(singular)\n# Output: The dog chased the cat."
    },
    "pluralize_words": {
        "title": "pluralize_words(x)",
        "badge": "Linguistic Processing \u2014 str",
        "desc": "Converts singular nouns to plural form.",
        "code": "import nlp_text_preprocessing as tp\n\ntext = \"The developer built an application.\"\nplural = tp.pluralize_words(text)\n\nprint(plural)\n# Output: The developers built an applications."
    },
    "detect_profanity": {
        "title": "detect_profanity(x)",
        "badge": "Safety & Sentiment \u2014 bool",
        "desc": "Returns True if input text contains profanity or explicit words.",
        "code": "import nlp_text_preprocessing as tp\n\ntext = \"This is a clean text example.\"\nhas_profanity = tp.detect_profanity(text)\n\nprint(f\"Profanity Detected: {has_profanity}\")\n# Output: Profanity Detected: False"
    },
    "censor_profanity": {
        "title": "censor_profanity(x)",
        "badge": "Safety & Sentiment \u2014 str",
        "desc": "Censors profanity words with asterisks (****).",
        "code": "import nlp_text_preprocessing as tp\n\ntext = \"What a damn bad day.\"\ncensored = tp.censor_profanity(text)\n\nprint(censored)\n# Output: What a **** bad day."
    },
    "detect_toxicity": {
        "title": "detect_toxicity(x)",
        "badge": "Safety & Sentiment \u2014 float",
        "desc": "Calculates baseline toxicity score (0.0 to 1.0) based on insult/hate keywords.",
        "code": "import nlp_text_preprocessing as tp\n\ntext = \"You are so stupid and trash.\"\ntox = tp.detect_toxicity(text)\n\nprint(f\"Toxicity Score: {tox:.2f}\")\n# Output: Toxicity Score: 0.33"
    },
    "detect_spam_signals": {
        "title": "detect_spam_signals(x)",
        "badge": "Safety & Sentiment \u2014 dict",
        "desc": "Detects spam signals (excessive caps, punctuation, URL density).",
        "code": "import nlp_text_preprocessing as tp\n\ntext = \"WIN FREE MONEY NOW!!! CLICK HERE http://spam.link\"\nsignals = tp.detect_spam_signals(text)\n\nprint(signals)\n# Output: {'is_spam_suspect': True, 'caps_ratio': 0.65, 'punct_density': 0.08, ...}"
    },
    "sentiment_analysis": {
        "title": "sentiment_analysis(x)",
        "badge": "Safety & Sentiment \u2014 dict",
        "desc": "Performs sentiment classification using TextBlob NaiveBayesAnalyzer.",
        "code": "import nlp_text_preprocessing as tp\n\ntext = \"I love using this package! It is amazing.\"\nsentiment = tp.sentiment_analysis(text)\n\nprint(sentiment)\n# Output: {'classification': 'pos', 'p_pos': 0.85, 'p_neg': 0.15}"
    },
    "polarity_subjectivity": {
        "title": "polarity_subjectivity(x)",
        "badge": "Safety & Sentiment \u2014 dict",
        "desc": "Returns pattern-based sentiment polarity (-1.0 to 1.0) and subjectivity (0.0 to 1.0).",
        "code": "import nlp_text_preprocessing as tp\n\ntext = \"Great features and easy setup!\"\nscores = tp.polarity_subjectivity(text)\n\nprint(scores)\n# Output: {'polarity': 0.625, 'subjectivity': 0.75}"
    },
    "emotion_detection": {
        "title": "emotion_detection(x)",
        "badge": "Safety & Sentiment \u2014 dict",
        "desc": "Calculates lexicon-based emotion counts (joy, anger, sadness, fear).",
        "code": "import nlp_text_preprocessing as tp\n\ntext = \"I am so happy and excited about this delight!\"\nemotions = tp.emotion_detection(text)\n\nprint(emotions)\n# Output: {'joy': 3, 'anger': 0, 'sadness': 0, 'fear': 0}"
    },
    "Pipeline": {
        "title": "Pipeline(steps=None)",
        "badge": "Pipeline Engine \u2014 Pipeline",
        "desc": "Pipeline engine class for chaining and executing sequential text cleaning steps.",
        "code": "from nlp_text_preprocessing import Pipeline\n\npipe = Pipeline(['to_lower_case', 'remove_urls', 'remove_extra_whitespace'])\nresult = pipe.run(\"Hello   WORLD! Visit https://test.com\")\n\nprint(result)\n# Output: hello world! visit"
    },
    "Pipeline_add_step": {
        "title": "Pipeline.add_step(step)",
        "badge": "Pipeline Engine \u2014 Pipeline",
        "desc": "Appends a step function or registered step name to the pipeline instance.",
        "code": "from nlp_text_preprocessing import Pipeline\n\npipe = Pipeline()\npipe.add_step('to_lower_case')\npipe.add_step('remove_emails')\n\nprint(pipe.run(\"Contact INFO@TEST.COM\"))\n# Output: contact"
    },
    "Pipeline_run": {
        "title": "Pipeline.run(text)",
        "badge": "Pipeline Engine \u2014 str",
        "desc": "Runs all registered pipeline steps sequentially on a single text string.",
        "code": "from nlp_text_preprocessing import Pipeline\n\npipe = Pipeline.default()\nclean = pipe.run(\"<b>Check https://test.com!</b>\")\n\nprint(clean)\n# Output: check"
    },
    "Pipeline_run_batch": {
        "title": "Pipeline.run_batch(texts)",
        "badge": "Pipeline Engine \u2014 list[str]",
        "desc": "Runs pipeline transformation across a list of text strings.",
        "code": "from nlp_text_preprocessing import Pipeline\n\npipe = Pipeline.default()\ntexts = [\"<b>Text 1</b>\", \"Contact user@test.com\"]\nresults = pipe.run_batch(texts)\n\nprint(results)\n# Output: ['text 1', 'contact']"
    },
    "Pipeline_run_series": {
        "title": "Pipeline.run_series(series)",
        "badge": "Pipeline Engine \u2014 Series",
        "desc": "Applies pipeline transformation across a pandas Series.",
        "code": "import pandas as pd\nfrom nlp_text_preprocessing import Pipeline\n\ns = pd.Series([\"  HELLO WORLD  \", \"TEST@EMAIL.COM\"])\npipe = Pipeline.default()\ncleaned_s = pipe.run_series(s)\n\nprint(cleaned_s)\n# Output Series: 0: 'hello world', 1: ''"
    },
    "Pipeline_default": {
        "title": "Pipeline.default()",
        "badge": "Pipeline Engine \u2014 Pipeline",
        "desc": "Factory classmethod returning a pre-configured 7-step default cleaning pipeline.",
        "code": "from nlp_text_preprocessing import Pipeline\n\ndefault_pipe = Pipeline.default()\nprint(default_pipe.steps)\n# Output: ['to_lower_case', 'contraction_to_expansion', 'remove_emails', 'remove_urls', ...]"
    },
    "register_step": {
        "title": "register_step(name)",
        "badge": "Pipeline Engine \u2014 decorator",
        "desc": "Decorator to register a custom python function into the global pipeline registry.",
        "code": "from nlp_text_preprocessing import register_step, Pipeline\n\n@register_step(\"remove_custom_foo\")\ndef remove_custom_foo(text):\n    return text.replace(\"foo\", \"\")\n\npipe = Pipeline(['remove_custom_foo'])\nprint(pipe.run(\"foobar\"))\n# Output: bar"
    },
    "diff_report": {
        "title": "diff_report(before_list, after_list)",
        "badge": "Pipeline Engine \u2014 dict",
        "desc": "Generates summary diff report comparing text before and after pipeline execution.",
        "code": "from nlp_text_preprocessing import diff_report\n\nbefore = [\"Contact test@domain.com at https://example.com\"]\nafter  = [\"Contact  at \"]\n\nreport = diff_report(before, after)\nprint(report)\n# Output: {'total_items': 1, 'char_reduction_pct': 64.29, 'emails_removed': 1, 'urls_removed': 1}"
    },
    "get_spacy_nlp": {
        "title": "get_spacy_nlp(model_name)",
        "badge": "Environment \u2014 Language",
        "desc": "Lazy-loads and caches spaCy language model (downloads automatically if missing).",
        "code": "import nlp_text_preprocessing as tp\n\nnlp = tp.get_spacy_nlp('en_core_web_sm')\ndoc = nlp(\"spaCy model loaded successfully!\")\n\nprint([token.text for token in doc])\n# Output: ['spaCy', 'model', 'loaded', 'successfully', '!']"
    },
    "download_nltk_packages": {
        "title": "download_nltk_packages()",
        "badge": "Environment \u2014 None",
        "desc": "Downloads required NLTK corpus and model packages (punkt, stopwords, wordnet, etc.).",
        "code": "import nlp_text_preprocessing as tp\n\n# Download missing NLTK resources\ntp.download_nltk_packages()\nprint(\"NLTK packages downloaded successfully.\")"
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
