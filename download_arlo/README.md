# Download Arlo

## Disclaimer
The following is a "work in progress" and is dependent on API/product limitations.

## Headers
| Header                      | Value                                                                                                                             |
|--|--|
|User-Agent	                  | Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36
|Upgrade-Insecure-Requests	  | 1                                                                                                                                 |
|Referer	                  | https://my.arlo.com/                                                                                                              |
|source	                      | arloCamWeb                                                                                                                        |
|Origin	                      | https://my.arlo.com                                                                                                               |
|Host	                      | ocapi-app.arlo.com; myapi.arlo.com                                                                                                |
|Authorization	              | <token>                                                                                                                           |
|dnt	                      | 1                                                                                                                                 |
|Auth-Version	              | 2                                                                                                                                 |
|authority	                  | ocapi-app.arlo.com                                                                                                                |


## Authentication Chain
1. Login to authenticate user account and password
2. Get MFA ID
3. Start authentication
4. Finish authentication
5. Open Session

### Example
```python
def auth(self):
    endpoint = "https://ocapi-app.arlo.com/api/auth";
    rsp = self.session.post(endpoint, json={"email":self.username, "password":self.password, "EnvSource":"prod", "language":"en"}, headers=self.headers);
    self.token = rsp.json()["data"]["token"];
    self.userid = rsp.json()["data"]["userId"];
    self.headers["Authorization"] = str(base64.b64encode(self.token.encode("utf-8")), "utf-8");
    rsp = self.session.get(endpoint.replace("auth", "getFactors") + "?data%20={0}".format(rsp.json()["data"]["authenticated"]), headers=self.headers);
    self.mfa_id = next(x for x in rsp.json()["data"]["items"] if x["factorType"] == "EMAIL")["factorId"];
    rsp = self.session.post(endpoint.replace("auth", "startAuth"), json={"factorId":self.mfa_id}, headers=self.headers);
    self.factor_code = rsp.json()["data"]["factorAuthCode"];
    mfa_code = input("MFA Code: ");
    rsp = self.session.post(endpoint.replace("auth", "finishAuth"), json={"factorAuthCode":self.factor_code, "otp":"{0}".format(mfa_code)}, headers=self.headers);
    self.token = rsp.json()["data"]["token"];
    self.headers["Authorization"] = str(base64.b64encode(self.token.encode("utf-8")), "utf-8");
    rsp = self.session.get(endpoint.replace("auth", "validateAccessToken?data={0}".format(int(time.time()))), headers=self.headers);
    self.headers["Authorization"] = self.token;
    self.headers["Host"] = "myapi.arlo.com";
    rsp = self.session.get("https://myapi.arlo.com/hmsweb/users/session/v3?time={0}".format(int(time.time())), headers=self.headers);
```
Note that:
* We use a completely different endpoint for auth.  This is by design.
* We constantly alternate the headers between base64 for standard.  This is dumb, but by design.
* We use OPT instead of MFA, this is a limitation of the API outside of a mobile app.
* OTP needs to be manually entered, that's by design of this example.

## Endpoints
### Base Endpoint
https://myapi.arlo.com/hmsweb
|Endpoint                                                | Method           | Body                                                                             |
|--|--|--|
|https://ocapi-app.arlo.com/api/auth                     | POST             | {"email":"", "password":"", "EnvSource":"prod", "language":"en"}                 |
|https://ocapi-app.arlo.com/api/getFactors               | GET              | ?data=<timestamp>                                                                |
|https://ocapi-app.arlo.com/api/startAuth                | POST             | {"factorId":""}                                                                  |
|https://ocapi-app.arlo.com/api/finishAuth               | POST             | {"factorAuthCode":"","otp":""}                                                   |
|https://ocapi-app.arlo.com/api/validateAccessToken      | GET              | ?data=<timestamp>                                                                |
|v2/users/devices                                        | GET              | -                                                                                |


## Retrospective
* As reasonable as the REST API is to use for development, it's still completely useless for local storage.
    * I believe this is by design to push customers is purchasing a cloud subscription.
    * Even with Port Forwarding, there's no option outside of their buggy app to access local recordings.
    * I believe they might be using some sort of gRPC protocol, which means without the stubs and internal components, developers are still SOL.
* I, as well as an abundance of others, take significant issues with this as we purchased the product, it's on our network, and many of us have legitimate need to have direct access.
* At the end of the day, I absolutely love the Arlo design and would hate to change to a different ecosystem, especially since the investment didn't come cheap.
* The focus on security doesn't need to be viewed as a bad thing, but the fact that most features are limited outside of the mobile app or a cloud subscription is a bit unacceptable.

## References
* https://robertogallea.com/posts/development/netgear-arlo-system-api
* https://github.com/jeffreydwalter/arlo/blob/master/arlo.py 
* https://github.com/twratl/arlo-mfa-aws 

