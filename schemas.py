from pydantic import BaseModel, Field, field_validator
from urllib.parse import urlparse
import re

class InputLink(BaseModel):
    url: str = Field(..., description="The URL of the GitHub PR")
    description: str = Field(None, description="A brief description of the link")
    
    @field_validator('url')
    @classmethod
    def validate_github_url(cls, v: str) -> str:
        """
        Validate that the URL is a genuine GitHub link.
        Checks for:
        - Proper URL format
        - GitHub domain (github.com)
        - HTTPS protocol
        - Valid GitHub path structure
        """
        if not v:
            raise ValueError("URL cannot be empty")
        
        # Parse the URL
        try:
            parsed = urlparse(v)
        except Exception:
            raise ValueError("Invalid URL format")
        
        # Check for HTTPS protocol
        if parsed.scheme != 'https':
            raise ValueError("Only HTTPS GitHub URLs are allowed")
        
        # Check for GitHub domain
        valid_domains = ['github.com', 'www.github.com']
        if parsed.netloc.lower() not in valid_domains:
            raise ValueError("URL must be from github.com domain")
        
        # Check for valid GitHub PR path structure
        # Only accept: /owner/repo/pull/123
        path = parsed.path.strip('/')
        if not path:
            raise ValueError("GitHub URL must include a repository path")
        
        path_parts = path.split('/')
        
        # Must have exactly 4 parts: owner, repo, 'pull', number
        if len(path_parts) < 4:
            raise ValueError("URL must be a GitHub Pull Request link (e.g., https://github.com/owner/repo/pull/123)")
        
        # Validate owner and repo names (GitHub naming rules)
        owner, repo = path_parts[0], path_parts[1]
        github_name_pattern = r'^[a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?$'
        
        if not re.match(github_name_pattern, owner):
            raise ValueError("Invalid GitHub owner name")
        
        if not re.match(github_name_pattern, repo):
            raise ValueError("Invalid GitHub repository name")
        
        # Validate it's specifically a pull request
        if path_parts[2] != 'pull':
            raise ValueError("Only GitHub Pull Request links are accepted (must contain '/pull/')")
        
        # Validate PR number
        try:
            pr_number = int(path_parts[3])
            if pr_number <= 0:
                raise ValueError("Invalid PR number")
        except (ValueError, IndexError):
            raise ValueError("Invalid PR number format")
        
        return v
    
    def get_pr_details(self) -> dict:
        """Extract owner, repo, and PR number from the validated GitHub PR URL."""
        parsed = urlparse(self.url)
        path_parts = parsed.path.strip('/').split('/')
        
        return {
            "owner": path_parts[0],
            "repo": path_parts[1],
            "pull_request": "pull",
            "pr_number": int(path_parts[3])
        }