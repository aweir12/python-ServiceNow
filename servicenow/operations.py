def _get_data(input_params):
    """
    Makes a single call to the ServiceNow API and returns the json response

    Parameters
    ----------
    input_params: tuple
        A tuple where [0] is equal to the API username, [1] is equal to the
        API user password, and [2] is equal to the query (or URL)
    """
    import requests
    api_user = input_params[0]
    api_password = input_params[1]
    query_string = input_params[2]
    result = requests.get(query_string, auth=(api_user, api_password)).json()
    return result


def _generate_batches(sn_instance, table_name, limit, reference_link):
    """
    Generates a list of URL's to call to retrieve ServiceNow data

    Parameters
    ----------
    sn_instance: servicenow.servicenow.ServiceNowInstance
        ServiceNow instance to retrieve data from
    table_name: str
        Table name to retrieve data from
    limit: int or None (Default: 500)
        Number of records to retrieve for each web service call
    reference_link: bool or None (Default: False)
        Indicates whether or not to include the reference link in
        the output
    """
    output = []
    counter = 0
    record_count = _get_table_count(sn_instance, table_name)
    url = ("https://{}.service-now.com/api/now/table/{}"
           "?sysparm_exclude_reference_link={}&sysparm_offset={}"
           "&sysparm_limit={}")

    while counter < record_count:
        query_string = url.format(sn_instance.subdomain, table_name,
                                  str(not reference_link), counter, limit)
        output.append(query_string)
        counter = counter + limit
    return output


def _get_table_count(sn_instance, table_name):
    """
    Retrieves the record count for a given table

    Parameters
    ----------
    sn_instance: servicenow.servicenow.ServiceNowInstance
        ServiceNow instance to retrieve data from
    table_name: str
        Table name to retrieve data from
    """
    url = ("https://{}.service-now.com/api/now/v1/stats/{}"
           "?sysparm_count=true")
    query_string = url.format(sn_instance.subdomain, table_name)
    record_count = int(_get_data((sn_instance.api_user,
                       sn_instance.api_password, query_string))
                       ['result']['stats']['count'])
    return record_count


def _parallel_table_read(sn_instance, batches):
    import multiprocessing as mp
    import pandas as pd
    pool = mp.Pool(mp.cpu_count())
    results = pool.map(_get_data, ((sn_instance.api_user,
                                    sn_instance.api_password, i)
                                   for i in batches))
    results = [pd.DataFrame.from_dict(i['result'], orient='columns')
               .set_index('sys_id') for i in results]
    results = pd.concat(results)
    return results


def _serial_table_read(sn_instance, batches):
    import pandas as pd
    results = pd.DataFrame()
    for i in batches:
        output = _get_data((sn_instance.api_user,
                            sn_instance.api_password, i))['result']
        df_temp = pd.DataFrame.from_records(output, index='sys_id')
        results = results.append(df_temp)
        del output, df_temp
    return results


def read_table_full(sn_instance, table_name, limit=500, parallel=False,
                    reference_link=False):
    """
    Reads a full table from ServiceNow via the API

    Parameters
    ----------
    sn_instance: servicenow.servicenow.ServiceNowInstance
        ServiceNow instance to retrieve data from
    table_name: str
        Table name to retrieve data from
    limit: int or None (Default: 500)
        Number of records to retrieve for each web service call
    parallel: bool or None (Default: False)
        Retrieve data using parallel processing
    reference_link: bool or None (Default: False)
        Indicates whether or not to include the reference link in
        the output
    """
    batches = _generate_batches(sn_instance, table_name, limit, reference_link)
    if parallel:
        output = _parallel_table_read(sn_instance, batches)
    else:
        output = _serial_table_read(sn_instance, batches)
    return output
