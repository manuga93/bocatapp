from customer.models import Report, Comment
import itertools

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

def commentsWithReports():
    reports = Report.objects.all().filter(accepted=False, decline=False)
    grouped = itertools.groupby(reports, lambda report: report.comment)
    #res = dict((r.comment, r) for r in reports)
    res = dict((r.comment, reports.filter(comment_id=r.comment.pk)) for r in reports)
    #res = {c: r for c, r in grouped}
    #res = dict((c,r) for c,r in grouped)
    return res