def test_create_task_success(client):
    """Valida a criação de uma FHIR Task e o cabeçalho RESTful Location."""
    payload = {
        "priority": "urgent",
        "description": "Transporte de Bolsa de Sangue O-",
        "owner": {
            "reference": "Device/MOCK-ROBOT-01",
            "display": "Robô Mock 01",
        },
        "location": {
            "reference": "Location/room-304",
            "display": "Room 304 - B",
        },
    }

    response = client.post("/fhir/Task", json=payload)
    assert response.status_code == 201

    created_task = response.json()
    task_id = created_task["id"]

    assert response.headers["Location"] == f"/fhir/Task/{task_id}"
    assert created_task["resourceType"] == "Task"
    assert created_task["status"] == "requested"
    assert created_task["priority"] == "urgent"
    assert created_task["owner"]["reference"] == "Device/MOCK-ROBOT-01"


def test_get_task_by_id(client):
    """Valida a recuperação de uma tarefa previamente criada."""
    # Cria a tarefa
    post_res = client.post("/fhir/Task", json={"priority": "routine"})
    assert post_res.status_code == 201
    task_id = post_res.json()["id"]

    # Consulta a tarefa
    get_res = client.get(f"/fhir/Task/{task_id}")
    assert get_res.status_code == 200
    assert get_res.json()["id"] == task_id
    assert get_res.json()["status"] == "requested"


def test_get_nonexistent_task_returns_404(client):
    """Valida retorno 404 para consulta de tarefa não existente."""
    response = client.get("/fhir/Task/task-nao-existe")
    assert response.status_code == 404


def test_list_tasks_and_filter(client):
    """Valida a listagem geral e filtros por status e owner."""
    # Cria 2 tarefas
    client.post(
        "/fhir/Task",
        json={"priority": "routine", "owner": {"reference": "Device/MOCK-ROBOT-01"}},
    )
    client.post(
        "/fhir/Task",
        json={"priority": "stat", "owner": {"reference": "Device/MOCK-ROBOT-02"}},
    )

    # Lista todas
    all_tasks = client.get("/fhir/Task").json()
    assert len(all_tasks) == 2

    # Filtro por owner
    filtered_tasks = client.get(
        "/fhir/Task", params={"owner": "Device/MOCK-ROBOT-01"}
    ).json()
    assert len(filtered_tasks) == 1
    assert filtered_tasks[0]["owner"]["reference"] == "Device/MOCK-ROBOT-01"


def test_patch_task_status(client):
    """Valida atualização de status da missão via PATCH."""
    post_res = client.post("/fhir/Task", json={"priority": "routine"})
    task_id = post_res.json()["id"]

    patch_payload = {
        "status": "in-progress",
        "businessStatus_txt": "Navegando no corredor em direção ao quarto 304",
    }
    patch_res = client.patch(f"/fhir/Task/{task_id}/status", json=patch_payload)
    assert patch_res.status_code == 200

    updated = patch_res.json()
    assert updated["status"] == "in-progress"
    assert (
        updated["businessStatus"]["text"]
        == "Navegando no corredor em direção ao quarto 304"
    )
