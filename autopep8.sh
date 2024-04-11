set -e
echo autopep8: `which autopep8`, version: `autopep8 --version`
autopep8 --diff -r services
autopep8 --in-place -r services