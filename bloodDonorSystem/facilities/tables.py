import django_tables2 as tables
from users.models import Donation, Request
import itertools
from django.utils.html import format_html


class FacilityDonationsTable(tables.Table):
    row_number = tables.Column(
        orderable=False,
        empty_values=(),
        verbose_name='#'
    )

    email = tables.Column(accessor='user.user.email', verbose_name='Email',
                          attrs={'td': {'class': 'email-col'}})
    phone = tables.Column(accessor='user.phone', verbose_name='Phone')
    blood_type = tables.Column(
        accessor='user.blood_group', verbose_name='Blood Type')

    actions = tables.TemplateColumn(
        template_name='facility/donations/row-actions.html',
        verbose_name='Actions',
        orderable=False
    )

    class Meta:
        model = Donation
        fields = ('row_number', 'user', 'email', 'phone', 'blood_type', 'donation_type',
                  'amount', 'donation_date', 'status', 'approval_status', 'actions')

        sequence = ('row_number', 'user', 'email', 'phone', 'blood_type', 'donation_type',
                    'amount',  'status', 'donation_date', 'approval_status', 'actions')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.counter = itertools.count(1)

    def render_row_number(self):
        return f"{next(self.counter)}"

    def render_user(self, record):
        return f"{record.user.firstname} {record.user.lastname}"

    def render_amount(self, record):
        return f"{record.amount} ml"

    def render_status(self, record):
        if record.status == 'completed':
            return format_html("<p class='flex items-center gap-2'> <i data-lucide='check' class='size-4' stroke-width='2'></i> Completed</p>")
        elif record.status == 'scheduled':
            return format_html("<p class='flex items-center gap-2'> <i data-lucide='clock' class='size-4' stroke-width='2'></i> Scheduled</p>")
        elif record.status == 'cancelled':
            return format_html("<p class='flex items-center gap-2'> <i data-lucide='x' class='size-4' stroke-width='2'></i> Cancelled</p>")

    def render_approval_status(self, record):
        if record.approval_status == 'approved':
            return format_html("<p class='flex items-center gap-2'> <i data-lucide='check' class='size-4' stroke-width='2'></i> Approved</p>")
        elif record.approval_status == 'rejected':
            return format_html("<p class='flex items-center gap-2'> <i data-lucide='x' class='size-4' stroke-width='2'></i> Rejected</p>")
        elif record.approval_status == 'pending':
            return format_html("<p class='flex items-center gap-2'> <i data-lucide='hourglass' class='size-4' stroke-width='2'></i> Pending</p>")


class FaciltyRequestsTable(tables.Table):

    row_number = tables.Column(
        orderable=False,
        empty_values=(),
        verbose_name='#'
    )

    email = tables.Column(
        accessor='user.user.email',
        verbose_name='Email',
        attrs={'td': {'class': 'email-col'}}
    )

    phone = tables.Column(accessor='user.phone', verbose_name='Phone')
    blood_type = tables.Column(
        accessor='user.blood_group', verbose_name='Blood Type')

    actions = tables.TemplateColumn(
        template_name='facility/requests/row-actions.html',
        verbose_name='Actions',
        orderable=False
    )

    request_amount = tables.Column(
        verbose_name='Amount'
    )
    urgency_level = tables.Column(
        verbose_name='Urgency'
    )
    request_status = tables.Column(
        verbose_name='Progress'
    )
    user = tables.Column(
        verbose_name='Individual'
    )

    class Meta:
        model = Request
        fields = ('row_number', 'user', 'email',  'blood_type', 'request_type',
                  'request_amount', 'urgency_level', 'request_status', 'needed_by', 'approval_status', 'actions')

        sequence = ('row_number', 'user', 'email',  'blood_type', 'request_type',
                    'request_amount', 'urgency_level', 'request_status', 'needed_by', 'approval_status', 'actions')

        exclude = ('phone',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        self.counter = itertools.count(1)

    def render_row_number(self, record):
        return f"{next(self.counter)}"

    def render_user(self, record):
        return f"{record.user.firstname} {record.user.lastname}"

    def render_request_amount(self, record):
        return f"{record.request_amount} ml"

    def render_request_status(self, record):
        if record.request_status == 'completed':
            return format_html("<p class='flex items-center gap-2'> <i data-lucide='check' class='size-4' stroke-width='2'></i> Completed</p>")
        elif record.request_status == 'scheduled':
            return format_html("<p class='flex items-center gap-2'> <i data-lucide='clock' class='size-4' stroke-width='2'></i> Scheduled</p>")
        elif record.request_status == 'cancelled':
            return format_html("<p class='flex items-center gap-2'> <i data-lucide='x' class='size-4' stroke-width='2'></i> Cancelled</p>")

    def render_approval_status(self, record):
        if record.approval_status == 'approved':
            return format_html("<p class='flex items-center gap-2'> <i data-lucide='check' class='size-4' stroke-width='2'></i> Approved</p>")
        elif record.approval_status == 'rejected':
            return format_html("<p class='flex items-center gap-2'> <i data-lucide='x' class='size-4' stroke-width='2'></i> Rejected</p>")
        elif record.approval_status == 'pending':
            return format_html("<p class='flex items-center gap-2'> <i data-lucide='hourglass' class='size-4' stroke-width='2'></i> Pending</p>")
