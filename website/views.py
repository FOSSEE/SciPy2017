# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.utils.encoding import force_text
from django.contrib.contenttypes.models import ContentType
from django.template.context import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, redirect
from django.views.decorators.csrf import csrf_exempt
from django.core.context_processors import csrf
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.admin.models import CHANGE
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db.models import F
import csv
from django.core.mail import EmailMultiAlternatives
import os
from scipy2017.local import *

from website.forms import ProposalForm, UserRegisterForm, UserLoginForm, WorkshopForm, ContactForm
from website.models import Proposal, Comments, Ratings
from social.apps.django_app.default.models import UserSocialAuth
import random
import string


def userregister(request):
    context = {}
    context.update(csrf(request))
    registered_emails = []
    users = User.objects.all()
    for user in users:
        registered_emails.append(user.email)
    if request.user.is_anonymous():
        if request.method == 'POST':
            form = UserRegisterForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                if data['email'] in registered_emails:
                    context['form'] = form
                    context['email_registered'] = True
                    return render_to_response('user-register.html', context)
                else:
                    form.save()
                    context['registration_complete'] = True
                    form = UserLoginForm()
                    context['form'] = form
                    context['user'] = request.user
                    return render_to_response('cfp.html', context)
            else:
                context.update(csrf(request))
                context['form'] = form
                return render_to_response('user-register.html', context)
        else:
            form = UserRegisterForm()
        context.update(csrf(request))
        context['form'] = form
        return render_to_response('user-register.html', context)
    else:
        context['user'] = request.user
        return render_to_response('cfp.html', context)

@csrf_exempt 
def gallery(request):
    return render(request, 'gallery.html')

@csrf_exempt 
def contact_us(request,next_url):
    pass
    # user = request.user
    # context = {}
    # if request.method == "POST":
    #     form = ContactForm(request.POST)
    #     sender_name = request.POST['name']
    #     sender_email = request.POST['email']
    #     to = ('scipy@fossee.in',)
    #     subject = "Query from - "+sender_name
    #     message = request.POST['message']
    #     try:
    #         send_mail(subject, message, sender_email, to)
    #         context['mailsent'] = True
    #         context['user'] = user
    #     except:
    #         context['mailfailed'] = True
    #         context['user'] = user
    # return redirect(next_url,context)

@csrf_exempt
def home(request):
    #pass
    context = {}
    if request.user.is_authenticated():
        social_user = request.user
        context.update(csrf(request))
        django_user = User.objects.get(username=social_user)
        context['user'] = django_user
    if request.method == "POST":
        sender_name = request.POST.get('name', None)
        sender_email = request.POST.get('email', None)
        to = (TO_EMAIL, sender_email)
        subject = "Query from - "+sender_name
        message = request.POST.get('message', None)
        try:
            send_mail(subject, message, sender_email, to)
            context['mailsent'] = True
        except:
            context['mailfailed'] = True
    return render_to_response('base.html', context)


def cfp(request):
    if request.method == "POST":
        context = {}
        context.update(csrf(request))
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            if 'next' in request.GET:
                next = request.GET.get('next', None)
                return HttpResponseRedirect(next)
            proposals = Proposal.objects.filter(user = request.user).count()
            context['user'] = user
            context['proposals'] = proposals
            return render_to_response('cfp.html', context)
        else:
            context['invalid'] = True
            context['form'] = UserLoginForm
            context['user'] = user
            return render_to_response('cfp.html', context)
    else:
        form = UserLoginForm()
        context = RequestContext(request, {'request': request,
                                           'user': request.user,
                                           'form': form})
        context.update(csrf(request))
        return render_to_response('cfp.html',
                             context_instance=context)

@login_required
def submitcfp(request):
    context = {}
    if request.user.is_authenticated():
        social_user = request.user
        context.update(csrf(request))
        django_user = User.objects.get(username=social_user)
        context['user'] = django_user
        proposals_a = Proposal.objects.filter(user = request.user, proposal_type = 'ABSTRACT').count()
        if request.method == 'POST':
            form = ProposalForm(request.POST, request.FILES)
            if form.is_valid():
                data = form.save(commit=False)
                data.user = django_user
                data.email = social_user.email
                data.save()
                context['proposal_submit'] = True
                sender_name = "SciPy India 2017"
                sender_email = TO_EMAIL
                subject = "SciPy India 2017 – Talk Proposal Submission Acknowledgment"
                to = (social_user.email, TO_EMAIL)
                message = """
                Dear {0}, <br><br>
                Thank you for showing interest & submitting a talk proposal at SciPy India 2017 conference for the talk titled <b>“{1}”</b>. Reviewal of the proposals will start once the CFP closes.
                <br><br>You will be notified regarding comments/selection/rejection of your talk via email.
                Visit this {2} link to view status of your submission.
                <br>Thank You ! <br><br>Regards,<br>SciPy India 2017,<br>FOSSEE - IIT Bombay.
                """.format(
                social_user.first_name,
                request.POST.get('title', None),
                'http://scipy.in/2017/view-abstracts/',  )
                email = EmailMultiAlternatives(
                subject,'',
                sender_email, to,
                headers={"Content-type":"text/html;charset=iso-8859-1"}
                )
                email.attach_alternative(message, "text/html")
                email.send(fail_silently=True)
                return render_to_response('cfp.html', context)
            else:
                context['proposal_form'] =  form
                context['proposals_a'] = proposals_a
                return render_to_response('submit-cfp.html', context)
        else:
            form = ProposalForm()
            context['proposals_a'] = proposals_a 
            context['proposal_form'] = form
        return render_to_response('submit-cfp.html', context) #when link clicked
    else:
        context['login_required'] = True
        return render_to_response('cfp.html', context)


@login_required
def submitcfw(request):
    context = {}
    if request.user.is_authenticated():
        social_user = request.user
        context.update(csrf(request))
        django_user = User.objects.get(username=social_user)
        context['user'] = django_user
        proposals_w = Proposal.objects.filter(user = request.user, proposal_type = 'WORKSHOP').count()
        if request.method == 'POST':
            form = WorkshopForm(request.POST, request.FILES)
            if form.is_valid():
                data = form.save(commit=False)
                data.user = django_user
                data.email = social_user.email
                data.save()
                context['proposal_submit'] = True
                sender_name = "SciPy India 2017"
                sender_email = TO_EMAIL
                subject = "SciPy India 2017 – Workshop Proposal Submission Acknowledgment"
                to = (social_user.email, TO_EMAIL)
                message = """
                Dear {0}, <br><br>
                Thank you for showing interest & submitting a workshop proposal at SciPy India 2017 conference for the workshop titled <b>“{1}”</b>. Reviewal of the proposals will start once the CFP closes.
                <br><br>You will be notified regarding comments/selection/rejection of your workshop via email.
                Visit this {2} link to view status of your submission.
                <br>Thank You ! <br><br>Regards,<br>SciPy India 2017,<br>FOSSEE - IIT Bombay.
                """.format(
                social_user.first_name,
                request.POST.get('title', None),
                'http://scipy.in/2017/view-abstracts/',  )
                email = EmailMultiAlternatives(
                subject,'',
                sender_email, to,
                headers={"Content-type":"text/html;charset=iso-8859-1"}
                )
                email.attach_alternative(message, "text/html")
                email.send(fail_silently=True)
                return render_to_response('cfp.html', context)
            else:
                context['proposal_form'] =  form
                context['proposals_w'] = proposals_w
                return render_to_response('submit-cfw.html', context)
        else:
            form = WorkshopForm()
            context['proposal_form'] = form
            context['proposals_w'] = proposals_w
        return render_to_response('submit-cfw.html', context)
    else:
        context['login_required'] = True
        return render_to_response('cfp.html', context)

@login_required
def view_abstracts(request):
    user = request.user
    context = {}
    count_list =[]
    if user.is_authenticated():
        if user.is_superuser :
            proposals = Proposal.objects.all().order_by('status')
            ratings = Ratings.objects.all()
            context['ratings'] = ratings
            context['proposals'] = proposals
            context['user'] = user
            return render(request, 'view-abstracts.html', context)
        elif user is not None:
            if Proposal.objects.filter(user = user).exists :
                proposals = Proposal.objects.filter(user = user).order_by('status')
                context['counts'] = count_list
                context['proposals'] = proposals
                context['user'] = user
            return render(request, 'view-abstracts.html', context)
        else:
            return render(request, 'cfp.html')
    else:
        return render(request, 'cfp.html', context)


@login_required
def edit_proposal(request, proposal_id = None):
    user = request.user
    context = {}
    if user.is_authenticated():
        try:
            proposal = Proposal.objects.get(id=proposal_id)
            if proposal.status == 'Edit':
                if proposal.proposal_type == 'ABSTRACT':
                    form = ProposalForm( instance=proposal)
                else:
                    form = WorkshopForm( instance=proposal)
            else:
                return render(request,'cfp.html')
            if request.method == 'POST':
                if proposal.status == 'Edit':
                    if proposal.proposal_type == 'ABSTRACT':
                        form = ProposalForm( request.POST, request.FILES, instance=proposal)
                    else:
                        form = WorkshopForm( request.POST, request.FILES, instance=proposal)
                else:
                    return render(request, 'cfp.html')
                if form.is_valid():
                    data = form.save(commit = False)
                    data.user = user
                    proposal.status = 'Resubmitted'
                    data.save()
                    context.update(csrf(request))
                    proposals = Proposal.objects.filter(user = user).order_by('status')
                    context['proposals'] = proposals
                    return render(request, 'view-abstracts.html', context)
                else:
                    context['user'] = user
                    context['form'] = form
                    context['proposal'] = proposal
                    return render(request, 'edit-proposal.html', context)
            context['user'] = user
            context['form'] = form
            context['proposal'] = proposal
        except:
            render(request, 'cfp.html')
    return render(request, 'edit-proposal.html', context)

@login_required
def abstract_details(request, proposal_id=None):
    user = request.user
    context = {}
    if user.is_authenticated():
        if user.is_superuser :
            proposals = Proposal.objects.all()
            context['proposals'] = proposals
            context['user'] = user
            return render(request, 'cfp.html', context)
        elif user is not None:
            try:
                proposal = Proposal.objects.get(id=proposal_id)
                print "------------------> owner",proposal.user
                if proposal.user == user:
                    try:
                        url = '/2017'+str(proposal.attachment.url) 
                        context['url'] = url
                    except:
                        pass
                    comments = Comments.objects.filter(proposal=proposal)
                    context['proposal'] = proposal
                    context['user'] = user
                    context['comments'] = comments
                    path, filename = os.path.split(str(proposal.attachment))
                    context['filename'] = filename
                    return render(request, 'abstract-details.html', context)
                else:
                    return render(request, 'cfp.html', context)
            except:
                return render(request, 'cfp.html', context)
        else:
            return render(request, 'cfp.html', context)
    else:
        return render(request, 'cfp.html', context)


@login_required
def rate_proposal(request, proposal_id = None):
    user = request.user
    context = {}
    if user.is_authenticated():
        proposal = Proposal.objects.get(id=proposal_id)
        if request.method == 'POST':
            ratings = Ratings.objects.filter(proposal_id= proposal_id, user_id = user.id)
            if ratings:
                for rate in ratings:
                    rate.rating = request.POST.get('rating', None)
                    rate.save()
            else:
                newrate = Ratings()
                newrate.rating = request.POST.get('rating', None)
                newrate.user = user
                newrate.proposal = proposal
                newrate.save()
            rates = Ratings.objects.filter(proposal_id=proposal_id)
            comments = Comments.objects.filter(proposal=proposal)
            context['comments'] = comments
            context['proposal'] = proposal
            context['rates'] = rates
            context.update(csrf(request))
            return render(request, 'comment-abstract.html', context)
        else:
            rates = Ratings.objects.filter(proposal=proposal)
            comments = Comments.objects.filter(proposal=proposal)
            context['comments'] = comments
            context['proposal'] = proposal
            context['rates'] = rates
            context.update(csrf(request))
            return render(request, 'comment-abstract.html', context)
    else:
        return render(request, 'comment-abstract.html', context)



@login_required
def comment_abstract(request, proposal_id = None):
    user = request.user
    context = {}
    if user.is_authenticated():
        if user.is_superuser :
            try:
                proposal = Proposal.objects.get(id=proposal_id)
                try:
                    url = '/2017'+str(proposal.attachment.url) 
                    context['url'] = url
                except:
                    pass
                if request.method == 'POST':
                    comment = Comments()
                    comment.comment = request.POST.get('comment', None)
                    comment.user = user
                    comment.proposal = proposal
                    comment.save()
                    comments = Comments.objects.filter(proposal=proposal)
                    sender_name = "SciPy India 2017"
                    sender_email = TO_EMAIL
                    to = (proposal.user.email, TO_EMAIL )
                    if proposal.proposal_type == 'ABSTRACT':
                        subject = "SciPy India 2017 - Comment on Your talk Proposal"
                        message = """
                            Dear {0}, <br><br>
                            There is a comment posted on your proposal for the talk titled <b>{1}</b>.<br>
                            Once we receive your response, you will be notified regarding further comments/acceptance/ rejection of your talk/workshop via email. 
                            Visit this link {2} to view comments on your submission.<br><br>
                            Thank You ! <br><br>Regards,<br>SciPy India 2017,<br>FOSSEE - IIT Bombay.
                            """.format(
                            proposal.user.first_name,
                            proposal.title, 
                            'http://scipy.in/2017/abstract-details/' + str(proposal.id),
                            )
                    elif proposal.proposal_type =='WORKSHOP':
                        subject = "SciPy India 2017 - Comment on Your Workshop Proposal"
                        message = """
                            Dear {0}, <br><br>
                            There is a comment posted on your proposal for the workshop titled <b>{1}</b>.<br>
                            Once we receive your response, you will be notified regarding further comments/acceptance/ rejection of your talk/workshop via email. 
                            Visit this {2} link to view comments on your submission.<br><br>
                            Thank You ! <br><br>Regards,<br>SciPy India 2017,<br>FOSSEE - IIT Bombay.
                            """.format(
                            proposal.user.first_name,
                            proposal.title, 
                            'http://scipy.in/2017/abstract-details/' + str(proposal.id),
                            )
                    email = EmailMultiAlternatives(
                        subject,'',
                        sender_email, to,
                        headers={"Content-type":"text/html;charset=iso-8859-1"}
                    )
                    email.attach_alternative(message, "text/html")
                    email.send(fail_silently=True)
                    proposal.status="Commented"
                    proposal.save()
                    rates = Ratings.objects.filter(proposal=proposal)
                    context['rates'] = rates
                    context['proposal'] = proposal
                    context['comments'] = comments
                    path, filename = os.path.split(str(proposal.attachment))
                    context['filename'] = filename
                    context.update(csrf(request))
                    return render(request, 'comment-abstract.html', context)
                else:
                    comments = Comments.objects.filter(proposal=proposal)
                    rates = Ratings.objects.filter(proposal=proposal)
                    context['rates'] = rates
                    context['proposal'] = proposal
                    context['comments'] = comments
                    path, filename = os.path.split(str(proposal.attachment))
                    context['filename'] = filename
                    context.update(csrf(request))
                    return render(request, 'comment-abstract.html', context)
            except:
                return render(request, 'cfp.html', context)
        else:
            return render(request, 'cfp.html', context)
    else:
        return render(request, 'cfp.html', context)


@login_required
def status(request, proposal_id= None):
    user = request.user
    context = {}
    if user.is_authenticated():
        if user.is_superuser :
            proposal = Proposal.objects.get(id=proposal_id)
            if 'accept' in request.POST:
                proposal.status="Accepted"
                proposal.save()
                sender_name = "SciPy India 2017"
                sender_email = TO_EMAIL
                to = (proposal.user.email, TO_EMAIL)
                if proposal.proposal_type == 'ABSTRACT':
                    subject = "SciPy India 2017 - Talk Proposal Accepted"
                    message = """Dear """+proposal.user.first_name+""",
                    Congratulations. Your proposal for the talk titled '"""+ proposal.title+ """' is accepted. 
                    You shall present the talk at the conference.\n\nYou will be notified regarding instructions of your talk via email.\n\nThank You ! \n\nRegards,\nSciPy India 2017,\nFOSSEE - IIT Bombay"""
                elif proposal.proposal_type == 'WORKSHOP':
                    subject = "SciPy India 2017 - Workshop Proposal Accepted"
                    message = """Dear """+proposal.user.first_name+""",
                    Congratulations. Your proposal for the workshop titled '"""+ proposal.title+ """' is accepted. 
                    You shall conduct the workshop at the conference.\n\nYou will be notified regarding instructions of your workshop via email.\n\nThank You ! \n\nRegards,\nSciPy India 2017,\nFOSSEE - IIT Bombay"""
                send_mail(subject, message, sender_email, to)
                context.update(csrf(request))
            elif 'reject' in request.POST:
                proposal.status="Rejected"
                proposal.save()
                sender_name = "SciPy India 2017"
                sender_email = TO_EMAIL
                to = (proposal.user.email,TO_EMAIL, )
                if proposal.proposal_type == 'ABSTRACT':
                    subject = "SciPy India 2017 - Talk Proposal Rejected"
                    message = """Dear """+proposal.user.first_name+""",
                    We regret to inform you that your proposal for the talk titled '"""+ proposal.title+ """' as not been shortlisted.<br> 
                    You may register and attend the conference by clicking http://scipyindia2017.doattend.com/
                    \n\nThank You ! \n\nRegards,\nSciPy India 2017,\nFOSSEE - IIT Bombay"""
                elif proposal.proposal_type == 'WORKSHOP':
                    subject = "SciPy India 2017 - Workshop Proposal Rejected"
                    message = """Dear """+proposal.user.first_name+""",
                    We regret to inform you that your proposal for the workshop titled '"""+ proposal.title+ """' as not been shortlisted.<br> 
                    You may register and attend the conference by clicking http://scipyindia2017.doattend.com/
                    \n\nThank You ! \n\nRegards,\nSciPy India 2017,\nFOSSEE - IIT Bombay"""
                send_mail(subject, message, sender_email, to)
                context.update(csrf(request))  
            elif 'resubmit' in request.POST:
                to = (proposal.user.email, TO_EMAIL )
                sender_name = "SciPy India 2017"
                sender_email = TO_EMAIL
                if proposal.proposal_type == 'ABSTRACT':
                    subject = "SciPy India 2017 - Talk Proposal Resumbmission"
                    message = """
                    Dear {0}, <br><br>
                    Thank you for showing interest & submitting a talk proposal at SciPy India 2017 conference for the talk titled <b>"{1}"</b>. You are requested to submit this talk proposal once again.<br>
                    You will be notified regarding comments/selection/rejection of your talk via email.
                    Visit this {2} link to view comments on your submission.<br><br>
                    Thank You ! <br><br>Regards,<br>SciPy India 2017,<br>FOSSEE - IIT Bombay.
                    """.format(
                    proposal.user.first_name,
                    proposal.title, 
                    'http://scipy.in/2017/view-abstracts/' 
                    )
                elif proposal.proposal_type =='WORKSHOP':
                    subject = "SciPy India 2017 - Workshop Proposal Resubmission"
                    message = """
                    Thank you for showing interest & submitting a workshop proposal at SciPy India 2017 conference for the workshop titled <b>"{1}"</b>. You are requested to submit this talk proposal once        again.<br>
                    You will be notified regarding comments/selection/rejection of your workshop via email.
                    Visit this {2} link to view comments on your submission.<br><br>
                    Thank You ! <br><br>Regards,<br>SciPy India 2017,<br>FOSSEE - IIT Bombay.
                    """.format(
                    proposal.user.first_name,
                    proposal.title, 
                    'http://scipy.in/2017/view-abstracts/' 
                    )
                email = EmailMultiAlternatives(
                subject,'',
                sender_email, to,
                headers={"Content-type":"text/html;charset=iso-8859-1"}
                )
                email.attach_alternative(message, "text/html")
                email.send(fail_silently=True)
                proposal.status="Edit"
                proposal.save()
                context.update(csrf(request)) 
        else:
            return render(request, 'cfp.html')  
    else:
        return render(request, 'cfp.html')  
    proposals = Proposal.objects.all().order_by('status')
    context['proposals'] = proposals
    context['user'] = user
    return render(request, 'view-abstracts.html', context)  
    

@login_required
def status_change(request):
    user = request.user
    context = {}
    if user.is_authenticated():
        if user.is_superuser:
            if 'delete' in request.POST:
                delete_proposal = request.POST.getlist('delete_proposal')
                for proposal_id in delete_proposal:
                    proposal = Proposal.objects.get(id = proposal_id)
                    proposal.delete()
                context.update(csrf(request)) 
                proposals = Proposal.objects.all()
                context['proposals'] = proposals
                context['user'] = user
                return render(request, 'view-abstracts.html', context)  
            elif 'dump' in request.POST:
                delete_proposal = request.POST.getlist('delete_proposal')
                blank = False
                if delete_proposal == [] :
                    blank = True
                try:
                    if blank == False:
                        response = HttpResponse(content_type='text/csv')
                        response['Content-Disposition'] = 'attachment; filename="Proposals.csv"'
                        writer = csv.writer(response)
                        header = [
                                    'name',
                                    'username',
                                    'email',
                                    'about_me',
                                    'phone',
                                    'title',
                                    'abstract',
                                    'prerequisite',
                                    'duration',
                                    'attachment',
                                    'date_created',
                                    'status',
                                    'proposal_type',
                                    'tags',
                              ]
                        writer.writerow(header)
                        for proposal_id in delete_proposal:
                            proposal = Proposal.objects.get(id = proposal_id)
                            row = [
                                    '{0} {1}'.format(proposal.user.first_name, proposal.user.last_name),
                                    proposal.user.username,
                                    proposal.user.email,
                                    proposal.about_me,
                                    proposal.phone,
                                    proposal.title,
                                    proposal.abstract,
                                    proposal.prerequisite,
                                    proposal.duration,
                                    proposal.attachment,
                                    proposal.date_created,
                                    proposal.status,
                                    proposal.proposal_type,
                                    proposal.tags,
                                    ]
                            writer.writerow(row)
                        return response
                    else:
                        proposals = Proposal.objects.all()
                        context['proposals'] = proposals
                        context['user'] = user
                        return render(request, 'view-abstracts.html', context) 
                except:
                    proposals = Proposal.objects.all()
                    context['proposals'] = proposals
                    context['user'] = user
                    return render(request, 'view-abstracts.html', context) 
            elif 'accept' in request.POST:
                delete_proposal = request.POST.getlist('delete_proposal') 
                for proposal_id in delete_proposal:
                    proposal = Proposal.objects.get(id = proposal_id)
                    proposal.status = "Accepted"
                    proposal.save()
                    sender_name = "SciPy India 2017"
                    sender_email = TO_EMAIL
                    to = (proposal.user.email, TO_EMAIL)
                    if proposal.proposal_type == 'ABSTRACT':
                        subject = "SciPy India 2017 - Talk Proposal Accepted"
                        message = """Dear """+proposal.user.first_name+""",
                        Congratulations. Your proposal for the talk titled '"""+ proposal.title+ """'is accepted. 
                        You shall present the talk at the conference.\n\nYou will be notified regarding instructions of your talk via email.\n\nThank You ! \n\nRegards,\nSciPy India 2017,\nFOSSEE - IIT Bombay"""
                    elif proposal.proposal_type == 'WORKSHOP':
                        subject = "SciPy India 2017 - Workshop Proposal Accepted"
                        message = """Dear """+proposal.user.first_name+""",
                        Congratulations. Your proposal for the workshop titled '"""+ proposal.title+ """'is accepted. 
                        You shall conduct the workshop at the conference.\n\nYou will be notified regarding instructions of your workshop via email.\n\nThank You ! \n\nRegards,\nSciPy India 2017,\nFOSSEE - IIT Bombay"""
                    send_mail(subject, message, sender_email, to)
                    context.update(csrf(request))
                proposals = Proposal.objects.all()
                context['proposals'] = proposals
                context['user'] = user
                return render(request, 'view-abstracts.html', context)  
            elif 'reject' in request.POST:
                delete_proposal = request.POST.getlist('delete_proposal') 
                for proposal_id in delete_proposal:
                    proposal = Proposal.objects.get(id = proposal_id)
                    proposal.status="Rejected"
                    proposal.save()
                    sender_name = "SciPy India 2017"
                    sender_email = TO_EMAIL
                    to = (proposal.user.email, TO_EMAIL)
                    if proposal.proposal_type == 'ABSTRACT':
                        subject = "SciPy India 2017 - Talk Proposal Rejected"
                        message = """Dear """+proposal.user.first_name+""",
                        We regret to inform you that your proposal for the talk titled '"""+ proposal.title+ """' as not been shortlisted.<br> 
                        You may register and attend the conference by clicking http://scipyindia2017.doattend.com/
                        \n\nThank You ! \n\nRegards,\nSciPy India 2017,\nFOSSEE - IIT Bombay"""
                    elif proposal.proposal_type == 'WORKSHOP':
                        subject = "SciPy India 2017 - Workshop Proposal Rejected"
                        message = """Dear """+proposal.user.first_name+""",
                        We regret to inform you that your proposal for the workshop titled '"""+ proposal.title+ """' as not been shortlisted.<br> 
                        You may register and attend the conference by clicking http://scipyindia2017.doattend.com/
                        \n\nThank You ! \n\nRegards,\nSciPy India 2017,\nFOSSEE - IIT Bombay"""
                    send_mail(subject, message, sender_email, to)
                    context.update(csrf(request))  
                proposals = Proposal.objects.all()
                context['proposals'] = proposals
                context['user'] = user
                return render(request, 'view-abstracts.html', context)  
            elif 'resubmit' in request.POST:
                delete_proposal = request.POST.getlist('delete_proposal') 
                for proposal_id in delete_proposal:
                    proposal = Proposal.objects.get(id = proposal_id)
                    sender_name = "SciPy India 2017"
                    sender_email = TO_EMAIL
                    to = (proposal.user.email, TO_EMAIL )
                    if proposal.proposal_type == 'ABSTRACT':
                        subject = "SciPy India 2017 - Talk Proposal Resumbmission"
                        message = """
                        Dear {0}, <br><br>
                        Thank you for showing interest & submitting a talk proposal at SciPy India 2017 conference for the talk titled <b>"{1}"</b>. You are requested to submit this talk proposal once again.<br>
                        You will be notified regarding comments/selection/rejection of your talk via email.
                        Visit this {2} link to view comments on your submission.<br><br>
                        Thank You ! <br><br>Regards,<br>SciPy India 2017,<br>FOSSEE - IIT Bombay.
                        """.format(
                        proposal.user.first_name,
                        proposal.title, 
                        'http://scipy.in/2017/view-abstracts/' 
                        )
                    elif proposal.proposal_type =='WORKSHOP':
                        subject = "SciPy India 2017 - Workshop Proposal Resubmission"
                        message = """
                        Thank you for showing interest & submitting a workshop proposal at SciPy India 2017 conference for the workshop titled <b>"{1}"</b>. You are requested to submit this talk proposal once        again.<br>
                        You will be notified regarding comments/selection/rejection of your workshop via email.
                        Visit this {2} link to view comments on your submission.<br><br>
                        Thank You ! <br><br>Regards,<br>SciPy India 2017,<br>FOSSEE - IIT Bombay.
                        """.format(
                        proposal.user.first_name,
                        proposal.title, 
                        'http://scipy.in/2017/view-abstracts/' 
                        )
                    email = EmailMultiAlternatives(
                    subject,'',
                    sender_email, to,
                    headers={"Content-type":"text/html;charset=iso-8859-1"}
                    )
                    email.attach_alternative(message, "text/html")
                    email.send(fail_silently=True)
                    proposal.status="Edit"
                    proposal.save()
                    context.update(csrf(request))  
                proposals = Proposal.objects.all()
                context['proposals'] = proposals
                context['user'] = user
                return render(request, 'view-abstracts.html', context)  
            else:
                proposals = Proposal.objects.all()
                context['proposals'] = proposals
                context['user'] = user
                return render(request, 'view-abstracts.html', context) 
        else:
            return render(request, 'cfp.html', context) 
    else:
        return render(request, 'view-abstracts.html', context) 


