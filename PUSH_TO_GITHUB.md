# Push this existing repository to GitHub

The ZIP contains a hidden `.git` directory and already has the required stage-by-stage commit history.
Do **not** delete `.git` and do not upload the files one by one through GitHub's web uploader, because that would lose the commit history.

## Steps

1. Extract the ZIP.
2. Open a terminal inside the extracted `task-crud-api-assignment` folder.
3. Create an empty **public** GitHub repository. Do not initialize it with a README, `.gitignore`, or license.
4. Run:

```bash
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
git push -u origin main
```

5. Confirm the commits:

```bash
git log --oneline
```

You should see Stage 0 through Stage 6 as separate commits.
