DEBUG = True
SECRET_KEY = 'no'
SITE_TITLE = 'lobbytransparency.eu'
REGISTRATION = True
SQLALCHEMY_DATABASE_URI = 'sqlite:///grano.db'
SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/grano_dev'


# HACK HACK - Need a proper mechanism for this.
STORED_QUERIES = {
    'test': {
        'label': 'Test Query',
        'query': 'SELECT * FROM entity_actor'
        },
    's1': {
        'label': 'TOP N companies (C II: companies and groups) spending most on lobbying',
        'query': 'SELECT id, title, "contactCountry", "fdCostAbsolute" as expenditure FROM entity_actor WHERE "subCategoryId" = 21 ORDER BY "fdCostAbsolute" DESC'
    }
}
