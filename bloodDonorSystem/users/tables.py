import django_tables2 as tables
from .models import Donation, Request
from facilities.models import FacilityProfile
import itertools
from django.utils.html import format_html
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
import django_filters


class DonationTable(tables.Table):
    row_number = tables.Column(
        empty_values=(),
        verbose_name='#',
        orderable=False,
    )

    status = tables.Column(
        attrs={
            'td': {
                'class': lambda record: 'status-{}'. format(record.status)}}
    )

    actions = tables.TemplateColumn(
        template_name="user/donations/row-actions.html", verbose_name="actions", orderable=False)

    class Meta:
        model = Donation
        fields = ('row_number', 'facility', 'donation_type',
                  'donation_date', 'status', 'approval_status', 'actions')

        sequence = ('row_number', 'facility', 'donation_type', 'status',
                    'donation_date', 'approval_status', 'actions')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.counter = itertools.count(1)

    def render_row_number(self):
        return f"{next(self.counter)}"

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


class RequestsTable(tables.Table):
    row_number = tables.Column(
        empty_values=(),
        orderable=False,
        verbose_name='#'
    )

    actions = tables.TemplateColumn(
        template_name="user/requests/requests-row-actions.html", verbose_name="actions", orderable=False)

    class Meta:
        model = Request
        fields = ('row_number', 'facility', 'request_type',
                  'request_amount', 'request_status', 'urgency_level', 'needed_by', 'approval_status', 'actions')

        sequence = ('row_number', 'facility', 'request_type',
                    'request_amount', 'request_status', 'needed_by', 'urgency_level', 'approval_status', 'actions')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.counter = itertools.count(1)

    def render_row_number(self):
        return f"{next(self.counter)}"

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


