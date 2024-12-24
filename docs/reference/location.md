# Location

The [location](api/project_forge/models/location.md) is a hashable reference to a source. A location consists of a `url` and `path` combination.

All fields that accept a [location](api/project_forge/models/location.md) object will also accept a string representing a URL _or_ a path. So the following are equivalent:

```toml title="Locations specified by strings"
overlays = [
  { pattern_location = "python-package/pattern.toml" },
  { pattern_location = "https://github.com/owner/repository/" },
]
```

```toml title="Locations specified by objects"
overlays = [
  { pattern_location = { path = "python-package/pattern.toml" } },
  { pattern_location = { url = "https://github.com/owner/repository/" } },
]
```

At least one of `path` or `url` must be specified. Here is how the `url` and `path` attributes work together:

- **`url` specified, `path` specified:** The `path` is resolved using the root of the repository. Relative paths cannot resolve to locations outside the repository.

- **`url` specified, `path` unspecified:** The `path` is the root of the repository.

- **`url` unspecified, `path` specified:** The `path` is resolved using the local filesystem and current working directory.

## Supported URL formats

- **Normal URLs:** `scheme://netloc/path;parameters?query#fragment`
- **SSH urls:** `user@domain/path`

## Path formats

- relative or absolute path to the object within the URL or local filesystem

## Recipes

### Specify branches, tags, or commits

**GitHub**

- `https://github.com/owner/repository/tree/[branch-or-tag]`
- `https://github.com/owner/repository/commit/[commit-SHA]`

**GitLab**

- `https://gitlab.com/owner/repository/-/tree/[branch-or-tag]`
- `https://gitlab.com/owner/repository/-/commit/[commit-SHA]`

**Using `@` or `#`**

- `https://<domain>/owner/repository@[branch/tag/commit]`
- `https://<domain>/owner/repository#[branch/tag/commit]`

### Specify a directory within a URL

Specify both the `url` and the `path` attributes. The `path` should be the path from the root of the repository to the location.
