import sqlite3


conn = sqlite3.connect('./pageRank/spider.sqlite')
cur = conn.cursor()

# make a list of all from id without repeat
cur.execute('SELECT DISTINCT from_id FROM Links')
from_ids = list()
for row in cur:
    from_ids.append(row[0])

# print(from_ids) # [1, 2, 4, 3, 13, 12, 10, 9]

# find the ids that reveive page rank
to_ids = list()
links = list()
cur.execute('SELECT DISTINCT from_id, to_id FROM Links')
for row in cur:
    from_id = row[0]
    to_id = row[1]
    if (from_id == to_id) or (from_id not in from_ids) or (to_id not in from_ids): continue
    links.append(row)
    if to_id not in to_ids: to_ids.append(to_id)


# print(to_ids, links) # [2, 3, 1, 4, 9, 10, 12, 13] [(1, 2), (1, 3), (2, 1), (2, 4), (2, 9), (2, 10), (2, 12), (2, 13), (4, 2), (4, 10), (13, 1), (13, 4), (13, 9), (13, 10), (13, 12), (12, 2), (12, 3), (10, 2), (10, 4), (9, 2)]
# get all ranks and save them
prev_ranks = dict()
for node in from_ids:
    cur.execute('SELECT new_rank FROM Pages WHERE id = ?' ,(node, ))
    row = cur.fetchone()
    prev_ranks[node] = row[0]

sval = input('How many iterations: ')
many = 1
if len(sval) > 0 : many = int(sval)

# sanity check
if len(prev_ranks) < 1:
    print('Nothing to page rank.  Check data.')
    quit()

# Do page rank memory to make this fast
for i in range(many):
    next_ranks = dict()
    total = 0.0

    # get the sum of all old ranks and init new_ranks dict
    for (node, old_rank) in list(prev_ranks.items()):
        total = total + old_rank
        next_ranks[node] = 0.0
        # print(total)
    
    # Find the number of outbound Links and sent the page rank down each
    for (node, old_rank) in list(prev_ranks.items()):
        give_ids = list()
        for (from_id, to_id) in links:
            if from_id != node or to_id not in to_ids: continue
            # print(from_id, to_id)
            give_ids.append(to_id)

        if( len(give_ids) < 1) : continue
        amount = old_rank / len(give_ids)
        # print(node, old_rank, amount, give_ids)
        # 1 1.0 0.5 [2, 3]
        # 2 1.0 0.16666666666666666 [1, 4, 9, 10, 12, 13]
        # 4 1.0 0.5 [2, 10]
        # 13 1.0 0.2 [1, 4, 9, 10, 12]
        # 12 1.0 0.5 [2, 3]
        # 10 1.0 0.5 [2, 4]
        # 9 1.0 1.0 [2]




    