from django.contrib.auth import authenticate, login as auth_login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Count
from .models import Poll, PollChoice, Vote


# Handles user login
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username') 
        password = request.POST.get('password')

        # Check if username and password are provided
        if not username or not password: 
            return HttpResponse("Username and password are required.")

        # Authenticate the user
        user = authenticate(request, username=username, password=password) 

        if user is not None:
            auth_login(request, user)  # Log in the user
            return redirect('polls:polls_list')  # Redirect to polls list after login
        else:
            messages.info(request, "Invalid credentials. Please try again.")
            return redirect('polls:login')  # Redirect to login page again

    return render(request, 'polls/login.html')  # Render login page if GET request


# Handles user logout
def logout_view(request):
    logout(request)  # Log out the user
    return redirect('polls:login')  # Redirect to login page after logout


# Renders index page; user must be logged in
@login_required
def index(request):
    return render(request, 'polls/index.html')


# Renders about page; user must be logged in
@login_required
def about(request):
    return render(request, 'polls/about.html')


# Renders contact page; user must be logged in
@login_required
def contact(request):
    return render(request, 'polls/contact.html')


# Displays a list of all polls; user must be logged in
@login_required
def polls_list(request):
    polls = Poll.objects.all()  # Fetch all polls from the database
    return render(request, 'polls/polls_list.html', {'polls': polls})


# Handles voting functionality
@login_required
def vote(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)  # Get the poll object or raise 404
    choices = PollChoice.objects.filter(poll=poll)  # Get all choices for the poll

    # Check if user has already voted
    existing_vote = Vote.objects.filter(user=request.user, poll=poll).first()
    
    if existing_vote:
        # If already voted, redirect to results page with a message
        messages.info(request, f"You have already voted for '{existing_vote.vote_choice}'. You cannot change your vote.")
        return redirect('polls:poll_results', poll_id=poll.id)

    if request.method == 'POST':
        choice_id = request.POST.get('vote_choice')  # Get selected choice

        if not choice_id:
            # If no choice selected, show error
            messages.error(request, "Please select a choice.")
            return render(request, 'polls/vote.html', {'poll': poll, 'choices': choices})

        choice = get_object_or_404(PollChoice, pk=choice_id)  # Get the chosen option

        # Save the vote
        vote = Vote(
            user=request.user,
            poll=poll,
            choice=choice,
            vote_choice=choice.choice
        )
        vote.save()

        return redirect('polls:poll_results', poll_id=poll.id)  # Redirect to results after voting

    return render(request, 'polls/vote.html', {'poll': poll, 'choices': choices})  # Render vote page


# Shows poll results with vote count and percentage
@login_required
def poll_results(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)  # Get the poll object

    choices = PollChoice.objects.filter(poll=poll)  # Get all choices for this poll
    all_votes = Vote.objects.filter(poll=poll)  # Get all votes for this poll
    total_votes = all_votes.count()  # Total number of votes

    choice_votes = []  # List to store vote count and percentage for each choice

    for choice in choices:
        # Count number of votes for each choice
        votes_count = all_votes.filter(choice=choice).count()

        # Append choice data with percentage
        choice_votes.append({
            'choice': choice.choice,
            'count': votes_count,
            'percent': round((votes_count / total_votes) * 100) if total_votes > 0 else 0
        })

    # Get current user's vote if exists
    user_vote = all_votes.filter(user=request.user).first()

    return render(request, 'polls/results.html', {
        'poll': poll,
        'results': choice_votes,
        'total_votes': total_votes,
        'user_vote': user_vote
    })  # Send results data to the template for display
