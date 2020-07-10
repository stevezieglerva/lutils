git status
git diff

echo 'Enter commit message:'
read msg
echo "Using $msg"

git add --all
git commit -m "$msg"
git push

