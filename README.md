# nlp-text-preprocessing documentation

Developer documentation for the Python package by Uditya Narayan Tiwari. This edition covers version 0.5.1.

[Read the documentation](https://udityamerit.github.io/NLP-Text-Processing-Package-Documentation/) · [Python package](https://pypi.org/project/nlp-text-preprocessing/) · [Package source](https://github.com/udityamerit/Text-Processing-Package-For-Natural-Language-Processing)

## Start here

| Page | What you can do |
| --- | --- |
| [Overview](index.html) | Install the library, run the quick start and see what each function family covers. |
| [Installation](installation.html) | Create an environment on Windows, macOS, Linux or Conda, choose extras, and prepare spaCy and NLTK resources. |
| [User guide](guide.html) | Recipes for pipelines, pandas, batch processing, custom steps, saving, scikit-learn, transformer models, PII masking, moderation and the `nlp-prep` command. |
| [API reference](api.html) | Every public function, class and CLI command with parameters, return types and a runnable example. Each entry has a permanent link. |

## Try the package

```sh
python -m pip install nlp-text-preprocessing
```

```python
import nlp_text_preprocessing as tp

print(tp.Pipeline.default().run("<b>Fresh   TEXT!</b>"))
# fresh text
```

## How the site is built

`api.html`, `guide.html`, `installation.html`, `index.html` and `search-index.js` are **generated**. Do not edit them by hand.

| File | Role |
| --- | --- |
| `tools/api_data.py` | Descriptions, parameters and examples for every API entry |
| `tools/pages.py` | Overview, installation and user guide content |
| `tools/layout.py` | Page shell, sidebar, code blocks and tables |
| `tools/build_docs.py` | Runs every example against the installed package and writes the pages |

The build executes each example, so the output shown on the site is real. It also fails if a name in `nlp_text_preprocessing.__all__` has no entry. To rebuild, install the package with its extras and the spaCy and NLTK resources, then run this from the repository root:

```sh
python -m pip install "nlp-text-preprocessing[all]"
python -c "import nlp_text_preprocessing as tp; tp.download_nltk_packages()"
python tools/build_docs.py
```

Pass `--api-only` to regenerate only `api.html` and the search index. Styles live in `index.css` and interactions (theme, search, copy buttons, tabs) in `app.js`.

## Preview the site

Run the following command from this directory and open [the local documentation](http://localhost:8000/).

```sh
python -m http.server 8000
```

## Publish

In the repository settings, open **Pages → Build and deployment** and select **GitHub Actions**. The [Pages workflow](.github/workflows/static.yml) deploys the site on pushes to `main` and supports manual runs.

The Python package uses the [MIT license](https://github.com/udityamerit/Text-Processing-Package-For-Natural-Language-Processing/blob/main/LICENSE).
