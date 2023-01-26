# Links:
# https://github.com/AzureAD/microsoft-authentication-library-for-python
# https://msal-python.readthedocs.io/en/latest/#msal.SerializableTokenCache
# https://learn.microsoft.com/en-us/azure/active-directory/develop/scenario-desktop-acquire-token?tabs=python

# pip install msal
# $env:tenant_id="<your_tenant_id>"
# $env:client_id="<your_client_id>"

from msal import PublicClientApplication, SerializableTokenCache
import os
import atexit

tenant_id = os.environ["tenant_id"]
client_id = os.environ["client_id"]

cache = SerializableTokenCache()
if os.path.exists("my_cache.bin"):
    cache.deserialize(open("my_cache.bin", "r").read())

atexit.register(lambda:
                open("my_cache.bin", "w").write(cache.serialize())
                # Hint: The following optional line persists only when state changed
                if cache.has_state_changed else None
                )

app = PublicClientApplication(
    client_id,
    authority="https://login.microsoftonline.com/" + tenant_id,
    token_cache=cache
)

result = None  # It is just an initial value. Please follow instructions below.

scopes = ["https://graph.microsoft.com/.default"]

# We now check the cache to see
# whether we already have some accounts that the end user already used to sign in before.
accounts = app.get_accounts()
accounts

if accounts:
    # If so, you could then somehow display these accounts and let end user choose
    print("Pick the account you want to use to proceed:")
    for a in accounts:
        print(a["username"])
    # Assuming the end user chose this one
    chosen = accounts[0]

    print("Account chosen:")
    print(chosen)

    print("Now let's try to find a token in cache for this account")
    result = app.acquire_token_silent(scopes=scopes, account=chosen)

if not result:
    print("Lets use device flow for authentication")
    device_flow = app.initiate_device_flow(scopes=scopes)
    print(device_flow["user_code"])  # Use browser to proceed with login
    # Use browser to proceed with login
    print(device_flow["verification_uri"])
    result = app.acquire_token_by_device_flow(device_flow)
    # This should contain "refresh_token"
    # print(result["refresh_token"])

if "access_token" in result:
    print(result["access_token"])
else:
    print(result.get("error"))
    print(result.get("error_description"))
    # You may need this when reporting a bug
    print(result.get("correlation_id"))
