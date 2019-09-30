def get_friends_of_friends(db, username):
    aql = '''
LET user = DOCUMENT('User', @user)
FOR v, e, p IN 1..10 OUTBOUND user Following
    SORT(LENGTH(p.vertices)) ASC

    RETURN p.vertices
    '''
    results = db.aql.execute(aql, bind_vars={'user': username})

    return list(results)
