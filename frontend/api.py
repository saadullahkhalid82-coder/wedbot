from typing import Dict, Any
import requests


BASE_URL: str = "http://127.0.0.1:8000"


def _headers(token: str) -> Dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def login_user(email: str, password: str) -> Dict[str, Any]:
    response = requests.post(
        f"{BASE_URL}/login",
        json={"email": email, "password": password},
        timeout=10,
    )
    response.raise_for_status()
    return response.json()

def mark_complete(token: str, title: str):
    response = requests.post(
        f"{BASE_URL}/tasks/complete",
        params={"title": title},
        headers=_headers(token),
        timeout=15,
    )
    response.raise_for_status()
    return response.json()


def chat(token: str, message: str):
    response = requests.post(
        f"{BASE_URL}/chat",
        json={"message": message},
        headers=_headers(token),
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def get_tasks(token: str) -> Dict[str, Any]:
    response = requests.get(
        f"{BASE_URL}/tasks",
        headers=_headers(token),
        timeout=10,
    )
    response.raise_for_status()
    return response.json()

def export_checklist(token: str):
    response = requests.get(
        f"{BASE_URL}/export/checklist",
        headers=_headers(token),
        timeout=30,
    )
    response.raise_for_status()
    return response.content


def export_budget(token: str):
    response = requests.get(
        f"{BASE_URL}/export/budget",
        headers=_headers(token),
        timeout=30,
    )
    response.raise_for_status()
    return response.content


def get_budgets(token: str) -> Dict[str, Any]:
    response = requests.get(
        f"{BASE_URL}/budgets",
        headers=_headers(token),
        timeout=10,
    )
    response.raise_for_status()
    return response.json()

def create_budget(token: str, total_budget: float):
    response = requests.post(
        f"{BASE_URL}/budget",
        json={"total_budget": total_budget},
        headers=_headers(token),
        timeout=15,
    )
    response.raise_for_status()
    return response.json()


def update_profile(token: str, data: dict):
    response = requests.put(
        f"{BASE_URL}/profile",
        json=data,
        headers=_headers(token),
        timeout=15,
    )
    response.raise_for_status()
    return response.json()

def get_profile(token: str) -> Dict[str, Any]:
    response = requests.get(
        f"{BASE_URL}/profile",
        headers=_headers(token),
        timeout=10,
    )

    if response.status_code == 401:
        raise Exception("Session expired. Please login again.")

    response.raise_for_status()
    return response.json()

def get_conversation(token: str) -> Dict[str, Any]:
    response = requests.get(
        f"{BASE_URL}/conversation",
        headers=_headers(token),
        timeout=10,
    )
    response.raise_for_status()
    return response.json()