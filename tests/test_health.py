def test_health_check_returns_200(client):
    """Valida se o endpoint GET /health responde com sucesso e status ok."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "service" in data
