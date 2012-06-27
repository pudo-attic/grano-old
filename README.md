Grano - open source social network analysis web platform
========================================================

Grano is an engine for running web sites that perform some sort of social
network analysis. Instances can be used in efforts to determine actor
relations in any number of domains, such as politics, business or crime.

The software is aimed at journalists and advocates who want to track 
networked structures, and we hope to cover some of the main activities 
necessary for such analysis:

* Schema creation, i.e. defining different types of actors and relations
  and their respective properties. 
* Data upload and integration, to easily add actors (or other entities)
  and links through the upload of structured data, such as spreadsheets.
* Easy-to-use full text search and navigation functions to explore the 
  database in a manner similar to a modern social networking site.
* Annotation facilities to allow users to make notes which attach to one
  or many entities (potentially later adding entity extraction to 
  automatically detect entities mentioned in a piece of text).
* Reporting tools to query the properties of entities and relations and
  to create lists and rankings.
* Graph metrics to determine actors which have a high centrality or
  betweenness.
* Visualization tools to power graph visualizations.
* An API to enable other uses of the site, e.g. as a backend store to 
  topic-specific applications. 
* Access control, allowing users to share all or part of a network, while
  keeping other networks fully private (e.g. during an investigation).


Current status
--------------

The system currently has a working, albeit limited, REST API that can be
used to store and retrieve versioned network information, to execute 
stored queries and to perform full-text search. 

The application does not currently have its own UI (the idea is to make 
a bootstrap-based interface sitting on top of the API) or support for 
bulk data import. 


Installation and Usage
----------------------

In order to run Grano you will need to have Python 2.7 installed and a
PostgreSQL database available on which Grano requires administrative
privileges. (At the moment, all tests run against SQLite but full-text
search - which is not covered - uses Postgres-specific features).

We strongly recommend that the application should be run from within its
own ``virtualenv``, a sandboxed install of the required Python 
dependencies. In general, the process for setting up Grano should be 
as follows::

# Check out Grano from Github
$ git clone http://github.com/pudo/grano

# Change into the working copy and make a virtualenv
$ cd grano
$ virtualenv env 
$ source env/bin/activate

# Install the dependencies 
$ python setup.py develop

# Set up a local config file:
$ cp grano/default_settings.py settings.py 
# edit the file to have a working DB connection string etc.
$ export GRANO_SETTINGS=settings.py

# Finally, run Grano:
$ python grano/web.py 


More Information
----------------

More information is available in the following files:

* DESIGN - outlines the main design considerations and the domain 
  model.
* API - gives instructions on using the web API

This is an open source project, everyone is invited to suggest or
implement new features. 
* We'll use the GitHub bugtracker to track ideas, bugs and features. 


Links, References and Prior Art
-------------------------------

* [LittleSis](http://littlesis.org/)
* [Influcence Networks](http://app.owni.fr/influence-networks/)
* [Blog post](http://pudo.org/2011/12/19/sna.html) lining out some
  rationale for this.
* [NetworkX](http://networkx.lanl.gov/) - python library.
* [Strength of Weak Ties](http://sociology.stanford.edu/people/mgranovetter/documents/granstrengthweakties.pdf), to explain the name ;)




