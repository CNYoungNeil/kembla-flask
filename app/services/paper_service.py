from app.models.paper_model import Paper


def listAll():
	list_paper = Paper.query.all()
	return [p.to_dict() for p in list_paper]