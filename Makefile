SOURCES=$(wildcard [0-9]*.md)
CSS=epub.css
TARGET=propaganda.epub

.PHONY: clean all

PANDOC_OPTS=--epub-title-page=false

all: $(TARGET)

$(TARGET): $(SOURCES) epub.css cover.jpg
	pandoc $(PANDOC_OPTS) --css $(CSS) -o $@ $(SOURCES)

clean:
	rm -f $(TARGET)

