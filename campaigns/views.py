from django.http.response import Http404, HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages



from .models import Campaign, Candidates

# Get questions and display them


def index(request):
	latest_candidate_list = Campaign.objects.order_by('-pub_date')[:5]
	context = {'latest_candidate_list': latest_candidate_list,}
	return render(request, 'campaigns/index.html', context)

# Show specific question and choices


def detail(request, campaign_id):
	campaign = Campaign.objects.get(pk = campaign_id)
	with open("new_data.txt","r") as rn:
		data = rn.read()
		if str(campaign.id) + ',' + str(request.user.username) in data:
			messages.warning(request,"you have already attended the pole.")
			return redirect(reverse("campaigns:index"))

	try:
		campaign = Campaign.objects.get(pk = campaign_id)
		with open('new_data.txt','a') as n:
			cid = str(campaign.id) + ','
			user = request.user.username
			n.writelines([cid,user])
			n.close
	except Campaign.DoesNotExist:
		raise Http404("Campaign does not exist")
	return render(request, 'campaigns/detail.html', {'campaign': campaign})

# Get question and display results


def results(request, campaign_id):
    campaign = get_object_or_404(Campaign, pk = campaign_id)
    return render(request, 'campaigns/results.html', {'campaign': campaign})

# Vote for a question choice

@login_required
def vote(request, campaign_id):
	
	
	# print(request.POST['choice'])
	campaign = get_object_or_404(Campaign, pk = campaign_id)

	# with open("Attendies-List.txt","r") as check:
	# 	lst = check.read()
	# 	data = str(campaign.organization_name)+','+str(request.user.username)
	# 	print(data)
	# 	if data in lst:
	# 		return(HttpResponse("You have already attended the pole"))

	
	try:
		selected_choice = campaign.candidates_set.get(pk = request.POST['choice'])
	except (KeyError, Candidates.DoesNotExist):
		# Redisplay the question voting form.
		return render(request, 'campaigns/detail.html', {
			'campaign': campaign,
			'error_message': "You didn't select a choice.",
		})
	else:

		selected_choice.votes += 1
		selected_choice.save()
		# with open("Attendies-List.txt",'a') as a:
		# 	name = str(campaign.organization_name) + ','
		# 	user = str(request.user.username)
		# 	a.writelines([name,user])
		# 	a.write('\n')
		# 	a.close()
	
		# Always return an HttpResponseRedirect after successfully dealing
		# with POST data. This prevents data from being posted twice if a
		# user hits the Back button.
		return HttpResponseRedirect(reverse('campaigns:results', args =(campaign.id,)))


