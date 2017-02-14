import click
import jinja2
import os
import shutil

from os import path

_EVENT_SOURCE_MODTYPE_MAP = {
    "api-hook": "api_hook",
    "cmp-connector": "connector",
    "cmp-connector.logs": "log_connector",
    "cmp-connector.metrics": "metric_connector",
    "cmp-connector.resources": "resource_connector",
    "cmp-connector.spend": "spend_connector",
    "cmp-connector.tickets": "ticket_connector",
    "cmp-connector.validate_credentials": "credential_connector",
    "cmp-resource-notification": "resource_notification",
    "monitor": "resource_monitor",
    "service-catalog": "service_catalog"
}


class ModuleTemplate(object):
    """
    Creates a new nFlex module from a set of Jinja2 templates.
    """

    def __init__(self, template_dir, event_source):
        """
        Create a new `ModuleTemplate` from the specified template directory.

        :param template_dir: The directory containing the template files.
        :param event_source: The event source that triggers the module.
        """

        self.template_dir = template_dir
        self.event_source = event_source
        self.module_type = ModuleTemplate.get_module_type(self.event_source)

    def apply(self, client, name, target_dir):
        """
        Apply the template to create a new nFlex module.

        :param client: The CMP API client.
        :param name: The name for the new template
        :param target_dir: The directory in which the module will be created.
        """

        click.echo(
            "Generating nFlex module in '{}'...".format(target_dir)
        )

        template_parameters = self.get_template_params(client, name)
        for template_file in os.listdir(self.template_dir):
            if template_file.endswith('.j2'):
                j2_file = open(
                    path.join(self.template_dir, template_file)
                )
                with j2_file:
                    template = jinja2.Template(j2_file.read())

                target_file = open(
                    path.join(target_dir, template_file[:-3]),
                    mode="w"
                )
                with target_file:
                    target_file.write(
                        template.render(**template_parameters)
                    )
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

        account = client.get("/accounts").json()[0]
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
        Add template-type-specific parameters (if any)
        for the current template type.

        :param template_params: The existing template parameters.
        :param client: The CMP API client.
        """

        additional_parameters = self.__class__.__dict__.get(
            'add_{}_template_params'.format(self.module_type)
        )
        if additional_parameters:
            additional_parameters.__func__(template_params, client)

    @staticmethod
    def get_module_type(event_source):
        """
        Get the nFlex module type corresponding
        to the specified CMP event source.

        :param event_source: The event source (e.g. "cmp-connector.resources").
        :return: The module type (e.g. "resource_connector").
        """

        if event_source not in _EVENT_SOURCE_MODTYPE_MAP:
            return event_source

        return _EVENT_SOURCE_MODTYPE_MAP[event_source]
