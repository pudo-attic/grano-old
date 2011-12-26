Installation instructions
=========================

For a developer install, a simple checkout in a virtualenv is sufficient::

  virtualenv env
  source env/bin/activate
  git clone https://github.com/pudo/grano
  cd grano
  pip install -e .

If you need to set local settings, create a copy of the file 
``grano/default_settings.py`` in the run-time directory, modify it to 
your needs and then set the environment variable ``GRANO_SETTINGS`` to 
point to the new file.


