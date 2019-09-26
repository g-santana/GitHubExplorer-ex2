import requests
from authdata import headers  # authdata.py -- this is where your GitHub auth token is encapsulated
from json import loads
from os import system

json = {
    "q": "language:python stars:>100",
    "per_page": "100",
    "page": "1",
    "sort": "stars",
    "order": "desc"
}  # example of json to query for the kind of repos you want

repos_path = ""  # insert path for cloned repos here


def get_urls():  # method that gets the repos names and urls from the response given to the query by GitHub
    git_urls = []
    for i in range(1, 11):
        json["page"] = str(i)
        response = requests.get(url='https://api.github.com/search/repositories', headers=headers, params=json)
        this_page_repos = loads(response.text)["items"]
        for item in this_page_repos:
            git_urls.append(
                {
                    "repo_name": item["name"],
                    "repo_url": item["clone_url"]
                }
            )
    return git_urls


def clone_repos(git_urls):  # method that clones the repos into a specific path in your system
    with open("last-cloning-repo-index.txt", "r") as file:
        last_index = int(file.read())
    file.close()
    if last_index < 1000:
        for i in range(last_index, len(git_urls)):
            with open("last-cloning-repo-index.txt", "w") as file:
                file.write(f"{i}")
            file.close()
            system(f"git clone {git_urls[i]['repo_url']} {repos_path}{i + 1}-{git_urls[i]['repo_name']}")
    else:
        print("All the 1000 repos have already been cloned into your machine.")


urls = get_urls()
clone_repos(urls)
