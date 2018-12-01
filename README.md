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

and install Firefox and [geckodriver](https://github.com/mozilla/geckodriver/releases).

## Features (done)

- Archives associated review conversations
- Provides Change-Id based search
- Archives associated patch files
- Archives all Change Sets
- Archives all Patch Sets
- Archive file diff pages if 50 files or less

## Features (todo)

- Archives *Open*, *Merged*, and *Abandoned* pages
