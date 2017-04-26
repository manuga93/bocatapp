from customer.models import Comment


def get_stars(local_id):
    comments = Comment.objects.filter(local=local_id)
    aux = 0.
    if comments.count() != 0:
        for i in comments:
            aux = aux + int(i.rating)
        aux = aux / comments.count()

    res = str(round(aux, 2))

    return res
