import pandas as pd
import logging
import grpc
import fet_pb2
import fet_pb2_grpc
import random
from sklearn import preprocessing


class TreeNode:
    def __init__(self, feature=None, split_value=0, tree_height=0, leaf_value=None, left=None, right=None):
        self.feature = feature
        self.split_value = split_value
        self.tree_height = tree_height
        self.leaf_value = leaf_value
        self.left = left
        self.right = right


class GiniImpurity:
    def __init__(self, gini_impurity=0, feature='', split_value=0):
        self.gini_impurity = gini_impurity
        self.feature = feature
        self.split_value = split_value


def getSplitValueFromClient(feature_name, client_id):
    response = 0
    with grpc.insecure_channel(f'localhost:{client_id}') as channel:
        # Fet service client test
        stub = fet_pb2_grpc.MasterClientCommunicationServiceStub(channel)
        request = fet_pb2.GetRandomSplitValueFromClientRequest()
        request.feature = feature_name
        request.clientId = client_id
        response = stub.GetRandomSplitValueFromClient(request)
        channel.close()
        return response


def getAggregatedValueFromClient(feature_name, client_id, split_value, data_set):
    response = None
    # print(f'{feature_name},{client_id}, {split_value}, {data_set}')
    with grpc.insecure_channel(f'localhost:{client_id}') as channel:
        stub = fet_pb2_grpc.MasterClientCommunicationServiceStub(channel)
        request = fet_pb2.GetAggregatedValuesFromClientRequest()
        request.feature = feature_name
        request.clientId = client_id
        request.splitValue = split_value
        request.dataSet = data_set
        response = stub.GetAggregatedValuesFromClient(request)
        channel.close()
        return response


def broadCastTreeNodeBasedOnBestSplit(client_id, feature, split_value, tree_height):
    with grpc.insecure_channel(f'localhost:{client_id}') as channel:
        stub = fet_pb2_grpc.MasterClientCommunicationServiceStub(channel)
        response = stub.BroadcastTreeNodesBasedOnBestSplit(
            fet_pb2.BroadcastTreeNodesBasedOnBestSplitRequest(feature=feature, splitValue=split_value,
                                                              treeHeight=tree_height))
        channel.close()
        return response


def isStoppingCondition(counts, treeheight):
    approvedLoan_count = counts[0]
    declinedLoan_count = counts[1]

    if sum(counts) == 0:
        return True
    if approvedLoan_count >= declinedLoan_count:
        percentage = (approvedLoan_count / sum(counts))
    else:
        percentage = (declinedLoan_count / sum(counts))

    decision = (percentage >= .80) or (treeheight >= 3)
    return decision


def get_random_element(arr):
    # Get a random index from the array
    random_index = random.randint(0, len(arr) - 1)
    # Return the element at the random index
    return arr[random_index]


def random_subset(lst):
    result = []
    for i in range(len(lst) // 2):
        index = random.randint(0, len(lst) - 1)
        result.append(lst[index])
    return result


def get_global_label_count(aggregatedValueList):
    accumulated_count_left = [0, 0]
    accumulated_count_right = [0, 0]

    for label in aggregatedValueList:
        accumulated_count_left[0] += label.aggregatedValueLeft.approvedLoan
        accumulated_count_left[1] += label.aggregatedValueLeft.declinedLoan

        accumulated_count_right[0] += label.aggregatedValueRight.approvedLoan
        accumulated_count_right[1] += label.aggregatedValueRight.declinedLoan

    return accumulated_count_left, accumulated_count_right


def gini_impurity_of_leaf(counts):
    # Get the size of the sample space
    n = sum(counts)
    if n == 0:
        return 1
    # Calculate the Gini impurity
    impurity = 1 - sum((count / n) ** 2 for count in counts)
    return impurity


def gini_impurity_of_node(gi1, count1, gi2, count2):
    n = sum(count1) + sum(count2)
    avg_impurity = (gi1 * sum(count1)) / n + (gi2 * sum(count2)) / n
    return avg_impurity


def get_min_gini_impurity(arr: list[GiniImpurity]):
    # Set the initial minimum value to the first element in the list
    min_value = arr[0]
    # Iterate over the elements in the list
    for element in arr:
        # If the current element is less than the current minimum value, update the minimum value
        if element.gini_impurity < min_value.gini_impurity:
            min_value = element
    # Return the minimum value
    return min_value


def print_tree(root, node_name):
    # Base case: if the root is None, return
    if root is None:
        return

    if root.leaf_value is not None:
        print(f'Leaf Node height={root.tree_height} ==> Leaf Node value = {root.leaf_value}')
    else:
        # Print the root value
        print(f'{node_name} height={root.tree_height} ==> feature = {root.feature} split_value = {root.split_value}')
    # Recursively print the left and right subtrees
    print_tree(root.left, 'left')
    print_tree(root.right, 'right')


# buildTree for master
# Append the tree inside the forest
forest = []


# for first time aggregated_label can be [1,1] or 50/50
# dataset can be 'Full'
# tree_height = 0
def buildTree(feature_list, aggregated_label, tree_height, dataset):
    if isStoppingCondition(aggregated_label, tree_height):
        if aggregated_label[0] >= aggregated_label[1]:
            return TreeNode(leaf_value='Y', tree_height=tree_height)
        else:
            return TreeNode(leaf_value='N', tree_height=tree_height)

    # Randomly choose feature subset
    random_feature_set = random_subset(feature_list)

    client_set = [8282, 8383]

    gini_impurity_list: list[GiniImpurity] = []

    for feature in random_feature_set:

        # get the split value for each client
        split_value_set = []
        for client in client_set:
            split_value_set.append(getSplitValueFromClient(feature, client))

        selected_sv_response = get_random_element(split_value_set)
        split_value = selected_sv_response.splitValue

        # gather sum_left and sum_right from each client
        aggregatedValueList = []
        for client in client_set:
            aggregatedValueList.append(getAggregatedValueFromClient(feature, client, split_value, dataset))

        CL, CR = get_global_label_count(aggregatedValueList)
        gini_impurity_value = gini_impurity_of_node(gini_impurity_of_leaf(CL), CL, gini_impurity_of_leaf(CR), CR)

        gini_impurity_list.append(
            GiniImpurity(gini_impurity=gini_impurity_value, feature=feature, split_value=split_value))

    currently_best_split_feature = get_min_gini_impurity(gini_impurity_list)

    # broadcast best_split_feature
    for client in client_set:
        broadCastTreeNodeBasedOnBestSplit(client,
                                          currently_best_split_feature.feature,
                                          currently_best_split_feature.split_value,
                                          tree_height)

    # calculate aggregated label
    bestAggregatedValueList = []
    for client in client_set:
        bestAggregatedValueList.append(
            getAggregatedValueFromClient(currently_best_split_feature.feature,
                                         client,
                                         currently_best_split_feature.split_value,
                                         dataset))

    BCL, BCR = get_global_label_count(bestAggregatedValueList)

    node = TreeNode(feature=currently_best_split_feature.feature,
                    split_value=currently_best_split_feature.split_value,
                    tree_height=tree_height)

    # for key of data we can use f'{tree_height}_left' and f'{tree_height}_right'
    new_tree_height = tree_height + 1
    node.left = buildTree(feature_list, BCL, new_tree_height, f'{new_tree_height}_left')
    node.right = buildTree(feature_list, BCR, new_tree_height, f'{new_tree_height}_right')
    return node


def classify(root, sample):
    # Base case: if the root is a leaf node, return the classification
    if root.leaf_value is not None:
        return root.leaf_value

    sample_feature_value = sample[root.feature]
    # Recursively classify the sample based on the value of the split feature
    if sample_feature_value <= root.split_value:
        return classify(root.left, sample)
    else:
        return classify(root.right, sample)


def classifyBagging(randomForest, sample):
    label_count = {'Y': 0, 'N': 0}
    for tree in randomForest:
        classification = classify(tree, sample)
        label_count[classification] += 1

    bagging_classification = 'Y' if label_count['Y'] >= label_count['N'] else 'N'
    return bagging_classification


def convert_string_columns_to_numeric():
    df = pd.read_csv('/Users/mohimenul.admin/PycharmProjects/fet/master/test.csv')

    # Select all columns with string values
    string_columns = df.select_dtypes(include='object')
    string_columns = string_columns.drop(columns=['Loan_Status', 'Loan_ID'], axis=1)

    # Create a label encoder for each string column
    label_encoders = {column: preprocessing.LabelEncoder() for column in string_columns}

    # Encode the string values in each column
    df[string_columns.columns] = string_columns.apply(lambda x: label_encoders[x.name].fit_transform(x))

    # Return the modified dataframe
    return df


def get_accuracy(correct, wrong):
    # Calculate the total number of predictions
    total = correct + wrong
    # Calculate the accuracy as a percentage
    accuracy = correct / total * 100
    # Return the accuracy
    return accuracy


def test(randomForest):
    df = convert_string_columns_to_numeric()
    correct = 0
    wrong = 0
    for index, row in df.iterrows():
        # Print the index and row data
        # print(index, row)
        y = row['Loan_Status']
        prediction = classifyBagging(randomForest, row)
        loan_id = row['Loan_ID']
        if y == prediction:
            print(f'correct {loan_id}')
            correct += 1
        else:
            print(f'wrong {loan_id}')
            wrong += 1

    print(f'Correct = {correct}, wrong= {wrong}')
    return get_accuracy(correct, wrong)


def run():
    feature_list = ['Education', 'Self_Employed', 'ApplicantIncome', 'LoanAmount', 'Credit_History', 'Property_Area']
    aggregated_label = [1, 1]
    tree_height = 0
    dataset = 'full'

    for i in range(10):
        root = buildTree(feature_list, aggregated_label, tree_height, dataset)
        forest.append(root)

    for i in range(10):
        print(f'Tree no {i} of the random forest ...')
        print_tree(forest[i], 'root')
        print('\n')

    print(f'The Accuracy of FET is : {test(forest)}')


if __name__ == '__main__':
    logging.basicConfig()
    run()
