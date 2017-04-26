from customer.models import Report, Comment

def accept_report(report_id):
    report = Report.objects.get(id=report_id)
    comment = Comment.objects.get(id=report.comment_id)
    report.accepted=True
    comment.reported=True

    report.save()
    comment.save()

def decline_report(report_id):
    report = Report.objects.get(id=report_id)
    report.decline=True

    report.save()