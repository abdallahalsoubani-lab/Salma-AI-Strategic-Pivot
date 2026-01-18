import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db.session import get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.session import Base

# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def cleanup():
    """Clean up test database before each test"""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield

@pytest.fixture
def auth_token():
    """Create a test user and return auth token"""
    response = client.post(
        "/api/auth/register",
        json={
            "email": "test@example.com",
            "password": "testpassword123",
            "full_name": "Test User",
        }
    )
    return response.json()["access_token"]

def test_create_api_key(auth_token):
    """Test creating an API key"""
    response = client.post(
        "/api/keys",
        json={"name": "Test Key"},
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Key"
    assert data["key"].startswith("sk_live_")

def test_list_api_keys(auth_token):
    """Test listing API keys"""
    # Create a key
    client.post(
        "/api/keys",
        json={"name": "Test Key"},
        headers={"Authorization": f"Bearer {auth_token}"}
    )

    # List keys
    response = client.get(
        "/api/keys",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Test Key"
    assert "masked_key" in data[0]

def test_delete_api_key(auth_token):
    """Test deleting an API key"""
    # Create a key
    create_response = client.post(
        "/api/keys",
        json={"name": "Test Key"},
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    key_id = create_response.json()["id"]

    # Delete the key
    response = client.delete(
        f"/api/keys/{key_id}",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200

    # Verify it's deleted (inactive)
    list_response = client.get(
        "/api/keys",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    keys = list_response.json()
    deleted_key = next((k for k in keys if k["id"] == key_id), None)
    assert deleted_key is not None
    assert deleted_key["is_active"] == False

def test_get_api_key_usage(auth_token):
    """Test getting API key usage stats"""
    # Create a key
    create_response = client.post(
        "/api/keys",
        json={"name": "Test Key"},
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    key_id = create_response.json()["id"]

    # Get usage
    response = client.get(
        f"/api/keys/{key_id}/usage",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["key_id"] == key_id
    assert "total_requests" in data
