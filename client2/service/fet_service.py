import fet_pb2
import fet_pb2_grpc
import logging
import numpy as np
import pandas as pd
from sklearn import preprocessing


my_sample_dict = {}


def convert_string_columns_to_numeric():
    df = pd.read_csv('/Users/mohimenul.admin/PycharmProjects/fet/client2/service/ds_client_two.csv')

    # Select all columns with string values
    string_columns = df.select_dtypes(include='object')
    string_columns = string_columns.drop(columns=['Loan_Status', 'Loan_ID'], axis=1)

    # Create a label encoder for each string column
    label_encoders = {column: preprocessing.LabelEncoder() for column in string_columns}

    # Encode the string values in each column
    df[string_columns.columns] = string_columns.apply(lambda x: label_encoders[x.name].fit_transform(x))

    # Return the modified dataframe
    return df


def get_random_value_from_range(column):
    # Get the minimum and maximum values of the column
    min_value = column.min()
    max_value = column.max()

    # Generate a random value between the min and max values
    random_value = np.random.uniform(min_value, max_value)
    return random_value


# #################### Second function ############################
def split_dataframe_on_column_value(df, column_name, split_value):
    # Select rows with values less than or equal to the split value
    df1 = df[df[column_name] <= split_value]

    # Select rows with values greater than the split value
    df2 = df[df[column_name] > split_value]

    # Return the two dataframes as a tuple
    return df1, df2


def get_aggregated_label_counts(df, column_name):
    # Get the value counts of the column
    value_counts = df[column_name].value_counts()

    # Get the unique values and counts as two separate lists
    unique_values = value_counts.index.tolist()
    counts = value_counts.values.tolist()

    count_map = {'Y': 0, 'N': 0}
    # Return the unique values and counts as a tuple

    for idx, uv in enumerate(unique_values):
        count_map[uv] = counts[idx]

    return count_map


class FetCommunication(fet_pb2_grpc.MasterClientCommunicationServiceServicer):

    def GetRandomSplitValueFromClient(self, request, context):
        logging.warning(f'GetRandomSplitValueFromClient requestObject: {request}')

        numerical_column = convert_string_columns_to_numeric()
        # Get the first column using its name
        column = numerical_column[request.feature]
        random_split_value = get_random_value_from_range(column)

        split_value_response = fet_pb2.GetRandomSplitValueFromClientResponse()
        split_value_response.clientId = request.clientId
        split_value_response.splitValue = random_split_value

        return split_value_response

    def GetAggregatedValuesFromClient(self, request, context):
        logging.warning(f'GetAggregatedValuesFromClient requestObject: {request}')

        # dataSet need to be used from the my_sample_dict
        numerical_column = convert_string_columns_to_numeric()
        if request.dataSet in my_sample_dict:
            numerical_column = my_sample_dict[request.dataSet]

        df1, df2 = split_dataframe_on_column_value(numerical_column, request.feature, request.splitValue)
        counts_left = get_aggregated_label_counts(df1, 'Loan_Status')
        counts_right = get_aggregated_label_counts(df2, 'Loan_Status')
        print(f' {counts_left},  {counts_right}')

        response = fet_pb2.GetAggregatedValuesFromClientResponse()

        ag_left = fet_pb2.AggregatedValue()
        ag_left.approvedLoan = counts_left['Y']
        ag_left.declinedLoan = counts_left['N']

        ag_right = fet_pb2.AggregatedValue()
        ag_right.approvedLoan = counts_right['Y']
        ag_right.declinedLoan = counts_right['N']

        response.aggregatedValueLeft.CopyFrom(ag_left)
        response.aggregatedValueRight.CopyFrom(ag_right)

        return response

    def BroadcastTreeNodesBasedOnBestSplit(self, request, context):
        logging.warning(f'BroadcastTreeNodesBasedOnBestSplit requestObject: {request}')

        # dataSet need to be used from the my_sample_dict
        numerical_column = convert_string_columns_to_numeric()
        if request.dataSet in my_sample_dict:
            numerical_column = my_sample_dict[request.dataSet]

        df1, df2 = split_dataframe_on_column_value(numerical_column, request.feature, request.splitValue)
        my_sample_dict[f'{request.treeHeight}_left'] = df1
        my_sample_dict[f'{request.treeHeight}_right'] = df2

        return fet_pb2.ReceivedResponse(response=True)
