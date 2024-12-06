#!/usr/bin/env python

import sys
import re
import xml.dom
from xml.dom import Node
from xml.dom.minidom import parse

chapter_names = {
    "I": "Chapter I: Organizing Chaos",
    "II": "Chapter II: The New Propaganda",
    "III": "Chapter III: The New Propagandists",
    "IV": "Chapter IV: Psychology of Public Relations",
    "V": "Chapter V: Business and the Public",
    "VI": "Chapter VI: Propaganda and Political Leadership",
    "VII": "Chapter VII: Women's Activities and Propaganda",
    "VIII": "Chapter VIII: Propaganda for Education",
    "IX": "Chapter IX: Propaganda in Social Service",
    "X": "Chapter X: Art and Science",
    "XI": "Chapter XI: The Mechanics of Propaganda",
}

def fix_ncx():
    filename = 'EPUB/toc.ncx'

    dom = parse(filename)

    for text_node in dom.getElementsByTagName("text"):
        #print(repr(text_node.firstChild.nodeValue))

        chapter_name = text_node.firstChild.nodeValue.strip()
        m = re.match(r'CHAPTER\s*([IXV]+)', chapter_name)

        if m is not None:
            chapter_roman = m.group(1)
            chapter_name = chapter_names[chapter_roman]
            text_node.firstChild.nodeValue = chapter_name
            #print(chapter_name)

    with open(filename, 'w') as fp:
        fp.write(dom.toxml('UTF-8').decode())

def extract_text(n):
    result = ''

    for c in n.childNodes:
        if c.nodeType == Node.TEXT_NODE or c.nodeType == Node.CDATA_SECTION_NODE:
            result += c.nodeValue
        else:
            result += extract_text(c)

    return result

def fix_nav():
    filename = 'EPUB/nav.xhtml'

    dom = parse(filename)

    toc_ol = None


    # Find the TOC <ol>
    for ol in dom.getElementsByTagName("ol"):
        cls = ol.getAttribute("class")
        if cls == "toc":
            toc_ol = ol
            break

    assert(toc_ol is not None)

    for a in toc_ol.getElementsByTagName("a"):
        chapter_name = extract_text(a)
        new_chapter_name = None

        #print(">>>" + chapter_name)
        m = re.match(r'CHAPTER\s*([XIV]+)', chapter_name)

        if m is not None:
            chapter_roman = m.group(1)
            new_chapter_name = chapter_names[chapter_roman]

        if new_chapter_name is not None:

            # Nuke old child nodes
            while len(a.childNodes) > 0:
                a.removeChild(a.firstChild)
            
            a.appendChild(dom.createTextNode(new_chapter_name))

    with open(filename, 'w') as fp:
        fp.write(dom.toxml('UTF-8').decode())

def main(argv):
    fix_ncx()
    fix_nav()

if __name__ == '__main__':
    sys.exit(main(sys.argv))
