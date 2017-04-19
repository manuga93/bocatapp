from customer.models import Comment


def get_stars(local_id):
    comments = Comment.objects.filter(local=local_id)
    res = 0.
    if comments.count() != 0:
        for i in comments:
            res = res + i.rating
        res = res / comments.count()


    return res
