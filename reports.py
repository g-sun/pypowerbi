# -*- coding: future_fstrings -*-
import io
from typing import Optional

import requests
import json
from requests.exceptions import HTTPError

import pypowerbi.client
from pypowerbi.report import Report


class Reports:
    # url snippets
    groups_snippet = 'groups'
    reports_snippet = 'reports'
    rebind_snippet = 'rebind'
    clone_snippet = 'clone'
    export_snippet = 'Export'
    generate_token_snippet = 'generatetoken'

    # json keys
    get_reports_value_key = 'value'

    def __init__(self, client):
        self.client = client
        self.base_url = f'{self.client.api_url}/{self.client.api_version_snippet}/{self.client.api_myorg_snippet}'

    def count(self, group_id=None):
        """
        Evaluates the number of reports
        :param group_id: The optional group id
        :return: The number of reports as returned by the API
        """
        return len(self.get_reports(group_id))

    def has_report(self, report_id, group_id=None):
        """
        Evaluates if the report exists
        :param report_id: The id of the report to evaluate
        :param group_id: The optional group id
        :return: True if the report exists, False otherwise
        """
        reports = self.get_reports(group_id)

        for report in reports:
            if report.id == str(report_id):
                return True

        return False

    def get_reports(self, group_id=None):
        """
        Gets all reports
        https://msdn.microsoft.com/en-us/library/mt634543.aspx
        :param group_id: The optional group id to get reports from
        :return: The list of reports for the given group
        """
        # group_id can be none, account for it
        if group_id is None:
            groups_part = '/'
        else:
            groups_part = f'/{self.groups_snippet}/{group_id}/'

        # form the url
        url = f'{self.base_url}{groups_part}{self.reports_snippet}/'
        # form the headers
        headers = self.client.auth_header

        # get the response
        response = requests.get(url, headers=headers)

        # 200 - OK. Indicates success. List of reports.
        if response.status_code == 200:
            reports = self.reports_from_get_reports_response(response)
        else:
            raise HTTPError(response, f'Get reports request returned http error: {response.json()}')

        return reports

    def get_report(self, report_id, group_id=None):
        """
        Gets a report
        https://msdn.microsoft.com/en-us/library/mt784668.aspx
        :param report_id: The id of the report to get
        :param group_id: The optional group id
        :return: The report as returned by the API
        """
        # group_id can be none, account for it
        if group_id is None:
            groups_part = '/'
        else:
            groups_part = f'/{self.groups_snippet}/{group_id}/'

        # form the url
        url = f'{self.base_url}{groups_part}{self.reports_snippet}/{report_id}'
        # form the headers
        headers = self.client.auth_header

        # get the response
        response = requests.get(url, headers=headers)

        # print(url, response.text)
        # 200 is the only successful code, raise an exception on any other response code
        if response.status_code != 200:
            raise HTTPError(response, f'Get the specified report request returned http error: {response.json()}')

        return Report.from_dict(json.loads(response.text))

    def clone_report(self, report_id, name, target_group_id, dataset_id, group_id=None):
        """
        Clones a report
        https://msdn.microsoft.com/en-us/library/mt784674.aspx
        :param report_id: The report id to clone
        :param name: The name to give the cloned report
        :param target_group_id: The target group for the cloned report
        :param dataset_id: The dataset id for the cloned report
        :param group_id: The optional group id
        :return: The cloned report
        """
        # group_id can be none, account for it
        if group_id is None:
            groups_part = '/'
        else:
            groups_part = f'/{self.groups_snippet}/{group_id}/'

        # form the url
        url = f'{self.base_url}{groups_part}{self.reports_snippet}/{report_id}/{self.clone_snippet}'
        # form the headers
        headers = self.client.auth_header
        # form the json
        json_dict = {
            Report.name_key: name,
            Report.target_model_id_key: str(dataset_id),
        }

        # target group id can be none, account for it
        if target_group_id is not None:
            json_dict[Report.target_workspace_id_key] = str(target_group_id)

        # get the response
        response = requests.post(url, headers=headers, json=json_dict)

        # 200 - OK. Indicates success.
        if response.status_code != 200:
            raise HTTPError(response, f'Clone report request returned http error: {response.json()}')

        return Report.from_dict(json.loads(response.text))

    def delete_report(self, report_id, group_id=None):
        """
        Deletes a report
        https://msdn.microsoft.com/en-us/library/mt784671.aspx
        :param report_id: The id of the report to delete
        :param group_id: The id of the group from which to delete the report
        """
        # group_id can be none, account for it
        if group_id is None:
            groups_part = '/'
        else:
            groups_part = f'/{self.groups_snippet}/{group_id}/'

        # form the url
        url = f'{self.base_url}{groups_part}{self.reports_snippet}/{report_id}/'
        # form the headers
        headers = self.client.auth_header

        # get the response
        response = requests.delete(url, headers=headers)

        # 200 - OK. Indicates success.
        if response.status_code != 200:
            raise HTTPError(response, f'Delete report request returned http error: {response.json()}')

    def rebind_report(self, report_id, dataset_id, group_id=None):
        """
        Rebinds a report to another dataset
        https://msdn.microsoft.com/en-us/library/mt784672.aspx
        :param report_id: The id of the report to rebind
        :param dataset_id: The id of the dataset to rebind the report to
        :param group_id: The optional id of the group from which the report belongs to
        """
        # group_id can be none, account for it
        if group_id is None:
            groups_part = '/'
        else:
            groups_part = f'/{self.groups_snippet}/{group_id}/'

        # form the url
        url = f'{self.base_url}{groups_part}{self.reports_snippet}/{report_id}/{self.rebind_snippet}'
        # form the headers
        headers = self.client.auth_header
        # form the json
        json_dict = {
            Report.dataset_id_key: dataset_id
        }

        # get the response
        response = requests.post(url, headers=headers, json=json_dict)

        # 200 - OK. Indicates success.
        if response.status_code != 200:
            raise HTTPError(response, f'Rebind report request returned http error: {response.json()}')

    def generate_token(self, report_id, token_request, group_id):
        """
        Generates an embed token for a report
        https://msdn.microsoft.com/en-us/library/mt784614.aspx
        :param report_id: The report to generate teh token for
        :param token_request: The token request object
        :param group_id: The group id
        :return: Returns the embed token
        """
        # form the url
        url = f'{self.base_url}/{self.groups_snippet}/{group_id}/' \
              f'{self.reports_snippet}/{report_id}/{self.generate_token_snippet}'
        # form the headers
        headers = self.client.auth_header
        # form the json
        json_dict = pypowerbi.client.TokenRequestEncoder().default(token_request)

        # get the response
        response = requests.post(url, headers=headers, json=json_dict)

        # 200 - OK. Indicates success.
        if response.status_code != 200:
            raise HTTPError(response, f'Generate token for report request returned http error: {response.json()}')

        return pypowerbi.client.EmbedToken.from_dict(json.loads(response.text))

    def export_report(
        self,
        report_id: str,
        save_path: str,
        filename: Optional[str] = None,
        group_id: Optional[str] = None
    ) -> None:
        """Exports the specified report to a pbix file.

        :param report_id: The report id
        :param save_path: The path where the pbix file should be saved
        :param filename: The name to assign to the downloaded file (without the pbix extension).
         If None, the report name will be used.
        :param group_id: The id of the workspace that contains the report. If None, then 'My workspace' is assumed.
        """
        # group_id can be None. Account for it here
        if group_id is None:
            groups_part = '/'
        else:
            groups_part = f'/{self.groups_snippet}/{group_id}/'

        # form the url
        url = f'{self.base_url}{groups_part}{self.reports_snippet}/{report_id}/{self.export_snippet}'

        # form the headers
        headers = self.client.auth_header

        # get the response
        response = requests.get(url, headers=headers)

        # 200 is the only valid response. Show an error in other cases.
        if response.status_code != 200:
            in_group_part = "" if group_id is None else "in Group"
            raise HTTPError(response, f'Export Report {in_group_part} request returned an http error: '
                                      f'{response.json()}')

        # save report to save path
        if filename is None:
            report = self.get_report(report_id, group_id)
            filename = report.name

        with open(f'{save_path}/{filename}.pbix', 'wb') as report_file:
            report_file.write(
                io.BytesIO(response.content).getbuffer()
            )

    @classmethod
    def reports_from_get_reports_response(cls, response):
        """
        Creates a list of reports from a http response
        :param response: The response to create the reports from
        :return: A list of reports created from the http response
        """
        # load the response into a dict
        response_dict = json.loads(response.text)
        reports = []
        # go through entries returned from API
        for entry in response_dict[cls.get_reports_value_key]:
            reports.append(Report.from_dict(entry))

        return reports
