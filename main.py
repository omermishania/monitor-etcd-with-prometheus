# imports
import requests
import json
import urllib3

# disable insecure request warning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# dictionary contains Prometheus queries and their valid maximum value
query_dict = {
  'histogram_quantile(0.99, rate(etcd_disk_backend_commit_duration_seconds_bucket[5m]))*1000' : 25
}

#vars
url = f'https://prometheus-k8s-openshift-monitoring.apps.ocp49-test.cloudlet-dev.com/api/v1/query?query=' # prometheus url
head = {"Authorization": "Bearer sha256~wouvtIMogxp1asaZV63SJ3J6BeN6zLnTRHlISG4LBgk"} # request headers


# returns the needed query metrics from Prometheus
def return_query_metrics(url, head, query):
    response = requests.get(url+query, headers=head, verify=False).text # get the response from prometehus query
    formated_response = json.loads(response)
    metrics = formated_response['data']['result'] # get only the needed metrics from the response
    return metrics


# returns a list contains the metrics values
def return_query_value(metrics):
    metrics_list = []
    for metric in metrics:
        metrics_list.append(metric['value'][1])
    return metrics_list


def main():
    final_result = 'success' # assuming the test is succesfull. if not, the variable value will be changed

    for query,valid_query_result in query_dict.items():
        response = return_query_metrics(url, head, query)
        query_result_list = return_query_value(response)

        for query_result in query_result_list: # runs on every query in the query dictionary
            if float(query_result) > valid_query_result: # if the query value doesn't meet the valid quary value by RedHat
                final_result = f'Error: Query: "{query}" result is: {query_result} and does not meet the condition: "<={valid_query_result}"'
        print(final_result) # prints the test's result


if __name__ == "__main__":
    main()
