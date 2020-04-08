import json

def is_json(myjson):
  try:
    json_object = json.loads(myjson)
  except ValueError as e:
    return False
  return True


def person_group_type(pg_type):

    if pg_type == 'emailuser':
         return 1 
    if pg_type == 'taskgroup':
         return 0
    if pg_type == 'group':
         return 2

    return None
