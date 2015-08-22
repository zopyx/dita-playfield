all: convert pdf

convert:
	bin/python parse.py out_sequence/index.html
	bin/python parse.py out_hierarchy/index.html
	bin/python parse.py out_taskbook/index.html

pdf:
	pdfreactor -s pdfreactor.css -a bookmarks out_sequence/out.html out_sequence/out.pdf
	pdfreactor -s pdfreactor.css -a bookmarks out_hierarchy/out.html out_hierarchy/out.pdf
	pdfreactor -s pdfreactor.css -a bookmarks out_taskbook/out.html out_taskbook/out.pdf
