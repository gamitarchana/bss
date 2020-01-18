from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.shortcuts import get_object_or_404
from .models import Employee, Babysitter, Client, UserProfile, JobRequest
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordResetForm
from django.utils.crypto import get_random_string
from django.contrib.admin import helpers
from django.utils.safestring import mark_safe
from django.forms.formsets import all_valid
#from django.contrib.auth.admin import UserAdmin
#from django.contrib.auth.models import User
from django_reverse_admin import ReverseModelAdmin
from django.shortcuts import render
from django.db.models import OneToOneField, ForeignKey
from django.contrib.admin.utils import (flatten_fieldsets, unquote)
from django.forms import modelformset_factory
from django_reverse_admin import ReverseInlineModelAdmin, ReverseInlineFormSet
import copy

class EmployeeAdmin(ReverseModelAdmin):
    inline_type = 'stacked'
    inline_reverse = [('user', {'fields': ['username', 'first_name', 'last_name', 'email', 'is_superuser', 'is_staff', 'is_active', 'primary_contact_number', 'alternate_contact_number', 'address' , 'avatar']}),
                      ]
admin.site.register(Employee, EmployeeAdmin)

class BabysitterAdmin(ReverseModelAdmin):
    inline_type = 'stacked'
    inline_reverse = [('user', {'fields': ['username', 'first_name', 'last_name', 'email', 'is_active', 'primary_contact_number', 'alternate_contact_number', 'address' , 'avatar']}),
    ]
    '''def get_queryset(self, request):
        query = super(BabysitterAdmin, self).get_queryset(request)
        filtered_query = query.filter(user__user_type=UserProfile.BABYSITTER)
        return filtered_query'''
admin.site.register(Babysitter, BabysitterAdmin)

class ClientAdmin(ReverseModelAdmin):
    inline_type = 'stacked'
    inline_reverse = [('user', {'fields': ['username', 'first_name', 'last_name', 'email', 'is_active', 'primary_contact_number', 'alternate_contact_number', 'address' , 'avatar']}),
    ]
admin.site.register(Client, ClientAdmin)

PENDING_APPROVAL_FROM_EXECUTIVE = 2
PENDING_APPROVAL_FROM_ADMIN = 3
ACCEPTED = 4
REJECTED = 5

def make_changes_suggested_by_executive(modeladmin, request, queryset):
    queryset.update(status=JobRequest.PENDING_APPROVAL_FROM_EXECUTIVE)
make_changes_suggested_by_executive.short_description = "Re-send for changes - Level 1"

def make_approved_by_executive(modeladmin, request, queryset):
    queryset.update(status=JobRequest.PENDING_APPROVAL_FROM_ADMIN)
make_approved_by_executive.short_description = "Approve - Level 1"

def make_changes_suggested_by_admin(modeladmin, request, queryset):
    queryset.update(status=JobRequest.PENDING_APPROVAL_FROM_ADMIN)
make_changes_suggested_by_admin.short_description = "Re-send for changes - Level 2"

def make_approved_by_admin(modeladmin, request, queryset):
    queryset.update(status=JobRequest.ACCEPTED)
make_approved_by_admin.short_description = "Approve - Level 2"

def make_rejected_by_admin(modeladmin, request, queryset):
    queryset.update(status=JobRequest.REJECTED)
make_rejected_by_admin.short_description = "Reject"



'''class JobRequestAdmin(ReverseModelAdmin):
    #pass
    #fields = ["babysitter"]
    inline_type = 'stacked'
    inline_reverse = [('babysitter', {'fields': ['user', 'peference_hours_per_day','preference_no_of_children']})]
    exclude = ["status"]
    #
    #actions = [make_changes_suggested_by_executive, make_approved_by_executive, make_changes_suggested_by_admin, make_approved_by_admin, make_rejected_by_admin]
admin.site.register(JobRequest, JobRequestAdmin)'''


'''def JobRequestAdminView(request):
    return render(request, 'admin/job_request.html', {})

#admin.site.register_view('jobrequest/', 'Babysitter Job Request', view=JobRequestAdminView)'''


''''class BabysitterInline(admin.StackedInline):
    model = Babysitter
    fields = ('peference_hours_per_day','preference_no_of_children','preference_locations')

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    fields = ('username','first_name','last_name','email','is_active', 'primary_contact_number','alternate_contact_number','address','avatar')'''

class JobRequestAdmin(admin.ModelAdmin):

    # A template for a very customized change view:
    change_form_template = 'admin/jobrequest.html'
    add_form_template = 'admin/jobrequest.html'
    exclude = ['babysitter', 'status',]

    tmp_inline_instances = []

    def get_inline_instances(self, request, obj=None):
        print("get_inline_instances")
        #return self.tmp_inline_instances #+ super(JobRequestAdmin, self).get_inline_instances(request, obj)
        return self.tmp_inline_instances

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        execlude = ['babysitter', 'status',]


        model = self.model
        opts = model._meta
        if not self.has_add_permission(request):
            raise PermissionDenied

        model_form = self.get_form(request)
        formsets = []

        obj = self.get_object(request, unquote(object_id))

        if not self.has_view_permission(request, obj) and not self.has_change_permission(request, obj):
            raise PermissionDenied

        if obj is None:
            return self._get_obj_does_not_exist_redirect(request, opts, object_id)

        inline_instances = []
        inline_admin_formsets = []

        if request.method == 'POST':
            form = model_form(request.POST, request.FILES, instance=obj)
            print("post form")
            print(form)
            form_validated = form.is_valid()
            if form_validated:
                new_object = self.save_form(request, form, change=True)#not add
            else:
                new_object = form.instance

            #print("-----------new_object--------------------")
            #print(new_object)
            prefixes = {}
            #print("self.get_formsets_with_inlines(request)-------------------------")
            #print(self.get_formsets_with_inlines(request))

            #print("self.get_formsets_with_inlines(request)-------------------------")
            #print(self.get_formsets_with_inlines(request))

            for FormSet, inline in self.get_formsets_with_inlines(request):
                #print("Formset inline")
                #print(FormSet)
                #print(inline)
                prefix = FormSet.get_default_prefix()
                prefixes[prefix] = prefixes.get(prefix, 0) + 1
                if prefixes[prefix] != 1:
                    prefix = "%s-%s" % (prefix, prefixes[prefix])
                #print("prefix---------------------------")
                #print(prefix)
                #data1 = copy.deepcopy(request.POST)
                '''tmp_data = {
                            'form-TOTAL_FORMS': ['2'],
                            'form-INITIAL_FORMS': '2',
                            'form-MAX_NUM_FORMS': '2',
                            'form-MIN_NUM_FORMS': '2',
                }'''
                #data.update(tmp_data)
                '''data1['form-TOTAL_FORMS'] = '1'
                data1['form-INITIAL_FORMS'] = '1'
                data1['form-MAX_NUM_FORMS'] = '1'
                data1['form-MIN_NUM_FORMS'] = '0'
                print("data=data----------------")'''
                #print(data1)
                formset = FormSet(data=request.POST, files=request.FILES,
                                  instance=new_object,
                                  save_as_new="_saveasnew" in request.POST)
                                  #prefix=prefix)
                ##print("formset")
                #print(formset)
                formsets.append(formset)
                print("-------------form_validated----------")
                print(form_validated)
                print("-------_formsets_are_blank-------------------")
                print(_formsets_are_blank(request, new_object, formsets))
                print("all_valid(formsets)")
                f=all_valid(formsets)
                print(f)
            if form_validated and _formsets_are_blank(request, new_object, formsets):
                print("-------_formsets_are_blank-------------------")
                self.save_model(request, new_object, form, change=True)#not add)
                return self.response_add(request, new_object)
            elif form_validated and all_valid(formsets):
                # Here is the modified code.
                print("-------------form_validated----------")
                for formset, inline in zip(formsets, self.get_inline_instances(request)):
                    print("-------------form_validated for loop----------")
                    print(inine)
                    if not isinstance(inline, ReverseInlineModelAdmin):
                        continue
                    # The idea or this piece is coming from https://stackoverflow.com/questions/50910152/inline-formset-returns-empty-list-on-save.
                    # Without this, formset.save() was returning None for forms that
                    # haven't been modified
                    forms = [f for f in formset]
                    if not forms:
                        continue
                    obj = forms[0].save()
                    print("----------form obj----------------")
                    print(obj)
                    setattr(new_object, inline.parent_fk_name, obj)
                self.save_model(request, new_object, form, change=not add)
                form.save_m2m()
                for formset in formsets:
                    self.save_formset(request, form, formset, change=not add)

                # self.log_addition(request, new_object)
                return self.response_add(request, new_object)
        else:
            form = model_form(instance=obj)
            formsets, inline_instances = self._create_formsets(request, obj, change=True)
            print("else -----------------formsets")
            print(formsets)
            print("formsets")


            #inline_instances = []
            #inline_admin_formsets = []

        for field in self.model._meta.get_fields():
            if isinstance(field, (OneToOneField, ForeignKey)):
                parent = field.remote_field.model
                BabysitterFormSet = modelformset_factory(Babysitter, fields=('peference_hours_per_day','preference_no_of_children','preference_locations'), extra = 0)
                babysitter_form = BabysitterFormSet(queryset=Babysitter.objects.filter(user_id=obj.babysitter.user.id))
                '''print("model--------------------")
                print(model)
                print("parent---------------------")
                print(parent)'''
                name=field.name
                inline_type = "stacked"
                babysitter_inline = ReverseInlineModelAdmin(model,
                                 name,
                                 parent,
                                 self.admin_site,
                                 inline_type)
                kwargs = { 'fields': ['peference_hours_per_day','preference_no_of_children','preference_locations']}
                babysitter_inline.__dict__.update(kwargs)

                inline_instances.append(babysitter_inline)
                fieldsets = [(None, { 'fields': ['peference_hours_per_day','preference_no_of_children','preference_locations']})]

                inline_admin_formset = helpers.InlineAdminFormSet(babysitter_inline, babysitter_form, fieldsets)
                inline_admin_formsets.append(inline_admin_formset)
                for field in parent._meta.get_fields():
                    if isinstance(field, (OneToOneField, ForeignKey)):
                        parent = field.remote_field.model

                        UserFormSet = modelformset_factory(UserProfile, fields=('username','first_name','last_name','email','is_active', 'primary_contact_number','alternate_contact_number','address','avatar'), extra = 0)
                        user_form = UserFormSet(queryset=UserProfile.objects.filter(id=obj.babysitter.user.id))
                        model = field.model
                        '''print("model--------------------")
                        print(model)
                        print("parent---------------------")
                        print(parent)
                        print("field------------")
                        print(field.model)'''
                        name=field.name
                        inline_type = "stacked"

                        user_inline = ReverseInlineModelAdmin(model,
                                 name,
                                 parent,
                                 self.admin_site,
                                 inline_type)
                        kwargs = { 'fields': ['username','first_name','last_name','email','is_active', 'primary_contact_number','alternate_contact_number','address','avatar']}
                        user_inline.__dict__.update(kwargs)
                        inline_instances.append(user_inline)
                        fieldsets = [(None, { 'fields': ['username','first_name','last_name','email','is_active', 'primary_contact_number','alternate_contact_number','address','avatar']})]

                        inline_admin_formset = helpers.InlineAdminFormSet(user_inline, user_form, fieldsets)
                        inline_admin_formsets.append(inline_admin_formset)

        self.tmp_inline_instances = inline_instances
        readonly_fields = self.get_readonly_fields(request, obj)
        adminForm = helpers.AdminForm(form,
                                      list(self.get_fieldsets(request)),
                                      self.prepopulated_fields,
                                      readonly_fields=readonly_fields,
                                      model_admin=self
                                      )
        media = self.media + adminForm.media

        '''inline_admin_formsets = []
        for inline, formset in zip(self.get_inline_instances(request), formsets):
            fieldsets = list(inline.get_fieldsets(request))
            inline_admin_formset = helpers.InlineAdminFormSet(inline, formset, fieldsets)
            inline_admin_formsets.append(inline_admin_formset)
            #print('inline_admin_formset--------------')
            #print(inline_admin_formset)
            #print(inline)
            #print(fieldsets)
            #print(inline_admin_formset.has_add_permission)
            media = media + inline_admin_formset.media'''

        context = self.admin_site.each_context(request)
        reverse_admin_context = {
            #'title': _(('Change %s', 'Add %s')[add] % force_text(opts.verbose_name)),
            'adminform': adminForm,
            # 'is_popup': '_popup' in request.REQUEST,
            'is_popup': False,
            'show_delete': False,
            'media': mark_safe(media),
            'inline_admin_formsets': inline_admin_formsets,
            'errors': helpers.AdminErrorList(form, formsets),
            # 'root_path': self.admin_site.root_path,
            'app_label': opts.app_label,
        }
        print("------------errors-----------")
        errors = helpers.AdminErrorList(form, formsets)
        print(errors)
        context.update(reverse_admin_context)
        context.update(extra_context or {})
        return self.render_change_form(request, context, form_url=form_url, add=False)


    def add_view(self, request, form_url='', extra_context=None):
        extra_context = extra_context or {}
        #extra_context['osm_data'] = self.get_osm_info()
        print("new objec id----------------------------------------------")
        #print(object_id)
        #print(context)
        #obj = self.get_object(request, unquote(object_id))
        #print(obj.id)
        #print(self.model)
        for field in self.model._meta.get_fields():
            #print(field)
            #print(getattr(self.model, "status"))
            #obj_babysitter = Babysitter.objects.filter(id=obj.babysitter)
            #print(obj.babysitter.user.id)
            if isinstance(field, (OneToOneField, ForeignKey)):
                #print("one to one")
                parent = field.remote_field.model
                #print(obj.parent_fk_name)
                #parent_obj = getattr(instance, self.parent_fk_name, None)

                for field in parent._meta.get_fields():
                    if isinstance(field, (OneToOneField, ForeignKey)):
                        #print("one to one")
                        parent = field.remote_field.model
                        UserFormSet = modelformset_factory(UserProfile, fields=('username','first_name','last_name','email','is_active', 'primary_contact_number','alternate_contact_number','address','avatar'), extra = 1)
                        #id=parent._meta.get_field('id')
                        #id_value = parent.username
                        #print()
                        #user_form = UserFormSet(queryset=UserProfile.objects.filter(id=obj.babysitter.user.id
                        user_form = UserFormSet(queryset=UserProfile.objects.none())
                        extra_context['user_form'] = user_form
                        #for field in parent._meta.get_fields():
                            #print(field)
                BabysitterFormSet = modelformset_factory(Babysitter, fields=('peference_hours_per_day','preference_no_of_children','preference_locations'), extra = 1)
                babysitter_form = BabysitterFormSet(queryset=Babysitter.objects.none())
                extra_context['babysitter_form'] = babysitter_form
                print(babysitter_form.instance)

        return super().add_view(
            request, form_url, extra_context=extra_context,
        )


    #ef _changeform_view(self, request, form_url='', extra_context=None):
    #    pass



def _formsets_are_blank(request, obj, formsets):
    """
    This function handles the blank/null inlines by checking whether the
    non-valid formsets are both unchanged and are for inline fields.
    """

    for formset in formsets:
        if isinstance(formset, ReverseInlineFormSet):
            field = next((f for f in obj._meta.fields if f.name == formset.parent_fk_name), None)
            if not field.blank or formset.has_changed():
                return False
        elif formset.has_changed():
            return False
    return True





admin.site.register(JobRequest, JobRequestAdmin)
