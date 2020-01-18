from utils.stringutils import remove_parentheses


class TimetableFormatter:

    def __init__(self, T_data_label):
        self.assigned_methods = {}
        for tag in T_data_label:
            data_title = T_data_label[tag]
            self.assigned_methods[data_title] = f"_format_{tag}"

    def ttformat(self, data):
        data_title = data["data-title"]
        format_method_name = self.assigned_methods[data_title]
        format_method = getattr(self, format_method_name)
        return format_method(data)

    def _format_lecture(self, data):
        return data.text.strip()

    def _format_group(self, data):
        return data.find("div", class_="auditory").next.strip()

    def _format_time(self, data):
        return data.text.strip().split('-')

    def _format_week(self, data):
        return data.text.strip()

    def _format_subgroup(self, data):
        return data.text.strip()

    def _format_subject(self, data):
        return data.text.strip()

    def _format_auditory(self, data):
        return data.find("div", class_="auditory").next.strip()

    def _format_lecturer(self, data):
        return data.text.strip()

    def _format_type(self, data):
        return remove_parentheses(data.text).strip()
