MONGO_HOST = 'localhost'
MONGO_PORT = 27017
MONGO_USERNAME = 'newsbank'
MONGO_PASSWORD = 'newsbank'
MONGO_DBNAME = 'newsbank'

ALLOW_UNKNOWN = True
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
    'article_id': {
        'type': 'string',
        'required': True,
        'unique': True,
    },
    'site': {
        'type': 'string',
    },
    'category': {
        'type': 'string',
    },
    'title': {
        'type': 'string',
    },
    'abstract': {
        'type': 'string',
    },
    'date': {
        'type': 'string',
    },
    'author': {
        'type': 'string',
    },
    'href': {
        'type': 'string',
    },
    
}

articles = {
    'item_title': 'article',

    'additional_lookup': {
        'url': 'regex("[\w]+")',
        'field': 'article_id'
    },

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
