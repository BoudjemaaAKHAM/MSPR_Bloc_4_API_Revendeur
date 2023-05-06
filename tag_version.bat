for /f "tokens=2 delims==" %%a in ('python .\get_version.py') do set "v=%%a"
echo Tagging version %v%
git tag -a %v% -m "Tag version %v%"
git push --tags