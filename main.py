from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from schemas import InputLink
from pydantic import ValidationError
from get_repo_details import get_details, get_patches
from single_agent import analyze_pr_full
from logic_agent import analyze_file_logic
from security_agent import analyze_file_security
from readability_agent import analyze_file_readability
from performance_agent import analyze_file_performance
from response_models import format_single_review, format_full_review
import time
import json

app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development (restrict in production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Github PR Agent API is running", "status": "active", "endpoints": ["/comprehensive_review/", "/full_review/", "/review_logic/", "/review_security/", "/review_readability/", "/review_performance/", "/get_pr_details/", "/get_pr_diffs/"]}

@app.post("/post_link/")
async def post_link(link_data: InputLink):
    try:
        # The validation happens automatically in the InputLink model
        pr_details = link_data.get_pr_details()
        
        return {
            "message": "Valid GitHub PR link received",
            "url": link_data.url,
            "owner": pr_details["owner"],
            "repo": pr_details["repo"],
            "pull_request": pr_details["pull_request"],
            "pr_number": pr_details["pr_number"],
            "description": link_data.description
        }
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.get("/get_pr_details/")
async def get_pr_details(link: InputLink):
    try:
        pr_details = link.get_pr_details()
        details = get_details(pr_details["owner"], pr_details["repo"], pr_details["pr_number"])
        return details
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/get_pr_diffs/")
async def get_pr_diffs(link_data: InputLink):
    """Get PR file diffs for code review."""
    try:
        pr_details = link_data.get_pr_details()
        
        # Get basic PR details
        details = get_details(pr_details["owner"], pr_details["repo"], pr_details["pr_number"])
        
        # Get file patches/diffs
        patches = get_patches(pr_details["owner"], pr_details["repo"], pr_details["pr_number"])
        
        return {
            "pr_info": {
                "owner": pr_details["owner"],
                "repo": pr_details["repo"],
                "pr_number": pr_details["pr_number"],
                "title": details["title"],
                "state": details["state"],
                "merged": details["merged"]
            },
            "files_changed": len(patches),
            "diffs": patches
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching PR diffs: {str(e)}")
    
@app.post("/review_logic/")
async def review_logic(link_data: InputLink):
    """Review the logic of code changes in a PR."""
    start_time = time.time()
    try:
        pr_details = link_data.get_pr_details()
        diffs = get_patches(pr_details["owner"], pr_details["repo"], pr_details["pr_number"])
        
        pr_info = {
            "owner": pr_details["owner"],
            "repo": pr_details["repo"],
            "pr_number": pr_details["pr_number"],
        }
        
        reviews = []
        for diff in diffs:
            if not diff.get('patch'):
                continue
            file_review = analyze_file_logic(diff['filename'], diff['patch'])
            reviews.append({
                "filename": diff['filename'],
                "status": diff.get('status', None),
                "logic_issues": file_review
            })
        
        result = format_single_review(pr_info, reviews, "logic")
        result["review_time_seconds"] = round(time.time() - start_time, 2)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
@app.post("/review_security/")
async def review_security(link_data: InputLink):
    """Review the security of code changes in a PR."""
    start_time = time.time()
    try:
        pr_details = link_data.get_pr_details()
        diffs = get_patches(pr_details["owner"], pr_details["repo"], pr_details["pr_number"])
        
        pr_info = {
            "owner": pr_details["owner"],
            "repo": pr_details["repo"],
            "pr_number": pr_details["pr_number"],
        }
        
        reviews = []
        for diff in diffs:
            if not diff.get('patch'):
                continue
            file_review = analyze_file_security(diff['filename'], diff['patch'])
            reviews.append({
                "filename": diff['filename'],
                "status": diff.get('status', None),
                "security_issues": file_review
            })
        
        result = format_single_review(pr_info, reviews, "security")
        result["review_time_seconds"] = round(time.time() - start_time, 2)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.post("/review_readability/")
async def review_readability(link_data: InputLink):
    """Review the readability of code changes in a PR."""
    start_time = time.time()
    try:
        pr_details = link_data.get_pr_details()
        diffs = get_patches(pr_details["owner"], pr_details["repo"], pr_details["pr_number"])
        
        pr_info = {
            "owner": pr_details["owner"],
            "repo": pr_details["repo"],
            "pr_number": pr_details["pr_number"],
        }
        
        reviews = []
        for diff in diffs:
            if not diff.get('patch'):
                continue
            file_review = analyze_file_readability(diff['filename'], diff['patch'])
            reviews.append({
                "filename": diff['filename'],
                "status": diff.get('status', None),
                "readability_issues": file_review
            })
        
        result = format_single_review(pr_info, reviews, "readability")
        result["review_time_seconds"] = round(time.time() - start_time, 2)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.post("/review_performance/")
async def review_performance(link_data: InputLink):
    """Review the performance of code changes in a PR."""
    start_time = time.time()
    try:
        pr_details = link_data.get_pr_details()
        diffs = get_patches(pr_details["owner"], pr_details["repo"], pr_details["pr_number"])
        
        pr_info = {
            "owner": pr_details["owner"],
            "repo": pr_details["repo"],
            "pr_number": pr_details["pr_number"],
        }
        
        reviews = []
        for diff in diffs:
            if not diff.get('patch'):
                continue
            file_review = analyze_file_performance(diff['filename'], diff['patch'])
            reviews.append({
                "filename": diff['filename'],
                "status": diff.get('status', None),
                "performance_issues": file_review
            })
        
        result = format_single_review(pr_info, reviews, "performance")
        result["review_time_seconds"] = round(time.time() - start_time, 2)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.post("/comprehensive_review/")
async def comprehensive_review(input_link: InputLink):
    """Get comprehensive PR review using single AI agent analyzing all aspects."""
    start_time = time.time()
    try:
        pr_details = input_link.get_pr_details()
        owner = pr_details['owner']
        repo = pr_details['repo']
        pr_number = pr_details['pr_number']
        
        patches = get_patches(owner, repo, pr_number)
        
        # Combine all patches into single string for comprehensive analysis
        all_patches = ""
        for patch in patches:
            all_patches += f"\n{'='*60}\n"
            all_patches += f"FILE: {patch['filename']}\n"
            all_patches += f"STATUS: {patch['status']}\n"
            all_patches += f"CHANGES: +{patch['additions']} -{patch['deletions']}\n"
            all_patches += f"{'='*60}\n"
            all_patches += patch.get('patch', 'No patch available') + "\n"
        
        # Single comprehensive analysis
        review_result = analyze_pr_full(all_patches)
        result = json.loads(review_result)
        
        # Add metadata
        result["success"] = True
        result["pr_info"] = {
            "owner": owner,
            "repo": repo,
            "pr_number": pr_number
        }
        result["review_time_seconds"] = round(time.time() - start_time, 2)
        
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"ERROR in comprehensive_review: {error_details}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.post("/full_review/")
async def full_review(link_data: InputLink):
    """Complete code review covering logic, security, readability, and performance."""
    start_time = time.time()
    try:
        pr_details = link_data.get_pr_details()
        diffs = get_patches(pr_details["owner"], pr_details["repo"], pr_details["pr_number"])
        
        pr_info = {
            "owner": pr_details["owner"],
            "repo": pr_details["repo"],
            "pr_number": pr_details["pr_number"],
        }
        
        logic_reviews = []
        security_reviews = []
        readability_reviews = []
        performance_reviews = []
        
        for diff in diffs:
            if not diff.get('patch'):
                continue
            
            logic_review = analyze_file_logic(diff['filename'], diff['patch'])
            security_review = analyze_file_security(diff['filename'], diff['patch'])
            readability_review = analyze_file_readability(diff['filename'], diff['patch'])
            performance_review = analyze_file_performance(diff['filename'], diff['patch'])
            
            logic_reviews.append({
                "filename": diff['filename'],
                "status": diff.get('status', None),
                "logic_issues": logic_review
            })
            security_reviews.append({
                "filename": diff['filename'],
                "status": diff.get('status', None),
                "security_issues": security_review
            })
            readability_reviews.append({
                "filename": diff['filename'],
                "status": diff.get('status', None),
                "readability_issues": readability_review
            })
            performance_reviews.append({
                "filename": diff['filename'],
                "status": diff.get('status', None),
                "performance_issues": performance_review
            })
        
        result = format_full_review(pr_info, logic_reviews, security_reviews, 
                                 readability_reviews, performance_reviews)
        result["review_time_seconds"] = round(time.time() - start_time, 2)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    
