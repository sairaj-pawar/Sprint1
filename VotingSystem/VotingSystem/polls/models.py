from django.db import models  # Import Django's model system to define database tables
from django.contrib.auth.models import User  # Import Django's built-in User model for authentication

# Department model to categorize polls
class Department(models.Model):
    name = models.CharField(max_length=100)  # Name of the department (e.g., IT, HR)

    def __str__(self):
        return self.name  # String representation shown in Django Admin and shell


# Poll model to store individual polls
class Poll(models.Model):
    question = models.CharField(max_length=200)  # Main question of the poll
    department = models.CharField(max_length=100)  # Department associated with the poll
    title = models.CharField(max_length=200, default="Poll Title")  # Optional title for display
    description = models.TextField(default="Poll Description")  # Optional description for display
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set poll creation date

    def __str__(self):
        return self.title  # Display title when representing the Poll object


# PollChoice model to store options for each poll
class PollChoice(models.Model):
    poll = models.ForeignKey(
        Poll,
        on_delete=models.CASCADE,
        related_name="choices"  # Enables reverse lookup: poll.choices.all()
    )
    choice = models.CharField(max_length=200)  # Text of the choice (e.g., "Yes", "No", "Maybe")

    def __str__(self):
        return self.choice  # Display choice text


# Vote model to store a user's vote on a poll
class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # User who voted
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)  # Poll being voted on
    vote_choice = models.CharField(max_length=200)  # Stores the choice text for quick access
    choice = models.ForeignKey(
        'PollChoice',
        on_delete=models.CASCADE,
        null=True,
        blank=True  # Choice object itself (optional, helps with data relations)
    )

    class Meta:
        unique_together = ('user', 'poll')  # Prevents a user from voting more than once per poll

    def __str__(self):
        # Returns readable string like: "alice voted for Yes"
        choice_text = self.vote_choice
        if self.choice:
            choice_text = self.choice.choice
        return f"{self.user.username} voted for {choice_text}"
