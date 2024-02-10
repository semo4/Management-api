
from src.database.connection import execute_one, execute_all
from src.models.workers import workers
from src.models.operations import operations
from src.models.salaries import salaries
from src.models.bills import bills
from src.models.outcomes import outcomes
from src.models.incomes import incomes


def calculation_contractors(data):
    if 'amount' in data.keys() and 'paid_amount' in data.keys():
        data['rest_amount'] = float(
            data['amount']) - float(data['paid_amount'])
        data['paid_amount'] += data['paid_amount']
    elif 'amount' in data.keys():
        data['rest_amount'] = float(data['amount'])
    return data


def calculation_operations(data):
    if 'worker_id' in data.keys() and 'working_hours' in data.keys():
        res = workers.select().where(workers.c.id == data['worker_id'])
        result = execute_one(res)
        if not result:
            data['payment_amount'] = 0
            return data
        hourly_payment = result[3] / 8
        data['payment_amount'] = hourly_payment * data['working_hours']
    return data


def calculation_workers_operations(worker_id):
    res_operations = operations.select().where(operations.c.worker_id == worker_id)
    result_operations = execute_all(res_operations)
    if not result_operations:
        return 0, 0
    total_number_of_working_hours = 0
    total_payment_amount = 0
    for row in result_operations:
        total_number_of_working_hours += row[5] if row[5] is not None else 0
        total_payment_amount += row[6] if row[6] is not None else 0
    return total_number_of_working_hours, total_payment_amount


def calculation_workers_salaries(worker_id):
    res_salaries = salaries.select().where(salaries.c.worker_id == worker_id)
    result_salaries = execute_all(res_salaries)
    if not result_salaries:
        return 0
    total_payed_amount = 0
    for row in result_salaries:
        total_payed_amount += row[5] if row[5] is not None else 0

    return total_payed_amount


def calculate_project_bills(project_id):
    res_bills = bills.select().where(bills.c.project_id == project_id)
    result_bills = execute_all(res_bills)
    total_expenses = 0
    if not result_bills:
        return total_expenses
    for row in result_bills:
        total_expenses += row[5] if row[5] is not None else 0

    return total_expenses


def calculate_project_outcomes(project_id):
    res_outcomes = outcomes.select().where(outcomes.c.project_id == project_id)
    result_outcomes = execute_all(res_outcomes)
    total_expenses = 0
    if not result_outcomes:
        return total_expenses
    for row in result_outcomes:
        total_expenses += row[2] if row[2] is not None else 0

    return total_expenses


def calculate_project_incomes(project_id):
    res_incomes = incomes.select().where(incomes.c.project_id == project_id)
    result_incomes = execute_all(res_incomes)
    total_incomes = 0
    if not result_incomes:
        return total_incomes
    for row in result_incomes:
        total_incomes += row[7] if row[7] is not None else 0

    return total_incomes


def calculate_project_operations(project_id):
    res_operations = operations.select().where(
        operations.c.project_id == project_id)
    result_operations = execute_all(res_operations)
    total_expenses = 0
    if not result_operations:
        return total_expenses
    for row in result_operations:
        total_expenses += row[6] if row[6] is not None else 0

    return total_expenses


def calculate_project_payments(project_id):
    total_expenses = calculate_project_bills(project_id)
    total_expenses += calculate_project_outcomes(project_id)
    total_expenses += calculate_project_operations(project_id)
    total_incomes = calculate_project_incomes(project_id)

    return total_expenses, total_incomes
