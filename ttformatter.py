class TTFormatter:

    def __init__(self, translations):
        self.assigned_methods = {}
        format_methods = [method for method in dir(self) if method.startswith("_format")]
        for tag in translations:
            data_title = translations[tag]
            self.assigned_methods[data_title] = f"_format_{tag}"

    def ttformat(self, data):
        data_title = data["data-title"]
        format_method_name = self.assigned_methods[data_title]
        format_method = getattr(self, format_method_name)
        return format_method(data)

    def _format_lecture(self, data):
        return data.text

    def _format_group(self, data):
        return data.find("div", class_="auditory").next

    def _format_time(self, data):
        return data.text.split('-')

    def _format_week(self, data):
        return data.text

    def _format_subgroup(self, data):
        return data.text

    def _format_subject(self, data):
        return data.text

    def _format_auditory(self, data):
        return data.find("div", class_="auditory").next

    def _format_lecturer(self, data):
        return data.text

    def _format_type(self, data):
        return data.text
