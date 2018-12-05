Gerrit Static Archive
----------------------

Create a static website archive of a [Gerrit Code
Review](https://www.gerritcodereview.com/) instance. Keep a record of all
review discussions and proposed code changes.

Developed and tested against Gerrit 2.12-1-g6f7dc21 with Python 3.6.6 for
http://review.source.kitware.com. Requires Python >= 3.6. Also,

```
pip install -r requirements.txt
```

and install Firefox and [geckodriver](https://github.com/mozilla/geckodriver/releases).

## Features

- Archives associated review conversations
- Provides Change-Id based search
- Archives associated patch files
- Archives all Change Sets
- Archives all Patch Sets
- Archive update to 30 file diff pages per Patch Set
- Archives *Open*, *Merged*, and *Abandoned* pages

This may serve as a useful reference for mirroring other Gerrit instances or
other GWT applications, but it will likely require some degree of porting effort.
