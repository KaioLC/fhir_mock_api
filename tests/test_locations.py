def test_list_locations(client):
    """Valida se GET /fhir/Location lista todos os locais pré-cadastrados."""
    response = client.get("/fhir/Location")
    assert response.status_code == 200
    locations = response.json()
    assert isinstance(locations, list)
    assert len(locations) >= 4

    location_ids = [loc["id"] for loc in locations]
    assert "pharmacy-center" in location_ids
    assert "room-304" in location_ids


def test_get_location_success(client):
    """Valida se GET /fhir/Location/{id} retorna os detalhes corretos de um local."""
    response = client.get("/fhir/Location/room-304")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "room-304"
    assert data["resourceType"] == "Location"
    assert data["floor"] == "3rd floor"


def test_get_location_not_found(client):
    """Valida se GET /fhir/Location/{id} retorna 404 para ID inexistente."""
    response = client.get("/fhir/Location/local-inexistente")
    assert response.status_code == 404
