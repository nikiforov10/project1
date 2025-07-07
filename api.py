import requests


# response = requests.get("https://api.github.com/repos/requests/requests")
#
# if response.status_code == 200:
#     repo_data = response.json()
#     print(f'Репозиторий: {repo_data['name']}')
#     print(f'Звезд: {repo_data['stargazers_count']}')
#     print(f'URL: {repo_data['html_url']}')
# else:
#     print(f'ОШибка: {response.status_code}')


# response = requests.post(
#     'https://httpbin.org/post',
#     json={'username': 'admin', 'password': '1234'}
# )
# files = {'file': open('report.xls', 'rb')}
# requests.post('https://httpbin.org/post', files=files)
# print(response)

token = 'f6a92336f6a92336f6a92336ccf59cfd59ff6a9f6a923369ec346b17a77b01a911a2fa4'
response = requests.get(
    'https://api.vk.com/method/users.get',
    params={'user_ids': '1', 'access_token': token, 'v': '5.131'}
)
print(response.json())