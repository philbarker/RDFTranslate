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
    translator1._set_inFileFormat("N3")  # should be case insensitive
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
    assert len(translator1.ds) == 0
    assert translator1.inFileName == testFileName
    assert translator1.outFileName == None
    assert translator1.inFileFormat == "json-ld"
    assert translator1.outFileFormat == "turtle"


def test_read_write_graph(translator1):
    t = translator1
    with pytest.raises(ValueError) as e:
        t.write_graph()
    assert str(e.value) == "Trying to write graph when no graph is stored."
    t.read_graph()
    assert len(t.ds) == 9
    s = URIRef("http://example.org/library/the-republic")
    p = URIRef("http://purl.org/dc/elements/1.1/title")
    o = Literal("The Republic")
    assert ((s, p, o)) in t.ds
    v = t.write_graph()
    assert v[:46] == "@prefix dc: <http://purl.org/dc/elements/1.1/>"
    t.outFileName = "tests/test_out.ttl"  # write to nowhere
    v = t.write_graph()
    assert v == "tests/test_out.ttl"


@pytest.fixture(scope="function")
def translator2():
    return RDFTranslator("tests/namedGraph.json", outFileFormat="ttl")


def test_read_write_graph(translator2):
    t = translator2
    with pytest.raises(ValueError) as e:
        t.write_graph()
    assert str(e.value) == "Trying to write graph when no graph is stored."
    t.read_graph()
    assert len(t.ds) == 5
    s = URIRef("https://example.edu/g/001")
    p = URIRef("https://purl.org/ctdl/terms/lifeCycleStatusType")
    o = URIRef("https://purl.org/ctdl/vocabs/lifeCycle/Developing")
    assert ((s, p, o)) in t.ds
    s = URIRef("https://example.edu/r/002")
    p = URIRef("https://purl.org/ctdl/terms/lifeCycleStatusType")
    o = URIRef("https://purl.org/ctdl/vocabs/lifeCycle/Active")
    g = URIRef("https://example.edu/g/001")
    assert ((s, p, o, g)) in t.ds
    v = t.write_graph()
    assert "# Graph: https://example.edu/g/001" in v
    assert (
        "<https://example.edu/g/001> ceterms:lifeCycleStatusType lifeCycle:Developing ."
        in v
    )
    assert "    ceterms:lifeCycleStatusType lifeCycle:Active ;" in v
    t.outFileName = "tests/namedGraph_Out.ttl"
    v = t.write_graph()
    assert v == "tests/namedGraph_Out.ttl"
