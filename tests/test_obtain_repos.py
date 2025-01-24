import responses
from pytest import fixture, raises
from requests import HTTPError
from responses import matchers

from cloner.obtain_repos import TokenNotFoundForGHEException, obtain_repos


@fixture()
def github_organization() -> str:
    return "octocat"


@fixture()
def github_response_one_private_repo():
    return [
        {
            "id": 1296269,
            "node_id": "MDEwOlJlcG9zaXRvcnkxMjk2MjY5",
            "name": "Hello-World-Private",
            "full_name": "octocat/Hello-World-Private",
            "owner": {
                "login": "octocat",
                "id": 1,
                "node_id": "MDQ6VXNlcjE=",
                "avatar_url": "https://github.com/images/error/octocat_happy.gif",
                "gravatar_id": "",
                "url": "https://api.github.com/users/octocat",
                "html_url": "https://github.com/octocat",
                "followers_url": "https://api.github.com/users/octocat/followers",
                "following_url": "https://api.github.com/users/octocat/following{/other_user}",
                "gists_url": "https://api.github.com/users/octocat/gists{/gist_id}",
                "starred_url": "https://api.github.com/users/octocat/starred{/owner}{/repo}",
                "subscriptions_url": "https://api.github.com/users/octocat/subscriptions",
                "organizations_url": "https://api.github.com/users/octocat/orgs",
                "repos_url": "https://api.github.com/users/octocat/repos",
                "events_url": "https://api.github.com/users/octocat/events{/privacy}",
                "received_events_url": "https://api.github.com/users/octocat/received_events",
                "type": "User",
                "site_admin": False,
            },
            "private": True,
            "html_url": "https://github.com/octocat/Hello-World-Private",
            "description": "This your first repo!",
            "fork": False,
            "url": "https://api.github.com/repos/octocat/Hello-World-Private",
            "archive_url": "https://api.github.com/repos/octocat/Hello-World-Private/{archive_format}{/ref}",
            "assignees_url": "https://api.github.com/repos/octocat/Hello-World-Private/assignees{/user}",
            "blobs_url": "https://api.github.com/repos/octocat/Hello-World-Private/git/blobs{/sha}",
            "branches_url": "https://api.github.com/repos/octocat/Hello-World-Private/branches{/branch}",
            "collaborators_url": "https://api.github.com/repos/octocat/Hello-World-Private/"
            "collaborators{/collaborator}",
            "comments_url": "https://api.github.com/repos/octocat/Hello-World-Private/comments{/number}",
            "commits_url": "https://api.github.com/repos/octocat/Hello-World-Private/commits{/sha}",
            "compare_url": "https://api.github.com/repos/octocat/Hello-World-Private/compare/{base}...{head}",
            "contents_url": "https://api.github.com/repos/octocat/Hello-World-Private/contents/{+path}",
            "contributors_url": "https://api.github.com/repos/octocat/Hello-World-Private/contributors",
            "deployments_url": "https://api.github.com/repos/octocat/Hello-World-Private/deployments",
            "downloads_url": "https://api.github.com/repos/octocat/Hello-World-Private/downloads",
            "events_url": "https://api.github.com/repos/octocat/Hello-World-Private/events",
            "forks_url": "https://api.github.com/repos/octocat/Hello-World-Private/forks",
            "git_commits_url": "https://api.github.com/repos/octocat/Hello-World-Private/git/commits{/sha}",
            "git_refs_url": "https://api.github.com/repos/octocat/Hello-World-Private/git/refs{/sha}",
            "git_tags_url": "https://api.github.com/repos/octocat/Hello-World-Private/git/tags{/sha}",
            "git_url": "git:github.com/octocat/Hello-World-Private.git",
            "issue_comment_url": "https://api.github.com/repos/octocat/Hello-World-Private/issues/comments{/number}",
            "issue_events_url": "https://api.github.com/repos/octocat/Hello-World-Private/issues/events{/number}",
            "issues_url": "https://api.github.com/repos/octocat/Hello-World-Private/issues{/number}",
            "keys_url": "https://api.github.com/repos/octocat/Hello-World-Private/keys{/key_id}",
            "labels_url": "https://api.github.com/repos/octocat/Hello-World-Private/labels{/name}",
            "languages_url": "https://api.github.com/repos/octocat/Hello-World-Private/languages",
            "merges_url": "https://api.github.com/repos/octocat/Hello-World-Private/merges",
            "milestones_url": "https://api.github.com/repos/octocat/Hello-World-Private/milestones{/number}",
            "notifications_url": "https://api.github.com/repos/octocat/Hello-World-Private/"
            "notifications{?since,all,participating}",
            "pulls_url": "https://api.github.com/repos/octocat/Hello-World-Private/pulls{/number}",
            "releases_url": "https://api.github.com/repos/octocat/Hello-World-Private/releases{/id}",
            "ssh_url": "git@github.com:octocat/Hello-World-Private.git",
            "stargazers_url": "https://api.github.com/repos/octocat/Hello-World-Private/stargazers",
            "statuses_url": "https://api.github.com/repos/octocat/Hello-World-Private/statuses/{sha}",
            "subscribers_url": "https://api.github.com/repos/octocat/Hello-World-Private/subscribers",
            "subscription_url": "https://api.github.com/repos/octocat/Hello-World-Private/subscription",
            "tags_url": "https://api.github.com/repos/octocat/Hello-World-Private/tags",
            "teams_url": "https://api.github.com/repos/octocat/Hello-World-Private/teams",
            "trees_url": "https://api.github.com/repos/octocat/Hello-World-Private/git/trees{/sha}",
            "clone_url": "https://github.com/octocat/Hello-World-Private.git",
            "mirror_url": "git:git.example.com/octocat/Hello-World-Private",
            "hooks_url": "https://api.github.com/repos/octocat/Hello-World-Private/hooks",
            "svn_url": "https://svn.github.com/octocat/Hello-World-Private",
            "homepage": "https://github.com",
            "language": None,
            "forks_count": 9,
            "stargazers_count": 80,
            "watchers_count": 80,
            "size": 108,
            "default_branch": "master",
            "open_issues_count": 0,
            "is_template": False,
            "topics": ["octocat", "atom", "electron", "api"],
            "has_issues": True,
            "has_projects": True,
            "has_wiki": True,
            "has_pages": False,
            "has_downloads": True,
            "archived": False,
            "disabled": False,
            "visibility": "public",
            "pushed_at": "2011-01-26T19:06:43Z",
            "created_at": "2011-01-26T19:01:12Z",
            "updated_at": "2011-01-26T19:14:43Z",
            "permissions": {"admin": False, "push": False, "pull": True},
            "template_repository": None,
        }
    ]


@fixture()
def not_found_organization_response():
    return {
        "message": "Not Found",
        "documentation_url": "https://docs.github.com/rest/reference/repos#list-organization-repositories",
    }


@fixture()
def github_response_enterprise_repo():
    return [
        {
            "id": 1234567,
            "node_id": "MDEwOlJlcG9zaXRvcnkxMjk2MjY5",
            "name": "Hello-World",
            "full_name": "octocat/Hello-World",
            "owner": {
                "login": "octocat",
                "id": 1,
                "node_id": "MDQ6VXNlcjE=",
                "avatar_url": "https://private.github.com/images/error/octocat_happy.gif",
                "gravatar_id": "",
                "url": "https://api.private.github.com/users/octocat",
                "html_url": "https://private.github.com/octocat",
                "followers_url": "https://api.private.github.com/users/octocat/followers",
                "following_url": "https://api.private.github.com/users/octocat/following{/other_user}",
                "gists_url": "https://api.private.github.com/users/octocat/gists{/gist_id}",
                "starred_url": "https://api.private.github.com/users/octocat/starred{/owner}{/repo}",
                "subscriptions_url": "https://api.private.github.com/users/octocat/subscriptions",
                "organizations_url": "https://api.private.github.com/users/octocat/orgs",
                "repos_url": "https://api.private.github.com/users/octocat/repos",
                "events_url": "https://api.private.github.com/users/octocat/events{/privacy}",
                "received_events_url": "https://api.private.github.com/users/octocat/received_events",
                "type": "User",
                "site_admin": False,
            },
            "private": False,
            "html_url": "https://private.github.com/octocat/Hello-World",
            "description": "This your first repo!",
            "fork": False,
            "url": "https://api.private.github.com/repos/octocat/Hello-World",
            "archive_url": "https://api.private.github.com/repos/octocat/Hello-World/{archive_format}{/ref}",
            "assignees_url": "https://api.private.github.com/repos/octocat/Hello-World/assignees{/user}",
            "blobs_url": "https://api.private.github.com/repos/octocat/Hello-World/git/blobs{/sha}",
            "branches_url": "https://api.private.github.com/repos/octocat/Hello-World/branches{/branch}",
            "collaborators_url": "https://api.private.github.com/repos/octocat/Hello-World"
            "/collaborators{/collaborator}",
            "comments_url": "https://api.private.github.com/repos/octocat/Hello-World/comments{/number}",
            "commits_url": "https://api.private.github.com/repos/octocat/Hello-World/commits{/sha}",
            "compare_url": "https://api.private.github.com/repos/octocat/Hello-World/compare/{base}...{head}",
            "contents_url": "https://api.private.github.com/repos/octocat/Hello-World/contents/{+path}",
            "contributors_url": "https://api.private.github.com/repos/octocat/Hello-World/contributors",
            "deployments_url": "https://api.private.github.com/repos/octocat/Hello-World/deployments",
            "downloads_url": "https://api.private.github.com/repos/octocat/Hello-World/downloads",
            "events_url": "https://api.private.github.com/repos/octocat/Hello-World/events",
            "forks_url": "https://api.private.github.com/repos/octocat/Hello-World/forks",
            "git_commits_url": "https://api.private.github.com/repos/octocat/Hello-World/git/commits{/sha}",
            "git_refs_url": "https://api.private.github.com/repos/octocat/Hello-World/git/refs{/sha}",
            "git_tags_url": "https://api.private.github.com/repos/octocat/Hello-World/git/tags{/sha}",
            "git_url": "git:private.github.com/octocat/Hello-World.git",
            "issue_comment_url": "https://api.private.github.com/repos/octocat/Hello-World/issues/comments{/number}",
            "issue_events_url": "https://api.private.github.com/repos/octocat/Hello-World/issues/events{/number}",
            "issues_url": "https://api.private.github.com/repos/octocat/Hello-World/issues{/number}",
            "keys_url": "https://api.private.github.com/repos/octocat/Hello-World/keys{/key_id}",
            "labels_url": "https://api.private.github.com/repos/octocat/Hello-World/labels{/name}",
            "languages_url": "https://api.private.github.com/repos/octocat/Hello-World/languages",
            "merges_url": "https://api.private.github.com/repos/octocat/Hello-World/merges",
            "milestones_url": "https://api.private.github.com/repos/octocat/Hello-World/milestones{/number}",
            "notifications_url": "https://api.private.github.com/repos/octocat/Hello-World/"
            "notifications{?since,all,participating}",
            "pulls_url": "https://api.private.github.com/repos/octocat/Hello-World/pulls{/number}",
            "releases_url": "https://api.private.github.com/repos/octocat/Hello-World/releases{/id}",
            "ssh_url": "git@private.github.com:octocat/Hello-World.git",
            "stargazers_url": "https://api.private.github.com/repos/octocat/Hello-World/stargazers",
            "statuses_url": "https://api.private.github.com/repos/octocat/Hello-World/statuses/{sha}",
            "subscribers_url": "https://api.private.github.com/repos/octocat/Hello-World/subscribers",
            "subscription_url": "https://api.private.github.com/repos/octocat/Hello-World/subscription",
            "tags_url": "https://api.private.github.com/repos/octocat/Hello-World/tags",
            "teams_url": "https://api.private.github.com/repos/octocat/Hello-World/teams",
            "trees_url": "https://api.private.github.com/repos/octocat/Hello-World/git/trees{/sha}",
            "clone_url": "https://private.github.com/octocat/Hello-World.git",
            "mirror_url": "git:git.example.com/octocat/Hello-World",
            "hooks_url": "https://api.private.github.com/repos/octocat/Hello-World/hooks",
            "svn_url": "https://svn.private.github.com/octocat/Hello-World",
            "homepage": "https://private.github.com",
            "language": None,
            "forks_count": 9,
            "stargazers_count": 80,
            "watchers_count": 80,
            "size": 108,
            "default_branch": "master",
            "open_issues_count": 0,
            "is_template": False,
            "topics": ["octocat", "atom", "electron", "api"],
            "has_issues": True,
            "has_projects": True,
            "has_wiki": True,
            "has_pages": False,
            "has_downloads": True,
            "archived": False,
            "disabled": False,
            "visibility": "public",
            "pushed_at": "2011-01-26T19:06:43Z",
            "created_at": "2011-01-26T19:01:12Z",
            "updated_at": "2011-01-26T19:14:43Z",
            "permissions": {"admin": False, "push": False, "pull": True},
            "template_repository": None,
        }
    ]


@responses.activate
def test_obtain_repos_retrieves_one_repo(github_organization, github_response_one_repo):
    github_url = f"https://api.github.com/orgs/{github_organization}/repos"
    responses.get(
        github_url,
        json=github_response_one_repo,
        status=200,
        match=[
            matchers.query_param_matcher({"per_page": 100}),
            matchers.header_matcher(
                {
                    "Accept": "application/vnd.github.v3+json",
                    "X-GitHub-Api-Version": "2022-11-28",
                }
            ),
        ],
    )

    result = obtain_repos(
        github_organization=github_organization,
        github_token=None,
    )

    assert len(result) == 1


@responses.activate
def test_obtain_repos_with_token_retrieves_one_public_repo_and_one_private_repo(
    github_organization,
    github_response_one_repo,
    github_response_one_private_repo,
):
    github_url = f"https://api.github.com/orgs/{github_organization}/repos"
    responses.get(
        github_url,
        json=github_response_one_repo + github_response_one_private_repo,
        status=200,
        match=[
            matchers.query_param_matcher({"per_page": 100}),
            matchers.header_matcher(
                {
                    "Accept": "application/vnd.github.v3+json",
                    "X-GitHub-Api-Version": "2022-11-28",
                    "Authorization": "token random_token",
                }
            ),
        ],
    )

    result = obtain_repos(
        github_organization=github_organization,
        github_token="random_token",
    )

    assert len(result) == 2


@responses.activate
def test_obtain_repos_raises_exception_if_organization_is_not_found(
    not_found_organization_response,
):
    github_url = "https://api.github.com/orgs/NOTANORG/repos"
    responses.get(
        github_url,
        json=not_found_organization_response,
        status=404,
        match=[
            matchers.query_param_matcher({"per_page": 100}),
            matchers.header_matcher(
                {
                    "Accept": "application/vnd.github.v3+json",
                    "X-GitHub-Api-Version": "2022-11-28",
                }
            ),
        ],
    )

    with raises(HTTPError):
        result = obtain_repos(
            github_organization="NOTANORG",
            github_token=None,
        )
        assert len(result) == 0


@responses.activate
def test_obtain_repos_can_append_repos_if_there_are_more_than_one_page(
    github_organization, github_response_one_repo, github_response_one_private_repo
):
    github_url = f"https://api.github.com/orgs/{github_organization}/repos"
    responses.get(
        github_url,
        json=github_response_one_repo,
        status=200,
        headers=[
            (
                "link",
                '<https://api.github.com/organizations/123456/repos?page=2>; rel="next"',
            )
        ],
        match=[
            matchers.query_param_matcher({"per_page": 100}),
            matchers.header_matcher(
                {
                    "Accept": "application/vnd.github.v3+json",
                    "X-GitHub-Api-Version": "2022-11-28",
                }
            ),
        ],
    )
    responses.get(
        "https://api.github.com/organizations/123456/repos",
        json=github_response_one_private_repo,
        status=200,
        match=[
            matchers.query_param_matcher({"page": 2, "per_page": 100}),
            matchers.header_matcher(
                {
                    "Accept": "application/vnd.github.v3+json",
                    "X-GitHub-Api-Version": "2022-11-28",
                }
            ),
        ],
    )

    result = obtain_repos(
        github_organization=github_organization,
        github_token="random_token",
    )

    assert len(result) == 2


@responses.activate
def test_obtain_repos_from_ghe_retrieves_one_repo(github_organization, github_response_enterprise_repo):
    github_url = f"https://private.ghe.com/api/v3/orgs/{github_organization}/repos"
    token = "random_token"
    responses.get(
        github_url,
        json=github_response_enterprise_repo,
        status=200,
        match=[
            matchers.query_param_matcher({"per_page": 100}),
            matchers.header_matcher(
                {
                    "Accept": "application/vnd.github+json",
                    "Authorization": f"Bearer {token}",
                }
            ),
        ],
    )

    result = obtain_repos(
        github_organization=github_organization,
        github_token=token,
        ghe="private.ghe.com",
    )

    assert len(result) == 1


def test_obtain_repos_raises_exception_if_token_is_none_when_cloning_from_ghe(
    not_found_organization_response,
):
    with raises(TokenNotFoundForGHEException):
        result = obtain_repos(
            github_organization="NOTANORG",
            github_token=None,
            ghe="123",
        )
        assert len(result) == 0
