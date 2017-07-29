formats: vmdb2.en.html vmdb2.en.pdf
en_srcs = $(wildcard en/*)

all: $(formats)

vmdb2.en.html: $(en_srcs) vmdb2.css
	./format-html "$@" ${en_srcs}

vmdb2.en.pdf: $(srcs)
	./format-pdf "$@" ${en_srcs}
