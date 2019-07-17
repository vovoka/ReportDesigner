import json
import copy

from aiohttp import web


def parse_file(file: str) -> dict:
    lines = file.splitlines()
    data = {}
    for line in lines:
        name, salary = line.split(',')
        if salary.isdigit():
            data[name] = int(salary)
    return data


def _create_project() -> dict:
    """ Create empty project with defaut names """
    return {'id': '0', 
            'name': 'NewProject', 
            'amount': '0', 
            'ownerBuh': '@vasya', 
            'employees': []}


def _populate_project(project: dict, employees: list) -> dict:
    """ Add employees to the project """

    for employee in employees:
        project['employees'].append({"name":employee, 
            "value": 'XXX'})
    return project


def _get_empoloyees(db_group, key_name = 'name') -> list:
    """ Returns list of employees from received report """
    try:
        empoloyees_by_key = ([employee["name"] 
            for project in db_group["data"]["projects"] 
            for employee in project["employees"]])
        return empoloyees_by_key
    except: AttributeError


def create_new_group(db_group: dict, new_group_employees: dict) -> dict:
    #? rename input parameter 'db_group' to 'prev_group_employees' 
    #? rename output var to 'modified_group_employees'
    """ Returns new group devived from lasttwo. 
    
    Args:
        db_group - employees of last modified report
        new_group_employees - employees of last modified report
    Calls:
        _create_project_with_new_employees()
        _populate_project()

    Returned new_group is based on db_group which is already exist in 
    the DB and has 'freshest' data amoung others.
    Next rules applied: 
    For each "employee" by their name:
     - if the name IS in BOTH received datasets:
        update the employee details (salary, project, position, etc.)
        with data from new_group_employees
     - if the name IS in new_group_employees only (new employee):
        add the new user to output dataset
     - if the name IS in prev list only (quited employee):
     delete them from output dataset
     
    """

    # Create sets        
    prev_group_emp = _get_empoloyees(db_group)
    new_group_emp = list(new_group_employees.keys())
    employees_new = set(new_group_emp) - set(prev_group_emp)
    employees_update = set(prev_group_emp).intersection(set(new_group_emp))
    employees_quited = set(prev_group_emp) - set(new_group_emp)

    # Modify db_data
    for project in db_group["data"]["projects"]:
        for employee in project["employees"]:
            # Update employees
            if employee["name"] in employees_update:
                employee["value"] = new_group_employees[employee["name"]]
                employees_update.remove(employee["name"])

        # Delete quited employees
        res = ([employee 
            for employee in project["employees"] 
            if not (employee["name"] in employees_quited)]) 
        project["employees"] = res

    # New project for new employees
    new_project = _create_project()
    new_project = _populate_project(new_project, employees_new)
    db_group["data"]["projects"].append(new_project)

    db_group['data'].update(new_group_employees)
    return db_group


def deserialize_json(data)->list:
    new_group = []
    for entry in (dict(i) for i in data):
        new_group.append({
                    'id': entry['id'],
                    'title': entry['title'],
                    'date_created': entry['date_created'].timestamp(),
                    'data': json.loads(entry['data'])
        })
    return new_group


def redirect(router, route_name):
    location = router[route_name].url_for()
    return web.HTTPFound(location)
