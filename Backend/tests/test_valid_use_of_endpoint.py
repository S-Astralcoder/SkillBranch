from datetime import UTC, datetime, timedelta
from uuid import uuid4

from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.app import app
from app.database import engine
from app.models import User

client = TestClient(app=app)


def create_user_with_resources(
    unique_value: str,
    resource_names: list[str],
) -> tuple[dict[str, str], dict[str, str], list[dict[str, dict]]]:
    test_user = {
        "username": f"endpoint-user-{unique_value}",
        "email": f"endpoint-{unique_value}@example.com",
        "password": "test-password-1234",
    }
    signup_response = client.post("/user/signup", json=test_user)
    assert signup_response.status_code == 201
    headers = {"Authorization": f"Bearer {signup_response.json()['access_token']}"}

    def request(method: str, path: str, json: dict | None = None):
        response = client.request(method, path, json=json, headers=headers)
        assert response.status_code == 200, response.json()
        return response.json()

    resources = []
    for index, name in enumerate(resource_names):
        skill = request(
            "POST",
            "/skill/create_skill",
            {
                "name": f"{name}-{unique_value}",
                "description": f"{name} skill",
            },
        )
        project = request(
            "POST",
            "/project/create_project",
            {
                "skill_id": skill["id"],
                "project_name": f"{name}-project-{unique_value}",
                "description": f"{name} project",
            },
        )
        task = request(
            "POST",
            "/task/create_task",
            {
                "skill_id": skill["id"],
                "project_id": project["id"],
                "task_name": f"{name}-task-{unique_value}",
                "description": f"{name} task",
                "deadline": (datetime.now(UTC) + timedelta(days=index + 1)).isoformat(),
            },
        )
        resources.append({"skill": skill, "project": project, "task": task})

    return test_user, headers, resources


def test_crud_workflow_from_skills_to_tasks():
    unique_value = uuid4().hex
    resource_names = ["Python", "FastAPI", "SQLAlchemy", "Pytest"]
    test_user, headers, resources = create_user_with_resources(
        unique_value,
        resource_names,
    )

    try:

        def request(method: str, path: str, json: dict | None = None):
            response = client.request(
                method,
                path,
                json=json,
                headers=headers,
            )
            assert response.status_code == 200, response.json()
            return response.json()

        all_skills = request("GET", "/skill/skills")
        assert {skill["id"] for skill in all_skills} == {
            resource["skill"]["id"] for resource in resources
        }

        for index, resource in enumerate(resources):
            skill = resource["skill"]
            project = resource["project"]
            task = resource["task"]

            fetched_skill = request("GET", f"/skill/skill/{skill['id']}")
            assert fetched_skill["id"] == skill["id"]

            projects = request("GET", f"/project/projects/{skill['id']}")
            assert [item["id"] for item in projects] == [project["id"]]
            fetched_project = request(
                "GET",
                f"/project/project/{skill['id']}/{project['id']}",
            )
            assert fetched_project["id"] == project["id"]

            tasks = request(
                "GET",
                f"/task/tasks/{skill['id']}/{project['id']}",
            )
            assert [item["id"] for item in tasks] == [task["id"]]
            fetched_task = request(
                "GET",
                f"/task/task/{skill['id']}/{project['id']}/{task['id']}",
            )
            assert fetched_task["id"] == task["id"]

            updated_skill = request(
                "PUT",
                "/skill/update_skill",
                {
                    "id": skill["id"],
                    "name": f"Updated-{resource_names[index]}-{unique_value}",
                    "description": "Updated skill",
                },
            )
            assert updated_skill["skill_name"].startswith("Updated-")

            updated_project = request(
                "PUT",
                "/project/update_project",
                {
                    "skill_id": skill["id"],
                    "project_id": project["id"],
                    "project_name": (
                        f"Updated-{resource_names[index]}-project-{unique_value}"
                    ),
                    "description": "Updated project",
                },
            )
            assert updated_project["project_name"].startswith("Updated-")

            updated_task = request(
                "PUT",
                "/task/update_task",
                {
                    "skill_id": skill["id"],
                    "project_id": project["id"],
                    "task_id": task["id"],
                    "task_name": (
                        f"Updated-{resource_names[index]}-task-{unique_value}"
                    ),
                    "description": "Updated task",
                    "deadline": (
                        datetime.now(UTC) + timedelta(days=index + 5)
                    ).isoformat(),
                },
            )
            assert updated_task["task_name"].startswith("Updated-")

        first = resources[0]
        toggled_task = request(
            "PATCH",
            "/task/toggle_task",
            {
                "skill_id": first["skill"]["id"],
                "project_id": first["project"]["id"],
                "task_id": first["task"]["id"],
                "toggle": True,
            },
        )
        assert toggled_task["completed"] is True

        near_deadline_tasks = request("GET", "/task/near_deadline_tasks")
        assert {task["id"] for task in near_deadline_tasks} == {
            resource["task"]["id"] for resource in resources[1:]
        }

        for resource in resources:
            skill = resource["skill"]
            project = resource["project"]
            task = resource["task"]

            deleted_task = request(
                "DELETE",
                "/task/delete_task",
                {
                    "skill_id": skill["id"],
                    "project_id": project["id"],
                    "task_id": task["id"],
                },
            )
            assert deleted_task["id"] == task["id"]

            deleted_project = request(
                "DELETE",
                "/project/delete_project",
                {
                    "skill_id": skill["id"],
                    "project_id": project["id"],
                },
            )
            assert deleted_project["id"] == project["id"]

            deleted_skill = request(
                "DELETE",
                "/skill/delete_skill",
                {"id": skill["id"]},
            )
            assert deleted_skill["id"] == skill["id"]

        assert request("GET", "/skill/skills") == []
    finally:
        with Session(engine) as session:
            user = session.scalar(select(User).where(User.email == test_user["email"]))
            if user is not None:
                session.delete(user)
                session.commit()
