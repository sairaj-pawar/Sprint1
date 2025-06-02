from django.contrib import admin
from django.http import HttpResponse
from django.utils.html import format_html
from django.urls import path
import csv

from .models import Department, Poll, PollChoice, Vote

# Inline class to allow adding/editing PollChoice options directly on the Poll admin page
class PollChoiceInline(admin.TabularInline):  # You could also use StackedInline for vertical layout
    model = PollChoice
    extra = 3  # Display 3 blank choices by default when adding a new poll
    fields = ['choice']  # Show only the 'choice' field

# Custom admin class for Poll model
class PollAdmin(admin.ModelAdmin):
    list_display = ['question', 'department', 'created_at', 'download_csv']  # Columns in admin list view
    inlines = [PollChoiceInline]  # Include PollChoice editing directly in Poll admin page

    # Custom link to download poll results as CSV
    def download_csv(self, obj):
        return format_html(
            '<a class="button" href="{}">Download Results</a>',
            f'/admin/polls/poll/{obj.id}/download-csv/'
        )
    download_csv.short_description = 'Download Results'

    # Add custom URL pattern for CSV download
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                '<int:poll_id>/download-csv/',
                self.admin_site.admin_view(self.download_poll_csv),
                name='poll-download-csv'
            ),
        ]
        return custom_urls + urls  # Add our custom URLs before the default ones

    # View to generate and return the CSV file
    def download_poll_csv(self, request, poll_id):
        poll = Poll.objects.get(id=poll_id)
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{poll.question}.csv"'

        writer = csv.writer(response)
        writer.writerow(['Choice', 'Votes'])  # CSV header

        for choice in poll.choices.all():  # Use related_name="choices" from model
            vote_count = Vote.objects.filter(choice=choice).count()
            writer.writerow([choice.choice, vote_count])

        return response

# Register all models with the admin site
admin.site.register(Department)
admin.site.register(Poll, PollAdmin)  # Register Poll with custom admin interface
admin.site.register(PollChoice)
admin.site.register(Vote)
