
Domain Model
------------

Grano defines a set of domain model objects that are used internally 
but also exposed through a REST API. Beyond a few basic objects 
(Network, Account, Schema), the domain model should be understood
as a set of building blocks rather than a fixed set of entities
and properties: the API is reflective and will generate new database 
tables, data validators and classes as defined through schemata.

**What is a Network?**

A ``Network`` is an isolated dataset within a grano installation, 
representing a specific graph. It will contain a set of ``Schema`` 
definitions, ``Entities`` and ``Relations``. Technically, each 
network is represented through a distinct set of tables in the 
database. These are automatically generated. 

**What are Entities and Relations?**

Within a ``Network``, all data is expressed in terms of ``Entities``
(or nodes) and ``Relations`` (or edges). By default, they have a 
few attributes, such as a ``title``, ``description`` and ``id`` for
``Entities`` and ``source``, ``target`` (as references) and an ``id``
for ``Relations``. A few service fields, such as ``created_at``, 
``type``, ``current`` and ``serial`` also exist - see below. Relations 
must  always be associated with two distinct entities, dangling 
references or loops are not permitted. 

**What are Schemata?***

Unlike RDF, Grano is based around the idea of a rich graph in which 
each node can have an arbitrary number of freely defined attributes.
This does not, however, mean that Grano is schema-less. Instead, 
schemata for both Entities and Relations can be specified at run 
time and define the names, types and labels for additional attributes
on graph elements. 

Whenever an Entity or Relation is created, it's ``type`` must be
specified to select the applicable schema. Grano will then validate
fields in the incoming data against the attribute definitions of that
schema.

**What are Queries?**

Queries are a work-around, they may go away in the future.

While graph models are particularly appropriate to express the 
relationships between entities in a network, they are not as useful
with regards to simpler, table-oriented questions like: which are
the entities with the highest value of attribute X? 

To enable such queries, we allow users to submit raw SQL queries. 
They are stored as domain objects and can be called by any user 
(i.e. only a network administrator can define the query everyone
else gets to run it).

This is a horrible idea from a number of points of view. 

**What are Accounts?**

A number of ``Accounts`` represent the users in the system. In a 
later stage of development, they will be able to take different 
roles with regards to a ``Network``, giving them administrative, 
read-write or read-only access to its data.

**How does versioning work?**

Entities and relations - the nodes and edges of the graph - are
versioned. Each write operation will create a complete copy of the
object that shares the ID of all other versions of the object. It
will be distinguished from other versions through a serial number,
identifying the time at which it was created. 

Further, a ``current`` flag will be set for exactly one version of 
each revisioned object. This need not necessarily be the latest one, 
but it will be returned from queries by default. Relations inside the 
graph are also set up to always link to the current revision of the
object, i.e. links update themselves.














Design Considerations
---------------------

Project goals include:

* Provide an easy way to model, store and explore actor networks.
* Customization of edge and node types, schema.
* Multi-tenancy, multiple networks with access control.
* Revisioning of edge and node data, moderated operations.
* Bulk import via API and user-friendly web forms for data entry.
* Simple export for advanced analytics or visualization.
* Built-in support for simple network metrics.

Goals don't include:

* Scale, i.e. more than 10mn nodes.
* Extensive Visualization of the data.
* Re-implementation of network metric algorithms (use existing
  implementations where available).
* RDF.
* Discovering the world conspiracy.

Random decisions:

* Directed multigraph.
* Schema changes at run time

Storage Mechanism
-----------------

Options: 

* Graph database (Neo4J): Can store graph flexibly; native
  representation. Yet not well explored as storage mechanism,
  constraints on supported complexity. Bad language bindings.
* RDF Triplestore (4Store, Virtuoso): Can store triple representation of
  data, but awkward modeling in RDF. F/OSS triple stores not mature,
  client bindings and SPARUL not ready.
* Document store (Couch, Mongo): Works well, but document model may be
  inappropriate for graph representation. 
* Relational DBMS (Postgres, MySQL): Known failure at modelling graphs,
  but lots of workarounds available, mature client libraries. 

-> DECISION: Don't go down the technology rabbit hole. We'll just use 
a plain RDBMS and work around the impedance, rather than paying the 
cost of immature technolgies or scaring off developers who cannot 
live in with a more exotic choice. 