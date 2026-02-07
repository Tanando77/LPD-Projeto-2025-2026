
% Latex style for final reports and dissertations (Instituto Politécnico de Beja)
\newcommand{\version}{Version 1.0, 2023/01/25}
% Author: João Paulo Barros, joao.barros@ipbeja.pt
% Com contribuições de Henrique Água-Doce, Nuno Mourinho e Raul Carvalho.
% Document adjustment
\LoadClass[11pt,a4paper]{memoir}
\RequirePackage[top=4cm, bottom=3cm, left=3.5cm, right=2.5cm]{geometry} 
\RequirePackage{ifthen}
\RequirePackage[T1]{fontenc}
\RequirePackage[utf8]{inputenc}
\RequirePackage[table]{xcolor}
\RequirePackage{float}
\RequirePackage[hypcap=false]{caption}
\RequirePackage{listings}
\RequirePackage{xcolor}
\RequirePackage{float}
%https://tex.stackexchange.com/questions/12428/code-spanning-over-two-pages-with-minted-inside-listing-with-caption
\newenvironment{code}{\captionsetup{type=listing}}{}

\DeclareOption{PT}{\newcommand{\PT}{PT}}
\DeclareOption{alphabetic}{\newcommand{\BIBSTYLE}{alphabetic}}
\DeclareOption{apa}{\newcommand{\BIBSTYLE}{apa}}
\DeclareOption*{\newcommand{\BIBSTYLE}{apa}} 

\ProcessOptions


\DeclareRobustCommand{\pten}[2]{%
	 \ifthenelse{\isundefined{\PT}}
	{#2} % then 
	{#1} % else
}

%\newcommand{\BIBSTYLE}{apa}



\pten{\RequirePackage[portuguese]{babel}
\babelprovide[import]{portuguese}
}
{\RequirePackage[english]{babel}}

%hifens de quebra de linha ‡ portuguesa
\defineshorthand{"-}{\nobreak\hskip0pt\discretionary{-}{-}{-}\nobreak\hskip0pt}

\usepackage{url}
%\newcommand{\url}[1]{\href{#1}{\texttt{#1}}}
%https://www.overleaf.com/learn/latex/biblatex_citation_styles
%https://ctan.org/pkg/biblatex-apa?lang=en
%veja também o manual da package biblatex em https://ftp.eq.uc.pt/software/TeX/macros/latex/contrib/biblatex/doc/biblatex.pdf
%e para o estilo apa, %https://ctan.org/pkg/biblatex-apa?lang=en
\usepackage[
backref=true,
backend=biber,
style=\BIBSTYLE,
%style=alphabetic, %section 3.3.2 no manual da package biblatex
]{biblatex}
\renewcommand{\cite}[1]{\parencite{#1}}

\usepackage{listings}
\usepackage{xcolor}
\usepackage{float}

\lstset{
    language=Python,
    basicstyle=\ttfamily\small,
    breaklines=true,
    breakatwhitespace=true,
    frame=single
}

\pten{
\DefineBibliographyStrings{portuges}{%
  backrefpage = {citado na página},% originally "cited on page"
  backrefpages = {citado nas páginas},% originally "cited on pages"
}
}{}

\addbibresource{03-bibliography.bib}

\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{ipbeja-format} [
2013/04/18, 2013/10/10, 2014/07/03, 2020/10/14, 2020/11/02, 2020/11/20, 
2021/12/01, 
\version, author: João Paulo Barros (joao.barros@ipbeja.pt)
Style for IPBeja Academic work 
]

% graphics, symbols and hyperlink packages
\RequirePackage{graphicx}
\RequirePackage{amssymb}
\RequirePackage{lipsum}

%https://tex.stackexchange.com/questions/103141/set-global-options-for-inputmintedRelatório de projeto final
\RequirePackage[newfloat=true]{minted}
\setminted{
%frame=lines,
%frame=single,
%framesep=2mm,
%baselinestretch=1.5,
fontsize=\footnotesize,
linenos
}
%https://tex.stackexchange.com/questions/292402/how-to-let-minted-break-across-pages-but-keep-the-caption-together-with-the-end
\RequirePackage{tcolorbox}
\tcbuselibrary{breakable}
\definecolor{light-gray}{cmyk}{0.0, 0.0, 0.0, .04}

\RequirePackage{datetime2}
\RequirePackage{datetime2-calc}

% Paragraph ajustement
%\setlength{\parindent}{0mm}
%\setlength{\parskip}{3mm}
\renewcommand{\baselinestretch}{1.2} % 1.5 for double-space

\DeclareOption*{\PassOptionsToClass{\CurrentOption}{memoir}}
\ProcessOptions

% Capa e folha de rosto
\DeclareRobustCommand{\folhacapa}{
	\thispagestyle{empty}
	\newpage
	%\noindent{\includegraphics[width=2.85cm]{logos/logo-ipbeja} 
	%\hfill 
	\vspace*{-1cm}	
    \parbox[c]{0.65\textwidth}{
        \begin{center}
    	\includegraphics[width=9cm]{logos/logo-ipbeja} \\
	    	%\vspace*{1cm}
        \end{center}
    }
	\begin{center}
		{{\footnotesize \textbf \ESCOLA}}\\
		\vspace*{.1cm}
		{{\footnotesize \textbf \CURSO}}\\
		\vspace{1.0cm}
		{\LARGE\textbf \TITULO}\\
		\vspace{.5cm}
		{\large\textbf \SUBTITULO}\\
		\vspace{1.5cm}
		{\Large\textit \NOMEALUNO}\\
		\vfill
		\LOCAL, \DATA
	\end{center}
	\newpage\hspace{1mm}
}

\DeclareRobustCommand{\folharosto}{
	\thispagestyle{empty}
	\newpage
	\thispagestyle{empty}
	\begin{center}
		\vspace*{0.2cm}
		{{\footnotesize\textbf{INSTITUTO POLITÉCNICO DE BEJA}}}\\
	    \vspace*{.1cm}
		{{\footnotesize\textbf {\ESCOLA}}}\\
		\vspace*{.1cm}
		{{\footnotesize\textbf{{\CURSO}}}}\\
		\vspace{1cm}
		{\LARGE\textbf \TITULO}\\
		\vspace{.5cm}
		{\large\textbf \SUBTITULO}\\
		\vspace{1.0cm}
		{\normalsize \NOMEALUNO}\\
		\vspace{2cm}
		\pten{Responsável da Disciplina}{Advisor}:\\
		\vspace{.2cm}
		\ifthenelse{\isundefined{\ORIENTADORENTIDADE}}
		{} % then vazio
		{%orientador estágio
			\vspace{.2cm}
			\ORIENTADORENTIDADE\\
		}
		%um orientador do curso
		\ORIENTADORIPBEJAA, IPBeja\\
        \ifthenelse{\isundefined{\ORIENTADORIPBEJAB}}
		{} % then vazio
		{% mais um orientador do curso
			\vspace{.2cm}
			\ORIENTADORIPBEJAB, IPBeja\\
		}
		\vspace{2cm}
		\ifthenelse{\isundefined{\DECLARACAO}}
		{} %then vazio
		{\DECLARACAO} 
		\vfill
		\small \the\year
	\end{center}
	\thispagestyle{empty}
	\cleardoublepage
         \pagestyle{ruled}
}

\DeclareRobustCommand{\paginadedicatoria}{
	\@blankoddpage
	\thispagestyle{empty}
	\begin{flushright}
	\ \\
	\vspace{5cm}
	\textit \DEDICATORIA
	\end{flushright}
	\@blankoddpage
}

% Tables of contents, figues and tables

\newcommand{\indicegeral}{
\cleardoublepage
\tableofcontents
}

\newcommand{\indicedefiguras}{
\cleardoublepage
\listoffigures
}

\newcommand{\indicedetabelas}{
\cleardoublepage
\listoftables
}

\pten{
\addto\captionsportuges{%
\SetupFloatingEnvironment{listing}{listname=Lista de Listagens}}

\addto\captionsportuges{%
    \SetupFloatingEnvironment{listing}{name=Listagem}
}

\newcommand{\indicedelistagens}{
\cleardoublepage
\listoflistings
}

\addto\captionsportuges{%
  \renewcommand{\contentsname}%
    {\'{I}ndice}%
}

\addto\captionsportuges{%
  \renewcommand{\listfigurename}%
    {\'{I}ndice de Figuras}%
}

\addto\captionsportuges{%
  \renewcommand{\listlistingsname}%
    {\'{I}ndice de Listagens}%
}

\addto\captionsportuges{%
  \renewcommand{\listtablename}%
    {\'{I}ndice de Tabelas}%
}

\addto\captionsportuges{%
  \renewcommand{\appendixpagename}%
    {Apêndices}%
}

\addto\captionsportuges{%
  \renewcommand{\appendixname}%
    {Apêndice}%
}

\addto\captionsportuges{%
  \renewcommand{\appendixtocname}%
    {Apêndices}%
}
} % para português
{} % nada a fazer para inglês


\DeclareRobustCommand{\apendices}{%
\appendixpage%
\appendix 
\renewcommand{\thechapter}{\Roman{chapter}}%
}

\DeclareRobustCommand{\anexos}{%
\pten{
\renewcommand{\appendixpagename}{Anexos}
\renewcommand{\appendixname}{Anexo}
\renewcommand{\appendixtocname}{Anexos}
}{
\renewcommand{\appendixpagename}{Annexes}
\renewcommand{\appendixname}{Annex}
\renewcommand{\appendixtocname}{Annexes}
}

\appendixpage
\appendix \renewcommand{\thechapter}{\Roman{chapter}}
}

\pten{
\DeclareRobustCommand{\agradecimentos}{%
\cleardoublepage
\vspace*{1cm}
\addcontentsline{toc}{chapter}{Agradecimentos}
\thispagestyle{plain}
{\LARGE \textit{Agradecimentos}}
}
}
{
\DeclareRobustCommand{\agradecimentos}{%
\cleardoublepage
\vspace*{1cm}
\addcontentsline{toc}{chapter}{Acknowledgements}
\thispagestyle{plain}
{\LARGE \textit{acknowledgements}}
}
}

%\addto\captionsportuges{%
  %\renewcommand{\bibname}%
 %   {Referências bibliográficas}%
%}

\maxtocdepth{subsection}
%http://tex.stackexchange.com/questions/3327/turn-on-subsection-numbering-in-memoir
\setsecnumdepth{subsection}
\newcommand{\rodape}[1]{\footnote{#1}}
% para palavras em inglês ou outras línguas diferentes do português
\newcommand{\ing}[1]{\textit{#1}}
\captionnamefont{\bfseries}


% configuracao da package listings para listagens de código
% http://www.ctan.org/pkg/listings
% http://tex.stackexchange.com/questions/24528/having-problems-with-listings-and-utf-8-can-it-be-fixed
% mais informação em https://en.wikibooks.org/wiki/LaTeX/Source_Code_Listings


% directoria para as figuras
\graphicspath{{figuras/}}

\newcommand{\Java}{Java\textsuperscript{TM}}
\usepackage{csquotes}
\usepackage{longtable}

\AtBeginDocument{
    \addto\captionsportuges{
        \SetupFloatingEnvironment{listing}{listname=Índice de Listagens}
        \SetupFloatingEnvironment{listing}{name=Listagem}
    }
}

\endinput