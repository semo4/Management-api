from fastapi import FastAPI

from src.controllers.authentication import auth_router
from src.controllers.bills import bills_router
from src.controllers.contractors import contractors_router
from src.controllers.covenants import covenants_cash_router, covenants_devices_router
from src.controllers.incomes import incomes_router
from src.controllers.operations import operations_router
from src.controllers.outcomes import outcomes_router
from src.controllers.outcomes_categories import categories_router
from src.controllers.partners import partners_router
from src.controllers.projects import projects_router
from src.controllers.salaries import salaries_router
from src.controllers.sections import section_router
from src.controllers.users import users_router
from src.controllers.withdraw import withdraw_router
from src.controllers.withdraw_contractors import withdraw_contractors_router
from src.controllers.workers import workers_router
from src.controllers.workplaces import workplace_router

routers = [
    section_router,
    workplace_router,
    categories_router,
    workers_router,
    projects_router,
    partners_router,
    covenants_cash_router,
    covenants_devices_router,
    bills_router,
    contractors_router,
    incomes_router,
    outcomes_router,
    operations_router,
    salaries_router,
    withdraw_contractors_router,
    withdraw_router,
    users_router,
    auth_router,
]


def setup_routers(app: FastAPI):
    for router in routers:
        app.include_router(router)
