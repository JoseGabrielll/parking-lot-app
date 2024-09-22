import pytest

@pytest.mark.integration
def test_get_users_success_e2e(test_app):
    response = test_app.get('/api/user')
    assert response.status_code == 200