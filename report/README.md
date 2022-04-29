Our detailed findings in a write-up, intended to be generated and served off of GitHub Pages.

Unfortunately, the limitations of (GitHub) Markdown and our interactive needs do not allow us to simply render Markdown for our entire report, so we wrote the report in `Report.md` and compiled it to `index.html` to get served automatically at `/report`. We also manually substitute some generated code-blocks from various sources (listed below) into `index.html`, delimited by comments. There's also a bug with the TOC generation where the incorrect number of hyphens are added into the hyperlinks, so hyphens are manually added afterwards (example: `<h1 id="1-introduction">` is correctly linked by `<a href="#1-introduction">`, but `<h2 id="1-1-background">` is incorrectly linked by `<a href="#11-background">`.)

The report consists of various non-interactive SVGs and interactive HTML snippets generated from the notebooks, using different methods:

| Asset                                | Source                                | Method                              |
| ------------------------------------ | ------------------------------------- | ----------------------------------- |
| `completion-rates.html`              | `ExploratoryDataAnalysis.ipynb`       | `altair.save()` with `altair-saver` |
| `substance-rates.html`               | `Visual_Testing.ipynb`                | `altair.save()` with `altair-saver` |
| `most-common-primary-substance.html` | `Visual_Testing.ipynb`                | `altair.save()` with `altair-saver` |
| `violin2016.svg`                     | `Visual_Testing.ipynb`                | `pyplot.savefig()`                  |
| `violin2017.svg`                     | `Visual_Testing.ipynb`                | `pyplot.savefig()`                  |
| `violin2018.svg`                     | `Visual_Testing.ipynb`                | `pyplot.savefig()`                  |
| `violin2019.svg`                     | `Visual_Testing.ipynb`                | `pyplot.savefig()`                  |
| `diff-in-diff.svg`                   | `01_Diff_in_Diff.ipynb`               | `seaborn.clustermap(...).savefig()` |
| `cluster-sse-before-pca.svg`         | `03_States_Clustering_Attempts.ipynb` | `pyplot.savefig()`                  |
| `cluster-sse-after-pca.svg`          | `03_States_Clustering_Attempts.ipynb` | `pyplot.savefig()`                  |
| `pca-cluster.html`                   | `03_States_Clustering_Attempts.ipynb` | `altair.save()` with `altair-saver` |
| `p-t.html`                           | `01_Diff_in_Diff.ipynb`               | `altair.save()` with `altair-saver` |
| `roc.svg`                            | `02_Classification.ipynb`             | `pyplot.savefig()`                  |

The table of contents and enumeration is generated using [Markdown All in One](https://marketplace.visualstudio.com/items?itemName=yzhang.markdown-all-in-one), which supports the `<!-- omit in toc -->` syntax for ignoring enumeration/TOC for some headers.

We also manually added a carousel to flip between multiple SVGs, representing the different violin plots over the years. This was used to show that there were few differences year-over-year.
