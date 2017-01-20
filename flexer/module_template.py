import jinja2
import os
import shutil

from os import path

MODTYPE_MAP = {
    "resource_connector": "cmp-connector.resources"
}


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

    def create_module(self, client, name, target_dir):
        """
        Create a new nFlex module.

        :param client: The CMP API client.
        :param name: The name for the new template
        :param target_dir: The directory in which the module will be created.
        """

        print "Creating nFlex module in '{}'...".format(target_dir)

        for template_file in os.listdir(self.template_dir):
            if template_file.endswith('.j2'):
                with open(path.join(self.template_dir, template_file)) as j2_file:
                    template = jinja2.Template(j2_file.read())

                with open(path.join(target_dir, template_file[:-3]), mode="w") as target_file:
                    target_file.write(template.render(
                        **self.get_template_params(client, name)
                    ))
            else:
                shutil.copyfile(
                    path.join(self.template_dir, template_file),
                    path.join(target_dir, template_file)
                )

    def get_template_params(self, client, module_name):
        """
        Get interpolation parameters for Jinja2 templates.

        :param client: The CMP API client.
        :param module_name: The name of the module being created.
        :return: A dict containing the template parameters.
        """

        template_params = {
            'module_name': module_name
        }

        # Add template-type-specific parameters (if any).
        self._add_parameters(template_params, client)

        return template_params

    @staticmethod
    def add_resource_connector_template_params(template_params, client):
        """
        Get additional template parameters for a resource connector template

        :param template_params: The existing template parameters.
        :param client: The CMP API client.
        """

        account = client.get("/accounts")[0]
        template_params.update({
            'account_id': account['id'],
            'account_name': account['name'],
            'provider_id': account['provider']['id'],
            'provider_name': account['provider']['name']
        })

    @staticmethod
    def add_metrics_connector_template_params(template_params, client):
        """
        Get additional template parameters for a resource connector template

        :param template_params: The existing template parameters.
        :param client: The CMP API client.
        """

        customer = client.get('/customers').json()['objects'][0]
        account = client.get('/accounts').json()[0]
        template_params.update({
            'account_id': account['id'],
            'account_name': account['name'],
            'provider_id': account['provider']['id'],
            'provider_name': account['provider']['name'],
            'customer_id': customer['id']
        })

    def _add_parameters(self, template_params, client):
        """
        Add template-type-specific parameters (if any) for the current template type.

        :param template_params: The existing template parameters.
        :param client: The CMP API client.
        """

        additional_parameters = self.__class__.__dict__.get(
            'add_{}_template_params'.format(self.template_type)
        )
        if additional_parameters:
            additional_parameters.__func__(template_params, client)

