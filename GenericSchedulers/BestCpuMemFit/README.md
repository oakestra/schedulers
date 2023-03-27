# BestCpuMemFit scheduler

This is a generic **scheduler implementation** compatible with oakestra which performs a best fit task placement based only on CPU and Memory. 

![scheduler implementation](figures/arch.png)

The BestCpuMemFit scheduler is designed to work both as a Cluster Scheduler and as a Root Scheduler. It only uses generic aggregated CPU and Memory information. 

#### Requirements:

* Redis task queue 
* Resource Abstractor 

#### Folder structure

* `calculation.py` -> Implementation of the scheduling algorithm
* `scheduler.py` -> instantiation of the celery worker 
* `test/calculation_benchmark_test.py` -> test and performance evaluation of the scheduling algorithm
* `abstractor_requests.py` -> requests to a generic resource abstractor to get the current resource status. 

## Run It 

#### Local  

1. Make sure redis is up and running 
2. Export the required environment variables 
```
export RESOURCE_ABSTRACTOR_URL=<resource abstractor url>
export RESOURCE_ABSTRACTOR_PORT=<resource abstractor port>
export REDIS_ADDR=redis://:<name>@<host>:<redisport>
```
3. Run it using celery
```
celery -A scheduler worker -l DEBUG
```

#### Docker 

This respository will soon automatically build the images for each one of the proposed schedulers. 
As of now you can edit and build your image using the provided dockerfile.

## Placement result

The placement result if a python dictionary with the following structure
```
{
    results: [string]   //list of resources' id
}
```

## Input Task Structure

```
{
"job_id": "string"
"requirements":
  {
    "memory": int64               //memory in MB 
    "vcpu": int64                 //vcpu cores requirement 
    "virtualization": [string]    //list of virtualization tech supported (e.g. "container")
  }
"direct_mapping": [string]    //list of the names of the only clusters or workers to be considered for the scheduling. It considers only cluster_name or the node's hostname.         
}
```

## Resource Abstractor API Call

This service performs the following request to the resource abstractor service:

`GET <url:port>/api/resources?job_id=<job_id>`

The resource abstractor must answer this service with the set of resources authorized for the provided job_id:

```
{
resources:
  [
    {
      'id': string                // resource id
      'name': string              // resource name
      'available_cpu': int64      //cpu cores available
      'available_memory': int64   //cpu cores available
      'virtualization': [string]  //list of the supported virtualization technologies
      ...
    },
    ...
  ]
}
```

N.b. make sure the resource abstractor is properly configured. E.g., If this scheduler is used at root level, the address of the root resource abstractor must be properly configured.