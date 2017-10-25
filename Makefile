LATEX=pdflatex
LATEXOPT=--shell-escape --interaction=nonstopmode -halt-on-error

LATEXMK=latexmk
LATEXMKOPT=-pdf
#CONTINUOUS=-pvc		# Used to update pdf in viewer
CONTINUOUS=


MAIN=test
SOURCES=$(MAIN).tex Makefile preamble.tex
# Since the -svg.tex files are created from the .svg files in diag/svg/ we use a shell command to analyze the contents of diag/svg/ and construct a list of -svg.tex files that will be created from them. This allows us to declare these as dependencies of the main tex file.
# To use tikz externalization we make any built pdf files dependencies of the main file.
FIGURES := $(shell find diag/*.tex -type f) $(shell find build/*.pdf -type f) $(shell find diag/svg/*.svg -type f | cut -d'/' -f3- | sed 's/.svg/-svg.tex/' | sed 's:^:diag/:')


all: show


show: $(MAIN).pdf
	vupdf $(MAIN).pdf


.refresh:
	touch .refresh


$(MAIN).pdf: $(MAIN).tex .refresh $(SOURCES) $(FIGURES) preamble.fmt
		$(LATEXMK) $(LATEXMKOPT) $(CONTINUOUS) -pdflatex="$(LATEX) $(LATEXOPT) %O %S" $(MAIN)


# Compile the preamble
preamble.fmt: preamble.tex quiz.sty abid-base.sty test-base.sty
		pdftex -ini -jobname=preamble "&pdflatex preamble.tex\dump"


# Convert svg images to tex files using svg2tikz
diag/%-svg.tex: diag/svg/%.svg
		svg2tikz --figonly -o $@ $<


# Explicit dependence of the built pdf files on the tex files. If the tex file is change we delete the corresponding pdf to force latex to build it again
build/%.pdf: diag/%.tex
		rm -f $@
		rm -f $(MAIN).pdf


clean:
		$(LATEXMK) -C $(MAIN)
		rm -f $(MAIN).pdfsync
		rm -rf *~ *.tmp
		rm -f *.fmt *.bbl *.blg *.aux *.end *.fls *.log *.out *.fdb_latexmk
		rm -f *.eps *-converted-to.pdf
		rm -f *.bib


debug:
		$(LATEX) $(LATEXOPT) $(MAIN)


.PHONY: clean all show
# Source: https://drewsilcock.co.uk/using-make-and-latexmk
