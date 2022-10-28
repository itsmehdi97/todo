import pytest 

from domain import model


@pytest.fixture
def prop():
    prop = model.Prop(id=1, price=100, owner=1)
    
    return prop
