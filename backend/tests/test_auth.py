from app.auth import hash_password, verify_password


def test_password_hash_round_trip():
    password = "Grove-test-password-123"
    encoded = hash_password(password)
    assert encoded != password
    assert verify_password(password, encoded)
    assert not verify_password("wrong-password", encoded)
