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
        "businessStatus": {
            "text": "Navegando no corredor em direção ao quarto 304",
        }
    }
    patch_res = client.patch(f"/fhir/Task/{task_id}", json=patch_payload)
    assert patch_res.status_code == 200

    updated = patch_res.json()
    assert updated["status"] == "in-progress"
    assert (
        updated["businessStatus"]["text"]
        == "Navegando no corredor em direção ao quarto 304"
    )
    assert updated["priority"] == "routine"


# ==============================================================================
# NOVOS TESTES DE INTEROPERABILIDADE, HARD BREAKS E CANONICAL PATCH
# ==============================================================================


def test_create_task_minimal_defaults(client):
    """Valida criação de Task com payload vazio utilizando todos os defaults."""
    response = client.post("/fhir/Task", json={})
    assert response.status_code == 201
    data = response.json()
    assert data["resourceType"] == "Task"
    assert data["id"].startswith("task-")
    assert data["status"] == "requested"
    assert data["priority"] == "routine"
    assert data["intent"] == "order"
    assert response.headers["Location"] == f"/fhir/Task/{data['id']}"


def test_create_task_complete_fields(client):
    """Valida criação de Task com todos os campos preenchidos."""
    payload = {
        "id": "task-complete-99",
        "status": "requested",
        "intent": "order",
        "priority": "stat",
        "description": "Transporte de Bolsa de Sangue O-",
        "focus": {"code": "BLOOD-O-NEG", "units": 2},
        "owner": {"reference": "Device/MOCK-ROBOT-01", "display": "Robô Mock 01"},
        "location": {"reference": "Location/room-304", "display": "Leito 304 - UTI"},
        "businessStatus": {"text": "Aguardando liberação de transporte"},
    }
    response = client.post("/fhir/Task", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == "task-complete-99"
    assert data["priority"] == "stat"
    assert data["owner"]["reference"] == "Device/MOCK-ROBOT-01"
    assert data["location"]["reference"] == "Location/room-304"
    assert data["businessStatus"]["text"] == "Aguardando liberação de transporte"


def test_hard_break_invalid_status_enum(client):
    """Hard Break: Status inválido fora do enum TaskStatus deve retornar 422."""
    response = client.post("/fhir/Task", json={"status": "status-invalido-xyz"})
    assert response.status_code == 422


def test_hard_break_invalid_priority_enum(client):
    """Hard Break: Prioridade inválida fora do enum TaskPriority deve retornar 422."""
    response = client.post("/fhir/Task", json={"priority": "super-maxima-urgencia"})
    assert response.status_code == 422


def test_hard_break_invalid_reference_type(client):
    """Hard Break: Envio de string simples onde se espera objeto Reference deve retornar 422."""
    response = client.post("/fhir/Task", json={"owner": "Device/MOCK-ROBOT-01"})
    assert response.status_code == 422


def test_list_tasks_empty_state(client):
    """Valida retorno de lista vazia quando nenhuma task foi cadastrada."""
    response = client.get("/fhir/Task")
    assert response.status_code == 200
    assert response.json() == []


def test_list_tasks_combined_filters(client):
    """Valida filtro combinado por status e owner."""
    client.post(
        "/fhir/Task",
        json={"status": "requested", "owner": {"reference": "Device/ROBOT-01"}},
    )
    client.post(
        "/fhir/Task",
        json={"status": "in-progress", "owner": {"reference": "Device/ROBOT-01"}},
    )
    client.post(
        "/fhir/Task",
        json={"status": "in-progress", "owner": {"reference": "Device/ROBOT-02"}},
    )

    # Filtro apenas por owner case-insensitive
    res_owner = client.get("/fhir/Task", params={"owner": "device/robot-01"})
    assert len(res_owner.json()) == 2

    # Filtro apenas por status
    res_status = client.get("/fhir/Task", params={"status": "in-progress"})
    assert len(res_status.json()) == 2

    # Filtro combinado
    res_comb = client.get(
        "/fhir/Task", params={"status": "in-progress", "owner": "Device/ROBOT-01"}
    )
    assert len(res_comb.json()) == 1


def test_canonical_patch_single_field_priority(client):
    """Valida PATCH canônico na raiz /{task_id} alterando apenas a prioridade."""
    post_res = client.post(
        "/fhir/Task", json={"priority": "routine", "description": "Desc original"}
    )
    task_id = post_res.json()["id"]

    patch_res = client.patch(f"/fhir/Task/{task_id}", json={"priority": "stat"})
    assert patch_res.status_code == 200
    data = patch_res.json()
    assert data["priority"] == "stat"
    assert data["description"] == "Desc original"


def test_canonical_patch_status_and_business_status(client):
    """Valida PATCH canônico alterando status e telemetria businessStatus."""
    post_res = client.post("/fhir/Task", json={"priority": "routine"})
    task_id = post_res.json()["id"]

    patch_payload = {
        "status": "in-progress",
        "businessStatus": {"text": "Navegando no corredor em direção ao quarto 304"},
    }
    patch_res = client.patch(f"/fhir/Task/{task_id}", json=patch_payload)
    assert patch_res.status_code == 200
    data = patch_res.json()
    assert data["status"] == "in-progress"
    assert (
        data["businessStatus"]["text"]
        == "Navegando no corredor em direção ao quarto 304"
    )
    assert data["priority"] == "routine"


def test_canonical_patch_reassign_owner_and_location(client):
    """Valida PATCH canônico alterando o robô responsável e o local de destino."""
    post_res = client.post(
        "/fhir/Task", json={"owner": {"reference": "Device/ROBOT-01"}}
    )
    task_id = post_res.json()["id"]

    patch_payload = {
        "owner": {"reference": "Device/ROBOT-02", "display": "Robô Backup"},
        "location": {
            "reference": "Location/lab-central",
            "display": "Laboratório Central",
        },
    }
    patch_res = client.patch(f"/fhir/Task/{task_id}", json=patch_payload)
    assert patch_res.status_code == 200
    data = patch_res.json()
    assert data["owner"]["reference"] == "Device/ROBOT-02"
    assert data["location"]["reference"] == "Location/lab-central"


def test_canonical_patch_focus_payload(client):
    """Valida PATCH canônico atualizando a carga transportada."""
    post_res = client.post("/fhir/Task", json={})
    task_id = post_res.json()["id"]

    patch_res = client.patch(
        f"/fhir/Task/{task_id}",
        json={"focus": {"item": "Medicamento X", "lote": "L12345"}},
    )
    assert patch_res.status_code == 200
    assert patch_res.json()["focus"]["item"] == "Medicamento X"


def test_canonical_patch_empty_payload_preserves_task(client):
    """Valida que PATCH com payload vazio mantém os dados intactos."""
    post_res = client.post(
        "/fhir/Task", json={"priority": "urgent", "status": "requested"}
    )
    task_id = post_res.json()["id"]

    patch_res = client.patch(f"/fhir/Task/{task_id}", json={})
    assert patch_res.status_code == 200
    data = patch_res.json()
    assert data["priority"] == "urgent"
    assert data["status"] == "requested"


def test_canonical_patch_invalid_enum_returns_422(client):
    """Valida que PATCH com status inválido retorna 422."""
    post_res = client.post("/fhir/Task", json={})
    task_id = post_res.json()["id"]

    patch_res = client.patch(f"/fhir/Task/{task_id}", json={"status": "dormindo"})
    assert patch_res.status_code == 422


def test_canonical_patch_nonexistent_task_returns_404(client):
    """Valida que PATCH em ID inexistente retorna 404."""
    res = client.patch("/fhir/Task/task-nao-existe-999", json={"status": "completed"})
    assert res.status_code == 404


def test_full_robot_mission_lifecycle_e2e(client):
    """
    Simula todo o ciclo de vida da missão:
    1. Criação da ordem (requested)
    2. Atribuição e aceite do robô (accepted)
    3. Trânsito e telemetria (in-progress)
    4. Conclusão da entrega (completed)
    5. Consulta final GET
    """
    # 1. Hospital cria tarefa
    create_res = client.post(
        "/fhir/Task",
        json={
            "description": "Entrega de antibiótico",
            "priority": "urgent",
            "location": {"reference": "Location/quarto-102"},
        },
    )
    assert create_res.status_code == 201
    task_id = create_res.json()["id"]

    # 2. Robô aceita missão
    accept_res = client.patch(
        f"/fhir/Task/{task_id}",
        json={
            "status": "accepted",
            "owner": {
                "reference": "Device/ROBOT-HOSPITALAR-01",
                "display": "Tug Robot 01",
            },
        },
    )
    assert accept_res.status_code == 200
    assert accept_res.json()["status"] == "accepted"

    # 3. Em trânsito com telemetria
    moving_res = client.patch(
        f"/fhir/Task/{task_id}",
        json={
            "status": "in-progress",
            "businessStatus": {"text": "Cruzando o corredor leste rumo ao elevador A"},
        },
    )
    assert moving_res.status_code == 200
    assert moving_res.json()["status"] == "in-progress"
    assert (
        moving_res.json()["businessStatus"]["text"]
        == "Cruzando o corredor leste rumo ao elevador A"
    )

    # 4. Conclusão
    finish_res = client.patch(
        f"/fhir/Task/{task_id}",
        json={
            "status": "completed",
            "businessStatus": {
                "text": "Compartimento destravado e material entregue à enfermagem"
            },
        },
    )
    assert finish_res.status_code == 200
    assert finish_res.json()["status"] == "completed"

    # 5. Consulta final consolidada
    final_get = client.get(f"/fhir/Task/{task_id}")
    assert final_get.status_code == 200
    final_data = final_get.json()
    assert final_data["status"] == "completed"
    assert final_data["owner"]["reference"] == "Device/ROBOT-HOSPITALAR-01"
    assert final_data["location"]["reference"] == "Location/quarto-102"
    assert final_data["priority"] == "urgent"
