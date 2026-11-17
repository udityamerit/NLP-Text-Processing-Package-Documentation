"""Reference content: one record per public function, method and command.

Signatures and return types are read from the installed package; the descriptions,
parameter notes and examples live here. Examples are executed at build time.
"""
from __future__ import annotations

X = "Input text. `None`, `NaN` and bytes are treated as empty text."
SPACY = "spaCy model `en_core_web_sm` (`python -m spacy download en_core_web_sm`)"
TB = "TextBlob corpora (`tp.download_nltk_packages()`)"
WN = "NLTK `wordnet` and `omw-1.4` (`tp.download_nltk_packages()`)"
PANDAS = "`pip install nlp-text-preprocessing[pandas]`"
VIZ = "`pip install nlp-text-preprocessing[viz]`"
SKL = "`pip install nlp-text-preprocessing[sklearn]`"

GROUPS: list[dict] = []


def group(gid: str, title: str, blurb: str):
    g = {"id": gid, "title": title, "blurb": blurb, "entries": []}
    GROUPS.append(g)

    def add(name, desc, code, params=(), returns=None, needs=None, sig=None, note=None, run=True, blocks=None, anchor=None):
        g["entries"].append(dict(name=name, desc=desc, code=code, params=list(params), returns=returns,
                                 needs=needs, sig=sig, note=note, run=run, blocks=blocks, anchor=anchor or name))
    return add


# --------------------------------------------------------------------------- setup
add = group("setup", "Setup & resources",
            "Check that models and corpora are installed, and fetch the ones that are missing. Nothing is downloaded when you import the package.")
add("download_nltk_packages", "One-time setup: downloads the NLTK data the package uses and, optionally, the spaCy model.",
    "tp.download_nltk_packages()\n",
    [("spacy_model", "Model to download as well. Pass `None` to skip spaCy."),
     ("include_sentiment_corpus", "Also fetch `movie_reviews`, only needed for `sentiment_analysis(method='naive_bayes')`.")],
    returns="None", run=False)
add("check_resources", "Reports which models and corpora are installed. Downloads nothing.",
    "status = tp.check_resources()\nprint(status[\"spacy_model\"])\nprint(all(status[\"nltk\"].values()))",
    [("include_optional", "Also check the optional `movie_reviews` corpus."),
     ("verbose", "Print a human-readable summary.")],
    returns="`dict` like `{'spacy_model': bool, 'nltk': {name: bool}}`")
add("get_spacy_nlp", "Loads a spaCy language model once and caches it (one cache entry per model name).",
    "nlp = tp.get_spacy_nlp()\nprint(nlp.meta[\"name\"])",
    [("model_name", "spaCy model package to load."),
     ("auto_download", "Download the model if it is missing. Defaults to `False`; set `NLP_TEXT_PREPROCESSING_AUTO_DOWNLOAD=1` to enable it globally.")],
    returns="spaCy `Language`", needs=SPACY)
add("get_stop_words", "Returns the English stop-word set (spaCy's list, loaded lazily).",
    "stops = tp.get_stop_words()\nprint(\"the\" in stops, \"python\" in stops)",
    returns="`frozenset[str]`")

# --------------------------------------------------------------------------- cleaning
add = group("cleaning", "Text cleaning",
            "Normalize case, whitespace, punctuation and word forms. Every function takes a string and returns a string.")
add("to_lower_case", "Converts text to lowercase.",
    "print(tp.to_lower_case(\"NLP Text Preprocessing v1.0\"))", [("x", X)], "`str`")
add("remove_extra_whitespace", "Collapses runs of spaces, tabs and newlines into one space and trims the ends.",
    "print(repr(tp.remove_extra_whitespace(\"  Too   many\\n\\tspaces  \")))", [("x", X)], "`str`")
add("normalize_whitespace_and_casing", "Lowercases and collapses whitespace in one call.",
    "print(tp.normalize_whitespace_and_casing(\"  Fresh   TEXT  \"))", [("x", X)], "`str`")
add("normalize_unicode_punctuation", "Replaces smart quotes, dashes, ellipses and non-breaking or zero-width spaces with ASCII equivalents.",
    "print(tp.normalize_unicode_punctuation(\"\\u201cSmart\\u201d quotes \\u2014 and\\u2026 dashes\"))", [("x", X)], "`str`")
add("remove_accented_chars", "Removes accents while keeping non-Latin scripts intact.",
    "print(tp.remove_accented_chars(\"Caf\\u00e9 na\\u00efve fa\\u00e7ade\"))", [("x", X)], "`str`")
add("remove_special_chars", "Removes punctuation and other special characters.",
    "print(tp.remove_special_chars(\"Hello, world! (100% sure) #nlp\"))", [("x", X)], "`str`")
add("remove_repeated_chars", "Shortens elongated words: three or more repeats of a letter become two.",
    "print(tp.remove_repeated_chars(\"soooo goooood\"))", [("x", X)], "`str`")
add("remove_numbers", "Removes standalone numbers such as `2026`, `3.14` and `1,000`. Digits inside words are kept.",
    "print(tp.remove_numbers(\"Order 66 shipped for 1,000 users in 2026 on python3\"))", [("x", X)], "`str`")
add("remove_currency_symbols", "Strips currency symbols (`$ € ₹ £ ¥ ₿` and more).",
    "print(tp.remove_currency_symbols(\"It costs $20 or \\u20ac18 or \\u20b91500\"))", [("x", X)], "`str`")
add("remove_stop_words", "Removes English stop words (case-insensitive and punctuation-aware). Negations are kept by default.",
    "text = \"I do not like this movie at all\"\nprint(tp.remove_stop_words(text))\nprint(tp.remove_stop_words(text, keep_negations=False))",
    [("x", X), ("keep_negations", "Keep `not`, `no`, `never` and friends. Removing them flips the meaning of a sentence.")], "`str`")
add("contraction_to_expansion", "Expands contractions and common slang.",
    "print(tp.contraction_to_expansion(\"I can't go, they're late and y'all won't wait\"))", [("x", X)], "`str`")
add("clean_text", "End-to-end classic cleaning: strips HTML, URLs and emails, lowercases, expands contractions, drops punctuation and lemmatizes.",
    "raw = \"<p>Check https://example.com! I'm LOVING these running shoes.</p>\"\nprint(tp.clean_text(raw))\nprint(tp.clean_text(raw, remove_stopwords=True))",
    [("text", "Input text."), ("remove_stopwords", "Also drop stop words (negations are kept).")], "`str`", needs=SPACY,
    note="For BERT/GPT-style models use [`light_clean`](#light_clean) instead. It keeps case and punctuation.")

# --------------------------------------------------------------------------- web & social
add = group("web-social", "Web, social & personal data",
            "Remove or inspect HTML, links, emails, mentions, emojis, phone numbers and other personal data.")
add("remove_html_tag", "Strips HTML tags and drops `<script>` and `<style>` content.",
    "print(tp.remove_html_tag(\"<div><b>Bold</b> text<script>alert(1)</script></div>\"))", [("x", X)], "`str`")
add("remove_urls", "Removes `http://`, `https://`, `ftp://` and `www.` links. Trailing sentence punctuation is kept.",
    "print(tp.remove_urls(\"Docs at https://example.com/a?b=1, or www.example.org.\"))", [("x", X)], "`str`")
add("remove_emails", "Removes email addresses.",
    "print(tp.remove_emails(\"Contact: jane.doe@example.com or support@site.io today\"))", [("x", X)], "`str`")
add("remove_mentions", "Removes `@user` mentions. Email addresses are left alone.",
    "print(tp.remove_mentions(\"Thanks @alice and @bob_99, mail me at me@x.com\"))", [("x", X)], "`str`")
add("remove_rt", "Removes the retweet prefix (`RT @user:`).",
    "print(tp.remove_rt(\"RT @nlp_news: New release is out\"))", [("x", X)], "`str`")
add("expand_hashtags", "Splits hashtags into words.",
    "print(tp.expand_hashtags(\"Loving #MachineLearning2024 and #NLPIsFun\"))", [("x", X)], "`str`")
add("remove_emojis", "Removes emojis, including flags, skin tones and joined (ZWJ) sequences.",
    "print(tp.remove_emojis(\"Great job \\U0001f44d\\U0001f3fd \\U0001f389 done\"))", [("x", X)], "`str`")
add("extract_emojis", "Returns the emojis found in the text.",
    "print(tp.extract_emojis(\"Love it \\u2764\\ufe0f \\U0001f602 \\U0001f680\"))", [("x", X)], "`list[str]`")
add("emoji_to_text", "Replaces emojis with their names.",
    "print(tp.emoji_to_text(\"Launch day \\U0001f680\"))", [("x", X)], "`str`")
add("remove_phone_numbers", "Removes phone numbers, including international formats.",
    "print(tp.remove_phone_numbers(\"Call +1 (555) 123-4567 or 020 7946 0958 now\"))", [("x", X)], "`str`")
add("mask_pii", "Redacts emails, card numbers, US Social Security numbers and phone numbers. Optionally redacts people's names.",
    "text = \"Mail jane@example.com, card 4111 1111 1111 1111, SSN 123-45-6789.\"\nprint(tp.mask_pii(text))\nprint(tp.mask_pii(text, token=\"<PII>\"))\nprint(tp.mask_pii(\"Ask Priya Sharma, 555-123-4567\", names=True))",
    [("x", X), ("token", "Replacement text for every match."),
     ("names", "Also redact person names with spaCy's entity recognizer. Statistical, so review the result when privacy matters.")],
    "`str`", needs=SPACY + " for `names=True`")

# --------------------------------------------------------------------------- statistics
add = group("statistics", "Counts & statistics",
            "Measure text: lengths, ratios, readability and per-document feature tables.")
add("word_count", "Total number of words.", "print(tp.word_count(\"Natural language processing is fun\"))", [("x", X)], "`int`")
add("char_count", "Number of characters, whitespace excluded.", "print(tp.char_count(\"Hello world\"))", [("x", X)], "`int`")
add("avg_word_len", "Average word length. `0.0` for empty text.", "print(tp.avg_word_len(\"Natural language processing\"))", [("x", X)], "`float`")
add("stop_words_count", "Number of stop words (case-insensitive, attached punctuation ignored).",
    "print(tp.stop_words_count(\"This is a test of the system\"))", [("x", X)], "`int`")
add("hashtags_count", "Number of `#hashtags`.", "print(tp.hashtags_count(\"Learning #python and #nlp today\"))", [("x", X)], "`int`")
add("mentions_count", "Number of `@mentions`. Email addresses are not counted.",
    "print(tp.mentions_count(\"Hi @alice, cc @bob and carol@example.com\"))", [("x", X)], "`int`")
add("numerics_count", "Number of standalone numeric tokens.", "print(tp.numerics_count(\"I bought 3 apples and 12 pears in 2026\"))", [("x", X)], "`int`")
add("upper_case_count", "Number of fully upper-case words of two or more letters (`I` and `A` are ignored).",
    "print(tp.upper_case_count(\"NASA and ESA signed the AGREEMENT. I agree\"))", [("x", X)], "`int`")
add("count_emails", "Number of email addresses.", "print(tp.count_emails(\"a@x.com, b@y.org and c\"))", [("x", X)], "`int`")
add("count_urls", "Number of URLs (`http://`, `https://`, `ftp://`, `www.`).", "print(tp.count_urls(\"See https://a.com and www.b.org\"))", [("x", X)], "`int`")
add("count_rt", "Number of retweets (`RT @user`).", "print(tp.count_rt(\"RT @a: hi\\nRT @b: yo\"))", [("x", X)], "`int`")
add("count_phone_numbers", "Number of phone numbers.", "print(tp.count_phone_numbers(\"Call 555-123-4567 or +44 20 7946 0958\"))", [("x", X)], "`int`")
add("sentence_count", "Number of sentences. Abbreviations such as `Dr.` and initials do not split a sentence.",
    "print(tp.sentence_count(\"Dr. Smith arrived. He said hello! Did you see?\"))", [("x", X)], "`int`")
add("avg_sentence_len", "Average sentence length in words.",
    "print(tp.avg_sentence_len(\"One two three. Four five.\"))", [("x", X)], "`float`")
add("punctuation_density", "Share of characters that are punctuation.",
    "print(tp.punctuation_density(\"Hi, there! Fine.\"))", [("x", X)], "`float`")
add("capital_ratio", "Share of words that are upper-case.", "print(tp.capital_ratio(\"NASA launched the ROCKET today\"))", [("x", X)], "`float`")
add("unique_word_ratio", "Unique words divided by total words (lexical diversity).",
    "print(tp.unique_word_ratio(\"the cat and the dog and the bird\"))", [("x", X)], "`float`")
add("readability_score", "Flesch Reading Ease. Higher is easier; 60–70 is plain English.",
    "print(tp.readability_score(\"The cat sat on the mat. It was happy.\"))", [("x", X)], "`float`")
add("readability_scores", "Five readability measures in one dictionary: Flesch Reading Ease, Flesch-Kincaid grade, Gunning Fog, Automated Readability Index and Coleman-Liau.",
    "scores = tp.readability_scores(\n    \"The quick brown fox jumps over the lazy dog. Simple words make text easy to read.\")\nfor name, value in scores.items():\n    print(f\"{name}: {value}\")",
    [("x", X)], "`dict[str, float]`", note="Syllables are estimated, so scores are approximate and unreliable for very short texts.")
add("text_stats", "Every summary statistic for one text, as a dictionary.",
    "stats = tp.text_stats(\"Hello @sam! Visit https://example.com #nlp 2026\")\nprint(stats)",
    [("x", X)], "`dict[str, Any]`")
add("text_stats_batch", "Computes `text_stats` for every row of a DataFrame column and returns a new DataFrame.",
    "import pandas as pd\nimport nlp_text_preprocessing as tp\n\ndf = pd.DataFrame({\"text\": [\"Hello world\", \"NLP is FUN! #ai\"]})\nstats = tp.text_stats_batch(df, \"text\")\nprint(stats[[\"word_count\", \"char_count\", \"hashtags_count\"]])",
    [("df", "A pandas DataFrame."), ("column", "Name of the column that holds the text.")], "`pandas.DataFrame`", needs=PANDAS)

# --------------------------------------------------------------------------- language
add = group("language", "Language analysis",
            "Lemmas, entities, parts of speech, keywords, n-grams, similarity, WordNet lookups and language detection. Most functions here use spaCy, NLTK or TextBlob.")
add("convert_to_base", "Lemmatizes only nouns and verbs. Other words are left as written.",
    "print(tp.convert_to_base(\"The children were running quickly\"))", [("x", X)], "`str`", needs=SPACY)
add("lemmatize", "Lemmatizes every token. Original spacing is kept.",
    "print(tp.lemmatize(\"The striped bats were hanging on their feet\"))", [("x", X)], "`str`", needs=SPACY)
add("singularize_words", "Converts plural nouns to singular. Spacing and punctuation are kept.",
    "print(tp.singularize_words(\"The cats chased two mice.\"))", [("x", X)], "`str`", needs=SPACY)
add("pluralize_words", "Converts singular common nouns to plural.",
    "print(tp.pluralize_words(\"The cat chased a mouse.\"))", [("x", X)], "`str`", needs=SPACY)
add("extract_entities", "Named entities as `(text, label)` pairs.",
    "print(tp.extract_entities(\"Apple opened an office in Berlin in March 2024.\"))", [("x", X)], "`list[tuple[str, str]]`", needs=SPACY)
add("extract_pos_tags", "Part-of-speech breakdown as `(text, pos, tag)` triples.",
    "print(tp.extract_pos_tags(\"Dogs bark loudly\"))", [("x", X)], "`list[tuple[str, str, str]]`", needs=SPACY)
add("get_dependency_tree", "Dependency parse as `(token, dependency, head)` triples.",
    "print(tp.get_dependency_tree(\"The cat sat on the mat\"))", [("x", X)], "`list[tuple[str, str, str]]`", needs=SPACY)
add("chunk_noun_phrases", "Noun phrases with exact character offsets (spaCy noun chunks).",
    "for chunk in tp.chunk_noun_phrases(\"The quick brown fox jumps over a lazy dog.\"):\n    print(chunk)", [("x", X)], "`list[dict]`", needs=SPACY)
add("get_noun_phrase", "Noun phrases as plain strings, using TextBlob.",
    "print(tp.get_noun_phrase(\"The quick brown fox jumps over the lazy dog\"))", [("x", X)], "`list[str]`", needs=TB)
add("n_grams", "Word n-grams as tuples. Punctuation is ignored.",
    "print(tp.n_grams(\"I love natural language processing\", n=2))\nprint(tp.n_grams(\"I love natural language processing\", n=3))",
    [("x", X), ("n", "Size of each n-gram (`2` = bigrams).")], "`list[tuple[str, ...]]`")
add("keyword_extraction", "The most frequent non-stop-word tokens of three or more letters, in any alphabet.",
    "text = \"Python makes text processing easy. Text processing with Python is powerful.\"\nprint(tp.keyword_extraction(text, top_n=3))",
    [("x", X), ("top_n", "How many keywords to return.")], "`list[str]`")
add("text_similarity", "Jaccard similarity of the two word sets, from `0.0` to `1.0`. Case and punctuation are ignored.",
    "print(tp.text_similarity(\"the cat sat on the mat\", \"the cat lay on the rug\"))",
    [("x1", "First text."), ("x2", "Second text.")], "`float`")
add("get_synonyms", "Sorted WordNet synonyms for a word (the word itself is excluded).",
    "print(tp.get_synonyms(\"happy\"))", [("word", "A single word.")], "`list[str]`", needs=WN)
add("get_antonyms", "Sorted WordNet antonyms for a word.",
    "print(tp.get_antonyms(\"happy\"))", [("word", "A single word.")], "`list[str]`", needs=WN)
add("correct_spelling", "Corrects spelling with TextBlob.",
    "print(tp.correct_spelling(\"I havv goood speling\"))", [("x", X)], "`str`", needs=TB)
add("detect_language", "Detects the language and returns an ISO 639-1 code.",
    "print(tp.detect_language(\"Bonjour tout le monde, comment allez-vous aujourd'hui ?\"))\nprint(tp.detect_language(\"This is clearly an English sentence.\"))",
    [("x", X)], "`str`")

# --------------------------------------------------------------------------- moderation
add = group("moderation", "Sentiment & moderation",
            "Sentiment, emotion, profanity, toxicity and spam signals. The moderation helpers are keyword baselines: they are fast and explainable, but they cannot read sarcasm or context. Use a trained model when the stakes are high.")
add("sentiment_analysis", "Classifies sentiment as `'pos'`, `'neg'` or `'neu'`.",
    "print(tp.sentiment_analysis(\"I absolutely love this product!\"))\nprint(tp.sentiment_analysis(\"This is terrible and I hate it.\"))\nprint(tp.sentiment_analysis(\"The meeting is at noon.\"))",
    [("x", X), ("method", "`'pattern'` (default, instant) or `'naive_bayes'` (legacy, needs the `movie_reviews` corpus, trains for about 30 s on first use and only answers `'pos'` or `'neg'`)."),
     ("threshold", "Pattern scores within ±`threshold` are `'neu'`.")], "`str`", needs=TB)
add("polarity_subjectivity", "TextBlob polarity (−1 to 1) and subjectivity (0 to 1).",
    "print(tp.polarity_subjectivity(\"The service was excellent but the food was cold.\"))", [("x", X)], "`dict[str, float]`", needs=TB)
add("emotion_detection", "Lexicon-based counts for joy, anger, sadness and fear. Negated words (`not happy`) are ignored.",
    "print(tp.emotion_detection(\"I am so happy and excited, but a little worried\"))", [("x", X)], "`dict`")
add("detect_profanity", "Returns `True` if the text contains profanity. Plurals and simple leetspeak (`sh1t`) are matched; `Hell's Kitchen` is not.",
    "print(tp.detect_profanity(\"What the hell is this\"))\nprint(tp.detect_profanity(\"What the hell is this\", include_mild=False))\nprint(tp.detect_profanity(\"Lovely weather today\"))",
    [("x", X), ("include_mild", "Include everyday words such as `damn` and `hell`."),
     ("extra_words", "Your own words to treat as profane."), ("allow_words", "Words to remove from the list.")], "`bool`")
add("censor_profanity", "Replaces each profane word with a mask character. Everything else is untouched.",
    "print(tp.censor_profanity(\"This is damn good, what the hell\"))\nprint(tp.censor_profanity(\"This is damn good\", mask_char=\"#\"))",
    [("x", X), ("include_mild", "Include everyday words."), ("extra_words", "Extra words to censor."),
     ("allow_words", "Words to leave alone."), ("mask_char", "Character used for the mask.")], "`str`")
add("detect_toxicity", "Baseline toxicity score from `0.0` to `1.0`. An insult aimed at someone scores `0.5` and hits accumulate towards `1.0`. `kill the process` and `I do not hate you` score `0`.",
    "print(tp.detect_toxicity(\"You are an idiot\"))\nprint(tp.detect_toxicity(\"Please kill the process\"))\nprint(tp.detect_toxicity(\"I do not hate you\"))", [("x", X)], "`float`")
add("toxicity_report", "Explains a toxicity score: the matches, their weights and the matches cancelled by a negation.",
    "report = tp.toxicity_report(\"You idiot, but I do not hate you\")\nprint(report)", [("x", X)], "`dict` with `score`, `matches`, `ignored`")
add("detect_spam_signals", "Detects shouting, punctuation runs, links and typical spam phrases. Short messages such as `OK` or `Hi!` are never flagged for caps alone.",
    "print(tp.detect_spam_signals(\"CLICK HERE!!! BUY NOW http://a.co http://b.co http://c.co\"))\nprint(tp.detect_spam_signals(\"OK\"))", [("x", X)], "`dict` including `spam_phrases` and `is_spam_candidate`")

# --------------------------------------------------------------------------- transformers
add = group("transformers", "Transformer-model preparation",
            "Light cleaning that keeps natural text for BERT and GPT style models, and helpers that enforce a token limit.")
add("light_clean", "Minimal cleaning for transformer models. Keeps case, punctuation and word forms; removes only noise.",
    "raw = \"<p>Great &amp; fast! Visit https://example.com or mail hi@x.com \\u2764\\ufe0f</p>\"\nprint(tp.light_clean(raw))\nprint(tp.light_clean(raw, urls=\"[URL]\", emails=\"[EMAIL]\", emojis=\"remove\"))",
    [("x", X), ("html", "Strip tags and decode entities such as `&amp;`."),
     ("urls", "`None` keeps URLs, `''` removes them, any other string replaces them."),
     ("emails", "Same options as `urls`."), ("mentions", "Same options as `urls`; defaults to keeping mentions."),
     ("emojis", "`None` keeps them, `'remove'` drops them, `'text'` turns them into `:name:`."),
     ("normalize", "Unicode normal form (`'NFKC'`), or `None` to skip."),
     ("keep_newlines", "Keep line breaks instead of one long line."), ("lowercase", "Lowercase the result for uncased models.")], "`str`")
add("truncate_text", "Cuts text to at most `max_tokens` tokens.",
    "text = \"one two three four five six seven eight\"\nprint(tp.truncate_text(text, max_tokens=5))",
    [("x", X), ("max_tokens", "Maximum number of tokens to keep."),
     ("tokenizer", "A HuggingFace tokenizer or any callable that returns a list of tokens. Without one, whitespace words are used as a rough stand-in. Leave a margin, because special tokens such as `[CLS]` count toward a model's limit.")], "`str`")
add("chunk_text", "Splits long text into chunks of at most `max_tokens` tokens, with optional overlap. Use it for documents longer than a model's input limit.",
    "text = \" \".join(f\"w{i}\" for i in range(1, 11))\nfor chunk in tp.chunk_text(text, max_tokens=4, overlap=1):\n    print(chunk)",
    [("x", X), ("max_tokens", "Maximum tokens per chunk."),
     ("overlap", "Tokens shared by consecutive chunks. Each chunk starts `max_tokens - overlap` tokens after the previous one."),
     ("tokenizer", "Same as in `truncate_text`.")], "`list[str]`")

# --------------------------------------------------------------------------- pipelines
add = group("pipelines", "Pipelines & extensions",
            "Chain steps into a reusable object, run it over strings, lists or pandas columns, save it as JSON and plug it into scikit-learn.")
add("Pipeline", "Chains cleaning steps. A step is a built-in function name, a registered name, a callable, or a `(name, kwargs)` pair. Every step except the last must return a string.",
    "pipe = tp.Pipeline([\n    \"remove_html_tag\",\n    \"remove_urls\",\n    \"to_lower_case\",\n    (\"remove_stop_words\", {\"keep_negations\": True}),\n    \"remove_extra_whitespace\",\n])\nprint(pipe)\nprint(len(pipe))\nprint(pipe.run(\"<p>This is NOT a test. Read https://example.com</p>\"))",
    [("steps", "List of steps. Typos raise an error when the pipeline is built, not halfway through a run.")],
    "`Pipeline`", sig="Pipeline(steps=None)")
add("Pipeline.default", "A ready-made pipeline: strip HTML, URLs and emails, lowercase, expand contractions, remove special characters and extra whitespace.",
    "pipe = tp.Pipeline.default()\nprint(pipe.run(\"<b>Fresh   TEXT!</b> It's great, isn't it?\"))", returns="`Pipeline`", sig="Pipeline.default()")
add("Pipeline.add_step", "Appends a step and returns the pipeline, so calls can be chained.",
    "pipe = tp.Pipeline().add_step(\"to_lower_case\").add_step(\"remove_extra_whitespace\")\nprint(pipe)\nprint(pipe.run(\"  HELLO   World \"))",
    [("step", "A step in any accepted form.")], "`Pipeline`", sig="Pipeline.add_step(step)")
add("Pipeline.run", "Runs the pipeline on one text. The last step may return anything, such as a float, list or dictionary.",
    "pipe = tp.Pipeline([\"remove_urls\", \"to_lower_case\", \"word_count\"])\nprint(pipe.run(\"Read https://example.com NOW please\"))",
    [("text", X)], "the last step's result", sig="Pipeline.run(text)")
add("Pipeline.run_batch", "Runs the pipeline over many texts. spaCy steps use `nlp.pipe`, so they are several times faster than calling the function per text.",
    "pipe = tp.Pipeline([\"to_lower_case\", \"lemmatize\"])\nprint(pipe.run_batch([\"The Cats are running\", \"Dogs were barking\"]))",
    [("texts", "Any iterable of texts.")], "`list`", sig="Pipeline.run_batch(texts)")
add("Pipeline.run_series", "Runs the pipeline over a pandas Series and keeps its index and name.",
    "import pandas as pd\nimport nlp_text_preprocessing as tp\n\ns = pd.Series([\"<b>Hi</b> THERE\", \"Good   BYE\"], name=\"text\")\nprint(tp.Pipeline.default().run_series(s))",
    [("series", "A `pandas.Series` of texts.")], "`pandas.Series`", needs=PANDAS, sig="Pipeline.run_series(series)")
add("Pipeline.fit", "scikit-learn convention: validates the steps and returns `self`. The pipeline has nothing to learn.",
    "pipe = tp.Pipeline([\"to_lower_case\"]).fit()\nprint(type(pipe).__name__)", [("X", "Ignored."), ("y", "Ignored.")], "`Pipeline`", sig="Pipeline.fit(X=None, y=None)")
add("Pipeline.transform", "scikit-learn convention: same as `run_batch`.",
    "pipe = tp.Pipeline([\"to_lower_case\"])\nprint(pipe.transform([\"A\", \"B\"]))", [("X", "Iterable of texts.")], "`list`", sig="Pipeline.transform(X)")
add("Pipeline.fit_transform", "scikit-learn convention: `fit` then `transform`.",
    "pipe = tp.Pipeline([\"to_lower_case\"])\nprint(pipe.fit_transform([\"Hello\", \"WORLD\"]))", [("X", "Iterable of texts."), ("y", "Ignored.")], "`list`", sig="Pipeline.fit_transform(X, y=None)")
add("Pipeline.get_params", "Returns `{'steps': ...}`, so scikit-learn can clone and tune the pipeline.",
    "print(tp.Pipeline([\"to_lower_case\"]).get_params())", [("deep", "Accepted for compatibility.")], "`dict`", sig="Pipeline.get_params(deep=True)")
add("Pipeline.set_params", "Replaces the steps (the only parameter) and validates them.",
    "pipe = tp.Pipeline([\"to_lower_case\"])\npipe.set_params(steps=[\"remove_urls\"])\nprint(pipe)", [("steps", "New list of steps.")], "`Pipeline`", sig="Pipeline.set_params(**params)")
add("Pipeline.to_config", "Returns a JSON-serializable description of the steps. Custom callables must be registered with `@register_step` first.",
    "pipe = tp.Pipeline([\"to_lower_case\", (\"remove_stop_words\", {\"keep_negations\": False})])\nprint(pipe.to_config())",
    returns="`list`", sig="Pipeline.to_config()")
add("Pipeline.from_config", "Builds a pipeline from the list returned by `to_config`.",
    "config = [\"to_lower_case\", {\"step\": \"remove_stop_words\", \"args\": {\"keep_negations\": False}}]\nprint(tp.Pipeline.from_config(config))",
    [("config", "List of step names or `{'step': name, 'args': {...}}` dictionaries.")], "`Pipeline`", sig="Pipeline.from_config(config)")
add("Pipeline.save", "Writes the pipeline to a JSON file.",
    "import tempfile, os\nimport nlp_text_preprocessing as tp\n\npath = os.path.join(tempfile.mkdtemp(), \"pipeline.json\")\ntp.Pipeline([\"remove_urls\", \"to_lower_case\"]).save(path)\nprint(open(path).read())",
    [("path", "Destination file path.")], "`None`", sig="Pipeline.save(path)")
add("Pipeline.load", "Reads a pipeline saved with `save`.",
    "import tempfile, os\nimport nlp_text_preprocessing as tp\n\npath = os.path.join(tempfile.mkdtemp(), \"pipeline.json\")\ntp.Pipeline([\"remove_urls\", \"to_lower_case\"]).save(path)\nprint(tp.Pipeline.load(path))",
    [("path", "Path of a JSON file written by `save`.")], "`Pipeline`", sig="Pipeline.load(path)")
add("register_step", "Decorator that registers your own function as a named step. Registered names can be saved to JSON.",
    "@tp.register_step(\"shout\")\ndef shout(text):\n    return text.upper() + \"!\"\n\npipe = tp.Pipeline([\"remove_extra_whitespace\", \"shout\"])\nprint(pipe.run(\"hello    there\"))",
    [("name", "Name to use in pipelines.")], "the decorated function")
add("diff_report", "Compares texts before and after a pipeline run: totals, average lengths and how many texts changed.",
    "before = [\"<b>Hello</b>   WORLD\", \"Already clean\"]\nafter = tp.Pipeline.default().run_batch(before)\nprint(tp.diff_report(before, after))",
    [("before_list", "Original texts."), ("after_list", "Processed texts, in the same order.")], "`dict`")
add("extract_features", "Convenience wrapper: word statistics, noun phrases and sentiment of one text in a single dictionary.",
    "print(tp.extract_features(\"Hello world\"))", [("x", X)], "`dict`")
add("TextPreprocessor", "A scikit-learn transformer that runs a `Pipeline` inside `sklearn.pipeline`. Import it from the package; it loads lazily so scikit-learn stays optional.",
    "from sklearn.feature_extraction.text import TfidfVectorizer\nfrom sklearn.linear_model import LogisticRegression\nfrom sklearn.pipeline import make_pipeline\nimport nlp_text_preprocessing as tp\n\nmodel = make_pipeline(\n    tp.TextPreprocessor([\"remove_html_tag\", \"to_lower_case\", \"remove_special_chars\"]),\n    TfidfVectorizer(),\n    LogisticRegression(),\n)\ntexts = [\"<b>Great</b> movie!\", \"Terrible film...\", \"Loved this great film\", \"Awful acting, terrible plot\"]\nmodel.fit(texts, [1, 0, 1, 0])\nprint(model.predict([\"A great movie\", \"Terrible!\"]))",
    [("steps", "Same format as `Pipeline`. Defaults to `Pipeline.default()` steps.")], "transformer", needs=SKL, sig="TextPreprocessor(steps=None)")

# --------------------------------------------------------------------------- viz
add = group("visualization", "Visualization", "Plot the most frequent words.")
add("get_wordcloud", "Builds a word cloud and optionally saves or shows it.",
    "cloud = tp.get_wordcloud(\n    \"python nlp text python data text python model\",\n    save_path=\"cloud.png\",\n    show=False,\n)\nprint(type(cloud).__name__)",
    [("x", X), ("save_path", "Write the image to this path."), ("show", "Display it with matplotlib.")], "`WordCloud`", needs=VIZ)

# --------------------------------------------------------------------------- CLI
add = group("cli", "Command line",
            "The `nlp-prep` command (or `python -m nlp_text_preprocessing`) cleans text files, CSV columns and standard input without writing Python.")
add("nlp-prep clean", "Cleans a `.txt` file (one document per line), a CSV column or standard input (`-`).",
    "", [("input", "File path, or `-` for standard input."), ("-o, --output", "Output file. Default: standard output."),
         ("-c, --column", "CSV column that holds the text (required for `.csv` input)."),
         ("--output-column", "CSV column to write to. Default `<column>_clean`; use the same name to overwrite."),
         ("-m, --mode", "`light` (default) keeps case and punctuation for transformer models; `standard` lowercases, drops punctuation and lemmatizes."),
         ("--lowercase", "Light mode: lowercase the text."), ("--url-token TEXT", "Light mode: replace URLs with TEXT."),
         ("--email-token TEXT", "Light mode: replace emails with TEXT."), ("--stopwords", "Standard mode: also remove stop words."),
         ("--steps a,b,c", "Comma-separated step names. Overrides `--mode`."), ("--pipeline FILE", "JSON file written by `Pipeline.save`. Overrides `--mode`.")],
    "cleaned text", sig="nlp-prep clean INPUT [options]", anchor="nlp-prep-clean",
    blocks=[
        ("Terminal", "echo \"<b>Hello   WORLD</b> https://example.com\" | nlp-prep clean -", ["clean", "-"], "<b>Hello   WORLD</b> https://example.com"),
        ("Terminal", "echo \"<b>Hello   WORLD</b> https://example.com\" | nlp-prep clean - --mode standard", ["clean", "-", "--mode", "standard"], "<b>Hello   WORLD</b> https://example.com"),
        ("Terminal", "echo \"Visit https://example.com NOW\" | nlp-prep clean - --steps remove_urls,to_lower_case", ["clean", "-", "--steps", "remove_urls,to_lower_case"], "Visit https://example.com NOW"),
        ("Terminal", "nlp-prep clean reviews.csv --column review --output-column review_clean -o cleaned.csv", None, None),
    ])
add("nlp-prep resources", "Shows which NLTK data and spaCy model are installed. Add `--download` to fetch what is missing.",
    "", [("--download", "Download whatever is missing.")], "exit code `0` when everything is installed", sig="nlp-prep resources [--download]",
    anchor="nlp-prep-resources",
    blocks=[("Terminal", "nlp-prep resources", ["resources"], None)])
