from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import json


class IssueBase(BaseModel):
    line: Optional[int] = Field(None, description="Line number where the issue occurs")
    severity: str = Field(..., description="Severity level of the issue")
    issue: str = Field(..., description="Description of the issue")
    suggestion: str = Field(..., description="Suggested fix for the issue")
    fixed_code: Optional[str] = Field(None, description="Fixed code snippet")


class FileReview(BaseModel):
    filename: str
    status: Optional[str] = None
    issues: List[Dict[str, Any]]
    issue_count: int
    
    
class PRInfo(BaseModel):
    owner: str
    repo: str
    pr_number: int


class ReviewSummary(BaseModel):
    total_files: int
    files_with_issues: int
    total_issues: int
    critical_issues: int = 0
    high_issues: int = 0
    medium_issues: int = 0
    low_issues: int = 0


class SingleReviewResponse(BaseModel):
    success: bool = True
    pr_info: PRInfo
    review_type: str
    summary: ReviewSummary
    files: List[FileReview]


class FullReviewResponse(BaseModel):
    success: bool = True
    pr_info: PRInfo
    overall_summary: Dict[str, Any]
    logic_review: Dict[str, Any]
    security_review: Dict[str, Any]
    readability_review: Dict[str, Any]
    performance_review: Dict[str, Any]
    recommendation: str


def parse_json_issues(issues_str: str) -> List[Dict[str, Any]]:
    """Parse JSON string from AI response to list of issues."""
    try:
        if isinstance(issues_str, str):
            return json.loads(issues_str)
        return issues_str
    except:
        return []


def count_severity(issues: List[Dict[str, Any]], severity: str) -> int:
    """Count issues by severity level."""
    return sum(1 for issue in issues if issue.get('severity', '').lower() == severity.lower())


def create_review_summary(files: List[FileReview]) -> ReviewSummary:
    """Create summary statistics for a review."""
    total_issues = sum(f.issue_count for f in files)
    files_with_issues = sum(1 for f in files if f.issue_count > 0)
    
    all_issues = []
    for f in files:
        all_issues.extend(f.issues)
    
    return ReviewSummary(
        total_files=len(files),
        files_with_issues=files_with_issues,
        total_issues=total_issues,
        critical_issues=count_severity(all_issues, 'critical'),
        high_issues=count_severity(all_issues, 'high'),
        medium_issues=count_severity(all_issues, 'medium'),
        low_issues=count_severity(all_issues, 'low')
    )


def format_single_review(pr_info: Dict, reviews: List[Dict], review_type: str) -> Dict:
    """Format a single type of review (logic, security, readability, or performance)."""
    
    issue_key = f"{review_type}_issues"
    files = []
    
    for review in reviews:
        issues = parse_json_issues(review.get(issue_key, []))
        files.append({
            "filename": review['filename'],
            "status": review.get('status'),
            "issues": issues,
            "issue_count": len(issues)
        })
    
    # Calculate summary
    total_issues = sum(f["issue_count"] for f in files)
    files_with_issues = sum(1 for f in files if f["issue_count"] > 0)
    
    all_issues = []
    for f in files:
        all_issues.extend(f["issues"])
    
    summary = {
        "total_files": len(files),
        "files_with_issues": files_with_issues,
        "total_issues": total_issues,
        "critical_issues": count_severity(all_issues, 'critical'),
        "high_issues": count_severity(all_issues, 'high'),
        "medium_issues": count_severity(all_issues, 'medium'),
        "low_issues": count_severity(all_issues, 'low')
    }
    
    return {
        "success": True,
        "pr_info": pr_info,
        "review_type": review_type,
        "summary": summary,
        "files": files
    }


def format_full_review(pr_info: Dict, logic_reviews: List, security_reviews: List, 
                       readability_reviews: List, performance_reviews: List) -> Dict:
    """Format complete review with all review types."""
    
    # Parse all reviews
    logic_files = []
    security_files = []
    readability_files = []
    performance_files = []
    
    for review in logic_reviews:
        issues = parse_json_issues(review.get('logic_issues', []))
        logic_files.append({
            "filename": review['filename'],
            "status": review.get('status'),
            "issues": issues,
            "issue_count": len(issues)
        })
    
    for review in security_reviews:
        issues = parse_json_issues(review.get('security_issues', []))
        security_files.append({
            "filename": review['filename'],
            "status": review.get('status'),
            "issues": issues,
            "issue_count": len(issues)
        })
    
    for review in readability_reviews:
        issues = parse_json_issues(review.get('readability_issues', []))
        readability_files.append({
            "filename": review['filename'],
            "status": review.get('status'),
            "issues": issues,
            "issue_count": len(issues)
        })
    
    for review in performance_reviews:
        issues = parse_json_issues(review.get('performance_issues', []))
        performance_files.append({
            "filename": review['filename'],
            "status": review.get('status'),
            "issues": issues,
            "issue_count": len(issues)
        })
    
    # Create summaries
    def create_summary(files):
        total_issues = sum(f["issue_count"] for f in files)
        files_with_issues = sum(1 for f in files if f["issue_count"] > 0)
        all_issues = []
        for f in files:
            all_issues.extend(f["issues"])
        return {
            "total_files": len(files),
            "files_with_issues": files_with_issues,
            "total_issues": total_issues,
            "critical_issues": count_severity(all_issues, 'critical'),
            "high_issues": count_severity(all_issues, 'high'),
            "medium_issues": count_severity(all_issues, 'medium'),
            "low_issues": count_severity(all_issues, 'low')
        }
    
    logic_summary = create_summary(logic_files)
    security_summary = create_summary(security_files)
    readability_summary = create_summary(readability_files)
    performance_summary = create_summary(performance_files)
    
    # Overall summary
    total_issues = (logic_summary["total_issues"] + security_summary["total_issues"] + 
                   readability_summary["total_issues"] + performance_summary["total_issues"])
    
    overall_summary = {
        "total_files_reviewed": len(logic_reviews),
        "total_issues_found": total_issues,
        "breakdown": {
            "logic_issues": logic_summary["total_issues"],
            "security_issues": security_summary["total_issues"],
            "readability_issues": readability_summary["total_issues"],
            "performance_issues": performance_summary["total_issues"]
        },
        "severity_breakdown": {
            "critical": security_summary["critical_issues"],
            "high": security_summary["high_issues"] + logic_summary["high_issues"] + performance_summary["high_issues"],
            "medium": security_summary["medium_issues"] + logic_summary["medium_issues"] + readability_summary["medium_issues"] + performance_summary["medium_issues"],
            "low": security_summary["low_issues"] + logic_summary["low_issues"] + readability_summary["low_issues"] + performance_summary["low_issues"]
        }
    }
    
    # Generate recommendation
    if security_summary["critical_issues"] > 0:
        recommendation = "❌ CRITICAL: This PR has critical security issues. DO NOT MERGE until resolved."
    elif security_summary["high_issues"] > 0 or logic_summary["high_issues"] > 0:
        recommendation = "⚠️ WARNING: This PR has high-severity issues. Review and fix before merging."
    elif total_issues > 10:
        recommendation = "⚠️ CAUTION: Multiple issues found. Consider addressing them before merging."
    elif total_issues > 0:
        recommendation = "✓ ACCEPTABLE: Minor issues found. Review and address if needed."
    else:
        recommendation = "✅ APPROVED: No issues found. This PR looks good!"
    
    return {
        "success": True,
        "pr_info": pr_info,
        "overall_summary": overall_summary,
        "logic_review": {
            "summary": logic_summary,
            "files": logic_files
        },
        "security_review": {
            "summary": security_summary,
            "files": security_files
        },
        "readability_review": {
            "summary": readability_summary,
            "files": readability_files
        },
        "performance_review": {
            "summary": performance_summary,
            "files": performance_files
        },
        "recommendation": recommendation
    }
