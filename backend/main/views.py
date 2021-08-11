# Forma AI take-home test by Ian Carreon, iancrrn@gmail.com, 26 May 2020

from django.http import JsonResponse
from typing import List, Union
from django.db.models import Sum, Q
from .models import EmployeeRelation, SalesLines
from datetime import datetime
from backend.helpers import date_range_intersect

from django.contrib.auth.models import User
from decimal import Decimal, ROUND_UP
from django.core.exceptions import ObjectDoesNotExist

def get_revenue_by_sales_rep(request, user_id):

    try:
        user = User.objects.get(pk=user_id)
    except ObjectDoesNotExist:
        return JsonResponse({ "Error": f"User with user_id {user_id} does not exist"})
    except ValueError:
        return JsonResponse({ "Error": f"Field 'id' expected a number but got '{user_id}'."})

    # Let's get the reverse relation from the User model back to the EmployeeRelation model
    employee = user.hierarchy_user.all()
    reporting_to = user.hierarchy_manager.all()

    # Decide the type of user: sales rep, manager or director
    if employee:
        if reporting_to:
            # Manager
            return JsonResponse({ "revenue": _get_revenue_by_manager(user_id)})

        # Sales Rep
        return JsonResponse({ "revenue": _get_revenue_by_sales_rep(user_id) })
    else:
        # Director (since there is no EmployeeRelation entry for this user)
        return JsonResponse({ "revenue": _get_revenue_by_director(user_id)})

#------------------
# Helper functions
#------------------
def _get_revenue_by_sales_rep(user_id):

    user = User.objects.get(pk=user_id)

    # Could possibly add to the filter if given a start and end date
    # E.g. reporting_day__range=(start_date, end_date)
    query_result = SalesLines.objects.filter(rep_id=user_id).aggregate(sum_=Sum('revenue'))

    revenue_dict = {
        "name": ' '.join([user.first_name, user.last_name]), 
        "revenue": 0
    }

    # Check if there are entries for this user
    if query_result['sum_']:
        revenue_dict.update({
            "revenue": Decimal(query_result['sum_']).quantize(Decimal('.01'), rounding=ROUND_UP)
        })

    return [revenue_dict]


def _get_revenue_by_manager(user_id):

    user = User.objects.get(pk=user_id)
    reporting_to = user.hierarchy_manager.all()

    # Get revenue for each sales rep under this manager
    revenue = []
    for sales_rep in reporting_to:
        revenue.extend(_get_revenue_by_sales_rep(sales_rep.employee.id))

    return revenue

def _get_revenue_by_director(user_id):

    user = User.objects.get(pk=user_id)
    reporting_to = user.hierarchy_manager.all()

    # Get revenue for each manager under this director
    revenue = []
    for manager in reporting_to:		
        revenue.extend(_get_revenue_by_manager(manager.employee.id))

    return revenue
