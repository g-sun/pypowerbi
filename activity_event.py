# -*- coding: future_fstrings -*-


class ActivityEvent:
    id_key = 'Id'
    name_key = 'name'
    is_readonly_key = 'isReadOnly'
    is_on_dedicated_capacity_key = 'isOnDedicatedCapacity'
    record_type_key = 'RecordType'
    creation_time_key = 'CreationTime'
    operation_key = 'Operation'
    organization_id_key = 'OrganizationId'
    user_type_key = 'UserType'
    user_key = 'UserKey'
    workload_key = 'Workload'
    user_id_key = 'UserId'
    activity_key = 'Activity'
    item_name_key = 'ItemName'
    workspace_name_key = 'WorkSpaceName'
    dataset_name_key = 'DatasetName'
    report_name_key = 'ReportName'
    capacity_id_key = 'CapacityId'
    capacity_name_key = 'CapacityName'
    workspace_id_key = 'WorkspaceId'
    object_id_key = 'ObjectId'
    dataset_id_key = 'DatasetId'
    report_id_key = 'ReportId'
    embed_token_id_key = 'EmbedTokenId'
    is_success_key = 'IsSuccess'
    report_type_key = 'ReportType'
    request_id_key = 'RequestId'
    activity_id_key = 'ActivityId'
    distribution_method_key = 'DistributionMethod'

    def __init__(self, id, name, is_readonly, is_on_dedicated_capacity, 
                 record_type, creation_time, operation, organization_id,
                 user_type, user, workload, user_id, activity,
                 item_name, workspace_name, dataset_name, report_name,
                 capacity_id, capacity_name, workspace_id, object_id, dataset_id,
                 report_id, is_success, report_type, request_id,
                 activity_id, distribution_method, embed_token_id=None):
        self.id = id
        self.name = name
        self.is_readonly = is_readonly
        self.is_on_dedicated_capacity = is_on_dedicated_capacity
        self.record_type = record_type
        self.creation_time = creation_time
        self.operation = operation
        self.organization_id = organization_id
        self.user_type = user_type
        self.user = user
        self.workload = workload
        self.user_id = user_id
        self.activity = activity
        self.item_name = item_name
        self.workspace_name = workspace_name
        self.dataset_name = dataset_name
        self.report_name = report_name
        self.capacity_id = capacity_id
        self.capacity_name = capacity_name
        self.workspace_id = workspace_id
        self.object_id = object_id
        self.dataset_id = dataset_id
        self.report_id = report_id
        self.embed_token_id = embed_token_id
        self.is_success = is_success
        self.report_type = report_type
        self.request_id = request_id
        self.activity_id = activity_id
        self.distribution_method = distribution_method

    @classmethod
    def from_dict(cls, dictionary):
        activity_event_id = dictionary.get(cls.id_key)
        if activity_event_id is None:
            raise RuntimeError("ActivityEvent dictionary has no id key")

        name = dictionary.get(cls.name_key)
        is_readonly = dictionary.get(cls.is_readonly_key)
        is_on_dedicated_capacity = dictionary.get(cls.is_on_dedicated_capacity_key)
        record_type = dictionary.get(cls.record_type_key)
        creation_time = dictionary.get(cls.creation_time_key)
        operation = dictionary.get(cls.operation_key)
        organization_id = dictionary.get(cls.organization_id_key)
        user_type = dictionary.get(cls.user_type_key)
        user = dictionary.get(cls.user_key)
        workload = dictionary.get(cls.workload_key)
        user_id = dictionary.get(cls.user_id_key)
        activity = dictionary.get(cls.activity_key)
        item_name = dictionary.get(cls.item_name_key)
        workspace_name = dictionary.get(cls.workspace_name_key)
        dataset_name = dictionary.get(cls.dataset_name_key)
        report_name = dictionary.get(cls.report_name_key)
        capacity_id = dictionary.get(cls.capacity_id_key)
        capacity_name = dictionary.get(cls.capacity_name_key)
        workspace_id = dictionary.get(cls.workspace_id_key)
        object_id = dictionary.get(cls.object_id_key)
        dataset_id = dictionary.get(cls.dataset_id_key)
        report_id = dictionary.get(cls.report_id_key)
        embed_token_id = dictionary.get(cls.embed_token_id_key)
        is_success = dictionary.get(cls.is_success_key)
        report_type = dictionary.get(cls.report_type_key)
        request_id = dictionary.get(cls.request_id_key)
        activity_id = dictionary.get(cls.activity_id_key)
        distribution_method = dictionary.get(cls.distribution_method_key)

        return cls(id, name, is_readonly, is_on_dedicated_capacity, 
                 record_type, creation_time, operation, organization_id,
                 user_type, user, workload, user_id, activity,
                 item_name, workspace_name, dataset_name, report_name,
                 capacity_id, capacity_name, workspace_id, object_id, dataset_id,
                 report_id, is_success, report_type, request_id,
                 activity_id, distribution_method, embed_token_id)

    def __repr__(self):
        return f'<ActivityEvent {str(self.__dict__)}>'
