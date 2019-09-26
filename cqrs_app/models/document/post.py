def get_more_like_this(es, post):
    params = {
        'query': {
            'more_like_this': {
                'fields': ['title', 'body'],
                'like': {
                    '_index': 'post',
                    '_id': post.id,
                },
            },
        },
    }

    return es.search(index=['post'], body=params).get('hits').get('hits')
