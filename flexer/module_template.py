import jinja2
import os
import shutil

from os import path


class ModuleTemplate(object):
    """
    Creates a new nFlex module from a set of Jinja2 templates.
    """

    def __init__(self, template_type, template_dir):
        """
        Create a new `ModuleTemplate` from the specified template directory.

        :param template_type: The type of module created by the template.
        :param template_dir: The directory containing the template files.
        """

        self.template_type = template_type
        self.template_dir = template_dir

    def create_module(self, name, target_dir):
        """
        Create a new nFlex module.

        :param name: The name for the new template
        :param target_dir: The directory in which the module will be created.
        """

        print 'Create nFlex module in "{}" from "{}"'.format(self.template_dir, target_dir)

        for template_file in os.listdir(self.template_dir):
            if template_file.endswith('.j2'):
                with open(path.join(self.template_dir, template_file)) as j2_file:
                    template = jinja2.Template(j2_file.read())

                with open(path.join(target_dir, template_file[:-3])) as target_file:
                    target_file.write(template.render(
                        **self.get_template_params(name)
                    ))
            else:
                shutil.copyfile(
                    path.join(self.template_dir, template_file),
                    path.join(target_dir, template_file)
                )

    def get_template_params(self, module_name):
        template_params = {
            'module_name': module_name
        }

        # Template-type-specific parameters.
        if self.template_type == "widget":
            # template_params.update({ 'baz': 'bonk' })

            pass
        elif self.template_type == "metrics_connector":
            # Look up valid account, resource, etc.

            # template_params.update({ 'account_id': account_id, 'resource_id': resource_id })

            pass

        return template_params
