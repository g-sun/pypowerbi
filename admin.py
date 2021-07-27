# -*- coding: future_fstrings -*-
import requests
import json
import urllib.parse

from requests.exceptions import HTTPError
from .group import Group
from .group_user import GroupUser
from .report import Report
from .report_user import ReportUser
from .dataset import Dataset
from .dataset_user import DatasetUser
from .activity_event import ActivityEvent

class Admin:
    # url snippets
    admin_snippet = 'admin'
    groups_snippet = 'groups'
    reports_snippet = 'reports'
    datasets_snippet = 'datasets'
    users_snippet = 'users'
    activity_events_snippet = 'activityevents'

    # json keys
    get_reports_value_key = 'value'
    get_users_value_key = 'value'
    get_datasets_value_key = 'value'
    get_activity_events_value_key = 'activityEventEntities'

    def __init__(self, client):
        self.client = client
        self.base_url = f'{self.client.api_url}/{self.client.api_version_snippet}/{self.client.api_myorg_snippet}'

    def get_groups(self, top=5000, expand_str=None, filter_str=None, skip=None):
        """
        Fetches all groups that the client has access to
        :param filter_str: OData filter string to filter results
        :param top: int > 0, OData top parameter to limit to the top n results
        :param skip: int > 0,  OData skip parameter to skip the first n results
        :return: list
            The list of groups
        """
        query_parameters = []

        if top:
            stripped_top = json.dumps(top).strip('"')
            query_parameters.append(f'$top={urllib.parse.quote(stripped_top)}')

        if expand_str:
            query_parameters.append(f'$expand={urllib.parse.quote(expand_str)}')

        if filter_str:
            query_parameters.append(f'$filter={urllib.parse.quote(filter_str)}')

        if skip:
            stripped_skip = json.dumps(skip).strip('"')
            query_parameters.append(f'$skip={urllib.parse.quote(stripped_skip)}')

        # form the url
        url = f'{self.base_url}/{self.admin_snippet}/{self.groups_snippet}'

        # add query parameters to url if any
        if len(query_parameters) > 0:
            url += f'?{str.join("&", query_parameters)}'

        # form the headers
        headers = self.client.auth_header
        # get the response
        response = requests.get(url, headers=headers)
        #print(url, headers, response)

        # 200 is the only successful code, raise an exception on any other response code
        if response.status_code != 200:
            print(response.content)
            raise HTTPError(response, f'Get Groups request returned http error: {response.json()}')

        return self.groups_from_get_groups_response(response)

    def get_group_users(self, group_id):
        """
        Returns a list of users that have access to the specified workspace.
        This API allows 200 requests per hour at maximum.
        GET https://api.powerbi.com/v1.0/myorg/admin/groups/{groupId}/users
        
        :param group_id:
            str - id of the group
        """
        # form the url
        url = url = f'{self.base_url}/{self.admin_snippet}/{self.groups_snippet}/{group_id}/{self.users_snippet}'
        # form the headers
        headers = self.client.auth_header

        # get the response
        response = requests.get(url, headers=headers)
        # 200 - OK. Indicates success. List of users.
        if response.status_code == 200:
            users = self.users_from_get_group_users_response(response)
        else:
            raise HTTPError(response, f'Get users request returned http error: {response.json()}')

        return users

    def get_reports(self, group_id=None):
        """
        Gets a list of reports from the organization or the specified group.
        :param group_id: The optional group id to get reports from
        :return: The list of reports for the organization or the specified group
        """
        # group_id can be none
        if group_id is None:
            groups_part = '/'
        else:
            groups_part = f'/{self.groups_snippet}/{group_id}/'

        # form the url
        url = f'{self.base_url}/{self.admin_snippet}{groups_part}{self.reports_snippet}/'
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

    def get_report_users(self, report_id):
        """
        Returns a list of users that have access to the specified report.
        GET https://api.powerbi.com/v1.0/myorg/admin/reports/{reportId}/users
        
        :param report_id:
            str - id of the report
        """
        # form the url
        url = url = f'{self.base_url}/{self.admin_snippet}/{self.reports_snippet}/{report_id}/{self.users_snippet}'
        # form the headers
        headers = self.client.auth_header

        # get the response
        response = requests.get(url, headers=headers)
        # 200 - OK. Indicates success. List of users.
        if response.status_code == 200:
            users = self.users_from_get_report_users_response(response)
        else:
            raise HTTPError(response, f'Get users request returned http error: {response.json()}')

        return users

    def get_datasets(self, group_id=None):
        """
        Fetches all datasets of the organization or the specified group
        :param group_id: The optional group id to get datasets from
        :return: The list of the datasets found
        """
        # group_id can be none, account for it
        if group_id is None:
            groups_part = '/'
        else:
            groups_part = f'/{self.groups_snippet}/{group_id}/'

        # form the url
        url = f'{self.base_url}/{self.admin_snippet}{groups_part}{self.datasets_snippet}'
        # form the headers
        headers = self.client.auth_header

        # get the response
        response = requests.get(url, headers=headers)

        # 200 is the only successful code, raise an exception on any other response code
        if response.status_code != 200:
            raise HTTPError(response, f'Get Datasets request returned http error: {response.json()}')

        return self.datasets_from_get_datasets_response(response)

    def get_dataset_users(self, dataset_id):
        """
        Returns a list of users that have access to the specified dataset.
        GET https://api.powerbi.com/v1.0/myorg/admin/datasets/{datasetId}/users
        
        :param dataset_id:
            str - id of the dataset
        """
        # form the url
        url = url = f'{self.base_url}/{self.admin_snippet}/{self.datasets_snippet}/{dataset_id}/{self.users_snippet}'
        # form the headers
        headers = self.client.auth_header

        # get the response
        response = requests.get(url, headers=headers)
        # 200 - OK. Indicates success. List of users.
        if response.status_code == 200:
            users = self.users_from_get_dataset_users_response(response)
        else:
            raise HTTPError(response, f'Get users request returned http error: {response.json()}')

        return users

    def get_activity_events(self, startDateTime, endDateTime, continuationToken=None, filter_str=None):
        """
        Fetches a list of audit activity events for a tenant
        This API allows 200 requests per hour at maximum
        :param startDateTime: Start date and time of the window for audit event results. Must be in ISO 8601 compliant UTC format
        :param endDateTime: End date and time of the window for audit event results. Must be in ISO 8601 compliant UTC format
        :param continuationToken: Token required to get the next chunk of the result set
        :param filter_str: Filters the results based on a boolean condition, using 'Activity', 'UserId', or both properties. Supports only 'eq' and 'and' operators
        :return: list
            The list of ActivityEvents
        """
        query_parameters = []

        query_parameters.append(f"startDateTime='{urllib.parse.quote(startDateTime)}'")

        query_parameters.append(f"endDateTime='{urllib.parse.quote(endDateTime)}'")

        if filter_str:
            query_parameters.append(f'$filter={urllib.parse.quote(filter_str)}')

        if continuationToken:
            query_parameters.append(f'continuationToken={urllib.parse.quote(continuationToken)}')

        # form the url
        url = f'{self.base_url}/{self.admin_snippet}/{self.activity_events_snippet}'

        # add query parameters to url if any
        if len(query_parameters) > 0:
            url += f'?{str.join("&", query_parameters)}'

        # form the headers
        headers = self.client.auth_header
        # get the response
        response = requests.get(url, headers=headers)

        # 200 is the only successful code, raise an exception on any other response code
        if response.status_code != 200:
            raise HTTPError(response, f'Get ActivityEvents request returned http error: {response.json()}')

        return self.activity_events_from_get_activity_events_response(response)

    @classmethod
    def groups_from_get_groups_response(cls, response):
        """
        Creates a list of groups from a http response object
        :param response:
            The http response object
        :return: list
            The list of groups
        """
        # load the response into a dict
        response_dict = json.loads(response.text)
        groups = []

        # go through entries returned from API
        for entry in response_dict[cls.get_reports_value_key]:
            groups.append(Group.from_dict(entry))

        return groups

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

    @classmethod
    def datasets_from_get_datasets_response(cls, response):
        """
        Creates a list of datasets from a http response object
        :param response: The http response object
        :return: A list of datasets created from the given http response object
        """
        # load the response into a dict
        response_dict = json.loads(response.text)
        datasets = []
        # go through entries returned from API
        for entry in response_dict[cls.get_datasets_value_key]:
            datasets.append(Dataset.from_dict(entry))

        return datasets

    @classmethod
    def activity_events_from_get_activity_events_response(cls, response):
        """
        Creates a list of activity events from a http response object
        :param response: The http response object
        :return: A list of activity events created from the given http response object
        """
        # load the response into a dict
        response_dict = json.loads(response.text)
        activity_events = []
        # go through entries returned from API
        for entry in response_dict[cls.get_activity_events_value_key]:
            activity_events.append(ActivityEvent.from_dict(entry))

        return activity_events
    @classmethod
    def users_from_get_group_users_response(cls, response):
        """
        Creates a list of users from a http response
        :param response: The response to create the users from
        :return: A list of users created from the http response
        """
        # load the response into a dict
        response_dict = json.loads(response.text)
        users = []
        # go through entries returned from API
        for entry in response_dict[cls.get_users_value_key]:
            users.append(GroupUser.from_dict(entry))

        return users

    @classmethod
    def users_from_get_report_users_response(cls, response):
        """
        Creates a list of users from a http response
        :param response: The response to create the users from
        :return: A list of users created from the http response
        """
        # load the response into a dict
        response_dict = json.loads(response.text)
        users = []
        # go through entries returned from API
        for entry in response_dict[cls.get_users_value_key]:
            users.append(ReportUser.from_dict(entry))

        return users

    @classmethod
    def users_from_get_dataset_users_response(cls, response):
        """
        Creates a list of users from a http response
        :param response: The response to create the users from
        :return: A list of users created from the http response
        """
        # load the response into a dict
        response_dict = json.loads(response.text)
        users = []
        # go through entries returned from API
        for entry in response_dict[cls.get_users_value_key]:
            users.append(DatasetUser.from_dict(entry))

        return users
