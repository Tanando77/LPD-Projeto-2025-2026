This repository is a LaTeX project (report/dissertation) using a local class and `biblatex`/`biber`.

**Big Picture**
- **Main file:** `01-main-document.tex` — assembles front matter (`parte-inicial/`), chapters (`capitulos/`), bibliography (`03-bibliography.bib`) and uses `ipbeja-format.cls`.
- **Class:** `ipbeja-format.cls` — sets `biblatex` with `backend=biber`, minted for code listings, and document options (`PT`, `alphabetic`, `apa`). Check this file when changing global layout or bibliography style.
- **Chapters & assets:** content lives in `capitulos/`; figures in `figuras/`; logos in `logos/`; code examples in `listagens/`.

**Build / Toolchain (explicit)**
- The project expects `pdflatex` (MiKTeX on Windows) and `biber` for bibliography. The class loads `minted`, so a syntax highlighter (Pygments) and `-shell-escape` are required.
- Recommended (automated) command — runs full build, biber and reruns as needed:
  - `latexmk -pdf -pdflatex="pdflatex -interaction=nonstopmode -shell-escape" 01-main-document.tex`
- Manual sequence (if `latexmk` not available):
  - `pdflatex -interaction=nonstopmode -shell-escape 01-main-document.tex`
  - `biber 01-main-document`
  - `pdflatex -interaction=nonstopmode -shell-escape 01-main-document.tex`
  - `pdflatex -interaction=nonstopmode -shell-escape 01-main-document.tex`
- Notes: ensure `biber` is on PATH; install Pygments (`pip install Pygments`) for `minted` to work.

**Project-specific conventions**
- Metadata and title/author: edit `02-info-to-fill.tex` (fields like `\TITULO`, `\NOMEALUNO`, `\DATA`).
- Add chapters by creating `capitulos/capituloN.tex` and adding `\input{capitulos/capituloN}` into `01-main-document.tex`.
- Bibliography: `03-bibliography.bib` is the single bib resource; `ipbeja-format.cls` selects style via class options (`alphabetic` or `apa`).
- Code listings: prefer `minted` (used via `\begin{listing}` or `\begin{minted}`); examples are in `listagens/` (e.g., `quicksort.java`, `quicksort.python`). Keep long code in `listagens/` and reference or `\input` them.

**When editing the class or packages**
- If you change `ipbeja-format.cls`, re-run a full build including `biber` and multiple `pdflatex` runs. Class changes may require clearing auxiliary files (`.aux`, `.bbl`, `.fdb_latexmk`) to avoid stale state.

**Debugging tips**
- If minted code doesn't appear or build fails: confirm `-shell-escape` is enabled and Pygments is installed.
- If citations are missing or `\cite` entries empty: run `biber` (not `bibtex`) and re-run `pdflatex` twice.
- Use the `.log` and `.blg` files produced in the root for detailed errors.

**Files to check first when asked to change behavior**
- `01-main-document.tex` — document assembly and overall flow.
- `ipbeja-format.cls` — global styles, bibliography backend, minted config.
- `02-info-to-fill.tex` — metadata and front-matter content.
- `capitulos/` — chapter contents and structure.
- `03-bibliography.bib` — bibliographic entries.

If anything above is unclear or you want the file formatted differently, tell me which sections to expand or adjust.
