# -*- coding: future_fstrings -*-


class ReportUser:
    report_user_access_right_key = 'reportUserAccessRight'
    email_address_key = 'emailAddress'
    display_name_key = 'displayName'
    identifier_key = 'identifier'
    principal_type_key = 'principalType'

    def __init__(
        self,
        report_user_access_right,
        email_address="",
        display_name="",
        identifier="",
        principal_type=None
    ):
        """Constructs a ReportUser object

        :param report_user_access_right: Enum ReportUserAccessRight - The access right to assign to the ReportUser
        :param email_address: str - E-mail address of the user if principal type is user
        :param display_name: str - Display name of the principal
        :param identifier: str - Identifier of the principal
        :param principal_type: Enum PrincipalType - The principal type
        """
        self.report_user_access_right = report_user_access_right
        self.email_address = email_address
        self.display_name = display_name
        self.identifier = identifier
        self.principal_type = principal_type

    @classmethod
    def from_dict(cls, dictionary):
        """
        Creates a user from a dictionary
        :param dictionary: The dictionary to create a user from
        :return: The created dictionary
        """
        if cls.email_address_key not in dictionary:
             dictionary[cls.email_address_key] = ""
        return ReportUser(str(dictionary[cls.report_user_access_right_key]), str(dictionary[cls.email_address_key]), str(dictionary[cls.display_name_key]), str(dictionary[cls.identifier_key]), str(dictionary[cls.principal_type_key]))

    def as_set_values_dict(self):
        """Convert ReportUser object to dict with only values that are actually set. This dict can be used for
        reports.add_report_user requests.

        :return: Dict with object attributes in camelCase as keys, and attribute values as values.
        """
        report_user_dict = dict()

        if self.report_user_access_right:
            report_user_dict[self.report_user_access_right_key] = self.report_user_access_right.value

        if self.email_address:
            report_user_dict[self.email_address_key] = self.email_address

        if self.display_name:
            report_user_dict[self.display_name_key] = self.display_name

        if self.identifier:
            report_user_dict[self.identifier_key] = self.identifier

        if self.principal_type:
            report_user_dict[self.principal_type_key] = self.principal_type.value

        return report_user_dict

    def __repr__(self):
        return f'<ReportUser {str(self.__dict__)}>'
