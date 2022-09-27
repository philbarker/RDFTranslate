import pytest
from rdftranslate import RDFTranslator

@pytest.fixture(scope="function")
def translator1():
    return(RDFTranslator("test.json", outFileFormat="ttl"))

def test__set_inFileFormat(translator1):
    assert translator1.inFileFormat == "json"  # set from filename ext
    translator1._set_inFileFormat("ttl")
    assert translator1.inFileFormat == "ttl"
    translator1._set_inFileFormat("N3")
    assert translator1.inFileFormat == "n3"
    translator1.inFileName = "test" # so that nothing set from file ext
    with pytest.raises(ValueError) as e:
        translator1._set_inFileFormat("rfd")
    assert str(e.value) == "File format rfd does not correspond to a known serialization format."
    with pytest.raises(ValueError) as e:
        translator1._set_inFileFormat(None)
    assert str(e.value) == "No input file format or file extension provided. Cannot set input file format."
    translator1.inFileName = "test.rfd" # unknown file extension
    with pytest.raises(ValueError) as e:
        translator1._set_inFileFormat(None)
    assert str(e.value) == "File extension rfd does not correspond to a known serialization format."

def test__set_outFileFormat(translator1):
    assert translator1.outFileFormat == "ttl" # from format set in fixture
    translator1._set_outFileFormat("N3")
    assert translator1.outFileFormat == "n3"
    with pytest.raises(ValueError) as e:
        translator1._set_outFileFormat("rfd")
    assert str(e.value) == "File format rfd does not correspond to a known serialization format."
    translator1.outFileName = "test.json"
    translator1._set_outFileFormat(None)
    assert translator1.outFileFormat == "json" # from outFileName
    translator1.outFileName = "test.rfd"
    with pytest.raises(ValueError) as e:
        translator1._set_outFileFormat(None)
    assert str(e.value) == "File extension rfd does not correspond to a known serialization format."
    translator1.outFileName = None
    translator1._set_outFileFormat(None)
    assert translator1.outFileFormat == "ttl" # default


def test_init(translator1):
    assert translator1.inFileName == "test.json"
    assert translator1.outFileName == None
    assert translator1.inFileFormat == "json"
    assert translator1.outFileFormat == "ttl"
