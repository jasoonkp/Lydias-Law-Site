from users.models import User 

# create a new instance
new_user = User.objects.create(
    first_name="jason",
    last_name="prakash",
    email="jason@example.com",
    password_hash="securepassword123" 
)
print(new_user)
