
git diff

echo 'Enter commit message:'
read msg
echo %msg%

git add --all
git commit -m "%msg%"
git push

