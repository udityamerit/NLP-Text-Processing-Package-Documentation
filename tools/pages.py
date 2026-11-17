"""Hand-written pages: overview, installation and user guide. Code blocks are executed at build time."""
from __future__ import annotations

IMP = "import nlp_text_preprocessing as tp\n\n"

GUIDE_SECTIONS = [
    ("pipeline", "Build a pipeline"),
    ("pandas", "Work with pandas"),
    ("batch", "Batch processing"),
    ("custom-steps", "Custom steps"),
    ("save-load", "Save & reuse"),
    ("sklearn", "Use with scikit-learn"),
    ("transformers", "Transformer models"),
    ("privacy", "Mask personal data"),
    ("moderation", "Moderate content"),
    ("cli", "Command line"),
]


def build(S, B):
    return {"index.html": overview(S, B), "installation.html": installation(S, B), "guide.html": guide(S, B)}


def _page(S, B, **kw):
    return S.page(version=B.VERSION, api_groups=B.API_GROUPS, guide_sections=B.GUIDE_SECTIONS, **kw)


def _sec(S, B, sid: str, title: str, body: str, where: str, desc: str) -> str:
    B.SEARCH.append([title, f"{where}#{sid}", {"guide.html": "User guide", "installation.html": "Installation", "index.html": "Overview"}[where], desc])
    return f'<section class="doc-section" id="{sid}">\n<h2>{S.esc(title)}</h2>{body}</section>'


def py(S, src: str, ctx: str, **kw) -> str:
    return S.code(src.strip("\n"), "Python", ctx=ctx, namespace={}, **kw)


def sh(S, src: str, lang: str = "Terminal") -> str:
    return S.code(src, lang)


def onward(S, href: str, label: str) -> str:
    return f'<a class="onward" href="{href}">{S.esc(label)}{S.icon("arrow")}</a>'


# =========================================================================== overview
def overview(S, B) -> str:
    v = B.VERSION
    groups = {g["id"]: g for g in B.api_data.GROUPS}

    def cell(gid: str, blurb: str) -> list[str]:
        g = groups[gid]
        return [f"[{g['title']}](api.html#{gid})", blurb, str(len(g["entries"]))]

    cards = "".join(
        f'<a class="nav-card" href="{href}">\n<div class="card-icons"><span>{S.icon(ic)}</span>{S.icon("arrow")}</div>\n<h3>{title}</h3><p>{text}</p></a>'
        for href, ic, title, text in [
            ("installation.html", "install", "Installation", "Set up an environment, pick extras and prepare models."),
            ("guide.html", "book", "User guide", "Pipelines, pandas, scikit-learn, transformers and the CLI."),
            ("api.html", "code", "API reference", f"{sum(len(g['entries']) for g in groups.values())} entries with parameters and runnable examples."),
        ])

    rows = [
        ("setup", "Check and fetch NLTK data, spaCy models and stop words."),
        ("cleaning", "Case, whitespace, punctuation, numbers, stop words, contractions."),
        ("web-social", "HTML, URLs, emails, mentions, emojis, phone numbers, PII masking."),
        ("statistics", "Counts, ratios, readability scores and feature tables."),
        ("language", "Lemmas, entities, POS tags, n-grams, keywords, WordNet, language ID."),
        ("moderation", "Sentiment, emotion, profanity, toxicity and spam signals."),
        ("transformers", "Light cleaning, truncation and chunking for BERT and GPT models."),
        ("pipelines", "Pipeline, custom steps, JSON save and load, scikit-learn transformer."),
        ("cli", "Clean files, CSV columns and stdin from the terminal."),
    ]
    table = S.table(["Area", "What it covers", "Entries"], [cell(g, t) for g, t in rows])

    quick = (
        '<p>Install the package, then run a built-in pipeline on a messy string.</p>'
        + sh(S, "python -m pip install nlp-text-preprocessing")
        + py(S, IMP + 'text = "<b>Fresh   TEXT!</b>"\nprint(tp.Pipeline.default().run(text))', "quick-start")
        + '<p>Use functions directly, or chain them. The last step of a pipeline may return anything, such as a count or a sentiment label.</p>'
        + py(S, IMP + 'review = "<p>Loved it!! Visit https://example.com for more.</p>"\n\n'
                "pipe = tp.Pipeline([\"remove_html_tag\", \"remove_urls\", \"to_lower_case\", \"remove_special_chars\", \"sentiment_analysis\"])\nprint(pipe.run(review))\n"
                "print(tp.text_stats(\"Hello world. NLP is fun!\")[\"word_count\"])", "quick-start-2")
        + S.note("The first call that needs a spaCy model, NLTK corpus or TextBlob data tells you what is missing. Run `tp.check_resources()` to see the status, or follow [Models & resources](installation.html#resources).")
        + onward(S, "guide.html#pipeline", "Build your first pipeline")
    )
    new = S.table(["Version", "Highlights"], [
        ["0.5", "`readability_scores`, `mask_pii(names=True)`, faster batch lemmatization, type hints."],
        ["0.4", "Pipeline steps with arguments, `save`/`load`, `TextPreprocessor`, `light_clean`, `truncate_text`, `chunk_text`, the `nlp-prep` CLI."],
        ["0.3", "Lighter core install; pandas, plotting and scikit-learn became optional extras."],
    ])
    compare = S.table(["Aspect", "Traditional approach", "With nlp-text-preprocessing"], [
        ["Cleaning steps", "Regular expressions copied between notebooks, each slightly different.", "Named, tested functions such as `remove_urls` and `remove_html_tag`."],
        ["Missing values", "`None` or `NaN` in a column raises an error half way through a run.", "Every function treats `None`, `NaN`, `pd.NA` and bytes as empty text."],
        ["Libraries", "Wire up `re`, BeautifulSoup, NLTK, spaCy and TextBlob separately, each with its own setup.", "One import and one API. Heavy libraries load only when a function needs them."],
        ["Reuse", "The preprocessing lives in a script that is hard to share or reproduce.", "A `Pipeline` is a list of steps. Save it to JSON and load it back anywhere."],
        ["Speed on large data", "Call the spaCy model once per document.", "`run_batch` and `run_series` use `nlp.pipe` for the spaCy steps, about 2x faster with identical output."],
        ["Downloads", "Models and corpora are fetched silently, or fail on first use.", "Nothing downloads on its own. `check_resources()` reports what is missing and `download_nltk_packages()` fetches it once."],
        ["Transformer models", "Aggressive classic cleaning can strip punctuation and casing that transformer models use.", "`light_clean`, `truncate_text` and `chunk_text` prepare text for transformer tokenizers."],
    ])
    why = (
        "<p>Preparing text is the first step of almost every NLP or machine learning project, and it is usually written from scratch each time. "
        "<code>nlp-text-preprocessing</code> turns that repeated work into a small, consistent toolkit: more than 60 single-purpose functions, "
        "an extensible <code>Pipeline</code>, and defensive handling of messy input, so you spend your time on the model and not on the cleaning code.</p>"
        "<h3>How it helps</h3>"
        "<ul><li><strong>Faster to start.</strong> Clean, analyse and visualise text with one install and one import.</li>"
        "<li><strong>Consistent results.</strong> The same named steps give the same output in every project and for every teammate.</li>"
        "<li><strong>Safe on real data.</strong> Missing values and odd types do not stop a long run.</li>"
        "<li><strong>Ready for both worlds.</strong> Use the full cleaning path for classic models, or the light path for transformers.</li></ul>"
        "<h3>How it differs from the traditional way</h3>" + compare
        + "<p>A typical hand-written cleaner and the same job as a pipeline:</p>"
        + py(S, 'import re\n\ntext = "<b>Fresh   TEXT!</b> Visit https://example.com"\ntext = re.sub(r"<[^>]+>", " ", text)\n'
                'text = re.sub(r"https?://\\S+", "", text)\ntext = re.sub(r"[^\\w\\s]", "", text)\n'
                'text = re.sub(r"\\s+", " ", text).strip().lower()\nprint(text)', "why-traditional")
        + py(S, IMP + 'text = "<b>Fresh   TEXT!</b> Visit https://example.com"\n'
                'pipe = tp.Pipeline(["remove_html_tag", "remove_urls", "remove_special_chars", "remove_extra_whitespace", "to_lower_case"])\nprint(pipe.run(text))\n'
                'print(repr(pipe.run(None)))', "why-pipeline")
        + S.note("The sentiment, profanity, toxicity and spam helpers are transparent keyword baselines. They are useful for quick checks and exploration. Use a trained model for anything high-stakes.")
    )
    author = (
        "<p>This documentation covers <strong>nlp-text-preprocessing</strong>, created and maintained by <strong>Uditya Narayan Tiwari</strong>. "
        "The package is open source under the MIT license, so you can use it in personal, academic and commercial projects.</p>"
        + S.table(["Where", "Link"], [
            ["Author website", "[udityanarayantiwari.netlify.app](https://udityanarayantiwari.netlify.app/)"],
            ["GitHub profile", "[github.com/udityamerit](https://github.com/udityamerit)"],
            ["Source code and issues", f"[Text-Processing-Package-For-Natural-Language-Processing]({S.REPO})"],
            ["PyPI", f"[nlp-text-preprocessing]({S.PYPI})"],
        ])
        + "<p>Found a bug or want a function added? Open an issue or a pull request on the source repository.</p>"
        + onward(S, S.REPO + "/issues", "Report an issue or suggest a feature")
    )
    body = f"""<section class="hero">
<div class="hero-copy">
<h1 id="hero-heading">Text preprocessing<br>in Python</h1>
<p>Clean raw text, build reusable pipelines and extract features, for classic NLP and transformer models.</p>
<div class="hero-actions"><a href="#quick-start">Run the quick start</a></div>
<div class="metadata"><a href="{S.PYPI}{v}/"><i></i>v{v}</a><span>Python ≥ 3.9</span><a href="{S.REPO}/blob/main/LICENSE">MIT license</a></div></div>
<figure class="specimen" aria-label="Default pipeline example">
<div class="dots"></div>
<div class="transformation">
<div class="sample raw"><span>Input</span><code>&lt;b&gt;Fresh   TEXT!&lt;/b&gt;</code></div>
<a class="transform-step" href="api.html#Pipeline.default"><span aria-hidden="true">↓</span><code>Pipeline.default()</code></a>
<div class="sample clean"><span>Output</span><samp>fresh text</samp></div></div></figure></section>
<section class="explore" id="features">
<h2 id="features-heading">Explore the docs</h2>
<div class="cards">{cards}</div></section>
{_sec(S, B, "why", "Why this package", why, "index.html", "The purpose of the package, how it helps and how it differs from hand-written text cleaning.")}
{_sec(S, B, "quick-start", "Quick start", quick, "index.html", "Install the package and clean your first string.")}
{_sec(S, B, "whats-inside", "What is inside", "<p>Every function takes plain text, treats <code>None</code>, <code>NaN</code> and bytes as empty text, and imports heavy libraries only when it needs them.</p>" + table, "index.html", "Overview of the function families.")}
{_sec(S, B, "whats-new", "Recent releases", new + onward(S, S.REPO + "/blob/main/CHANGELOG.md", "Read the full changelog"), "index.html", "Release highlights for versions 0.3 to 0.5.")}
{_sec(S, B, "author", "About the author", author, "index.html", "Uditya Narayan Tiwari, author and maintainer of nlp-text-preprocessing.")}"""
    return _page(S, B, name="index", title="Overview", crumb=("Getting started", "Overview"), body=body,
                 description=f"Documentation for nlp-text-preprocessing {v}: text cleaning, feature extraction, pipelines and transformer-ready text preparation in Python.")


# =========================================================================== installation
def installation(S, B) -> str:
    v = B.VERSION
    envs = [
        ("windows", "Windows", "PowerShell", "py -3.11 -m venv .venv\n.\\.venv\\Scripts\\Activate.ps1"),
        ("macos", "macOS", "Terminal", "python3 -m venv .venv\nsource .venv/bin/activate"),
        ("linux", "Linux", "Terminal", "python3 -m venv .venv\nsource .venv/bin/activate"),
        ("conda", "Conda", "Terminal", "conda create -n nlp-docs python=3.11\nconda activate nlp-docs"),
    ]
    panels = "".join(f'<div class="os-panel" id="os-{i}">\n<h3>{n}</h3>\n{S.code(c, lang)}</div>\n' for i, n, lang, c in envs)
    env = f'<p>Use a virtual environment. Python 3.9 or later is required.</p>\n<div class="os-tabs" aria-label="Environment"></div>\n{panels}'

    extras = S.table(["Extra", "Installs", "Enables"], [
        ["Core (always)", "spaCy, TextBlob, NLTK, BeautifulSoup, lxml, emoji, langdetect", "All cleaning, language and moderation functions"],
        ["`pandas`", "pandas", "`text_stats_batch`, `Pipeline.run_series`"],
        ["`viz`", "wordcloud, matplotlib", "`get_wordcloud`"],
        ["`sklearn`", "scikit-learn", "`TextPreprocessor`"],
        ["`transformers`", "transformers", "Tokenizers for `truncate_text` and `chunk_text`"],
        ["`all`", "pandas, wordcloud, matplotlib, scikit-learn", "Everything above except transformers"],
    ])
    install = (
        sh(S, "python -m pip install nlp-text-preprocessing")
        + "<p>Add extras only for the features you use. Put the extra name in brackets, and quote it so zsh does not expand it.</p>" + sh(S, 'python -m pip install "nlp-text-preprocessing[pandas,sklearn]"') + extras
        + "<p>Check the installed version:</p>"
        + py(S, 'from importlib.metadata import version\nimport nlp_text_preprocessing as tp\n\nprint(version("nlp-text-preprocessing"))\nprint(tp.__version__)', "install-version", output=f"{v}\n{v}")
        + S.note("Importing the package downloads nothing, and `import nlp_text_preprocessing` stays fast because spaCy, TextBlob and NLTK load on first use.")
    )
    resources = (
        "<p>Counting words and normalizing whitespace need no extra data. Language functions use a spaCy model and NLTK corpora. Install them once while you are online:</p>"
        + py(S, IMP + "tp.download_nltk_packages()", "res-download", run=False)
        + "<p>This fetches the NLTK data (<code>punkt_tab</code>, <code>wordnet</code>, <code>omw-1.4</code>) and the spaCy model <code>en_core_web_sm</code>. Add <code>include_sentiment_corpus=True</code> for the legacy Naive Bayes sentiment method. To install the spaCy model yourself:</p>"
        + sh(S, "python -m spacy download en_core_web_sm")
        + "<h3>Check what is installed</h3>"
        + py(S, IMP + "print(tp.check_resources())", "res-check")
        + "<p>The same check is available from the terminal, and <code>--download</code> installs whatever is missing.</p>"
        + sh(S, "nlp-prep resources\nnlp-prep resources --download")
        + "<h3>Automatic download</h3><p>By default nothing is downloaded behind your back. Set this variable to let <code>get_spacy_nlp()</code> fetch a missing model on first use, which is handy in notebooks and CI.</p>"
        + sh(S, "# macOS / Linux\nexport NLP_TEXT_PREPROCESSING_AUTO_DOWNLOAD=1\n\n# PowerShell\n$env:NLP_TEXT_PREPROCESSING_AUTO_DOWNLOAD = \"1\"")
        + S.table(["Resource", "Used by"], [
            ["spaCy `en_core_web_sm`", "`lemmatize`, `convert_to_base`, `clean_text`, `extract_entities`, `extract_pos_tags`, `get_dependency_tree`, `chunk_noun_phrases`, `singularize_words`, `pluralize_words`, `mask_pii(names=True)`, `get_stop_words`"],
            ["NLTK `punkt_tab`, TextBlob corpora", "`sentiment_analysis`, `polarity_subjectivity`, `correct_spelling`, `get_noun_phrase`, `extract_features`"],
            ["NLTK `wordnet`, `omw-1.4`", "`get_synonyms`, `get_antonyms`"],
            ["NLTK `movie_reviews` (optional)", "`sentiment_analysis(method='naive_bayes')`"],
        ])
        + S.note("Some NLTK versions ask for `averaged_perceptron_tagger_eng` for part-of-speech tagging. If it is missing, run `python -m nltk.downloader averaged_perceptron_tagger_eng`.")
        + onward(S, "index.html#quick-start", "Try the quick start")
    )
    sections = [
        _sec(S, B, "environment", "Create an environment", env, "installation.html", "Virtual environment commands for Windows, macOS, Linux and Conda."),
        _sec(S, B, "install", "Install the package", install, "installation.html", "pip install and optional extras: pandas, viz, sklearn, transformers."),
        _sec(S, B, "resources", "Models & resources", resources, "installation.html", "Download spaCy and NLTK resources, check them and enable automatic download."),
    ]
    outline = [("environment", "Create an environment"), ("install", "Install the package"), ("resources", "Models & resources")]
    body = S.intro("Installation", f"Set up an isolated environment and install version {v} from PyPI. Python 3.9 or later is required.") + S.reading("\n".join(sections), outline)
    return _page(S, B, name="installation", title="Installation", crumb=("Getting started", "Installation"), body=body,
                 description=f"Install nlp-text-preprocessing {v}, choose optional extras and download the spaCy and NLTK resources.")


# =========================================================================== guide
def guide(S, B) -> str:
    G = []

    def add(sid, title, body, desc):
        G.append(_sec(S, B, sid, title, body, "guide.html", desc))

    add("pipeline", "Build a pipeline", (
        "<p>A step is the name of a built-in function, a name you registered, a callable, or a <code>(name, kwargs)</code> pair. Every step except the last must return a string. Names are checked when the pipeline is created, so a typo fails immediately.</p>"
        + py(S, IMP + 'pipe = tp.Pipeline([\n    "remove_html_tag",\n    "remove_urls",\n    "to_lower_case",\n    "contraction_to_expansion",\n    "remove_special_chars",\n    "remove_extra_whitespace",\n])\nprint(pipe.run("<p>It\'s GREAT!! Read https://example.com</p>"))', "g-pipeline")
        + "<h3>Pass arguments to a step</h3>"
        + py(S, IMP + 'pipe = tp.Pipeline([\n    "to_lower_case",\n    ("remove_stop_words", {"keep_negations": False}),\n])\nprint(pipe.run("This is NOT a drill"))\nprint(pipe)', "g-args")
        + "<h3>End with a measurement</h3><p>The final step may return a number, label, list or dictionary instead of text.</p>"
        + py(S, IMP + 'pipe = tp.Pipeline(["remove_urls", "remove_html_tag", "sentiment_analysis"])\nprint(pipe.run("<p>I really love this! https://example.com</p>"))', "g-final")
        + "<h3>Build step by step</h3>"
        + py(S, IMP + 'pipe = tp.Pipeline()\npipe.add_step("to_lower_case").add_step("remove_extra_whitespace")\nprint(len(pipe), pipe.run("  Mixed   CASE  "))', "g-add")
        + "<h3>Errors are explicit</h3>"
        + py(S, IMP + 'try:\n    tp.Pipeline(["to_lowercase"])\nexcept Exception as exc:\n    print(type(exc).__name__ + ":", exc)\n\ntry:\n    tp.Pipeline(["text_stats", "to_lower_case"]).run("hello")\nexcept TypeError as exc:\n    print("TypeError:", exc)', "g-errors")
        + onward(S, "api.html#Pipeline", "Pipeline reference")
    ), "Chain steps, pass arguments, end with a measurement and see the errors.")

    add("pandas", "Work with pandas", (
        f"<p>Install the extra with {S.md('`pip install \"nlp-text-preprocessing[pandas]\"`')}. <code>run_series</code> keeps the index and name; missing values become empty strings.</p>"
        + py(S, "import pandas as pd\nimport nlp_text_preprocessing as tp\n\ndf = pd.DataFrame({\"review\": [\"<b>LOVED</b> it!! \\U0001f60d\", \"Not good, https://spam.io\", None]})\ndf[\"clean\"] = tp.Pipeline.default().run_series(df[\"review\"])\nprint(df)", "g-series")
        + "<h3>Feature table in one call</h3><p><code>text_stats_batch</code> returns one row of statistics per text.</p>"
        + py(S, "import pandas as pd\nimport nlp_text_preprocessing as tp\n\ndf = pd.DataFrame({\"text\": [\"Short one.\", \"A longer sentence, with #tags and @mentions!\"]})\nfeatures = tp.text_stats_batch(df, \"text\")\nprint(features[[\"word_count\", \"sentence_count\", \"hashtags_count\", \"mentions_count\"]].astype(int))", "g-stats-batch")
        + "<h3>Apply any single function</h3>"
        + py(S, "import pandas as pd\nimport nlp_text_preprocessing as tp\n\ns = pd.Series([\"Call 555-123-4567\", \"No phone here\"])\nprint(s.map(tp.count_phone_numbers).tolist())", "g-map")
    ), "Clean a DataFrame column with run_series and build feature tables with text_stats_batch.")

    add("batch", "Batch processing", (
        "<p>Use <code>run_batch</code> for lists. Steps run across the whole list one after another, and the spaCy steps (<code>lemmatize</code>, <code>convert_to_base</code>, <code>singularize_words</code>, <code>pluralize_words</code>) use <code>nlp.pipe</code>, which is several times faster than calling them text by text.</p>"
        + py(S, IMP + 'pipe = tp.Pipeline(["remove_html_tag", "to_lower_case", "lemmatize", "remove_stop_words"])\ntexts = ["The <b>dogs</b> were barking loudly", "She has been studying for exams"]\nprint(pipe.run_batch(texts))', "g-batch")
        + "<h3>Measure what cleaning changed</h3><p><code>diff_report</code> summarizes characters, words, URLs and emails removed between two lists.</p>"
        + py(S, IMP + 'before = ["<p>Mail me@x.com</p>", "Plain text", "See https://example.com now"]\nafter = tp.Pipeline.default().run_batch(before)\nprint(tp.diff_report(before, after))', "g-diff")
    ), "Process lists quickly with run_batch and measure the effect with diff_report.")

    add("custom-steps", "Custom steps", (
        "<p>Register a function once and use it by name. The first argument is the text; extra keyword arguments come from the step's <code>kwargs</code>.</p>"
        + py(S, IMP + 'import re\n\n@tp.register_step("strip_ticket_ids")\ndef strip_ticket_ids(text, prefix="TKT"):\n    return re.sub(rf"{prefix}-\\d+", "", text)\n\npipe = tp.Pipeline([\n    "to_lower_case",\n    ("strip_ticket_ids", {"prefix": "tkt"}),\n    "remove_extra_whitespace",\n])\nprint(pipe.run("Re: TKT-4821 printer is  broken"))', "g-custom")
        + "<p>Plain callables work too, but only registered names can be saved to JSON.</p>"
        + py(S, IMP + 'pipe = tp.Pipeline(["to_lower_case", lambda t: t.replace("colour", "color")])\nprint(pipe.run("Favourite COLOUR"))\n\ntry:\n    pipe.to_config()\nexcept ValueError as exc:\n    print("ValueError:", exc)', "g-callable")
    ), "Register custom functions with register_step and pass arguments.")

    add("save-load", "Save & reuse", (
        "<p>Pipelines serialize to JSON, so the exact preprocessing used in training can ship with the model.</p>"
        + py(S, IMP + 'import os, tempfile\n\npipe = tp.Pipeline(["remove_urls", ("remove_stop_words", {"keep_negations": True}), "to_lower_case"])\npath = os.path.join(tempfile.mkdtemp(), "preprocess.json")\npipe.save(path)\nprint(open(path).read())\n\nrestored = tp.Pipeline.load(path)\nprint(restored.run("This is NOT bad https://x.io"))', "g-save")
        + "<p>For your own storage use <code>to_config()</code> and <code>Pipeline.from_config()</code>. The same file works from the command line with <code>nlp-prep clean --pipeline preprocess.json</code>.</p>"
        + onward(S, "api.html#Pipeline.save", "save and load reference")
    ), "Save a pipeline to JSON, load it again and reuse it from the CLI.")

    add("sklearn", "Use with scikit-learn", (
        f"<p>{S.md('`TextPreprocessor`')} wraps a pipeline as a transformer, so cleaning travels with the model and is applied identically at predict time. Requires {S.md('`pip install \"nlp-text-preprocessing[sklearn]\"`')}.</p>"
        + py(S, "from sklearn.feature_extraction.text import TfidfVectorizer\nfrom sklearn.linear_model import LogisticRegression\nfrom sklearn.pipeline import make_pipeline\nimport nlp_text_preprocessing as tp\n\ntexts = [\"<b>Great</b> movie!\", \"Terrible film...\", \"Loved this great film\", \"Awful acting, terrible plot\"]\nlabels = [1, 0, 1, 0]\n\nmodel = make_pipeline(\n    tp.TextPreprocessor([\"remove_html_tag\", \"to_lower_case\", \"remove_special_chars\"]),\n    TfidfVectorizer(),\n    LogisticRegression(),\n)\nmodel.fit(texts, labels)\nprint(model.predict([\"A great movie\", \"Terrible!\"]))", "g-sklearn")
        + "<p>Because the steps are a parameter, grid search can tune the cleaning itself.</p>"
        + py(S, "from sklearn.feature_extraction.text import TfidfVectorizer\nfrom sklearn.pipeline import make_pipeline\nimport nlp_text_preprocessing as tp\n\nmodel = make_pipeline(tp.TextPreprocessor([\"to_lower_case\"]), TfidfVectorizer())\nmodel.set_params(textpreprocessor__steps=[\"to_lower_case\", \"remove_stop_words\"])\nprint(model.get_params()[\"textpreprocessor__steps\"])", "g-sklearn-params")
    ), "Use TextPreprocessor inside scikit-learn pipelines and grid search.")

    add("transformers", "Transformer models", (
        "<p>BERT and GPT style models were trained on natural text. Use <code>light_clean</code> to remove noise only, and keep case, punctuation and word forms.</p>"
        + py(S, IMP + 'raw = "<p>Can\'t BELIEVE it\'s &amp; working!! \\u2764\\ufe0f  https://example.com</p>"\nprint(tp.light_clean(raw))\nprint(tp.clean_text(raw))', "g-light")
        + "<p>Compare: <code>clean_text</code> is the classic route for bag-of-words models and removes the information a transformer uses.</p>"
        + "<h3>Respect the token limit</h3><p>Without a tokenizer, whitespace words are a rough stand-in. Pass any callable that returns tokens.</p>"
        + py(S, IMP + 'text = "one two three four five six seven eight nine ten"\nprint(tp.truncate_text(text, max_tokens=4))\nfor chunk in tp.chunk_text(text, max_tokens=4, overlap=1):\n    print(chunk)', "g-chunk")
        + "<p>With a real tokenizer, counts match what the model sees. Leave room for special tokens such as <code>[CLS]</code> and <code>[SEP]</code>.</p>"
        + py(S, IMP + 'from transformers import AutoTokenizer\n\ntok = AutoTokenizer.from_pretrained("bert-base-uncased")\nchunks = tp.chunk_text(long_document, max_tokens=500, overlap=50, tokenizer=tok)', "g-hf", run=False)
    ), "Light cleaning, truncation and overlapping chunks for transformer models.")

    add("privacy", "Mask personal data", (
        "<p><code>mask_pii</code> redacts emails, card numbers, US Social Security numbers and phone numbers. Set <code>names=True</code> to add person names (uses spaCy and is statistical, so review the output when privacy matters).</p>"
        + py(S, IMP + 'record = "Contact Priya Sharma at priya@example.com or 555-123-4567. Card 4111 1111 1111 1111."\nprint(tp.mask_pii(record))\nprint(tp.mask_pii(record, token="<PII>", names=True))', "g-pii")
        + "<p>Count first, remove selectively, or mask everything.</p>"
        + py(S, IMP + 'text = "Email a@b.com, call 555-123-4567, see https://example.com"\nprint(tp.count_emails(text), tp.count_phone_numbers(text), tp.count_urls(text))\nprint(tp.remove_phone_numbers(tp.remove_emails(text)))', "g-pii-count")
    ), "Redact emails, phone numbers, card numbers, SSNs and names.")

    add("moderation", "Moderate content", (
        "<p>The moderation helpers are transparent keyword baselines. They are useful for triage and dashboards, not as a replacement for a trained classifier.</p>"
        + py(S, IMP + 'comment = "You damn idiot. CLICK HERE!!! BUY NOW http://spam.example"\n\nprint("profane:", tp.detect_profanity(comment))\nprint("toxicity:", tp.detect_toxicity(comment))\nprint("spam:", tp.detect_spam_signals(comment)["is_spam_candidate"])\nprint(tp.censor_profanity("What the hell, damn it"))', "g-mod")
        + "<h3>Understand a score</h3><p><code>toxicity_report</code> lists what matched and what a negation cancelled, so reviewers can see why a text scored as it did.</p>"
        + py(S, IMP + 'print(tp.toxicity_report("You idiot. I do not hate you."))', "g-tox")
        + "<h3>Tune the word list</h3>"
        + py(S, IMP + 'print(tp.detect_profanity("what the hell", include_mild=False))\nprint(tp.detect_profanity("that was a frack-up", extra_words=["frack"]))', "g-tune")
    ), "Detect profanity, toxicity and spam, and explain scores with toxicity_report.")

    add("cli", "Command line", (
        "<p>The <code>nlp-prep</code> command (or <code>python -m nlp_text_preprocessing</code>) cleans text without writing Python. Input is a <code>.txt</code> file with one document per line, a CSV column, or standard input (<code>-</code>).</p>"
        + sh(S, "# one document per line, light cleaning for transformer models (default)\nnlp-prep clean reviews.txt -o cleaned.txt\n\n# a CSV column; the result goes to <column>_clean\nnlp-prep clean reviews.csv --column review -o cleaned.csv\n\n# classic cleaning: lowercase, no punctuation, lemmatized, stop words removed\nnlp-prep clean reviews.txt --mode standard --stopwords\n\n# your own steps, or a saved pipeline\nnlp-prep clean reviews.txt --steps remove_urls,to_lower_case\nnlp-prep clean reviews.txt --pipeline preprocess.json")
        + "<p>It also works in shell pipelines:</p>"
        + S.code('echo "<b>Hello   WORLD</b> https://example.com" | nlp-prep clean - --url-token "[URL]"', "Terminal",
                 output=B.run_cli(["clean", "-", "--url-token", "[URL]"], "<b>Hello   WORLD</b> https://example.com\n"))
        + onward(S, "api.html#nlp-prep-clean", "All command options")
    ), "Clean text files, CSV columns and stdin with nlp-prep.")

    outline = list(GUIDE_SECTIONS)
    body = S.intro("User guide", "Task-focused recipes. Every example runs as written, and the output shown is real.") + S.reading("\n".join(G), outline)
    return _page(S, B, name="guide", title="User guide", crumb=("User guide", "Recipes"), body=body,
                 description="Recipes for pipelines, pandas, scikit-learn, transformer models, PII masking, moderation and the nlp-prep command line.")
