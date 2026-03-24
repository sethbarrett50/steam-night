from cyber.server import DemoConfig, create_app


def test_password_check_endpoint() -> None:
    app = create_app(DemoConfig(password='dragon'))
    client = app.test_client()

    response = client.post('/api/check', json={'password': 'dragon'})
    assert response.status_code == 200
    assert response.json == {'success': True, 'password': 'dragon'}
