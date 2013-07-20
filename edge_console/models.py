# encoding: utf-8

from django.db import models

class Salog(models.Model):

    LOG_TYPE_CHOICES = (
        (1, 'idc-预维护'),
        (2, '故障记录'),
    )

    log_type = models.SmallIntegerField(
        '类型', choices=LOG_TYPE_CHOICES, default=1, db_index=True,
        help_text='')

    isp = models.ForeignKey('ISP', help_text="", blank=True, null=True)
    idc = models.ForeignKey('IDC', help_text="", blank=True, null=True)

    record_type = models.CharField("类型", max_length=128, db_index=True,
                              help_text="")

    operator = models.CharField("操作人", max_length=128, db_index=True,
                              help_text="。")

    memo = models.TextField("备注", default='',
                      help_text="")

    send_email = models.BooleanField("send email", default=False)

    start_time = models.DateTimeField("操作开始的时间", null=True, db_index=True)
    end_time = models.DateTimeField("截止的时间", null=True, db_index=True)


    class Meta:
        verbose_name = "Salog"
        verbose_name_plural = "Salog"
        db_table = 'salog'

    def __unicode__(self):
        return u"%s: %s" % (self.idc, self.record_type)