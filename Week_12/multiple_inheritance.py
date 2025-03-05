## Program designed to demonstrate multiple inheritance in Python with Mixins
## First, we define two Mixins: JSONSerializableMixin and AuthenticableMixin.
## JSONSerializableMixin provides a method to convert an object to a JSON string.
class JSONSerializableMixin:
    def to_json(self):        
        import json
        return json.dumps(self.__dict__)
## AuthenticableMixin provides a method to authenticate a user by comparing a password hash.
class AuthenticableMixin:
    def authenticate(self, password):        
        return self.password_hash == hash(password)

class User(AuthenticableMixin, JSONSerializableMixin):
    def __init__(self, username, password):
        self.username = username
        self.password_hash = hash(password)  # Simplified hashing for demonstration
def main():
    # Usage
    user = User("alice", "securepassword123")
    print(user.authenticate("securepassword123"))  # Output: True
    print(user.to_json())  

if __name__ == "__main__":
    main()