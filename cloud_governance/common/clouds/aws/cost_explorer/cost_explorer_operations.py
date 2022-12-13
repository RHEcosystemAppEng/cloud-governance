from datetime import datetime, timedelta

import boto3


class CostExplorerOperations:
    """
    This class extracts the price data from AWS Cost Explorer
    """

    def __init__(self):
        self.cost_explorer_client = boto3.client('ce')

    def get_cost_by_tags(self, tag: str, granularity: str = 'DAILY', cost_metric: str = 'UnblendedCost', start_date: str = '', end_date: str = ''):
        """
        This method extracts the price by Tag provided
        @return:
        """
        if not start_date and not end_date:
            end_date = datetime.now() - timedelta(1)
            start_date = end_date - timedelta(1)
            start_date = str(start_date.strftime('%Y-%m-%d'))
            end_date = str(end_date.strftime('%Y-%m-%d'))
        return self.get_cost_and_usage_from_aws(start_date=start_date, end_date=end_date, granularity=granularity, cost_metric=cost_metric, GroupBy=[{'Type': 'TAG', 'Key': tag}])

    def get_cost_and_usage_from_aws(self, start_date: str, end_date: str, granularity: str = 'DAILY', cost_metric: str = 'UnblendedCost', **kwargs):
        """
        This method returns the cost and usage reports
        @param start_date:
        @param end_date:
        @param granularity:
        @param cost_metric:
        @param kwargs:
        @return:
        """
        return self.cost_explorer_client.get_cost_and_usage(TimePeriod={
            'Start': start_date,
            'End': end_date
        }, Granularity=granularity, Metrics=[cost_metric], **kwargs)

    def get_cost_forecast(self, start_date: str, end_date: str, granularity: str, cost_metric: str):
        """
        This method return the cost forecasting
        @param start_date:
        @param end_date:
        @param granularity:
        @param cost_metric:
        @return:
        """
        return self.cost_explorer_client.get_cost_forecast(
            TimePeriod={
                'Start': start_date,
                'End': end_date
            },
            Granularity=granularity,
            Metric=cost_metric
        )
