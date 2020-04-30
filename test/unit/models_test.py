from ...application.models import User

def test_new_user():
    """
    GIVEN a User Model
    WHEN a new User is created
    THEN check the id, email, username, password, first name, last name,
    chase the ace wins and authenticated fields are defined correctly.
    """
    new_user = User('testEmail123@hotmail.com', 'testUsername', 'testPassword', 'testFirstName', 'TestLastName', 123)
    assert new_user.email == 'testEmail123@hotmail.com'
    assert new_user.username == 'testUsername'
    assert new_user.password == 'testPassword'
    assert new_user.firstName == 'testFirstName'
    assert new_user.lastName == 'testLastName'
    assert new_user.chaseTheAceWins == 123
    assert not new_user.authenticated
