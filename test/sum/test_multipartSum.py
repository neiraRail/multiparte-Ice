from src.sum.MultipartSum import MultipartSum
from src.comms.MockComms import MockComms

def test_suma_correcta():
    id = 3
    n = 4
    mockComms = MockComms(id, n)
    handler = MultipartSum(id, mockComms)
    result = handler.sumar(13)
    assert result == 13
    



