# python_project/admin.py
from django.contrib import admin
from django.urls import path
from django.template.response import TemplateResponse
from .models import Alert, Document, University, Speciality, Level, Semester, Matiere


class SupNumAdminSite(admin.AdminSite):
    site_header = "Administration SupNum"
    site_title = "SupNum Admin"
    index_title = "Tableau de bord"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "dashboard/",
                self.admin_view(self.dashboard_view),
                name="dashboard",
            ),
        ]
        return custom_urls + urls

    def dashboard_view(self, request):
        context = dict(
            self.each_context(request),
            total_alerts=Alert.objects.count(),
            total_documents=Document.objects.count(),
            total_universities=University.objects.count(),
            total_specialities=Speciality.objects.count(),
            total_levels=Level.objects.count(),
            total_semesters=Semester.objects.count(),
            total_matieres=Matiere.objects.count(),
        )
        return TemplateResponse(
            request,
            "admin/custom_dashboard.html",
            context,
        )


admin_site = SupNumAdminSite(name="supnum_admin")

admin_site.register(Alert)
admin_site.register(Document)
admin_site.register(University)
admin_site.register(Speciality)
admin_site.register(Level)
admin_site.register(Semester)
admin_site.register(Matiere)