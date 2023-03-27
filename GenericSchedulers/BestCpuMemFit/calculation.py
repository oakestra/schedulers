from abstractor_requsts import get_available_resources


def calculate(job):
    # check here if job has any user preferences, e.g. on a specific node, a specific cpu architecture,
    direct_mapping = job.get('direct_mapping', [])
    if len(direct_mapping) > 0:
        return deploy_on_best_among_desired_resources(job, direct_mapping)
    else:
        return greedy_load_balanced_algorithm(job=job)


def deploy_on_best_among_desired_resources(job, direct_mapping_list):
    active_resources = get_available_resources(job.get('job_id'))
    selected_resources = []
    for resource in active_resources:
        if resource.get('name') in direct_mapping_list:
            selected_resources.append(resource)
    return greedy_load_balanced_algorithm(job, resources_candidates=selected_resources)


def greedy_load_balanced_algorithm(job, resources_candidates=None):
    """return a sorted list of the candidate resources sorted accordingly to availablememory+availablecpu"""
    if resources_candidates is None:
        resources_candidates = get_available_resources(job.get('job_id'))

    qualified_resources = []

    qualified_resources = filter(lambda res: does_respects_requirements(res, job), resources_candidates)
    return {
        "results": list(
            map(lambda x: x.get('id'), sorted(qualified_resources, key=lambda res: resource_score(res), reverse=True))
        )
    }


def does_respects_requirements(resource, job):
    memory = job.get("requirements", {}).get('memory', 0)
    vcpu = job.get("requirements", {}).get('vcpu', 0)
    virtualization = job.get("requirements", {}).get('virtualization', '')

    if resource.get('available_cpu', 0) >= vcpu and \
            resource.get('available_memory', 0) >= memory and \
            virtualization in resource.get('virtualization', []):
        return True
    return False


def resource_score(resource):
    memory = resource.get('available_cpu', 0)
    vcpu = resource.get('available_memory', 0)
    return memory + vcpu
