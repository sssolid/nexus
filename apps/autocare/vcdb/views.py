from django.apps import apps
from django.http import Http404
from django.views.generic import ListView, DetailView


class VCdbModelMixin:
    app_label = "autocare"

    def get_model(self):
        model_name = self.kwargs["model"]
        try:
            return apps.get_model(self.app_label, model_name)
        except LookupError:
            raise Http404(f"Unknown VCDB model: {model_name}")


class VCdbListView(VCdbModelMixin, ListView):
    paginate_by = 50
    template_name = "autocare/vcdb/list.html"

    def get_queryset(self):
        self.model = self.get_model()
        return self.model.objects.all()


class VCdbDetailView(VCdbModelMixin, DetailView):
    template_name = "autocare/vcdb/detail.html"

    def get_object(self):
        self.model = self.get_model()
        return super().get_object()
