1. User wants to log into a Client by clicking a “Login” button. The initially requested URL can be passed using the next GET parameter.
2. The Client’s Python code does a HTTP request to the Server to request a authentication token, this is called the Request Token Request.
3. The Server returns a Request Token.
4. The Client redirects the User to a view on the Server using the Request Token, this is the Authorization Request.
5. If the user is not logged in the the Server, they are prompted to log in.
6. The user is redirected to the Client including the Request Token and a Auth Token, this is the Authentication Request.
7. The Client’s Python code does a HTTP request to the Server to verify the Auth Token, this is called the Auth Token Verification Request.
8. If the Auth Token is valid, the Server returns a serialized Django User object.
9. The Client logs the user in using the Django User recieved from the Server.

From: https://pypi.org/project/django-simple-sso/

