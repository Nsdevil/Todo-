from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView
from django.utils.decorators import method_decorator
# from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from django.views import View

from .forms import AddLeadForm, AddCommentForm, AddFileForm
from .models import Lead

from client.models import Client, Comment as ClientComment
from team.models import Team
# Create your views here.


class LeadListView(ListView):
    model = Lead

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        queryset = super(LeadListView, self).get_queryset()
        return queryset.filter(
            created_by=self.request.user, converted_to_cient=False)


@login_required
def leads_list(request):
    leads = Lead.objects.filter(
        created_by=request.user, converted_to_cient=False)

    return render(request, 'lead/leads_list.html', {
        'leads': leads
    })


class LeadDetailView(DetailView):
    model = Lead

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = AddCommentForm()
        context['fileform'] = AddFileForm()

        return context

    def get_queryset(self):
        queryset = super(LeadDetailView, self).get_queryset()
        return queryset.filter(
            created_by=self.request.user, pk=self.kwargs.get('pk'))


@login_required
def leads_details(request, pk):
    lead = get_object_or_404(Lead, created_by=request.user, pk=pk)
    # lead=Lead.objects.filter(created_by=request.user).get(pk=pk)
    return render(request, 'lead/leads_details.html', {
        'lead': lead
    })


class LeadDeleteView(DeleteView):
    model = Lead
    success_url = reverse_lazy('leads:list')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        queryset = super(LeadDeleteView, self).get_queryset()
        return queryset.filter(
            created_by=self.request.user, pk=self.kwargs.get('pk'))

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


@login_required
def leads_delete(request, pk):
    lead = get_object_or_404(Lead, created_by=request.user, pk=pk)
    lead.delete()
    messages.success(request, 'The Task was deleted')
    return redirect('leads:list')


class LeadUpdateView(UpdateView):
    model = Lead
    fields = ('name', 'email', 'description', 'priority', 'status')
    success_url = reverse_lazy('leads:list')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['title'] = 'Edit-Task'

        return context

    def get_queryset(self):
        queryset = super(LeadUpdateView, self).get_queryset()
        return queryset.filter(
            created_by=self.request.user, pk=self.kwargs.get('pk'))

    # def get_success_url(self) -> str:
    #     return reverse_lazy('leads:list')


@login_required
def leads_edit(request, pk):
    lead = get_object_or_404(Lead, created_by=request.user, pk=pk)

    if request.method == 'POST':
        form = AddLeadForm(request.POST, instance=lead)
        if form.is_valid():
            form.save()
            messages.success(request, 'The Task was Edited')
            return redirect('leads:list')
    form = AddLeadForm(instance=lead)
    return render(request, 'lead/leads_edit.html', {
        'form': form
    })


class LeadCreateView(CreateView):
    model = Lead
    fields = ('name', 'email', 'description', 'priority', 'status')
    success_url = reverse_lazy('leads:list')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        team = Team.objects.filter(created_by=self.request.user)[0]
        context['team'] = team
        context['title'] = 'Add-Task'

        return context

    # def get_success_url(self) -> str:
    #     return reverse_lazy('leads:list')

    def form_valid(self, form):
        team = Team.objects.filter(created_by=self.request.user)[0]
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        self.object.team = team
        self.object.save()

        return redirect(self.get_success_url())


@login_required
def add_lead(request):
    team = Team.objects.filter(created_by=request.user)[0]
    if request.method == 'POST':
        form = AddLeadForm(request.POST)

        if form.is_valid():
            team = Team.objects.filter(created_by=request.user)[0]
            lead = form.save(commit=False)
            lead.created_by = request.user
            lead.team = team
            lead.save()
            messages.success(request, 'The Task was Created')

            return redirect('leads:list')

    form = AddLeadForm()
    return render(request, 'lead/add_lead.html', {
        'form': form,
        'team': team
    })


class AddFileView(View):
    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        form = AddFileForm(request.POST, request.FILES)
        if form.is_valid():
            team = Team.objects.filter(created_by=request.user)[0]
            file = form.save(commit=False)
            file.team = team
            file.lead_id = pk
            file.created_by = request.user
            file.save()
        return redirect('leads:details', pk=pk)


class AddCommentView(View):
    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        form = AddCommentForm(request.POST)
        if form.is_valid():
            team = Team.objects.filter(created_by=request.user)[0]
            comment = form.save(commit=False)
            comment.team = team
            comment.created_by = request.user
            comment.lead_id = pk
            comment.save()
        return redirect('leads:details', pk=pk)


class ConvertToClient(View):
    def get(self, request, *args, **kwargs):
        lead = get_object_or_404(
            Lead, created_by=request.user, pk=self.kwargs.get('pk'))
        team = Team.objects.filter(created_by=request.user)[0]

        client = Client.objects.create(
            name=lead.name,
            email=lead.email,
            description=lead.description,
            created_by=request.user,
            team=team
        )
        lead.converted_to_cient = True
        lead.save()
# convert leads comments to client comments
        comments = lead.comments.all()

        for comment in comments:
            ClientComment.object.create(
                client=client,
                content=comment.content,
                created_by=comment.created_by,
                team=team
            )

        messages.success(request, 'The Task was converted to a Task in Progress')
        return redirect('leads:list')


@login_required
def convert_to_client(request, pk):
    lead = get_object_or_404(Lead, created_by=request.user, pk=pk)
    team = Team.objects.filter(created_by=request.user)[0]

    client = Client.objects.create(
        name=lead.name,
        email=lead.email,
        description=lead.description,
        created_by=request.user,
        team=team
    )
    lead.converted_to_cient = True
    lead.save()
    messages.success(request, 'The Task was converted to a Task in Progress')
    return redirect('leads:list')
