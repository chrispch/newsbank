MONGO_HOST = 'localhost'
MONGO_PORT = 27017
MONGO_USERNAME = 'newsbank'
MONGO_PASSWORD = 'newsbank'
MONGO_DBNAME = 'newsbank'

ALLOW_UNKNOWN = False
X_DOMAINS = '*'
X_HEADERS = ['Authorization','Content-type']

users_schema = {
    'u_id': {
        'type': 'string',
        'required': True,
        'unique': True,
    }
}

saved_articles_schema = {
    'article_id': {
        'type':'string',
        'required': True
    },
    'u_id': {
        'type':'string',
        'required': True
    },
    'starred': {
        'type':'boolean',
        'required': True
    },
    'labels': {
        'type':'list'
    }
}

comments_schema = {
        'article_id': {
            'type':'string',
            'required': True
        },
        'u_id': {
            'type':'string',
            'required': True
        },
        'comment_text': {
            'type':'string',
            'required':True
        },
        'start_char': {
            'type':'integer'
        },
        'end_char': {
            'type':'integer'
        }
}

articles_schema = {
    'site': {
        'type': 'string',
        'required': True
    },
    'category': {
        'type': 'string',
        'required': True
    },
    'title': {
        'type': 'string',
        'required': True
    },
    'abstract': {
        'type': 'string',
        'required': True
    },
    'full_text': {
        'type': 'string',
        'required': True
    },
    'date_seconds': {
        'type': 'float',
        'required': True
    },
    'author': {
        'type': 'string',
        'required': True
    },
    'href': {
        'type': 'string',
        'required': True
    },
    
}

articles = {
    'item_title': 'article',
    'resource_methods': ['GET', 'POST'],
    'schema': articles_schema
}


users = {
    'item_title': 'user',
    'additional_lookup': {
        'url': 'regex("[\w]+")',
        'field': 'u_id'
    },
    'resource_methods': ['GET', 'POST'],
    'schema': users_schema
}

saved_articles = {
    'item_title': 'saved_article',
    'resource_methods': ['GET', 'POST'],
    'schema': saved_articles_schema
}

comments = {
    'item_title': 'comment',
    'resource_methods': ['GET', 'POST'],
    'schema': comments_schema
}

DOMAIN = {
            'users': users,
            'articles': articles,
            'saved_articles': saved_articles,
            'comments': comments
         }
