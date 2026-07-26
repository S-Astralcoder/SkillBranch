from datetime import UTC, datetime, timedelta
from uuid import UUID, uuid4

from fastapi.testclient import TestClient
from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.app import app
from app.database import engine
from app.models import Project, Skill, Task, User

client = TestClient(app=app)


def create_test_user(unique_value: str) -> dict[str, str]:
    return {
        "username": f"invalid-endpoint-user-{unique_value}",
        "email": f"invalid-endpoint-{unique_value}@example.com",
        "password": "test-password-1234",
    }


def signup_and_get_headers(test_user: dict[str, str]) -> dict[str, str]:
    signup_response = client.post("/user/signup", json=test_user)
    assert signup_response.status_code == 201
    return {"Authorization": f"Bearer {signup_response.json()['access_token']}"}


def request(
    headers: dict[str, str],
    method: str,
    path: str,
    json: dict | None = None,
    expected_status: int = 200,
):
    response = client.request(method, path, json=json, headers=headers)
    assert response.status_code == expected_status, response.json()
    return response


def create_tree(
    headers: dict[str, str],
    name: str,
    unique_value: str,
    created_ids: dict[str, list[UUID]],
) -> dict[str, dict]:
    skill = request(
        headers,
        "POST",
        "/skill/create_skill",
        {
            "name": f"{name}-skill-{unique_value}",
            "description": f"{name} skill",
        },
    ).json()
    created_ids["skills"].append(UUID(skill["id"]))

    project = request(
        headers,
        "POST",
        "/project/create_project",
        {
            "skill_id": skill["id"],
            "project_name": f"{name}-project-{unique_value}",
            "description": f"{name} project",
        },
    ).json()
    created_ids["projects"].append(UUID(project["id"]))

    task = request(
        headers,
        "POST",
        "/task/create_task",
        {
            "skill_id": skill["id"],
            "project_id": project["id"],
            "task_name": f"{name}-task-{unique_value}",
            "description": f"{name} task",
            "deadline": (datetime.now(UTC) + timedelta(days=1)).isoformat(),
        },
    ).json()
    created_ids["tasks"].append(UUID(task["id"]))

    return {"skill": skill, "project": project, "task": task}


def assert_malformed_ids_rejected(
    headers: dict[str, str],
    tree: dict[str, dict],
) -> None:
    malformed_requests = [
        ("GET", "/skill/skill/not-a-uuid", None),
        (
            "GET",
            f"/project/project/{tree['skill']['id']}/not-a-uuid",
            None,
        ),
        (
            "GET",
            (f"/task/task/{tree['skill']['id']}/{tree['project']['id']}/not-a-uuid"),
            None,
        ),
        ("PUT", "/skill/delete_skill", {"id": "not-a-uuid"}),
        (
            "DELETE",
            "/project/delete_project",
            {
                "skill_id": tree["skill"]["id"],
                "project_id": "not-a-uuid",
            },
        ),
        (
            "DELETE",
            "/task/delete_task",
            {
                "skill_id": tree["skill"]["id"],
                "project_id": tree["project"]["id"],
                "task_id": "not-a-uuid",
            },
        ),
    ]

    for method, path, payload in malformed_requests:
        request(headers, method, path, payload, expected_status=422)


def assert_nonexistent_ids_rejected(
    headers: dict[str, str],
    tree: dict[str, dict],
) -> None:
    nonexistent_id = str(uuid4())
    nonexistent_requests = [
        ("GET", f"/skill/skill/{nonexistent_id}"),
        (
            "GET",
            f"/project/project/{tree['skill']['id']}/{nonexistent_id}",
        ),
        (
            "GET",
            (
                f"/task/task/{tree['skill']['id']}/"
                f"{tree['project']['id']}/{nonexistent_id}"
            ),
        ),
    ]

    for method, path in nonexistent_requests:
        request(headers, method, path, expected_status=404)


def assert_cross_parent_access_rejected(
    headers: dict[str, str],
    first: dict[str, dict],
    second: dict[str, dict],
    unique_value: str,
) -> None:
    cross_parent_requests = [
        (
            "GET",
            (f"/project/project/{first['skill']['id']}/{second['project']['id']}"),
            None,
        ),
        (
            "GET",
            (f"/task/tasks/{first['skill']['id']}/{second['project']['id']}"),
            None,
        ),
        (
            "GET",
            (
                f"/task/task/{second['skill']['id']}/"
                f"{second['project']['id']}/{first['task']['id']}"
            ),
            None,
        ),
        (
            "PUT",
            "/project/update_project",
            {
                "skill_id": first["skill"]["id"],
                "project_id": second["project"]["id"],
                "project_name": f"cross-parent-project-{unique_value}",
                "description": "Must not be updated",
            },
        ),
        (
            "PATCH",
            "/task/toggle_task",
            {
                "skill_id": second["skill"]["id"],
                "project_id": second["project"]["id"],
                "task_id": first["task"]["id"],
                "toggle": True,
            },
        ),
        (
            "DELETE",
            "/task/delete_task",
            {
                "skill_id": second["skill"]["id"],
                "project_id": second["project"]["id"],
                "task_id": first["task"]["id"],
            },
        ),
    ]

    for method, path, payload in cross_parent_requests:
        request(headers, method, path, payload, expected_status=404)


def delete_project_and_assert_api_inaccessible(
    headers: dict[str, str],
    tree: dict[str, dict],
) -> None:
    request(
        headers,
        "DELETE",
        "/project/delete_project",
        {
            "skill_id": tree["skill"]["id"],
            "project_id": tree["project"]["id"],
        },
    )
    request(
        headers,
        "GET",
        (f"/project/project/{tree['skill']['id']}/{tree['project']['id']}"),
        expected_status=404,
    )
    request(
        headers,
        "GET",
        (
            f"/task/task/{tree['skill']['id']}/"
            f"{tree['project']['id']}/{tree['task']['id']}"
        ),
        expected_status=404,
    )


def delete_skill_and_assert_api_inaccessible(
    headers: dict[str, str],
    tree: dict[str, dict],
) -> None:
    request(
        headers,
        "PUT",
        "/skill/delete_skill",
        {"id": tree["skill"]["id"]},
    )
    request(
        headers,
        "GET",
        f"/skill/skill/{tree['skill']['id']}",
        expected_status=404,
    )
    request(
        headers,
        "GET",
        f"/project/projects/{tree['skill']['id']}",
        expected_status=404,
    )


def assert_dependent_database_rows_deleted(
    first: dict[str, dict],
    second: dict[str, dict],
) -> None:
    with Session(engine) as session:
        remaining_rows = {
            "first skill": session.get(Skill, UUID(first["skill"]["id"])) is not None,
            "first project": session.get(Project, UUID(first["project"]["id"]))
            is not None,
            "first task": session.get(Task, UUID(first["task"]["id"])) is not None,
            "second skill": session.get(Skill, UUID(second["skill"]["id"])) is not None,
            "second project": session.get(Project, UUID(second["project"]["id"]))
            is not None,
            "second task": session.get(Task, UUID(second["task"]["id"])) is not None,
        }

    assert remaining_rows == {
        "first skill": True,
        "first project": False,
        "first task": False,
        "second skill": False,
        "second project": False,
        "second task": False,
    }


def cleanup_test_resources(
    test_user: dict[str, str],
    created_ids: dict[str, list[UUID]],
) -> None:
    with Session(engine) as session:
        if created_ids["tasks"]:
            session.execute(delete(Task).where(Task.id.in_(created_ids["tasks"])))
        if created_ids["projects"]:
            session.execute(
                delete(Project).where(Project.id.in_(created_ids["projects"]))
            )
        if created_ids["skills"]:
            session.execute(delete(Skill).where(Skill.id.in_(created_ids["skills"])))
        user = session.scalar(select(User).where(User.email == test_user["email"]))
        if user is not None:
            session.delete(user)
        session.commit()


def test_invalid_ids_cross_parent_access_and_cascading_deletes():
    unique_value = uuid4().hex
    test_user = create_test_user(unique_value)
    created_ids: dict[str, list[UUID]] = {
        "skills": [],
        "projects": [],
        "tasks": [],
    }

    try:
        headers = signup_and_get_headers(test_user)
        first = create_tree(headers, "first", unique_value, created_ids)
        second = create_tree(headers, "second", unique_value, created_ids)

        assert_malformed_ids_rejected(headers, first)
        assert_nonexistent_ids_rejected(headers, first)
        assert_cross_parent_access_rejected(headers, first, second, unique_value)
        delete_project_and_assert_api_inaccessible(headers, first)
        delete_skill_and_assert_api_inaccessible(headers, second)
        assert_dependent_database_rows_deleted(first, second)
    finally:
        cleanup_test_resources(test_user, created_ids)
