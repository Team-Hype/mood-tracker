# backend/tests/unit/test_uuid_mixin.py
import pytest
from sqlalchemy.orm import MappedColumn
from app.db.models.mixins.index import UUIDMixin


def test_uuid_mixin_has_id():
    """Test that UUIDMixin provides id column."""
    assert hasattr(UUIDMixin, "id")
    assert isinstance(UUIDMixin.id, MappedColumn)





def test_uuid_mixin_id_exists():
    """Simple test that UUIDMixin has id attribute."""
    from sqlalchemy.orm import declarative_mixin
    
    @declarative_mixin
    class TestModel(UUIDMixin):
        pass
    
    assert hasattr(TestModel, "id")
    assert isinstance(TestModel.id, MappedColumn)