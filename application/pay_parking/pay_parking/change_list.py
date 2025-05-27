from django.contrib.admin.views.main import ChangeList

class CustomChangeList(ChangeList):
    filter_form_class = None

    def __init__(self, request, model, list_display, list_display_links, list_filter, date_hierarchy, search_fields, list_select_related, list_per_page, list_max_show_all, list_editable, model_admin, sortable_by, search_help_text,):
        self.filter_form = self.filter_form_class(request.GET)
        super().__init__(request, model, list_display, list_display_links, list_filter, date_hierarchy, search_fields, list_select_related, list_per_page, list_max_show_all, list_editable, model_admin, sortable_by, search_help_text,)

    def get_queryset(self, request):
        (
            self.filter_specs,
            self.has_filters,
            remaining_lookup_params,
            filters_may_have_duplicates,
            self.has_active_filters,
        ) = self.get_filters(request)
        # Then, we let every list filter modify the queryset to its liking.
        qs = self.root_queryset
        for filter_spec in self.filter_specs:
            if (
                filter_spec.expected_parameters()[0] not in self.filter_form.errors
            ):
                new_qs = filter_spec.queryset(request, qs)
                if new_qs is not None:
                    qs = new_qs

        # try:
        #     # Finally, we apply the remaining lookup parameters from the query
        #     # string (i.e. those that haven't already been processed by the
        #     # filters).
        #     q_object = build_q_object_from_lookup_parameters(
        #         remaining_lookup_params)
        #     qs = qs.filter(q_object)
        # except (SuspiciousOperation, ImproperlyConfigured):
        #     # Allow certain types of errors to be re-raised as-is so that the
        #     # caller can treat them in a special way.
        #     raise
        # except Exception as e:
        #     # Every other error is caught with a naked except, because we don't
        #     # have any other way of validating lookup parameters. They might be
        #     # invalid if the keyword arguments are incorrect, or if the values
        #     # are not in the correct type, so we might get FieldError,
        #     # ValueError, ValidationError, or ?.
        #     raise IncorrectLookupParameters(e)

        if not qs.query.select_related:
            qs = self.apply_select_related(qs)

        # Set ordering.
        ordering = self.get_ordering(request, qs)
        qs = qs.order_by(*ordering)

        # Apply search results
        qs, search_may_have_duplicates = self.model_admin.get_search_results(
            request,
            qs,
            self.query,
        )

        # Set query string for clearing all filters.
        self.clear_all_filters_qs = self.get_query_string(
            new_params=remaining_lookup_params,
            remove=self.get_filters_params(),
        )
        # Remove duplicates from results, if necessary
        if filters_may_have_duplicates | search_may_have_duplicates:
            return qs.distinct()
        else:
            return qs
