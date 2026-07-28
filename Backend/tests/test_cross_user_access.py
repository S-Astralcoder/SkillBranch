from datetime import UTC, datetime, timedelta
from uuid import UUID, uuid4

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.database import engine
from app.models import Project, Skill, Task, User
from tests.test_valid_use_of_endpoint import (
    client,
    create_user_with_resources,
)


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


def assert_user_only_lists_own_data(
    headers: dict[str, str],
    own_tree: dict[str, dict],
) -> None:
    skills = request(headers, "GET", "/skill/skills").json()
    assert {skill["id"] for skill in skills} == {own_tree["skill"]["id"]}

    tasks = request(
        headers,
        "GET",
        "/task/near_deadline_tasks",
    ).json()
    assert {task["id"] for task in tasks} == {own_tree["task"]["id"]}


def assert_user_cannot_access_tree(
    headers: dict[str, str],
    other_tree: dict[str, dict],
    unique_value: str,
) -> None:
    skill_id = other_tree["skill"]["id"]
    project_id = other_tree["project"]["id"]
    task_id = other_tree["task"]["id"]
    deadline = (datetime.now(UTC) + timedelta(days=2)).isoformat()

    forbidden_requests = [
        ("GET", f"/skill/skill/{skill_id}", None),
        ("GET", f"/project/projects/{skill_id}", None),
        ("GET", f"/project/project/{skill_id}/{project_id}", None),
        ("GET", f"/task/tasks/{skill_id}/{project_id}", None),
        (
            "GET",
            f"/task/task/{skill_id}/{project_id}/{task_id}",
            None,
        ),
        (
            "PUT",
            "/skill/update_skill",
            {
                "id": skill_id,
                "name": f"unauthorized-skill-{unique_value}",
                "description": "Must not be updated",
            },
        ),
        ("DELETE", "/skill/delete_skill", {"id": skill_id}),
        (
            "POST",
            "/project/create_project",
            {
                "skill_id": skill_id,
                "project_name": f"unauthorized-project-{unique_value}",
                "description": "Must not be created",
            },
        ),
        (
            "PUT",
            "/project/update_project",
            {
                "skill_id": skill_id,
                "project_id": project_id,
                "project_name": f"unauthorized-project-{unique_value}",
                "description": "Must not be updated",
            },
        ),
        (
            "DELETE",
            "/project/delete_project",
            {
                "skill_id": skill_id,
                "project_id": project_id,
            },
        ),
        (
            "POST",
            "/task/create_task",
            {
                "skill_id": skill_id,
                "project_id": project_id,
                "task_name": f"unauthorized-task-{unique_value}",
                "description": "Must not be created",
                "deadline": deadline,
            },
        ),
        (
            "PUT",
            "/task/update_task",
            {
                "skill_id": skill_id,
                "project_id": project_id,
                "task_id": task_id,
                "task_name": f"unauthorized-task-{unique_value}",
                "description": "Must not be updated",
                "deadline": deadline,
            },
        ),
        (
            "PATCH",
            "/task/toggle_task",
            {
                "skill_id": skill_id,
                "project_id": project_id,
                "task_id": task_id,
                "toggle": True,
            },
        ),
        (
            "DELETE",
            "/task/delete_task",
            {
                "skill_id": skill_id,
                "project_id": project_id,
                "task_id": task_id,
            },
        ),
    ]

    for method, path, payload in forbidden_requests:
        request(
            headers,
            method,
            path,
            payload,
            expected_status=404,
        )


def assert_owner_still_has_tree(
    headers: dict[str, str],
    tree: dict[str, dict],
) -> None:
    skill_id = tree["skill"]["id"]
    project_id = tree["project"]["id"]
    task_id = tree["task"]["id"]

    assert (
        request(
            headers,
            "GET",
            f"/skill/skill/{skill_id}",
        ).json()["id"]
        == skill_id
    )
    assert (
        request(
            headers,
            "GET",
            f"/project/project/{skill_id}/{project_id}",
        ).json()["id"]
        == project_id
    )
    assert (
        request(
            headers,
            "GET",
            f"/task/task/{skill_id}/{project_id}/{task_id}",
        ).json()["id"]
        == task_id
    )


def cleanup_users_and_resources(
    users: list[dict[str, str]],
    resources: list[dict[str, dict]],
) -> None:
    task_ids = [UUID(resource["task"]["id"]) for resource in resources]
    project_ids = [UUID(resource["project"]["id"]) for resource in resources]
    skill_ids = [UUID(resource["skill"]["id"]) for resource in resources]
    emails = [user["email"] for user in users]

    with Session(engine) as session:
        session.execute(delete(Task).where(Task.id.in_(task_ids)))
        session.execute(delete(Project).where(Project.id.in_(project_ids)))
        session.execute(delete(Skill).where(Skill.id.in_(skill_ids)))
        database_users = session.scalars(
            select(User).where(User.email.in_(emails))
        ).all()
        for user in database_users:
            session.delete(user)
        session.commit()


def test_users_cannot_access_each_others_data():
    unique_value = uuid4().hex
    users: list[dict[str, str]] = []
    resources: list[dict[str, dict]] = []

    try:
        first_user, first_headers, first_resources = create_user_with_resources(
            f"first-{unique_value}",
            ["First"],
        )
        users.append(first_user)
        resources.extend(first_resources)

        second_user, second_headers, second_resources = create_user_with_resources(
            f"second-{unique_value}",
            ["Second"],
        )
        users.append(second_user)
        resources.extend(second_resources)

        first_tree = first_resources[0]
        second_tree = second_resources[0]

        assert_user_only_lists_own_data(first_headers, first_tree)
        assert_user_only_lists_own_data(second_headers, second_tree)

        assert_user_cannot_access_tree(
            first_headers,
            second_tree,
            f"first-{unique_value}",
        )
        assert_user_cannot_access_tree(
            second_headers,
            first_tree,
            f"second-{unique_value}",
        )

        assert_owner_still_has_tree(first_headers, first_tree)
        assert_owner_still_has_tree(second_headers, second_tree)
    finally:
        cleanup_users_and_resources(users, resources)
