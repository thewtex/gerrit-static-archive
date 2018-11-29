Gerrit Static Archive
----------------------

Create a static website archive of a [Gerrit Code
Review](https://www.gerritcodereview.com/) instance. Keep a record of all
review discussions and proposed code changes.

Developed and tested against Gerrit 2.12-1-g6f7dc21 with Python 3.6.6 for
http://review.source.kitware.com.

Also,

```
pip install -r requirements.txt
```

## Features (done)

- Archives associated review conversations
- Provides Change-Id based search

## Features (todo)

- Archives all Change Sets
- Archives all Patch Sets
- Archives associated patch files
- Git repositories with named branches for patch sets
- Archives *Open*, *Merged*, and *Abandoned* pages
