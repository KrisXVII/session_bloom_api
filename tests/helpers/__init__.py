
def response_fields(records, *fields):
	return [{field: record[field] for field in fields} for record in records]

def list_fields(records, *fields):
	return [{field: getattr(record, field) for field in fields} for record in records]
