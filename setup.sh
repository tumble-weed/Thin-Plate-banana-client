pip install -r requirements.txt
# prevent secrets from accidentally being commited
git update-index --skip-worktree secrets.json
