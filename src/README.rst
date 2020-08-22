So I wanted to rewrite pyreadline.
So winreadline.
But for the actual layout, I wanted all of the python stuff
in a folder called src.

Top Level
============
At the top level of this repo can be all the random ass git shit.

.gitconfig .gitignore .gitattributes
setup.py !!
maybe a scripts folder, docs, and test.

Then in src is the shit that's not exactly related but related enough.

tox.ini
pytest.ini
meta.yaml
pyproject.toml
.flake8.cfg
Pipfile

With both of those at the top level, your repos start looking really cluttered.

So let's try separating!
