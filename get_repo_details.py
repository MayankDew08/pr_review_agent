import requests

def get_details(owner,repo,pr_number):
    """Fetch GitHub PR details using GitHub API."""
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}"
    response = requests.get(url)
    
    if response.status_code != 200:
        raise ValueError("Failed to fetch PR details from GitHub API")
    
    pr_data = response.json()
    return {
        "title": pr_data.get("title"),
        "body": pr_data.get("body"),
        "state": pr_data.get("state"),
        "created_at": pr_data.get("created_at"),
        "updated_at": pr_data.get("updated_at"),
        "merged": pr_data.get("merged"),
        "merge_commit_sha": pr_data.get("merge_commit_sha"),
    }

def get_patches(owner, repo, pr_number):
    """Fetch PR file diffs/patches for code review."""
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/files"
    response = requests.get(url)

    if response.status_code != 200:
        raise ValueError("Failed to fetch PR diffs")

    data = response.json()

    patches = []
    for file in data:
        patches.append({
            "filename": file["filename"],
            "status": file.get("status", ""),  # added, modified, removed, renamed
            "additions": file.get("additions", 0),
            "deletions": file.get("deletions", 0),
            "changes": file.get("changes", 0),
            "patch": file.get("patch", "")  # The actual diff
        })
    
    return patches