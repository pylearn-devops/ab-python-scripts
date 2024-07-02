import logging
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

def close_pulls_and_issues(org_name):
    org = g.get_organization(org_name)
    repos = org.get_repos()

    exempt_prs = []
    exempt_issues = []
    closed_count = 0
    max_to_close = 60

    for repo in repos:
        # Close open pull requests created before the ignored date
        pull_requests = repo.get_pulls(state='open')
        for pr in pull_requests:
            logger.info(f"Processing PR: {pr.title} created at {pr.created_at}")
            if closed_count >= max_to_close:
                break  # Stop processing if we've reached the limit
            if pr.created_at < ignored_date:  # Only consider PRs created before the ignored date
                if has_exempt_labels(pr):
                    exempt_prs.append([pr.number, pr.title, pr.user.login, pr.created_at, repo.name])
                else:
                    pr.create_issue_comment(CLOSE_COMMENT)
                    pr.edit(state='closed')
                    closed_count += 1
                    logger.info(f"Closed PR: {pr.title} in repo {repo.name}")

        # Close open issues created before the ignored date
        issues = repo.get_issues(state='open')
        for issue in issues:
            logger.info(f"Processing Issue: {issue.title} created at {issue.created_at}")
            if closed_count >= max_to_close:
                break  # Stop processing if we've reached the limit
            if issue.created_at < ignored_date and issue.pull_request is None:  # Only consider issues created before the ignored date
                if has_exempt_labels(issue):
                    exempt_issues.append([issue.number, issue.title, issue.user.login, issue.created_at, repo.name])
                else:
                    issue.create_comment(CLOSE_COMMENT)
                    issue.edit(state='closed')
                    closed_count += 1
                    logger.info(f"Closed Issue: {issue.title} in repo {repo.name}")

    print(closed_count, exempt_prs, exempt_issues)
    return closed_count, exempt_prs, exempt_issues