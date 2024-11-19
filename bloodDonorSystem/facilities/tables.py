import django_tables2 as tables
from users.models import Donation, Request, UserProfile
from .models import Inventory, BloodUnit
import itertools
from django.utils.html import format_html
from django.utils.timezone import localdate


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


class InventoryTable(tables.Table):

    row_number = tables.Column(
        orderable=False,
        empty_values=(),
        verbose_name='#'
    )

    blood_type = tables.Column(verbose_name='Blood Type')
    total_quantity = tables.Column(verbose_name='Total Quantity (L)')
    units_received = tables.Column(verbose_name='Units Received')
    available_units = tables.Column(verbose_name='Available Units')
    restock_status = tables.Column(verbose_name='Restock Status')
    updated_at = tables.DateTimeColumn(verbose_name='Last Updated')

    class Meta:
        fields = ('row_number', 'blood_type', 'total_quantity',
                  'units_received', 'available_units', 'restock_status', 'updated_at')
        sequence = fields

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.counter = itertools.count(1)

    def render_row_number(self, record):
        return f"{next(self.counter)}"

    def render_total_quantity(self, record):
        return f"{record['total_quantity']} L"

    def render_units_received(self, record):
        return record['units_received']

    def render_available_units(self, record):
        return record['available_units']

    def render_restock_status(self, record):
        return record['restock_status']

    def render_updated_at(self, record):
        return record['updated_at'].strftime("%Y-%m-%d, %H:%M")


class BloodUnitsTable(tables.Table):
    row_number = tables.Column(
        orderable=False,
        empty_values=(),
        verbose_name='#'
    )

    days_left = tables.Column(
        verbose_name="Days Left",
        empty_values=(),
        orderable=False
    )

    class Meta:
        model = BloodUnit
        fields = ('row_number', "unit_id", "donor", "blood_type", "quantity",
                  "donation_type", "collection_date", 'expiration_date', 'days_left', 'status')
        sequence = ('row_number', "unit_id", "donor", "blood_type", "quantity",
                    "donation_type", "collection_date", 'expiration_date', 'days_left', 'status')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.counter = itertools.count(1)

    def render_row_number(self, record):
        return f"{next(self.counter)}"

    def render_donor(self, record):
        return f"{record.donor.firstname} {record.donor.lastname}"

    def render_quantity(self, record):
        return f"{record.quantity} ml"

    def render_days_left(self, record):
        today = localdate()
        if record.expiration_date:
            days_left = (record.expiration_date - today).days
            return f"{days_left} days" if days_left >= 0 else "Expired"
        return "No Expiration Date"


class DonorsTable(tables.Table):
    row_number = tables.Column(
        orderable=False,
        empty_values=(),
        verbose_name='#'
    )

    fullname = tables.Column(verbose_name='Full Name', empty_values=())
    gender = tables.Column(accessor='profile.gender', verbose_name='Gender')
    email = tables.Column(accessor='profile.user.email', verbose_name='Email',
                          attrs={'td': {'class': 'email-col'}})

    phone = tables.Column(accessor='profile.phone',
                          verbose_name='Phone', empty_values=())
    county = tables.Column(accessor='profile.county',
                           verbose_name='County', empty_values=())
    blood_group = tables.Column(
        accessor='profile.blood_group', verbose_name='Blood Type', empty_values=())
    completed_donations = tables.Column(
        verbose_name='Completed Donations', empty_values=())
    blood_donated = tables.Column(
        verbose_name='Blood Donated', empty_values=())
    requests = tables.Column(verbose_name='Requests', empty_values=())

    class Meta:
        model = UserProfile
        fields = ('row_number','fullname','gender', 'email', 'phone', 'county', 'blood_group',
                  'completed_donations', 'blood_donated', 'requests')
        sequence = fields

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.counter = itertools.count(1)

    def render_row_number(self, record):
        return f"{next(self.counter)}"

    def render_fullname(self, record):
        return f'{record["profile"].firstname} {record["profile"].lastname}'

    def render_blood_donated(self,record):
        return f"{record['total_blood_donated']} L"
    
    def render_requests(self, record):
        return format_html(
            '<p><span class="text-purple-600 text-lg">{}</span> - '
            '<span class="text-green-600 text-lg">{}</span> - '
            '<span class="text-red-600 text-lg">{}</span> - '
            '<span class="text-black text-lg">{}</span></p>',
            record['pending_requests'],
            record['approved_requests'],
            record['rejected_requests'],
            record['total_requests']
        )
