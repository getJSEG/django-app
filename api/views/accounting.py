from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.db import transaction
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from ..authenticate import CustomAuthentication

from datetime import datetime, timedelta, date, time
from django.db.models.functions import TruncDate
from django.utils import timezone
from django.db.models import Q, Sum, F
from dateutil import rrule
import calendar
from django.db.models import Prefetch

from django.db.models import Sum

#MODELS
from ..models import  PurchaseOrder, Expense

from ..models import  Order

from ..repeated_responses.repeated_responses import not_assiged_location, denied_permission, emptyField

from ..serializers import accounting_serializer


# this gets all of the income by month
# from Jan - Dec ( month name in spanish)
class IncomeView(APIView):

    authentication_classes = [CustomAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        # Get the user location ID
        try:
           location_id = request.user.location.id
        except:
            return not_assiged_location()
        
        month = ["Ene", "Feb", "Mar", "Abri", "May", "Jun", "Jul", "Ago", " Sep", "Oct", "Nov", "Dic"]
      
        response_data = []
        total_amount = 0
        datetime_year= datetime.today().strftime("%Y")
        datetime_month = int(datetime.today().strftime("%m"))

        # This options get the sales for each month - today date
        for datetime_month in range(0, 12):
            transInstance = Order.objects.filter(location_id = location_id, dateCreated__month=datetime_month)
            month_name = month[datetime_month]
            if transInstance.exists():
                total_amount = { "mes": month_name , 
                                  "ventas" : transInstance.aggregate(total=Sum("totalAmount"))["total"]}
            else:
                total_amount = { "mes" : month_name, "ventas" : 0 }

            response_data.append(total_amount)

        return Response(response_data, status=status.HTTP_200_OK)


# Expenses
class ExpensesView(APIView):
    
    authentication_classes = [CustomAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]

    expesesSerializer = accounting_serializer.ExpensesSerializer

    # Creating expeses here
    def post(self, request, format=None): 

        try:
           locationID = request.user.location.id
           username = request.user.username
        except:
            return not_assiged_location()
        
        data = request.data.copy()

        data["location"] = locationID
        data["created_by"] =  username
        
        with transaction.atomic():
            serializer = self.expesesSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            else:
                raise Exception(serializer.errors)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Getting All expenses
    def get(self, request, format=None): 
        # Get the user location ID
        try:
           location_id = request.user.location.id
        except:
            return not_assiged_location()
        
        month = ["Ene", "Feb", "Mar", "Abri", "May", "Jun", "Jul", "Ago", " Sep", "Oct", "Nov", "Dic"]
      
        response_data = []
        total_amount = 0
        datetime_year= datetime.today().strftime("%Y")
        datetime_month = int(datetime.today().strftime("%m"))

        # This options get the sales for each month - today date
        for datetime_month in range(0, 12):
            transInstance = Expense.objects.filter(location_id = location_id, creationDate__month=datetime_month)
            month_name = month[datetime_month]
            if transInstance.exists():
                total_amount = { "mes": month_name , 
                                  "gastos" : transInstance.aggregate(total=Sum("totalAmount"))["total"]}
            else:
                total_amount = { "mes" : month_name, "gastos" : 0 }

            response_data.append(total_amount)

        return Response(response_data, status=status.HTTP_200_OK)


# retriving the sales of the store by category
# can be select by day, month 6 month or year
class salesbyCategory(APIView):

    authentication_classes = [CustomAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request, format=None):
        # check permission
        try:
           location_id = request.user.location.id
           username = request.user.username
        except:
            return not_assiged_location()
        
        option = int(request.GET.get('option', 1))

        # get the todays date
        datenow = datetime.now()
        revenue = {}

        # This get the sales of the todays date
        if option == 1:
            # Filters the revenue of todays date
            orders = Order.objects.filter(location_id = location_id, dateCreated__date=datetime.now().date()) 
            if orders.exists():
                # sum all revenues that are shipping
                shipping_revenue = orders.filter(paymentExecution="SHIPPING").aggregate(total=Sum("totalAmount"))["total"] 
                shipping_revenue = 0 if shipping_revenue is None else shipping_revenue
                # sum all revenues that are total sales
                instore_revenue = orders.filter(paymentExecution="POS").aggregate(total=Sum("totalAmount"))["total"] or 0
                shipping_revenue = 0 if instore_revenue is None else instore_revenue

                total_store_revenue = shipping_revenue + instore_revenue
                revenue = {
                    "shippingRevenue": shipping_revenue,
                    "storeRevenue": instore_revenue,
                    "totalStoreRevenue": total_store_revenue
                }
            else:
                # return 0
                revenue = { "shippingRevenue": 0, "storeRevenue": 0, "totalStoreRevenue": 0 }
        elif option == 2:
            # this obtion return the sales of the month
            orders = Order.objects.filter(location_id = location_id, dateCreated__month=datetime.now().month) 
            if orders.exists():
                # sum all revenues that are shipping
                shipping_revenue = orders.filter(paymentExecution="SHIPPING").aggregate(total=Sum("totalAmount"))["total"]
                # sum all revenues that are total sales
                instore_revenue = orders.filter(paymentExecution="POS").aggregate(total=Sum("totalAmount"))["total"]
                total_store_revenue = shipping_revenue + instore_revenue
                revenue = {
                    "shippingRevenue": shipping_revenue,
                    "storeRevenue": instore_revenue,
                    "totalStoreRevenue": total_store_revenue
                }
            else:
                # return 0
                revenue = { "shippingRevenue": 0, "storeRevenue": 0, "totalStoreRevenue": 0 }
        elif option == 4:
            orders = Order.objects.filter(location_id = location_id, dateCreated__year=datetime.now().year) 

            if orders.exists():
                # sum all revenues that are shipping
                shipping_revenue = orders.filter(paymentExecution="SHIPPING").aggregate(total=Sum("totalAmount"))["total"]
    
                # sum all revenues that are total sales
                instore_revenue = orders.filter(paymentExecution="POS").aggregate(total=Sum("totalAmount"))["total"]
                total_store_revenue = shipping_revenue + instore_revenue

                revenue = {
                    "shippingRevenue": shipping_revenue,
                    "storeRevenue": instore_revenue,
                    "totalStoreRevenue": total_store_revenue
                }
            else:
                # return 0
                revenue = { "shippingRevenue": 0, "storeRevenue": 0, "totalStoreRevenue": 0 }
        # this get the revenu of the current year
            # if transInstance.exists():
            #     total_amount = { "label": "Today",
            #                         "value" : transInstance.aggregate(total = Sum("grandTotal"))["total"] }
            # else:
            #     total_amount = { "label": "Today", 
            #                         "value" : 0 }
            
            # response_data.append( total_amount )


        return Response(revenue, status=status.HTTP_200_OK)
        









# Creating and Retriving Expenses
class PurchaseOrderView(APIView):

    authentication_classes = [CustomAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]

    purchaseOrderSerializer = accounting_serializer.purchaseOrderSerializer
    expensesSerialzier  = accounting_serializer.ExpensesSerializer
    # Creating Method
    def post(self, request, format=None):
        # checking permission
        if not request.user.has_perm('api.add_purchaseorder'):
            return denied_permission()
        
        try:
            locationID = request.user.location.id
            username = request.user.username
        except:
            return not_assiged_location()
        
        data = request.data.copy()

        data['location'] = locationID
        data['createdBy'] = username

        with transaction.atomic():
            serializer = self.purchaseOrderSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            else:
                raise Exception(serializer.errors)
            
        # Only if the status is paid we add it to the expeses
        if serializer.data.get("status", None) == 'PAID': 
            expeseData = {
                "totalAmount": serializer.data.get("totalAmount", None),
                "created_by": username, 
                "location": locationID,
                "expenses": [{
                    "description": serializer.data.get("id", None),
                    "amount": serializer.data.get("totalAmount", None),
                    "merchant": serializer.data.get("merchant", None),
                    "approvalDate": timezone.now().date(),
                    "expense_date": timezone.now(),
                    "expense_type": "Purchase Order"
                }]
            } 
            with transaction.atomic():
                expenseserializer = self.expensesSerialzier(data=expeseData)
                if expenseserializer.is_valid(raise_exception=True):
                    expenseserializer.save()
                else:
                    raise Exception(expenseserializer.errors)
            

        return Response({"data": "Articulo Creado"} , status=status.HTTP_200_OK)
    # Updating the purchaseOrder
    def patch(self, request, format=None):
        # TODO: set permission here

        # This gets the id from the query
        pk = request.GET.get('id')
        try:
            # search purchase order
            instance = PurchaseOrder.objects.get(id=pk)
            print(instance)
        except:
            return Response({"data": "articulo no existe"} , status=status.HTTP_200_OK)

        data = request.data.copy()

        with transaction.atomic():
            serializer = self.purchaseOrderSerializer(instance, data=data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            else:
                raise Exception(serializer.errors)
            
        # Only if the status is paid we add it to the expeses
        if serializer.data.get("status", None) == 'PAID': 
            expeseData = {
                "totalAmount": serializer.data.get("totalAmount", None),
                "created_by": serializer.data.get("createdBy", None), 
                "location": serializer.data.get("location", None),
                "expenses": [{
                    "description": serializer.data.get("id", None),
                    "amount": serializer.data.get("totalAmount", None),
                    "merchant": serializer.data.get("merchant", None),
                    "approvalDate": timezone.now().date(),
                    "expense_date": timezone.now(),
                    "expense_type": "Purchase Order"
                }]
            } 
            with transaction.atomic():
                expenseserializer = self.expensesSerialzier(data=expeseData)
                if expenseserializer.is_valid(raise_exception=True):
                    expenseserializer.save()
                else:
                    raise Exception(expenseserializer.errors)
        # get file 
        return Response({"data": "Articulo Actualisado"} , status=status.HTTP_200_OK)

    # Getting Method 
    def get(self, request, format=None):
        user = request.user
        # Only serting user can view purchase order
        if not user.has_perm('api.view_purchaseorder'):
            return denied_permission()
        try:
            location = request.user.location.id
        except:
            return not_assiged_location()

        purchaseOrder = PurchaseOrder.objects.filter(locationId=location).prefetch_related("POLines")
        # Filter by date
        serializer = self.purchaseOrderSerializer(purchaseOrder, many=True)
        # Get the purchase order by user location 
        return Response(serializer.data , status=status.HTTP_200_OK)




# TODO:Running Reports Here
# All Details expenses and all of income by date range startDate - EndDate



















        # # Gets the income for the month (30 days)
        # today = date.today()
        # monthData = []

        # # Get the first day of the month
        # first_day_of_month = date(today.year, today.month, 1)
        # # Get last day fo the month
        # if today.month == 12:
        #     last_day_of_month = date(today.year, 12, 31)
        # else:
        #     last_day_of_month = date(today.year, today.month + 1, 1) - timedelta(days=1)

        # # loop trought all the days and sum up all of the sales for current days
        # current_day = first_day_of_month

        # while current_day <= last_day_of_month:
        #     daily_data = Expense.objects.filter(location = locationID).filter(creationDate__date=current_day)
        #     # print(current_day)
        #     monthData.append({ 
        #         "dia": current_day.strftime("%d/%m"),
        #         "gastos" : daily_data.aggregate(total = Sum("totalAmount"))['total'] or 0
        #     })

        #     current_day += timedelta(days=1)



# Calculate all of the Expenses acumulated



# Retrive Recent Transactions 
# of the week or day ???



# Get all Recipts
# Categorize them by the selections
# getting all trasactions for that day
# TODO: GET the sales Order and the get the transaction
# class Revenue(APIView):

#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]

#     serializer_class =  pos_serializer.TransactionReceiptSerializer

#     def  get(self, request, format=None):
#         if not request.user.has_perm('api.view_transactionreceipt'):
#             return denied_permission()
#         # get the quaters
#         # print(date(2024,5,11).month)
#         # date_instance = date(2024,9,11)
#         option = int(request.GET.get('option', 1))

#         try:
#             location =  request.user.location.id
#         except:
#             return not_assiged_location()

#         # datenow = datetime.now() 

#         # first_day = quarters.before(datenow)
#         # last_day = (quarters.after(datenow) - relativedelta.relativedelta(days=1))
    
#         response_data = []
#         total_amount = 0
#         datetime_year= datetime.today().strftime("%Y")
#         datetime_month = int(datetime.today().strftime("%m"))

#         try: 
#             if option == 1:
#                 # print this will print all of the revenue of today
#                 transInstance = TransactionReceipt.objects.filter(location_id = location, date_created__date=datetime.now().date()) 
#                 if transInstance.exists():
#                     total_amount = { "label": "Today",
#                                      "value" : transInstance.aggregate(total = Sum("grandTotal"))["total"] }
#                 else:
#                     total_amount = { "label": "Today", 
#                                      "value" : 0 }
                
#                 response_data.append( total_amount )

#             elif option == 2:
#                 # Return only the sales for the specific week Mon - Sun.
#                 date = datetime.now()
#                 start_week =  date - timedelta(date.weekday())
#                 end_week = start_week + timedelta(7)

#                 for i in rrule.rrule(rrule.DAILY, dtstart=start_week, until=end_week):
#                     year = i.strftime('%Y')
#                     month = i.strftime('%m')
#                     day = i.strftime('%d')

#                     transInstance = TransactionReceipt.objects.filter(location_id = location,  date_created__date= i.date() )

#                     name_of_day = calendar.day_name[calendar.weekday(int(year),int(month),int(day))]

#                     if transInstance.exists():
#                         total_amount = { "label": name_of_day,
#                                           "value": transInstance.aggregate(total=Sum("grandTotal"))["total"]}
#                     else:
#                         total_amount = { "label": name_of_day,
#                                          "value": 0 }
                        
#                     response_data.append(total_amount)

#             elif option == 3:
#                 # This options get the sales for each month - today date
#                 for datetime_month in range(1, datetime_month+1):
#                     transInstance = TransactionReceipt.objects.filter(location_id = location, date_created__month=datetime_month)
#                     month_name =  calendar.month_name[datetime_month]
#                     if transInstance.exists():
#                         total_amount = { "label": month_name , 
#                                          "value" :transInstance.aggregate(total=Sum("grandTotal"))["total"]}
#                     else:
#                         total_amount = { "label" : month_name,
#                                          "value" : 0 }

#                     response_data.append(total_amount)
#             elif option == 4:
#                 # datetime.now().year
#                 # this options only gets the quaterly or yearly sales
#                 # quarters = rrule.rrule(
#                 #     rrule.MONTHLY,
#                 #     bymonth=(1, 4, 7, 10),
#                 #     bysetpos=-1,
#                 #     dtstart = datetime(datetime.now().year, 1, 1),
#                 #     count=4
#                 #     )
                
#                 # for i in quarters:
#                 #     print(i.date())
#                 #     print(i)
#                 print("Porfavor Ecoje Otra Opcion")
#             else:
#                 raise Exception("Algo Salio Mal.")

#         except Exception as e:
#             return Response({'data':  str(e)}, status=status.HTTP_400_BAD_REQUEST) 

#         return Response(response_data, status=status.HTTP_200_OK)
    

















#Create items for expenses
# class ExpensesType(APIView):

#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]

#     expenseSerialzier = accounting_serializer.ExpenseSerializer
#     def post(self, request, format=None):
#         user = request.user
#         if not user.has_perm('api.add_expense'):
#             return denied_permission()
#         try:
#             location = location = request.user.location.id
#             username = request.user.username
#         except:
#             return not_assiged_location()

#         data = request.data.copy()
#         expenseType = data.pop("expenseType")

#         expenseType.update({'location_id': location})
#         data.update({'location_id': location, "created_by":username, "expenseType": expenseType })

#         try:
#             with transaction.atomic():
#                     expSerializer = self.expenseSerialzier(data=data)
#                     if expSerializer.is_valid():
#                         expSerializer.save()
#                     else:
#                         raise Exception(expSerializer.errors)
#         except Exception as e:
#             return Response({"data": str(e) }, status=status.HTTP_400_BAD_REQUEST)       

#         return Response({"data": "Articulo Creado"} , status=status.HTTP_200_OK) 

#     def get(self, request, format=None):
#         user = request.user
#         # Only serting user can view purchase order
#         if not user.has_perm('api.view_expense'):
#             return denied_permission()
#         try:
#             location = request.user.location.id
#         except:
#             return not_assiged_location()
        
#         expenses = Expense.objects.filter(location_id=location).prefetch_related("expenseType")
#         # Filter by date
#         serializer = self.expenseSerialzier(expenses, many=True)
#         # Get the purchase order by user location 
#         return Response(serializer.data , status=status.HTTP_200_OK)



# # get all expense Report
# # TODO: TO SENT BACK TO THE USER FOR MAT THE DATA AS { 'LABEL':'', VALUE:''} 
# # 
# class ExpenseReport(APIView):

#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]

#     expenseSerialzier = accounting_serializer.ExpenseSerializer
#     purchaseOrderSerializer = accounting_serializer.purchaseOrderSerializer

#     def get(self, request, format=None):

#         if not request.user.has_perm('api.view_expense') and not request.user.has_perm('api.view_purchaseorder'):
#             return denied_permission()
        
#         try:
#             location = request.user.location
#         except:
#             return not_assiged_location()
#         # data =  request.data.copy()
#         # startDate = request.GET.get('startDate') 
#         # endDate = request.GET.get('endDate') 

#         # if not "startDate" in data and not "endDate" in data:
#         #     return emptyField()

#         # Filter By Date Range
#         cleanedStartDT= request.GET.get('startDate') 
#         cleanedEndDT = request.GET.get('endDate') 
#         # cleanedStartDT= str(data["startDate"]).strip()
#         # cleanedEndDT = str(data["endDate"]).strip()

#         try:
#             start_date = timezone.make_aware(datetime.strptime(f"{cleanedStartDT} 01:00:00", '%m-%d-%Y %H:%M:%S') , timezone.get_current_timezone()  )    
#             end_date = timezone.make_aware(datetime.strptime(f"{cleanedEndDT} 23:59:59", '%m-%d-%Y %H:%M:%S') , timezone.get_current_timezone()  )
#         except:
#             return Response({ "data": "La fecha no está en un formato correcto" }, status=status.HTTP_400_BAD_REQUEST)

#         purchaseOrder = PurchaseOrder.objects.filter(locationId=location, createdOn__range=(start_date, end_date)).prefetch_related("POLines")
#         # TODO: Double check if to get the Expese date or the creation date
#         expenses = Expense.objects.filter(location_id=location, expense_date__range=(start_date, end_date)).prefetch_related("expenseType")

#         POTotalAmount = purchaseOrder.aggregate(total_units=Sum(F("POLines__units") * F("POLines__unitPrice")))["total_units"]
#         ExpenseTotalAmount = expenses.aggregate(total_units=Sum(F("amount")))["total_units"]
        
#         if ExpenseTotalAmount is None:
#            ExpenseTotalAmount = 0

#         if POTotalAmount is None:
#             POTotalAmount = 0

#         CombinedQuery = {
#             "Expenses": ExpenseTotalAmount,
#             "TotalPOs": POTotalAmount,
#             "TotalPurchases": ExpenseTotalAmount + POTotalAmount
#         }

#         return Response({ "data": CombinedQuery }, status=status.HTTP_200_OK)
    


# Trans History
# TODO: Ad UUID
# class TransactionHistory(ListAPIView):
   
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]

#     queryset =  TransactionReceipt.objects.all().order_by('date_created')
#     serializer_class =  pos_serializer.TransactionReceiptSerializer

#     def  get(self, request, format=None):

#         if not request.user.has_perm('api.view_transactionreceipt'):
#             return denied_permission()

#         try:
#             location =  request.user.location.id
#         except:
#             return not_assiged_location()

#         # TODO: FOR DATE TIME , JUST REDUCE TO MONTH/DAY/YEAR
#         queryset = self.queryset.filter(order__location_id = location, date_created__date=datetime.now().date())

#         queryset = queryset.annotate(date=TruncDate('date_created'))

#         if not queryset.exists():
#             return Response({'data': []}, status=status.HTTP_204_NO_CONTENT)
        
#         # results =  self.paginate_queryset(productsAttr, request, view=self)
#         serializer = self.serializer_class(queryset, many=True)

#         return Response(serializer.data , status=status.HTTP_200_OK)