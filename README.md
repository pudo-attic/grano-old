Grano - open source social network web analysis
===============================================

Grano is an engine for running social network discovery and analysis 
sites. Such sites can be used in efforts to determine actor relations
in any number of domains, such as politics, business or crime.



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
* Schema changes at run time?

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


API
---

The graph API must enable read/write operations on both entites and 
relations. A resource layout could look like this:

* ``/api/1/net`` - network (i.e. tenant of the system), listing via
  ``GET`` and creation via ``POST``. Deletion probably not required.
* ``/api/1/net/<network>`` - network instance, ``GET`` and ``PUT``. 
* ``/api/1/net/<network>/entity`` - collection of entities in a
  specified network. Can be paginated through with ``GET``, new entities
  can be created with ``POST`` and bulk updates performed with ``PUT``.
* ``/api/1/net/<network>/entity/<id>`` - entity ``id``, supports
  ``GET`` and ``PUT``. This may or may not include the adjacency list,
  which may also be stored in its own sub-resource (e.g.
  ``.../relations``, or ``.../incoming``; ``.../outgoing``).
* ``/api/1/net/<network>/rel/<id>`` - relation ``id``, ``PUT`` and 
  ``GET``.

Open questions:

* History API
* Granular/non-revisioned write operations, such as HEAD pointer move.
* Is ``/api/1/net/<network>/rel`` a proper resource (i.e. the full 
  adjacency list)?




