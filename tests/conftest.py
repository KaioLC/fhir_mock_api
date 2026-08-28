import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services.state_store import state_store


@pytest.fixture
def client():
    """Retorna uma instância de TestClient para simular chamadas HTTP."""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_state():
    """Reseta o estado em memória antes de cada teste para garantir isolamento."""
    state_store.tasks.clear()
    yield
