LATEX=pdflatex
LATEXOPT=--shell-escape
NONSTOP=--interaction=nonstopmode

LATEXMK=latexmk
LATEXMKOPT=-pdf
#CONTINUOUS=-pvc		# Used to update pdf in viewer
CONTINUOUS=


MAIN=test
SOURCES=$(MAIN).tex Makefile preamble.tex
#FIGURES := $(shell find data/*.pdf diag/*.pdf -type f)
FIGURES=


all: show


show: $(MAIN).pdf
	vupdf $(MAIN).pdf


.refresh:
	touch .refresh


$(MAIN).pdf: $(MAIN).tex .refresh $(SOURCES) $(FIGURES) preamble.fmt
		$(LATEXMK) $(LATEXMKOPT) $(CONTINUOUS) -pdflatex="$(LATEX) $(LATEXOPT) $(NONSTOP) %O %S" $(MAIN)


# Compile the preamble
preamble.fmt: preamble.tex
		pdftex -ini -jobname=preamble "&pdflatex preamble.tex\dump"


# Generate eps files from pdf files using 'pdftops'
AbidHMujtabaFig00.eps: diag/circuit-resistors.pdf
	pdftops -eps $< $@

AbidHMujtabaFig01a.eps: data/bar_binary.pdf
	pdftops -eps $< $@

AbidHMujtabaFig01b.eps: data/bar_descriptive.pdf
	pdftops -eps $< $@

AbidHMujtabaFig01c.eps: data/bar_computational.pdf
	pdftops -eps $< $@

AbidHMujtabaFig01d.eps: data/bar_total.pdf
	pdftops -eps $< $@

AbidHMujtabaFig02a.eps: data/scatter_bin_des.pdf
	pdftops -eps $< $@

AbidHMujtabaFig02b.eps: data/scatter_com_des.pdf
	pdftops -eps $< $@

AbidHMujtabaFig02c.eps: data/scatter_com_bin.pdf
	pdftops -eps $< $@

AbidHMujtabaFig03.eps: diag/venn.pdf
	pdftops -eps $< $@


force:
		touch .refresh
		rm $(MAIN).pdf
		$(LATEXMK) $(LATEXMKOPT) $(CONTINUOUS) \
			-pdflatex="$(LATEX) $(LATEXOPT) %O %S" $(MAIN)

clean:
		$(LATEXMK) -C $(MAIN)
		rm -f $(MAIN).pdfsync
		rm -rf *~ *.tmp
		rm -f *.fmt *.bbl *.blg *.aux *.end *.fls *.log *.out *.fdb_latexmk
		rm -f *.eps *-converted-to.pdf
		rm -f *.bib

once:
		$(LATEXMK) $(LATEXMKOPT) -pdflatex="$(LATEX) $(LATEXOPT) %O %S" $(MAIN)

debug:
		$(LATEX) $(LATEXOPT) $(MAIN)

cover: cover-letter.pdf
	vupdf cover-letter.pdf

cover-letter.pdf: cover-letter.md Makefile
	pandoc -V papersize:letter -V geometry:margin=1in -V fontsize=12pt -o cover-letter.pdf cover-letter.md

.PHONY: clean force once all show cover
# Source: https://drewsilcock.co.uk/using-make-and-latexmk
