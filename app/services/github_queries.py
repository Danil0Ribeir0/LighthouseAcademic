COMMIT_HISTORY_QUERY = """
query($owner: String!, $name: String!, $branch: String!, $cursor: String) {
  repository(owner: $owner, name: $name) {
    ref(qualifiedName: $branch) {
      target {
        ... on Commit {
          history(first: 100, after: $cursor) {
            pageInfo {
              hasNextPage
              endCursor
            }
            nodes {
              oid
              committedDate
              additions
              deletions
              author {
                user {
                  login
                }
                name
              }
            }
          }
        }
      }
    }
  }
}
"""