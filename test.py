import logging

from icecream import ic

log = logging.getLogger(__name__)
plugins = [{
    'id': 226408450,
    'node_id': 'MDEwOlJlcG9zaXRvcnkyMjY0MDg0NTA=',
    'name': 'neovide',
    'full_name': 'neovide/neovide',
    'private': False,
    'owner': {
        'login': 'neovide',
        'id': 88021264,
        'node_id': 'MDEyOk9yZ2FuaXphdGlvbjg4MDIxMjY0',
        'avatar_url': 'https://avatars.githubusercontent.com/u/88021264?v=4',
        'gravatar_id': '',
        'url': 'https://api.github.com/users/neovide',
        'html_url': 'https://github.com/neovide',
        'followers_url': 'https://api.github.com/users/neovide/followers',
        'following_url':
            'https://api.github.com/users/neovide/following{/other_user}',
        'gists_url': 'https://api.github.com/users/neovide/gists{/gist_id}',
        'starred_url':
            'https://api.github.com/users/neovide/starred{/owner}{/repo}',
        'subscriptions_url':
            'https://api.github.com/users/neovide/subscriptions',
        'organizations_url': 'https://api.github.com/users/neovide/orgs',
        'repos_url': 'https://api.github.com/users/neovide/repos',
        'events_url': 'https://api.github.com/users/neovide/events{/privacy}',
        'received_events_url':
            'https://api.github.com/users/neovide/received_events',
        'type': 'Organization',
        'site_admin': False
    },
    'html_url': 'https://github.com/neovide/neovide',
    'description': 'No Nonsense Neovim Client in Rust',
    'fork': False,
    'url': 'https://api.github.com/repos/neovide/neovide',
    'forks_url': 'https://api.github.com/repos/neovide/neovide/forks',
    'keys_url': 'https://api.github.com/repos/neovide/neovide/keys{/key_id}',
    'collaborators_url':
        'https://api.github.com/repos/neovide/neovide/collaborators{/collaborator}',
    'teams_url': 'https://api.github.com/repos/neovide/neovide/teams',
    'hooks_url': 'https://api.github.com/repos/neovide/neovide/hooks',
    'issue_events_url':
        'https://api.github.com/repos/neovide/neovide/issues/events{/number}',
    'events_url': 'https://api.github.com/repos/neovide/neovide/events',
    'assignees_url':
        'https://api.github.com/repos/neovide/neovide/assignees{/user}',
    'branches_url':
        'https://api.github.com/repos/neovide/neovide/branches{/branch}',
    'tags_url': 'https://api.github.com/repos/neovide/neovide/tags',
    'blobs_url': 'https://api.github.com/repos/neovide/neovide/git/blobs{/sha}',
    'git_tags_url':
        'https://api.github.com/repos/neovide/neovide/git/tags{/sha}',
    'git_refs_url':
        'https://api.github.com/repos/neovide/neovide/git/refs{/sha}',
    'trees_url': 'https://api.github.com/repos/neovide/neovide/git/trees{/sha}',
    'statuses_url':
        'https://api.github.com/repos/neovide/neovide/statuses/{sha}',
    'languages_url': 'https://api.github.com/repos/neovide/neovide/languages',
    'stargazers_url': 'https://api.github.com/repos/neovide/neovide/stargazers',
    'contributors_url':
        'https://api.github.com/repos/neovide/neovide/contributors',
    'subscribers_url':
        'https://api.github.com/repos/neovide/neovide/subscribers',
    'subscription_url':
        'https://api.github.com/repos/neovide/neovide/subscription',
    'commits_url': 'https://api.github.com/repos/neovide/neovide/commits{/sha}',
    'git_commits_url':
        'https://api.github.com/repos/neovide/neovide/git/commits{/sha}',
    'comments_url':
        'https://api.github.com/repos/neovide/neovide/comments{/number}',
    'issue_comment_url':
        'https://api.github.com/repos/neovide/neovide/issues/comments{/number}',
    'contents_url':
        'https://api.github.com/repos/neovide/neovide/contents/{+path}',
    'compare_url':
        'https://api.github.com/repos/neovide/neovide/compare/{base}...{head}',
    'merges_url': 'https://api.github.com/repos/neovide/neovide/merges',
    'archive_url':
        'https://api.github.com/repos/neovide/neovide/{archive_format}{/ref}',
    'downloads_url': 'https://api.github.com/repos/neovide/neovide/downloads',
    'issues_url': 'https://api.github.com/repos/neovide/neovide/issues{/number}',
    'pulls_url': 'https://api.github.com/repos/neovide/neovide/pulls{/number}',
    'milestones_url':
        'https://api.github.com/repos/neovide/neovide/milestones{/number}',
    'notifications_url':
        'https://api.github.com/repos/neovide/neovide/notifications{?since,all,participating}',
    'labels_url': 'https://api.github.com/repos/neovide/neovide/labels{/name}',
    'releases_url': 'https://api.github.com/repos/neovide/neovide/releases{/id}',
    'deployments_url':
        'https://api.github.com/repos/neovide/neovide/deployments',
    'created_at': '2019-12-06T20:51:39Z',
    'updated_at': '2024-03-07T11:06:26Z',
    'pushed_at': '2024-03-07T14:17:31Z',
    'git_url': 'git://github.com/neovide/neovide.git',
    'ssh_url': 'git@github.com:neovide/neovide.git',
    'clone_url': 'https://github.com/neovide/neovide.git',
    'svn_url': 'https://github.com/neovide/neovide',
    'homepage': 'https://neovide.dev',
    'size': 80663,
    'stargazers_count': 11643,
    'watchers_count': 11643,
    'language': 'Rust',
    'has_issues': True,
}, {
    'id': 101762821,
    'node_id': 'MDEwOlJlcG9zaXRvcnkxMDE3NjI4MjE=',
    'name': 'CrossHair',
    'full_name': 'pschanely/CrossHair',
    'private': False,
    'owner': {
        'login': 'pschanely',
        'id': 332622,
        'node_id': 'MDQ6VXNlcjMzMjYyMg==',
        'avatar_url': 'https://avatars.githubusercontent.com/u/332622?v=4',
        'gravatar_id': '',
        'url': 'https://api.github.com/users/pschanely',
        'html_url': 'https://github.com/pschanely',
        'followers_url': 'https://api.github.com/users/pschanely/followers',
        'following_url':
            'https://api.github.com/users/pschanely/following{/other_user}',
        'gists_url': 'https://api.github.com/users/pschanely/gists{/gist_id}',
        'starred_url':
            'https://api.github.com/users/pschanely/starred{/owner}{/repo}',
        'subscriptions_url':
            'https://api.github.com/users/pschanely/subscriptions',
        'organizations_url': 'https://api.github.com/users/pschanely/orgs',
        'repos_url': 'https://api.github.com/users/pschanely/repos',
        'events_url': 'https://api.github.com/users/pschanely/events{/privacy}',
        'received_events_url':
            'https://api.github.com/users/pschanely/received_events',
        'type': 'User',
        'site_admin': False
    },
    'html_url': 'https://github.com/pschanely/CrossHair',
    'description':
        'An analysis tool for Python that blurs the line between testing and type systems.',
    'fork': False,
    'url': 'https://api.github.com/repos/pschanely/CrossHair',
    'forks_url': 'https://api.github.com/repos/pschanely/CrossHair/forks',
    'keys_url': 'https://api.github.com/repos/pschanely/CrossHair/keys{/key_id}',
    'collaborators_url':
        'https://api.github.com/repos/pschanely/CrossHair/collaborators{/collaborator}',
    'teams_url': 'https://api.github.com/repos/pschanely/CrossHair/teams',
    'hooks_url': 'https://api.github.com/repos/pschanely/CrossHair/hooks',
    'issue_events_url':
        'https://api.github.com/repos/pschanely/CrossHair/issues/events{/number}',
    'events_url': 'https://api.github.com/repos/pschanely/CrossHair/events',
    'assignees_url':
        'https://api.github.com/repos/pschanely/CrossHair/assignees{/user}',
    'branches_url':
        'https://api.github.com/repos/pschanely/CrossHair/branches{/branch}',
    'tags_url': 'https://api.github.com/repos/pschanely/CrossHair/tags',
    'blobs_url':
        'https://api.github.com/repos/pschanely/CrossHair/git/blobs{/sha}',
    'git_tags_url':
        'https://api.github.com/repos/pschanely/CrossHair/git/tags{/sha}',
    'git_refs_url':
        'https://api.github.com/repos/pschanely/CrossHair/git/refs{/sha}',
    'trees_url':
        'https://api.github.com/repos/pschanely/CrossHair/git/trees{/sha}',
    'statuses_url':
        'https://api.github.com/repos/pschanely/CrossHair/statuses/{sha}',
    'languages_url':
        'https://api.github.com/repos/pschanely/CrossHair/languages',
    'stargazers_url':
        'https://api.github.com/repos/pschanely/CrossHair/stargazers',
    'contributors_url':
        'https://api.github.com/repos/pschanely/CrossHair/contributors',
    'subscribers_url':
        'https://api.github.com/repos/pschanely/CrossHair/subscribers',
    'subscription_url':
        'https://api.github.com/repos/pschanely/CrossHair/subscription',
    'commits_url':
        'https://api.github.com/repos/pschanely/CrossHair/commits{/sha}',
    'git_commits_url':
        'https://api.github.com/repos/pschanely/CrossHair/git/commits{/sha}',
    'comments_url':
        'https://api.github.com/repos/pschanely/CrossHair/comments{/number}',
    'issue_comment_url':
        'https://api.github.com/repos/pschanely/CrossHair/issues/comments{/number}',
    'contents_url':
        'https://api.github.com/repos/pschanely/CrossHair/contents/{+path}',
    'compare_url':
        'https://api.github.com/repos/pschanely/CrossHair/compare/{base}...{head}',
    'merges_url': 'https://api.github.com/repos/pschanely/CrossHair/merges',
    'archive_url':
        'https://api.github.com/repos/pschanely/CrossHair/{archive_format}{/ref}',
    'downloads_url':
        'https://api.github.com/repos/pschanely/CrossHair/downloads',
    'issues_url':
        'https://api.github.com/repos/pschanely/CrossHair/issues{/number}',
    'pulls_url':
        'https://api.github.com/repos/pschanely/CrossHair/pulls{/number}',
    'milestones_url':
        'https://api.github.com/repos/pschanely/CrossHair/milestones{/number}',
    'notifications_url':
        'https://api.github.com/repos/pschanely/CrossHair/notifications{?since,all,participating}',
    'labels_url':
        'https://api.github.com/repos/pschanely/CrossHair/labels{/name}',
    'releases_url':
        'https://api.github.com/repos/pschanely/CrossHair/releases{/id}',
    'deployments_url':
        'https://api.github.com/repos/pschanely/CrossHair/deployments',
    'created_at': '2017-08-29T13:11:40Z',
    'updated_at': '2024-02-26T18:24:46Z',
    'pushed_at': '2024-02-28T19:50:06Z',
    'git_url': 'git://github.com/pschanely/CrossHair.git',
    'ssh_url': 'git@github.com:pschanely/CrossHair.git',
    'clone_url': 'https://github.com/pschanely/CrossHair.git',
    'svn_url': 'https://github.com/pschanely/CrossHair',
    'homepage': '',
    'size': 4483,
    'stargazers_count': 929,
    'watchers_count': 929,
    'language': 'Python',
    'has_issues': True
}, {
    'id': 767429452,
    'node_id': 'R_kgDOLb4LTA',
    'name': 'mattern.nvim',
    'full_name': 'domsch1988/mattern.nvim',
    'private': False,
    'owner': {
        'login': 'domsch1988',
        'id': 1961154,
        'node_id': 'MDQ6VXNlcjE5NjExNTQ=',
        'avatar_url': 'https://avatars.githubusercontent.com/u/1961154?v=4',
        'gravatar_id': '',
        'url': 'https://api.github.com/users/domsch1988',
        'html_url': 'https://github.com/domsch1988',
        'followers_url': 'https://api.github.com/users/domsch1988/followers',
        'following_url':
            'https://api.github.com/users/domsch1988/following{/other_user}',
        'gists_url': 'https://api.github.com/users/domsch1988/gists{/gist_id}',
        'starred_url':
            'https://api.github.com/users/domsch1988/starred{/owner}{/repo}',
        'subscriptions_url':
            'https://api.github.com/users/domsch1988/subscriptions',
        'organizations_url': 'https://api.github.com/users/domsch1988/orgs',
        'repos_url': 'https://api.github.com/users/domsch1988/repos',
        'events_url': 'https://api.github.com/users/domsch1988/events{/privacy}',
        'received_events_url':
            'https://api.github.com/users/domsch1988/received_events',
        'type': 'User',
        'site_admin': False
    },
    'html_url': 'https://github.com/domsch1988/mattern.nvim',
    'description': 'Custom Pattern base Marks for NeoVIM',
    'fork': False,
    'url': 'https://api.github.com/repos/domsch1988/mattern.nvim',
    'forks_url': 'https://api.github.com/repos/domsch1988/mattern.nvim/forks',
    'keys_url':
        'https://api.github.com/repos/domsch1988/mattern.nvim/keys{/key_id}',
    'collaborators_url':
        'https://api.github.com/repos/domsch1988/mattern.nvim/collaborators{/collaborator}',
    'teams_url': 'https://api.github.com/repos/domsch1988/mattern.nvim/teams',
    'hooks_url': 'https://api.github.com/repos/domsch1988/mattern.nvim/hooks',
    'issue_events_url':
        'https://api.github.com/repos/domsch1988/mattern.nvim/issues/events{/number}',
    'events_url': 'https://api.github.com/repos/domsch1988/mattern.nvim/events',
    'assignees_url':
        'https://api.github.com/repos/domsch1988/mattern.nvim/assignees{/user}',
    'branches_url':
        'https://api.github.com/repos/domsch1988/mattern.nvim/branches{/branch}',
    'tags_url': 'https://api.github.com/repos/domsch1988/mattern.nvim/tags',
    'blobs_url':
        'https://api.github.com/repos/domsch1988/mattern.nvim/git/blobs{/sha}',
    'git_tags_url':
        'https://api.github.com/repos/domsch1988/mattern.nvim/git/tags{/sha}',
    'git_refs_url':
        'https://api.github.com/repos/domsch1988/mattern.nvim/git/refs{/sha}',
    'trees_url':
        'https://api.github.com/repos/domsch1988/mattern.nvim/git/trees{/sha}',
    'statuses_url':
        'https://api.github.com/repos/domsch1988/mattern.nvim/statuses/{sha}',
    'languages_url':
        'https://api.github.com/repos/domsch1988/mattern.nvim/languages',
    'stargazers_url':
        'https://api.github.com/repos/domsch1988/mattern.nvim/stargazers',
    'contributors_url':
        'https://api.github.com/repos/domsch1988/mattern.nvim/contributors',
    'subscribers_url':
        'https://api.github.com/repos/domsch1988/mattern.nvim/subscribers',
    'subscription_url':
        'https://api.github.com/repos/domsch1988/mattern.nvim/subscription',
    'commits_url':
        'https://api.github.com/repos/domsch1988/mattern.nvim/commits{/sha}',
    'git_commits_url':
        'https://api.github.com/repos/domsch1988/mattern.nvim/git/commits{/sha}',
    'comments_url':
        'https://api.github.com/repos/domsch1988/mattern.nvim/comments{/number}',
    'issue_comment_url':
        'https://api.github.com/repos/domsch1988/mattern.nvim/issues/comments{/number}',
    'contents_url':
        'https://api.github.com/repos/domsch1988/mattern.nvim/contents/{+path}',
    'compare_url':
        'https://api.github.com/repos/domsch1988/mattern.nvim/compare/{base}...{head}',
    'merges_url': 'https://api.github.com/repos/domsch1988/mattern.nvim/merges',
    'archive_url':
        'https://api.github.com/repos/domsch1988/mattern.nvim/{archive_format}{/ref}',
    'downloads_url':
        'https://api.github.com/repos/domsch1988/mattern.nvim/downloads',
    'issues_url':
        'https://api.github.com/repos/domsch1988/mattern.nvim/issues{/number}',
    'pulls_url':
        'https://api.github.com/repos/domsch1988/mattern.nvim/pulls{/number}',
    'milestones_url':
        'https://api.github.com/repos/domsch1988/mattern.nvim/milestones{/number}',
    'notifications_url':
        'https://api.github.com/repos/domsch1988/mattern.nvim/notifications{?since,all,participating}',
    'labels_url':
        'https://api.github.com/repos/domsch1988/mattern.nvim/labels{/name}',
    'releases_url':
        'https://api.github.com/repos/domsch1988/mattern.nvim/releases{/id}',
    'deployments_url':
        'https://api.github.com/repos/domsch1988/mattern.nvim/deployments',
    'created_at': '2024-03-05T09:26:40Z',
    'updated_at': '2024-03-07T01:17:50Z',
    'pushed_at': '2024-03-05T14:49:18Z',
    'git_url': 'git://github.com/domsch1988/mattern.nvim.git',
    'ssh_url': 'git@github.com:domsch1988/mattern.nvim.git',
    'clone_url': 'https://github.com/domsch1988/mattern.nvim.git',
    'svn_url': 'https://github.com/domsch1988/mattern.nvim',
    'homepage': None,
    'size': 32,
    'stargazers_count': 8,
    'watchers_count': 8,
    'language': 'Lua',
    'has_issues': True
}, {
    'id': 636697601,
    'node_id': 'R_kgDOJfM8AQ',
    'name': 'neorg-exec',
    'full_name': 'laher/neorg-exec',
    'private': False,
    'owner': {
        'login': 'laher',
        'id': 125845,
        'node_id': 'MDQ6VXNlcjEyNTg0NQ==',
        'avatar_url': 'https://avatars.githubusercontent.com/u/125845?v=4',
        'gravatar_id': '',
        'url': 'https://api.github.com/users/laher',
        'html_url': 'https://github.com/laher',
        'followers_url': 'https://api.github.com/users/laher/followers',
        'following_url':
            'https://api.github.com/users/laher/following{/other_user}',
        'gists_url': 'https://api.github.com/users/laher/gists{/gist_id}',
        'starred_url':
            'https://api.github.com/users/laher/starred{/owner}{/repo}',
        'subscriptions_url': 'https://api.github.com/users/laher/subscriptions',
        'organizations_url': 'https://api.github.com/users/laher/orgs',
        'repos_url': 'https://api.github.com/users/laher/repos',
        'events_url': 'https://api.github.com/users/laher/events{/privacy}',
        'received_events_url':
            'https://api.github.com/users/laher/received_events',
        'type': 'User',
        'site_admin': False
    },
    'html_url': 'https://github.com/laher/neorg-exec',
    'description': 'code block execution for neorg (similar to org-eval)',
    'fork': False,
    'url': 'https://api.github.com/repos/laher/neorg-exec',
    'forks_url': 'https://api.github.com/repos/laher/neorg-exec/forks',
    'keys_url': 'https://api.github.com/repos/laher/neorg-exec/keys{/key_id}',
    'collaborators_url':
        'https://api.github.com/repos/laher/neorg-exec/collaborators{/collaborator}',
    'teams_url': 'https://api.github.com/repos/laher/neorg-exec/teams',
    'hooks_url': 'https://api.github.com/repos/laher/neorg-exec/hooks',
    'issue_events_url':
        'https://api.github.com/repos/laher/neorg-exec/issues/events{/number}',
    'events_url': 'https://api.github.com/repos/laher/neorg-exec/events',
    'assignees_url':
        'https://api.github.com/repos/laher/neorg-exec/assignees{/user}',
    'branches_url':
        'https://api.github.com/repos/laher/neorg-exec/branches{/branch}',
    'tags_url': 'https://api.github.com/repos/laher/neorg-exec/tags',
    'blobs_url': 'https://api.github.com/repos/laher/neorg-exec/git/blobs{/sha}',
    'git_tags_url':
        'https://api.github.com/repos/laher/neorg-exec/git/tags{/sha}',
    'git_refs_url':
        'https://api.github.com/repos/laher/neorg-exec/git/refs{/sha}',
    'trees_url': 'https://api.github.com/repos/laher/neorg-exec/git/trees{/sha}',
    'statuses_url':
        'https://api.github.com/repos/laher/neorg-exec/statuses/{sha}',
    'languages_url': 'https://api.github.com/repos/laher/neorg-exec/languages',
    'stargazers_url': 'https://api.github.com/repos/laher/neorg-exec/stargazers',
    'contributors_url':
        'https://api.github.com/repos/laher/neorg-exec/contributors',
    'subscribers_url':
        'https://api.github.com/repos/laher/neorg-exec/subscribers',
    'subscription_url':
        'https://api.github.com/repos/laher/neorg-exec/subscription',
    'commits_url': 'https://api.github.com/repos/laher/neorg-exec/commits{/sha}',
    'git_commits_url':
        'https://api.github.com/repos/laher/neorg-exec/git/commits{/sha}',
    'comments_url':
        'https://api.github.com/repos/laher/neorg-exec/comments{/number}',
    'issue_comment_url':
        'https://api.github.com/repos/laher/neorg-exec/issues/comments{/number}',
    'contents_url':
        'https://api.github.com/repos/laher/neorg-exec/contents/{+path}',
    'compare_url':
        'https://api.github.com/repos/laher/neorg-exec/compare/{base}...{head}',
    'merges_url': 'https://api.github.com/repos/laher/neorg-exec/merges',
    'archive_url':
        'https://api.github.com/repos/laher/neorg-exec/{archive_format}{/ref}',
    'downloads_url': 'https://api.github.com/repos/laher/neorg-exec/downloads',
    'issues_url':
        'https://api.github.com/repos/laher/neorg-exec/issues{/number}',
    'pulls_url': 'https://api.github.com/repos/laher/neorg-exec/pulls{/number}',
    'milestones_url':
        'https://api.github.com/repos/laher/neorg-exec/milestones{/number}',
    'notifications_url':
        'https://api.github.com/repos/laher/neorg-exec/notifications{?since,all,participating}',
    'labels_url': 'https://api.github.com/repos/laher/neorg-exec/labels{/name}',
    'releases_url':
        'https://api.github.com/repos/laher/neorg-exec/releases{/id}',
    'deployments_url':
        'https://api.github.com/repos/laher/neorg-exec/deployments',
    'created_at': '2023-05-05T12:43:47Z',
    'updated_at': '2024-02-04T00:23:02Z',
    'pushed_at': '2024-01-07T09:35:15Z',
    'git_url': 'git://github.com/laher/neorg-exec.git',
    'ssh_url': 'git@github.com:laher/neorg-exec.git',
    'clone_url': 'https://github.com/laher/neorg-exec.git',
    'svn_url': 'https://github.com/laher/neorg-exec',
    'homepage': None,
    'size': 169,
    'stargazers_count': 30,
    'watchers_count': 30,
    'language': 'Lua',
    'has_issues': True
}]

unwanted_config = [
    "dotfiles", "dots", "nvim-dotfiles", "nvim-qt", "nvim-config", "neovim-lua",
    "vim-config", "config-nvim",
]
ignore_list = [
    "lspconfig", "lsp_config", "cmp", "coq", "neorg", "norg", "neovide"
]

def key_mapper(key):
    """
    helper for working with annoying dicts and lists of dicts
    runs a function over external iterable on a specific dict key

    Examples:
    --------

    >>> d = {'a':1, 'b':2}
    >>> d2 = {'a':0, 'b':2}
    >>> l = [0,2,3,4,5,6,7]
    >>> a_mapper = key_mapper('a')
    >>> b_mapper = key_mapper('b')
    >>> equals_l = b_mapper(lambda x,y: x == y, l)
    >>> equals_l(d)
    >>> # 0
    >>> equals_l(d2)
    >>> # 1

    Parameters
    ----------
    key : key to map a function over



    Returns
    -------
    cond_mapper : function which takes in a function which asserts a condition over an iterable, and returns a function which runs the supplied function over the supplied iterable and the input

    """

    def cond_mapper(fn, iterable):
        """

        Parameters
        ----------
        fn : a callable, which takes in 2 positional args, the first of which is supplied later on, and the second of which comes from the supplied iterable

        iterable : list of parameters to supply to fn


        Returns
        -------
        output : a function which takes in a dict, indexes it with previously supplied key, and compares that index to a previously supplied iterable

        """

        def output(d: dict):
            # logging.info(ic.format(d))
            return sum(
                fn(d[key], x) if key in d.keys() else 0 for x in iterable)

        return output

    return cond_mapper

def make_jobs(base) -> None:
    """
    Given a response list, generate jobs(read: sets of parameters) for extract_data to run asynchronously
    Iterates through the response list, and for each one, creates a plugin or dotfile job. For some edge cases,
    it creates a list of jobs to parse some html relating to the plugin or dotfile, and uses the result of that to create more jobs

    Parameters
    ----------
    base : BaseRequestResponse


    """
    name_mapper = key_mapper("name")  # uses d['name']
    fullname_mapper = key_mapper("full_name")  # uses d['full_name']
    description_mapper = key_mapper("description")  # uses d['description']
    language_mapper = key_mapper("language")
    ends_nvim = fullname_mapper(
        lambda x,
        y: x.lower().endswith(y.lower()), [".nvim", "-nvim", ".vim"],
    )  # checks if d['full_name'] ends with .nvim, -nvim, .vim
    begins_dot = name_mapper(
        lambda x, y: x.lower().startswith(y.lower()),
        ".")  # check if d['name'] starts with '.'

    def name_function(x, y):
        return any(x.lower().startswith(ig.lower()) for ig in y)


    fixed_plugin_conds = [
    ]
    fixed_dotfile_conds = [
        fullname_mapper(
            lambda x, y: y.lower() in x.lower(),unwanted_config
        ),  # checks if any of the unwanted config names are in d['full_name']
        description_mapper(
            lambda x,
            y: y.lower() in x.lower() if x is not None else 0,
            unwanted_config,
        ),  # check if any of the unwanted config names are in d['description']
    ]
    both_conditions = [
        language_mapper(
            lambda x, y: x.lower() == "lua", ["lua"]
        )
    ]

    optional_plugin_conds = [
        ends_nvim,


    ]
    optional_dotfile_conds = [
        begins_dot,
    ]

    conds = (fixed_plugin_conds,fixed_dotfile_conds)
    cases = {
        # mappings for conditions based on conditions
        (1, 0): "plugin_count",
        (0, 1): "dotfile_count",
    }




    def make_jobtype(response):
        plugin_data = response
        # case = tuple(min(1, sum(cn(plugin_data) for cn in c)) for c in conds)
        # case = tuple(map(lambda c: sum(cn(plugin_data) for cn in c), conds))
        # case = tuple(map(lambda x: min(1, x), case))

        case = custom_case(plugin_data)

        if case in cases.keys():
            return (plugin_data, bool(case[0]))
        else:
            return (plugin_data,)

    [make_jobtype(i) for i in base]

make_jobs(plugins)
