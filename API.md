

API
---

The graph API must enable read/write operations on both entites and 
relations. A resource layout could look like this:

* ``/api/1/types/entity`` - allow users to see metadata on registered
  entity types. Only ``GET``. Detailed view required?
* ``/api/1/types/relation`` - same for relations.
* ``/api/1/networks`` - network (i.e. tenant of the system), listing via
  ``GET`` and creation via ``POST``. Deletion probably not required.
* ``/api/1/<network>`` - network instance, ``GET`` and ``PUT``. 
* ``/api/1/<network>/entity`` - collection of entities in a
  specified network. Can be paginated through with ``GET``, new entities
  can be created with ``POST`` and bulk updates performed with ``PUT``.
* ``/api/1/<network>/entity/<id>`` - entity ``id``, supports
  ``GET`` and ``PUT``. This may or may not include the adjacency list,
  which may also be stored in its own sub-resource (e.g.
  ``.../relations``, or ``.../incoming``; ``.../outgoing``).
* ``/api/1/<network>/rel/<id>`` - relation ``id``, ``PUT`` and 
  ``GET``.

Open questions:

* History API
* Granular/non-revisioned write operations, such as HEAD pointer move.
* Is ``/api/1/net/<network>/rel`` a proper resource (i.e. the full 
  adjacency list)?

Entity (node) representation::

    {
      "id": 483,
      "current": true,
      "serial": 201201010,
      "created_at": 2012-01-01 01:01:01.1111,
      "slug": "dngela-merkel",
      "title": "Dr. Angela Merkel",
      "tagline": "Chancellor of the Federal Republic of Germany",
      "description": "....",
      "type": "person",
      /* Type-specific schema: */
      "birth_date": ...,
      "death_date": null,
      "place_of_birth": "Osten"
    }

Relation (edge) representation::

    {
      "id": 944847527,
      "current": true,
      "serial": 20121212235911,
      "created_at": 2012-12-12 23:59:11.0000,
      "type": "owner_of",
      "source": {
          "id": 3883,
          "uri": "/api/1/net/foo/entity/3883",
          "title": "Some person",
          "type": "person"
        },
      "target": {
          "id": 4,
          "uri": "/api/1/net/foo/entity/4"
          "title": "Cool Jetboat",
          "type": "asset"
        },
      "acquisition_date": null
    }




REST API
--------

The first iteration of the API will expose three primary resources: 
``network``, ``entity`` and ``relation``. Each of those expose basic
CRUD methods to list, read and write the data. The read and write
representations are usually equivalent. The REST API uses JSON for 
up- and download, although generic form data is supported for all 
write operations as well.

**Network**

* ``GET /api/1/networks`` - list all the stored networks. This is a 
  list of slugs that can be resolved individually to retrieve more 
  data.
* ``POST /api/1/networks`` - create a new network; requires at least 
  a ``title``, optionally a ``description`` and ``slug`` can also be
  submitted. If ``slug`` is missing, it will be derived from the 
  ``title``. After the initial creation, the ``slug`` will become 
  immutable.
* ``GET /api/1/networks/<slug>`` - retrieve a full JSON representation
  of a specific network, identified by ``slug``. 
* ``PUT /api/1/networks/<slug>`` - update a network by submitting a 
  modified form of its representation. ``slug`` cannot be changed.
* ``DELETE /api/1/networks/<slug>`` - delete a network; this does not 
  actually remove the record but flags it as deleted in the database.

**Entity**

* ``GET /api/1/entities`` - list all ids of entities in the database.
* ``GET /api/1/network/<slug>/entities`` - list all ids of entities 
  in the given network.
* ``POST /api/1/entities`` - create a new entity; requires at least 
  a ``title`` and a ``type``, optionally a ``description``, ``summary``
  and ``slug`` can also be submitted. If ``slug`` is missing, it will
  be derived from the ``title``. Further, any additional fields 
  mandated by the schema given through ``type`` must also be specified.
* ``GET /api/1/entities/<id>`` - retrieve a full JSON representation
  of a specific entity, identified by ``id``. 
* ``GET /api/1/entities/<id>/history`` - retrieve the full history of
  the entity identified by ``id``, including the full JSON 
  representation of all prior revisions.
* ``PUT /api/1/entities/<id>`` - update an entity by submitting a 
  modified form of its representation. ``type`` (and thus the required
  set of dependent attributes) cannot be changed.
* ``DELETE /api/1/entities/<id>`` - delete an entity; this does not 
  actually remove the record but removes any ``current`` flag from the
  database.

**Relation**

* ``GET /api/1/relations`` - list all ids of relations in the database.
* ``GET /api/1/network/<slug>/relations`` - list all ids of relations 
  in the given network.
* ``POST /api/1/relations`` - create a new relation; requires at least 
  a ``type`` and both ``source`` and ``target`` to be valid entity IDs
  Further, any additional fields mandated by the schema given through 
  ``type`` must also be specified.
* ``GET /api/1/relations/<id>`` - retrieve a full JSON representation
  of a specific relation, identified by ``id``. 
* ``GET /api/1/relations/<id>/history`` - retrieve the full history of
  the relation identified by ``id``, including the full JSON 
  representation of all prior revisions.
* ``PUT /api/1/relations/<id>`` - update a relation by submitting a 
  modified form of its representation. ``source``, ``target`` and 
  ``type`` (and thus the required set of dependent attributes) cannot 
  be changed.
* ``DELETE /api/1/relations/<id>`` - delete a relatin; this does not 
  actually remove the record but removes any ``current`` flag from the
  database.

**Schema**

* ``GET /api/1/schemata/entity`` - list the names of all schemata for 
  entities. 
* ``GET /api/1/schemata/relation`` - list the names of all schemata for 
  relations. 
* ``GET /api/1/schemata/[entity|relation]/<name>`` - get the full JSON 
  representation of a specific schema type.

Authentication and authorization is not yet available in the current 
version.