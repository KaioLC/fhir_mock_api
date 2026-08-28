def test_list_devices(client):
    """Valida se GET /fhir/Device lista todos os robôs pré-cadastrados."""
    response = client.get("/fhir/Device")
    assert response.status_code == 200
    devices = response.json()
    assert isinstance(devices, list)
    assert len(devices) >= 2

    device_ids = [d["id"] for d in devices]
    assert "MOCK-ROBOT-01" in device_ids


def test_get_device_success(client):
    """Valida se GET /fhir/Device/{id} retorna a telemetria correta do robô."""
    response = client.get("/fhir/Device/MOCK-ROBOT-01")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "MOCK-ROBOT-01"
    assert data["resourceType"] == "Device"
    assert data["status"] == "online"
    assert data["battery"] == 95


def test_get_device_not_found(client):
    """Valida se GET /fhir/Device/{id} retorna 404 para ID inexistente."""
    response = client.get("/fhir/Device/ROBOT-INEXISTENTE")
    assert response.status_code == 404
