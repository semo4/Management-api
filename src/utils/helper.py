
from src.utils.calculation import calculation_workers_operations, calculation_workers_salaries, calculate_project_payments


def build_section_dict(row):
    data = dict()
    data['id'] = row[0]
    data['name'] = row[1]
    return data


def build_workers_dict(row):
    data = dict()
    data['id'] = row[0]
    data['name'] = row[1]
    data['profession'] = row[2]
    data['daily_amount'] = row[3]
    data['total_payed_amount'] = calculation_workers_salaries(row[0])
    data['total_number_of_working_hours'], data['total_payment_amount'] = calculation_workers_operations(
        row[0])
    data['rest_amount'] = data['total_payment_amount'] - \
        data['total_payed_amount']
    return data


def build_workers_post_dict(row):
    data = dict()
    data['id'] = row[0]
    data['name'] = row[1]
    data['profession'] = row[2]
    data['daily_amount'] = row[3]
    return data


def build_projects_dict(row):
    data = dict()
    data['id'] = row[0]
    data['name'] = row[1]
    data['place'] = row[2]
    data['description'] = row[3]
    data['start_date'] = row[4]
    data['end_date'] = row[5]
    data['project_evaluation'] = row[7]
    data['section_name'] = row[10]
    total_expenses, total_incomes = calculate_project_payments(row[0])
    data['project_revenue'] = data['project_evaluation'] - total_expenses
    data['project_depth'] = data['project_evaluation'] - total_incomes
    return data


def build_projects_post_dict(row):
    data = dict()
    data['id'] = row[0]
    data['name'] = row[1]
    data['section_id'] = row[2]
    data['place'] = row[3]
    data['description'] = row[4]
    data['start_date'] = row[5]
    data['end_date'] = row[6]
    data['project_evaluation'] = row[7]
    return data


def build_partners_dict(row):
    data = dict()
    data['id'] = row[0]
    data['name'] = row[1]
    data['amount'] = row[2]
    data['pre_amount'] = row[3]
    data['section_id'] = row[4]
    data['section_name'] = row[7]
    return data


def build_partners_post_dict(row):
    data = dict()
    data['id'] = row[0]
    data['name'] = row[1]
    data['section_id'] = row[2]
    data['amount'] = row[3]
    data['pre_amount'] = row[4]
    return data


def build_response_dict(row):
    data = dict()
    data['id'] = row[0]
    data['title'] = row[1]
    return data


def build_covenants_cash_dict(row):
    data = dict()
    data['id'] = row[0]
    data['name'] = row[1]
    data['price'] = row[3]
    data['date'] = row[4]
    data['partner_name'] = row[7]
    return data


def build_covenants_cash_post_dict(row):
    data = dict()
    data['id'] = row[0]
    data['partner_id'] = row[1]
    data['name'] = row[2]
    data['price'] = row[3]
    data['date'] = row[4]
    return data


def build_covenants_devices_dict(row):
    data = dict()
    data['id'] = row[0]
    data['title'] = row[1]
    data['desc'] = row[3]
    data['date'] = row[4]
    data['worker_name'] = row[7]
    return data


def build_covenants_devices_post_dict(row):
    data = dict()
    data['id'] = row[0]
    data['worker_id'] = row[1]
    data['title'] = row[2]
    data['desc'] = row[3]
    data['date'] = row[4]
    return data


def build_bills_dict(row):
    data = dict()
    data['id'] = row[0]
    data['store_name'] = row[1]
    data['buyer_name'] = row[2]
    data['item'] = row[3]
    data['amount'] = row[4]
    data['bill_number'] = row[5]
    data['bill_picture'] = row[6]
    data['project_name'] = row[10]
    return data


def build_bills_post_dict(row):
    data = dict()
    data['id'] = row[0]
    data['project_id'] = row[1]
    data['store_name'] = row[2]
    data['buyer_name'] = row[3]
    data['item'] = row[4]
    data['amount'] = row[5]
    data['bill_number'] = row[6]
    data['bill_picture'] = row[7]
    return data


def build_contractors_dict(row):
    data = dict()
    data['id'] = row[0]
    data['name'] = row[1]
    data['project_id'] = row[2]
    data['section_id'] = row[3]
    data['amount'] = row[4]
    data['paid_amount'] = row[5]
    data['rest_amount'] = row[6]
    data['section_name'] = row[9]
    data['project_name'] = row[10]
    return data


def build_contractors_dict_post(row):
    data = dict()
    data['id'] = row[0]
    data['name'] = row[1]
    data['project_id'] = row[2]
    data['section_id'] = row[3]
    data['amount'] = row[4]
    data['paid_amount'] = row[5]
    data['rest_amount'] = row[6]
    return data


def build_incomes_dict(row):
    data = dict()
    data['id'] = row[0]
    data['project_id'] = row[1]
    data['section_id'] = row[2]
    data['receiving_person'] = row[3]
    data['gave_person'] = row[4]
    data['check_number'] = row[5]
    data['payment_number'] = row[6]
    data['amount'] = row[7]
    data['way_of_receiving'] = row[8]
    data['description'] = row[9]
    data['receiving_date'] = row[10]
    data['section_name'] = row[13]
    data['project_name'] = row[14]
    return data


def build_incomes_dict_post(row):
    data = dict()
    data['id'] = row[0]
    data['project_id'] = row[1]
    data['section_id'] = row[2]
    data['receiving_person'] = row[3]
    data['gave_person'] = row[4]
    data['check_number'] = row[5]
    data['payment_number'] = row[6]
    data['amount'] = row[7]
    data['way_of_receiving'] = row[8]
    data['description'] = row[9]
    data['receiving_date'] = row[10]
    if len(row) > 13:
        data['section_name'] = row[13]
        data['project_name'] = row[14]
    return data


def build_outcomes_dict(row):
    data = dict()
    data['id'] = row[0]
    data['buyer_name'] = row[1]
    data['amount_payed'] = row[2]
    data['project_id'] = row[3]
    data['category_id'] = row[4]
    data['reason'] = row[5]
    data['date'] = row[6]
    data['project_name'] = row[9]
    data['category_name'] = row[10]
    return data


def build_outcomes_dict_post(row):
    data = dict()
    data['id'] = row[0]
    data['buyer_name'] = row[1]
    data['amount_payed'] = row[2]
    data['project_id'] = row[3]
    data['category_id'] = row[4]
    data['reason'] = row[5]
    data['date'] = row[6]
    if len(row) > 9:
        data['project_name'] = row[9]
        data['category_name'] = row[10]
    return data


def build_operations_dict(row):
    data = dict()
    data['id'] = row[0]
    data['section_id'] = row[1]
    data['project_id'] = row[2]
    data['worker_id'] = row[3]
    data['work_place_id'] = row[4]
    data['working_hours'] = row[5]
    data['payment_amount'] = row[6]
    data['description'] = row[7]
    data['operation_add_date'] = row[8]
    data['section_name'] = row[11]
    data['project_name'] = row[12]
    data['worker_name'] = row[13]
    data['workplace_name'] = row[14]
    return data


def build_operations_dict_post(row):
    data = dict()
    data['id'] = row[0]
    data['section_id'] = row[1]
    data['project_id'] = row[2]
    data['worker_id'] = row[3]
    data['work_place_id'] = row[4]
    data['working_hours'] = row[5]
    data['payment_amount'] = row[6]
    data['description'] = row[7]
    data['operation_add_date'] = row[8]
    if len(row) > 11:
        data['section_name'] = row[11]
        data['project_name'] = row[12]
        data['worker_name'] = row[13]
        data['workplace_name'] = row[14]
    return data


def build_salaries_dict(row):
    data = dict()
    data['id'] = row[0]
    data['project_id'] = row[1]
    data['worker_id'] = row[2]
    data['section_id'] = row[3]
    data['salary_type'] = row[4]
    data['amount'] = row[5]
    data['date'] = row[6]
    data['project_name'] = row[9]
    data['worker_name'] = row[10]
    data['section_name'] = row[11]
    return data


def build_salaries_dict_post(row):
    data = dict()
    data['id'] = row[0]
    data['project_id'] = row[1]
    data['worker_id'] = row[2]
    data['section_id'] = row[3]
    data['salary_type'] = row[4]
    data['amount'] = row[5]
    data['date'] = row[6]
    if len(row) > 9:
        data['project_name'] = row[9]
        data['worker_name'] = row[10]
        data['section_name'] = row[11]

    return data


def build_withdraw_contractors_dict(row):
    data = dict()
    data['id'] = row[0]
    data['section_id'] = row[1]
    data['project_id'] = row[2]
    data['contractor_id'] = row[3]
    data['amount'] = row[4]
    data['date'] = row[5]
    data['section_name'] = row[8]
    data['project_name'] = row[9]
    data['contractor_name'] = row[10]
    return data


def build_withdraw_contractors_dict_post(row):
    data = dict()
    data['id'] = row[0]
    data['section_id'] = row[1]
    data['project_id'] = row[2]
    data['contractor_id'] = row[3]
    data['amount'] = row[4]
    data['date'] = row[5]
    if len(row) > 8:
        data['section_name'] = row[8]
        data['project_name'] = row[9]
        data['contractor_name'] = row[10]

    return data


def build_withdraw_dict(row):
    data = dict()
    data['id'] = row[0]
    data['section_id'] = row[1]
    data['project_id'] = row[2]
    data['partner_id'] = row[3]
    data['amount'] = row[4]
    data['date'] = row[5]
    data['section_name'] = row[8]
    data['project_name'] = row[9]
    data['partner_name'] = row[10]
    return data


def build_withdraw_dict_post(row):
    data = dict()
    data['id'] = row[0]
    data['section_id'] = row[1]
    data['project_id'] = row[2]
    data['partner_id'] = row[3]
    data['amount'] = row[4]
    data['date'] = row[5]
    if len(row) > 8:
        data['section_name'] = row[8]
        data['project_name'] = row[9]
        data['partner_name'] = row[10]

    return data


def build_users_dict(row):
    data = dict()
    data['id'] = row[0]
    data['first_name'] = row[1]
    data['Last_name'] = row[2]
    data['username'] = row[3]
    data['email'] = row[4]
    data['password'] = row[5]
    data['is_super_admin'] = row[6]
    data['is_admin'] = row[7]
    data['is_active'] = row[8]
    data['is_stuff'] = row[9]
    return data
