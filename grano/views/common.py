from itertools import groupby

from grano.core import db
from grano.exc import BadRequest


def split_fields(field):
    key, value = field.split(':', 1)
    if key in ('source', 'target'):
        key = key + '_id'
    return (key, value)


def filtered_query(type_, request, fts=False):
    query = type_.all()
    try:
        filter_ = [split_fields(f) for f in request.args.getlist('filter')]
        for key, values in groupby(filter_, lambda a: a[0]):
            attr = getattr(type_, key)
            clause = db.or_(*[attr == v[1] for v in values])
            query = query.filter(clause)
        if fts:
            q = request.args.get('q', '').strip()
            if len(q):
                query = query.filter('_fts @@ to_tsquery(:q)')
                query = query.order_by('ts_rank_cd(_fts, plainto_tsquery(:q)) DESC')
                query = query.params(q=q)
        count = query.count()
        query = query.limit(min(10000, int(request.args.get('limit', 100))))
        query = query.offset(int(request.args.get('offset', 0)))
        return count, query
    except (ValueError, AttributeError, IndexError) as e:
        raise BadRequest(e)
