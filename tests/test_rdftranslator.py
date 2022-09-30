import pytest
from rdftranslate import RDFTranslator
import pprint
from rdflib import URIRef, Literal

testFileName = "tests/test.json"

@pytest.fixture(scope="function")
def translator1():
    return RDFTranslator(testFileName, outFileFormat="ttl")


def test__set_inFileFormat(translator1):
    assert translator1.inFileFormat == "json-ld"  # set from filename ext
    translator1._set_inFileFormat("ttl")
    assert translator1.inFileFormat == "turtle"
    translator1._set_inFileFormat("N3") # should be case insensitive
    assert translator1.inFileFormat == "n3"
    translator1.inFileName = "test"  # so that nothing set from file ext
    with pytest.raises(ValueError) as e:
        translator1._set_inFileFormat("rfd")
    assert (
        str(e.value)
        == "File format rfd does not correspond to a known serialization format."
    )
    with pytest.raises(ValueError) as e:
        translator1._set_inFileFormat(None)
    assert (
        str(e.value)
        == "No input file format or file extension provided. Cannot set input file format."
    )
    translator1.inFileName = "test.rfd"  # unknown file extension
    with pytest.raises(ValueError) as e:
        translator1._set_inFileFormat(None)
    assert (
        str(e.value)
        == "File extension rfd does not correspond to a known serialization format."
    )


def test__set_outFileFormat(translator1):
    assert translator1.outFileFormat == "turtle"  # format set in fixture
    translator1._set_outFileFormat("N3")
    assert translator1.outFileFormat == "n3"
    with pytest.raises(ValueError) as e:
        translator1._set_outFileFormat("rfd")
    assert (
        str(e.value)
        == "File format rfd does not correspond to a known serialization format."
    )
    translator1.outFileName = "test.json"
    translator1._set_outFileFormat(None)
    assert translator1.outFileFormat == "json-ld"  # from outFileName
    translator1.outFileName = "test.rfd"
    with pytest.raises(ValueError) as e:
        translator1._set_outFileFormat(None)
    assert (
        str(e.value)
        == "File extension rfd does not correspond to a known serialization format."
    )
    translator1.outFileName = None
    translator1._set_outFileFormat(None)
    assert translator1.outFileFormat == "turtle"  # default


def test_init(translator1):
    assert len(translator1.g) == 0
    assert translator1.inFileName == testFileName
    assert translator1.outFileName == None
    assert translator1.inFileFormat == "json-ld"
    assert translator1.outFileFormat == "turtle"

def test_read_write_graph(translator1):
    t = translator1
    with pytest.raises(ValueError) as e:
        t.write_graph()
    assert (
        str(e.value) == "Trying to write graph when no graph is stored."
    )
    t.read_graph()
    assert len(t.g) == 9
    s = URIRef('http://example.org/library/the-republic')
    p = URIRef('http://purl.org/dc/elements/1.1/title')
    o = Literal('The Republic')
    assert ((s, p, o)) in t.g
    t.write_graph()
    assert False
