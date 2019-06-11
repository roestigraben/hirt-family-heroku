from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from pages.forms import PersonForm, RelationForm
from django.urls import reverse
from users.models import Person, Relation, XtraPhotos, XtraInfo
import logging
from django.shortcuts import render
from django.contrib import messages
from django import forms
import json, csv, os, sys
from django.http import JsonResponse
from django.db.models import Q
import random


class XPageView(LoginRequiredMixin, TemplateView):
	'''
	example only, should not remain
	'''
	login_url = 'home'
	template_name = 'pages/person_add.html'
	form_class = PersonForm

	def get(self, request, *args, **kwargs):
		form = self.form_class()
		return render(request, self.template_name, {'form': form})

	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST)
		if form.is_valid():
			
			data = form.cleaned_data

			person = Person()
			person.first_name = data['first_name']
			person.last_name = data['last_name']
			person.profession = data['profession']
			person.city = data['city']
			person.birth_date = data['birth_date']
			person.date_of_death = data['date_of_death']
			#person.thumbnail = data['thumbnail']
			person.x_pos = data['x_pos']
			person.y_pos = data['y_pos']
			person.save()
			print("SAVED DATA")
			return HttpResponseRedirect('/tree/')
		return render(request, self.template_name, {'form': form})


def person_add_view(request):
	'''
	example of form editing and saving
	'''
	form = PersonForm(request.POST or None)
	if form.is_valid():
		form.save()
	context = {
		'form' : form
	}
	return render(request, "pages/person_add.html", context)


def edge_add_view(request):
	'''
	example of form editing and saving
	'''
	form = RelationForm(request.POST or None)
	if form.is_valid():
		form.save()
	context = {
		'form': form
	}
	return render(request, "pages/edge_add.html", context)

def presentOptions(p):
	for pp in p:
		data = list(XtraPhotos.objects.filter(parent_id=pp['id']).values())
		if data:
			pp['opt'] = True
		data = list(XtraInfo.objects.filter(parent_id=pp['id']).values())
		if data:
			pp['opt'] = True
	return p

def addMembersToFamily(p, familyId):
	'''
	complements the list of persons belonging to a specific family with persons who have affiliations
	'''
	# print(p)
	schwab_list = [
		['Hans','Hirt','1916'],
		['Hans', 'Hirt', '1949'],
		['Peter', 'Hirt'],
		['Alida','Surian'],
		['Urs','Hirt'],
		['Laura', 'Hirt'],
		['Andreas','Hirt'],
		['Alain', 'Hirt'],
		['Stephanie','Hirt'],
		['Adriano', 'Hirt'],
		['Sophie', 'Sondrum'],
		['Svetlana', ''],
		['Francisca Neuman','Farias da Costa'],
		['Cyrielle','Millet'],
		['Rebeka','Rodriguez'],
		['Bilge','Cetincaya'],
		['Gisela','Schöfl'],
		['Madeesen','Sondrum'],
		['Naomi','Nido'],
	]
	surian_list = [
		['Peter', 'Hirt'],
		['Laura', 'Hirt'],
		['Andreas', 'Hirt'],
		['Alain', 'Hirt'],
		['Cyrielle', 'Millet'],
		['Rebeka', 'Rodriguez'],
		['Bilge', 'Cetincaya'],
	]
	if familyId == 'Schwab':
		person_list = schwab_list
	
	if familyId == 'Surian':
		person_list = surian_list

	for person in person_list:
		# print(person[0], person[1])
		if len(person) == 2:
			p_special = list(Person.objects.filter(
					Q(first_name__iexact=person[0]) & Q(last_name__contains=person[1])).values())
			if len(p_special) != 0:
				p.append(p_special[0])
		else:
			p_special = list(Person.objects.filter(
                    Q(first_name__iexact=person[0]) & Q(last_name__contains=person[1]) & Q(birth_date__contains=person[2])).values())
			if len(p_special) != 0:
				p.append(p_special[0])
	
	return p

def get_hirt_family():
	'''
	return a list of persons belonging to the Hirt family (or clan)
	'''
	p = list(Person.objects.filter(last_name__in=[
		'Wolf',
		'Farias da Costa',
		'Hirt',
		'Roth',
		'Kocher',
		'Pfister',
		'Forster',
		'Sondrum',
		'Cetincaya',
		'Nido',
		'Fischer',
		'Lüthi',
		'Marti',
		'Godoy',
		'Morel',
		'Schöfl',
		'Rodriguez',
		'Millet',
		'Zesiger',
		'Strahm',
		'Steiner',
		'Zesiger',
		'Sallaz',
		'Fuchs',
		'Müllhaupt',
		'Servetiadis',
		'von Bergen',
		'Servetiadou',
		'Fabbri',
		'Fuster',
		]).values())
	# for people sharing common last names, a query with first and last name is used below
	p_special = list(Person.objects.filter(
				Q(first_name__contains="Alida") & Q(last_name__contains="Surian")).values())
	if len(p_special) != 0:
		p.append(p_special[0])
	p_special = list(Person.objects.filter(
				Q(first_name__contains="Sophie") & Q(last_name__contains="Schwab")).values())
	if len(p_special) != 0:
		p.append(p_special[0])
	p_special = list(Person.objects.filter(
				Q(first_name__contains="Berta") & Q(last_name__contains="Affolter")).values())
	if len(p_special) != 0:
		p.append(p_special[0])

	presentOptions(p)
	
	return p

def get_schwab_family():
	'''
	creates a list of Persons to be displayed when selecting the Schwab family
	returns the created list. 
	'''
	schwab_list = [
		'Schwab',
		'Stuber',
		'Jaggi',
		'Wuethrich',
		'Lüscher',
		'Frieden',
		'Haefliger',
		'Adams',
		'Jufer',
		'Grossert',
		'Hutter',
		'Ruegg',
		'Schluep',
		'Emch',
		'Leibundgut',
		'Schlosser',
		'Birrer',
		'Hauser',
		'Lanz',
		'Hofer',
	]
	my_filter_qs = Q()
	for name in schwab_list:
		my_filter_qs = my_filter_qs | Q(last_name=name)
	p = list(Person.objects.filter(my_filter_qs).values())

	p_special = list(Person.objects.filter(
				Q(first_name__contains="Anna Barbara") & Q(last_name__contains="Affolter")).values())
	if len(p_special) != 0:
		p.append(p_special[0])
	p_special = list(Person.objects.filter(
				Q(first_name__contains="Samuel") & Q(last_name__contains="Affolter")).values())
	if len(p_special) != 0:
		p.append(p_special[0])
	
	final_p = addMembersToFamily(p, familyId='Schwab')

	presentOptions(final_p)

	return final_p

def get_surian_family():
	'''
	return a list of persons belonging to the Surian family (or clan)
	'''
	p = list(Person.objects.filter(last_name__in=[
            'Dantomio',
			'Forner',
			'Tonin',
			'Richard',
			'Surian',
			'Monteiro',
			'Laesser',
			'Ruchet',
			'Donadel',
			'Luison',
			'Toenz',
			'de Meier',
			'Adamo',
			'Bison',
			'Perizzolo',
			'de Vecchi',
			'Zanin',
			'de Boni',
			'Martin',
			'Losano',
			'Andreatta',
			'Ricciardella',
			'Trouve',
			'de Marchi',
        ]).values())

	final_p = addMembersToFamily(p, familyId='Surian')

	presentOptions(final_p)

	return final_p

def get_family_ref(clanId):
	
	ref = []
	if clanId == None:
		p = get_hirt_family()
		fid = 1
		#print(p)
	if clanId == '1':
		p = get_hirt_family()
		fid = 1
		#print(p)
	if clanId == '2':
		p = get_schwab_family()
		fid = 2
	if clanId == '3':
		p = get_surian_family()
		fid = 3
	# print("####################################", clanId)
	# for x in p:
	#  	print(x['first_name'], x['last_name'], x['city'])
	
	r = list(Relation.objects.all().values())
	for item in r:
		# print('===> ',item)
		for member in p:
			if member['id'] == item['parent_id']:
				####################################### this section is a hack ###########
				###### identify who is the ' corner person' and eliminate #################
				####### for Surian (3), it is Alida (276), for Schwab (2) it is Sophie (243)######### 
				if fid == 1:
					ref.append([{'parent_id': member['id'], 'family_id': fid}])
				if fid == 3: #and member['id'] != 276:
					ref.append([{'parent_id': member['id'], 'family_id': fid}])
				if fid == 2: #and member['id'] != 243:
					ref.append([{'parent_id': member['id'], 'family_id': fid}])

	# only for debugging	
	# for rr in ref:
	# 	print("rr ", rr)
	return ref


def get_edges(clanId):
	relations_list = []
	# print("Hello from Edges")

	ref = get_family_ref(clanId)
	# print("ref      ", ref, clanId)

	p = list(Relation.objects.values('parent_id').distinct())
	# print(len(p), p)

	# for all persons who are parents
	for i in p:
			records = Relation.objects.filter(parent_id=i['parent_id'])
			xxx = [item.child_id for item in records]
			#print('parent  ', i['parent_id'])

			for family in ref:
				# print(family[0]['parent_id'])
				if i['parent_id'] == family[0]['parent_id']:
					f = family[0]['family_id']
					break
				else:
					f = 9999
			if f < 9999:
				newRecord = [i['parent_id'], xxx, f]

				relations_list.append(newRecord)
		
	return relations_list


class HomePageView(TemplateView):

	template_name = 'pages/home.html'

	def clan_name(self):
		global clanId
		clanId = self.kwargs.get('family_id')
		# print('The Family ID selected is   : ', clanId)
		# sys.stdout.flush()
		if clanId == '2':
			return 'Schwab'
		if clanId == '3':
			return 'Surian'
		return 'Hirt'

	def family(self):
		clanId = self.kwargs.get('family_id')
		if clanId == '2':
			return get_schwab_family()
		if clanId == '3':
			return get_surian_family()
		return get_hirt_family()
	
	def getNames(self):

		names = []
		n = list(Person.objects.all().values())

		for p in n:
			names.append({'id': p['id'], 'full_name' : p['first_name'] + ' ' + p['last_name']})
		
		return JsonResponse(names, safe=False)


	def edges(self):
		# print('clanId', clanId, type(clanId))
		#relations_list = get_edges(clanId)

		big_list = []
		big_list.append(get_edges('1'))
		big_list.append(get_edges('2'))
		big_list.append(get_edges('3'))
		#print (big_list)
		
		#messages.success(self, 'edges are loaded' + str(clanId))
		# for t in relations_list:
		#   	print("t  ", t)
		# return JsonResponse(relations_list, safe=False)
		return JsonResponse(big_list, safe=False)




class TreePageView(LoginRequiredMixin, TemplateView):
	login_url = 'home'
	template_name = 'pages/tree.html'
	form_class = PersonForm

	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST)
		if form.is_valid():

			data = form.cleaned_data

			person = Person()
			person.first_name = data['first_name']
			person.last_name = data['last_name']
			person.profession = data['profession']
			person.city = data['city']
			person.birth_date = data['birth_date']
			person.date_of_death = data['date_of_death']
			#person.thumbnail = data['thumbnail']
			person.x_pos = data['x_pos']
			person.y_pos = data['y_pos']
			person.save()
			print("SAVED DATA")
			return HttpResponseRedirect('/tree/')
		return render(request, self.template_name, {'form': form})


	def get_context_data(self, **kwargs):
		context = super(TreePageView, self).get_context_data(**kwargs)
		# print("context data", self.request.POST)
		form = PersonForm(self.request.POST or None)  
		
		context["form"] = form
		
		return context
	

	def clan_name(self):
		global clanId
		clanId = self.kwargs.get('family_id')
		# print(clanId)
		if clanId == '2':
			return 'Schwab'
		if clanId == '3':
			return 'Surian'
		return 'Hirt'

	def family(self):
		clanId = self.kwargs.get('family_id')
		if clanId == '2':
			return get_schwab_family()
		if clanId == '3':
			return get_surian_family()
		return get_hirt_family()

	def edges(self):

		relations_list = get_edges(clanId)

		# for t in relations_list:
		#	print("ttttt  ", t)
		return JsonResponse(relations_list, safe=False)

	def persons(self):
		p = Person.objects.all()
		# print("called for Person object")
		return p
	
	def hirt_family(self):
		p = get_hirt_family()
		return p

	def schwab_family(self):
		p = get_schwab_family()
		return p

	def surian_family(self):
		p = get_surian_family()
		return p
	

	def importPersons(self):
		print("importing persons")
		return HttpResponseRedirect(reverse("tree"))

	def addPerson(self, request):
		form = PersonForm(request.POST or None)
		print("add Person")
		return HttpResponseRedirect(reverse("tree"))

	


class FamilyPageView(LoginRequiredMixin, TemplateView):
	login_url = 'home'
	template_name = 'pages/family.html'
	#print("you are in the Detail view of a family")

	def clan_name(self):
		'''
		Defining to which page returning when hitting the back button
		'''
		pk = self.kwargs.get('pk')
		
		clan = get_hirt_family()
		for p in clan:
			if int(pk) == p['id']:
				return 'Hirt'
		
		clan = get_surian_family()
		for p in clan:
			if int(pk) == p['id']:
				return 'Surian'

		clan = get_schwab_family()
		for p in clan:
			if int(pk) == p['id']:
				return 'Schwab'

		return 'Hirt'

	def person(self):
		pk = self.kwargs.get('pk')
		p = list(Person.objects.filter(pk=pk).values())
		# print(" Person started ------------ ")
		# print(p)

		person1_x_pos = p[0]['x_pos']
		person1_y_pos = p[0]['y_pos']
		# print(person1, person1_x_pos, person1_y_pos)
		married_persons = list(Person.objects.filter(x_pos__range=(
			person1_x_pos-60, person1_x_pos+60), y_pos=person1_y_pos).values())
		# print(married_persons)
		r = list(Relation.objects.filter(parent_id=pk).values())
		#print(r)
		if not r:
			# person has no children, now lets check if his a married partner who has
			# print("person has no children")
			if married_persons[0]['id'] == int(pk):
				# print('is himself')
				if len(married_persons) < 2:
					# print("person is not married")
					parent = list(Relation.objects.filter(child_id=pk).values())
					# print(parent[0]['parent_id'])
					if parent:
						p[0]['has_parents'] = True
						# print("has parents")
					else:
						p[0]['has_parents'] = False
						# print("has no parents")
				else:
					r = list(Relation.objects.filter(
						parent_id=married_persons[1]['id']).values())
			else:
				# print(' is partner')
				r = list(Relation.objects.filter(
					parent_id=married_persons[0]['id']).values())
			# print("still arriving here")
		
		# r = list(Relation.objects.filter(parent_id=pk).values())
		# print(r)
		if r:
			p[0]['has_children'] = True
			# print("has children")
		else:
			p[0]['has_children'] = False
			# print("has no children")

		# check now for parents of selected person
		parent = list(Relation.objects.filter(child_id=pk).values())
		# print(parent)
		if parent:
			p[0]['has_parents'] = True
		else:
			p[0]['has_parents'] = False

		p[0]['y_pos'] = 200
		p[0]['x_pos'] = 100
		#print(p[0])
		return p

	def partner(self):
		pk = self.kwargs.get('pk')
		# print(pk)

		person1 = list(Person.objects.filter(pk=pk).values())
		person1_x_pos = person1[0]['x_pos']
		person1_y_pos = person1[0]['y_pos']
		# print(person1, person1_x_pos, person1_y_pos)
		married_persons = list(Person.objects.filter(x_pos__range=(
			person1_x_pos-60, person1_x_pos+60), y_pos=person1_y_pos).values())
		#print(len(married_persons), married_persons)
		if married_persons[0]['id'] == int(pk):
			#print('is himself')
			if len(married_persons) < 2:
				x= []
				return x
			r = Person.objects.filter(pk=married_persons[1]['id'])	
			# print(r)
		else:
			# print(' is partner')
			r = Person.objects.filter(pk=married_persons[0]['id'])
		
		rr = list(r.values())
		rr[0]['y_pos'] = 200
		rr[0]['x_pos'] = 40

		# print(rr)
		return rr

	def siblings(self):
			pk = self.kwargs.get('pk')
			# print(pk)

			r = list(Relation.objects.filter(child_id=pk).values())
			if r:
				parent = r[0]['parent_id']
				# print(parent)
				rr = list(Relation.objects.filter(parent_id=parent).values())
				# print(rr)
				cList = []
				for child in rr:
					# print(child['child_id'])
					if not child['child_id'] == int(pk):
						cList.append(child['child_id'])
				# print(cList)
			else:
				cList = []
			siblings = list(Person.objects.filter(pk__in=cList).values())
			# place the children in recalculatd x_positions
			i = 0
			for s in siblings:
				i = i + 1
				s['x_pos'] = 200 + i*100
				s['y_pos'] = 200

			# siblings = [{'id': 284, 'first_name': 'Francisca Neuman', 'last_name': 'Farias da Costa', 'city': 'Hettlingen', 'profession': '', 'birth_date': 1959, 'date_of_death': 0, 'x_pos': 830, 'y_pos': 600, 'thumbnail': 'neumanHirt.png'}, {
			# 'id': 283, 'first_name': 'Urs', 'last_name': 'Hirt', 'city': 'Hettlingen', 'profession': 'Finanzkontroller', 'birth_date': 1951, 'date_of_death': 0, 'x_pos': 890, 'y_pos': 600, 'thumbnail': 'ursHirt.png'}]
			return siblings


	def children(self):
		pk = self.kwargs.get('pk')
		# print('pk : ', pk)
		# calculate the descendants list (cList) 
		r = list(Relation.objects.filter(parent_id=pk).values())
		if not r:
			#print('has no children')
			person1 = list(Person.objects.filter(pk=pk).values())
			person1_x_pos = person1[0]['x_pos']
			person1_y_pos = person1[0]['y_pos']
			#print(person1)
			married_persons = list(Person.objects.filter(x_pos__range=(
                            person1_x_pos-60, person1_x_pos+60), y_pos=person1_y_pos).values())
			#print(married_persons, pk, married_persons[0]['id'])
			
			if married_persons[0]['id']==int(pk):
				#print('is father, hence take the other person', married_persons[0]['id'])
				# checks if sombeody is not married
				if len(married_persons) < 2:
					x = []
					return x
				r = list(Relation.objects.filter(
					parent_id=married_persons[1]['id']).values())
			else:
				#print(' is mother')
				r = list(Relation.objects.filter(
					parent_id=married_persons[0]['id']).values())
			
		cList = []
		for child in r:
			# print(child['child_id'])
			cList.append(child['child_id'])
		# print(cList)
		children = list(Person.objects.filter(pk__in=cList).values())
		# place the children in recalculatd x_positions
		children_count = len(children)
		i = 0
		for c in children:
			if children_count == 1:
				c['x_pos'] = 130 + i*100
			elif children_count == 2:
				c['x_pos'] = 80 + i*100
			else:
				c['x_pos'] = 30 + i*100
			c['y_pos'] = 440
			i = i + 1
			
		#print(children)
		return children
	
	def parents(self):
		pk = self.kwargs.get('pk')

		p = list(Relation.objects.filter(child_id=pk).values())
		if p:
			parentID = p[0]['parent_id']
			# parent 1 calculation is not needed as parents filers not only the husband or wife,
			# but also the person with the link to the displayed person
			parent1 = list(Person.objects.filter(pk=parentID).values())
			parent1_x_pos = parent1[0]['x_pos']
			parent1_y_pos = parent1[0]['y_pos']
			parent2 = list(Person.objects.filter(x_pos__range=(parent1_x_pos-60, parent1_x_pos+60), y_pos=parent1_y_pos).values())
			#print(parent2)
			pList = []
			pList.append(parentID)
		
			#parents = list(Person.objects.filter(pk__in=pList).values())
			parents = parent2
			i = 0
			for p in parents:
				i = i + 1
				p['x_pos'] = 40 + i*60
				p['y_pos'] = 20
			# print(parents)
		else:
			parents = []
		return parents

	def edges(self):
		pk = self.kwargs.get('pk')
		# print("edges children started -------")

		r = list(Relation.objects.filter(parent_id=pk).values())
		# print(r, '--------- has ', len(r), ' children')
		if not r:
			# print("edge:  person has no children but maybe the husband of the wife")
			person1 = list(Person.objects.filter(pk=pk).values())
			person1_x_pos = person1[0]['x_pos']
			person1_y_pos = person1[0]['y_pos']
			# print(person1)
			married_persons = list(Person.objects.filter(x_pos__range=(
						person1_x_pos-60, person1_x_pos+60), y_pos=person1_y_pos).values())
			# print('edge:', married_persons, pk, married_persons[0]['id'])

			if len(married_persons) != 1:
				if married_persons[0]['id'] == int(pk):
					# print(' is mother')
					r = list(Relation.objects.filter(
						parent_id=married_persons[1]['id']).values())
				else:
					r = list(Relation.objects.filter(
						parent_id=married_persons[0]['id']).values())

			# print(r)

		

		# below code is for children  horizontal line management only
		offset = 0
		if r:
			if len(r) == 1:
				offset = 110
			elif len(r) == 2:
				offset = 105
			elif len(r) == 3:
				offset = 55
			elif len(r) == 4:
				offset = 55
			elif len(r) == 5:
				offset = 55
			else:
				offset = 55

		edgeData = [{
                            'width_children': (len(r)-1)*100,
							'x_pos_children': offset
			}]

		# print('edgeData : ', edgeData)
		return edgeData

	def edgesSibling(self):
		pk = self.kwargs.get('pk')
		# print("edges siblings started -------")

		

		r = list(Relation.objects.filter(parent_id=pk).values())
		
		# print('edge : ', len(r), ' children ------------')

		c = list(Relation.objects.filter(child_id=pk).values())
		# print('edge : ', c, '---siblings------')
		s = []
		has = False
		if c:
			parentId = c[0]['parent_id']
			s = list(Relation.objects.filter(parent_id=parentId).values())
			if len(s) > 1:
				has = True
			else:
				has = False
			# print(parentId, s)

		# below code is for children  horizontal line management only
		offset = 0
		if r:
			if len(r) == 1:
				offset = 110
			elif len(r) == 2:
				offset = 105
			elif len(r) == 3:
				offset = 55
			elif len(r) == 4:
				offset = 55
			else:
				offset = 55

		edgeData = [
                    {
                        'width_siblings': (len(s)-1)*100+70,
                        'has_siblings': has,
                    }
                ]
		# print(edgeData)

		return edgeData

	def buttons(self):

		p = list(Person.objects.all().values())

		random.shuffle(p)
		sample_array = p[0:7]
		data = []
		i = 0
		for sample in sample_array:
			data.append({'exists': random.choice([True, False]), 'id': sample_array[i]['id'], 'label': sample_array[i]['first_name']})
			i = i + 1

		# data = [
		# 	{'exists': True, 'id': 283, 'label': 'edit data'},
		# 	{'exists': True, 'id': 286, 'label': 'home'},
		# 	{'exists': True, 'id': 254, 'label': 'google'},
		# 	]
		return data

	def accordeonContent(self):
		pk = self.kwargs.get('pk')
		#print(type(pk))

		data = list(XtraInfo.objects.filter(parent_id=pk).values())
		return data

	def photos(self):
		pk = self.kwargs.get('pk')
		#print(pk)
		data = list(XtraPhotos.objects.filter(parent_id=pk).values())

		# processing of data to take out the directory info from the filename
		i = 0
		for d in data:
			f = os.path.basename(d['source'])
			# print(f)
			data[i]['source'] = './photos/' + f
			i += 1


		
		
		return data


def exportCSV(request):
	data = Person.objects.all().values()
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="persons.csv"'
	writer = csv.writer(response)
	for item in data:
		writer.writerow([item['id'], item['first_name'], item['last_name'], item['city'], item['profession'], item['birth_date'], item['date_of_death'], item['x_pos'], item['y_pos'], item['thumbnail'], item['phone_number'], item['cell_number'], item['email'], item['created_at'], item['updated_at']])
	return response

def exportEdges(request):
	data = Relation.objects.all().values()
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="relations.csv"'
	writer = csv.writer(response)

	persons = Person.objects.all().values()

	for item in data:
		for person in persons:
			if person['id'] == item['parent_id']:
				parentFullName = person['first_name'] + ' ' + person['last_name']

			if person['id'] == item['child_id']:
				childFullName = person['first_name'] + ' ' + person['last_name']
			
		writer.writerow([item['id'], item['child_id'], childFullName, item['parent_id'], parentFullName])
	return response
	

	
def person_new_coordinates(request):

	xx = request.POST.get('x_pos')
	yy = request.POST.get('y_pos')

	# reformat: take last 2 characters out (px) and convert to integer
	x = int(xx[:-2])
	y = int(yy[:-2])
	# print("response  : ", request.POST.get('id'), x, y)

	qs = Person.objects.get(id=request.POST.get('id'))
	# qsx = Position.objects.get(id=qs.coordinates_id)

	# print(qs.first_name, qs.last_name, qs.x_pos, qs.y_pos)

	qs.x_pos = x
	qs.y_pos = y
	qs.save()

	return render(request, "pages/tree.html", {})


def upload_csv(request):
	data = {}
	if "GET" == request.method:
		return render(request, "pages/tree.html", data)
    # if not GET, then proceed
	try:
		csv_file = request.FILES["csv_file"]
		if not csv_file.name.endswith('.csv'):
			messages.error(request, 'File is not CSV type')
			return HttpResponseRedirect(reverse("pages/tree.html"))
        #if file is too large, return
		if csv_file.multiple_chunks():
			messages.error(request, "Uploaded file is too big (%.2f MB)." %
			               (csv_file.size/(1000*1000),))
			return HttpResponseRedirect(reverse("pages/tree.html"))

		file_data = csv_file.read().decode("utf-8")
		

		lines = file_data.split("\n")
		#loop over the lines and save them in db. If error , store as string and then display
		for line in lines:
			fields = line.split(",")
			

			person = Person()
			person.first_name = fields[1]
			person.last_name = fields[2]
			person.profession = fields[4]
			person.city = fields[3]
			person.birth_date = fields[8]
			person.date_of_death = fields[9]
			person.thumbnail = fields[7]
			person.x_pos = fields[5]
			person.y_pos = fields[6]
			person.save()
			try:
				#Person.objects.create(data_dict)
				
				print(person)
			except Exception as e:
				logging.getLogger("error_logger").error(repr(e))
				pass 

	except Exception as e:
		logging.getLogger("error_logger").error("Unable to upload file. "+repr(e))
		messages.error(request, "Unable to upload file. "+repr(e))

	return HttpResponseRedirect(reverse("upload_csv"))


def upload_edges(request):
	data = {}
	if "GET" == request.method:
		return render(request, "pages/tree.html", data)
    # if not GET, then proceed
	try:
		csv_file = request.FILES["csv_file"]
		if not csv_file.name.endswith('.csv'):
			messages.error(request, 'File is not CSV type')
			return HttpResponseRedirect(reverse("pages/tree.html"))
        #if file is too large, return
		if csv_file.multiple_chunks():
			messages.error(request, "Uploaded file is too big (%.2f MB)." %
			               (csv_file.size/(1000*1000),))
			return HttpResponseRedirect(reverse("pages/tree.html"))

		file_data = csv_file.read().decode("utf-8")

		lines = file_data.split("\n")
		#loop over the lines and save them in db. If error , store as string and then display
		for line in lines:
			fields = line.split(",")

			edge = Relation()
			edge.child_id = fields[1]
			edge.parent_id = fields[2]

			edge.save()
			try:

				print(edge)
			except Exception as e:
				logging.getLogger("error_logger").error(repr(e))
				pass

	except Exception as e:
		logging.getLogger("error_logger").error("Unable to upload file. "+repr(e))
		messages.error(request, "Unable to upload file. "+repr(e))

	return HttpResponseRedirect(reverse("upload_edges"))
