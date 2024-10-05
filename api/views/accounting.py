from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from datetime import datetime, timedelta, date, time
from dateutil import rrule
import calendar

from django.db.models import Sum

#MODELS
from ..models import  TransactionReceipt


from ..serializers import pos_serializer

# getting all trasactions for that day
class Revenue(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class =  pos_serializer.TransactionReceiptSerializer

    def  get(self, request, format=None):

        # get the quaters
        # print(date(2024,5,11).month)
        # date_instance = date(2024,9,11)
        option = int(request.GET.get('option', 1))

        try:
            location =  request.user.location.id
        except:
            return Response({'data': "you are not assign to a location" }, status=status.HTTP_400_BAD_REQUEST)

        # datenow = datetime.now() 

        # first_day = quarters.before(datenow)
        # last_day = (quarters.after(datenow) - relativedelta.relativedelta(days=1))
    
        response_data = []
        total_amount = 0
        datetime_year= datetime.today().strftime("%Y")
        datetime_month = int(datetime.today().strftime("%m"))

        try: 
            if option == 1:
                # print this will print all of the revenue of today
                salesOrder_instance = TransactionReceipt.objects.filter(location_id = location, date_created__date=datetime.now().date()) 
                if salesOrder_instance.exists():
                    total_amount = { "label": "Today",
                                     "value" : salesOrder_instance.aggregate(total = Sum("amount"))["total"] }
                else:
                    total_amount = { "label": "Today", 
                                     "value" : 0 }
                
                response_data.append( total_amount )

            elif option == 2:
                # Return only the sales for the specific week Mon - Sun.
                date = datetime.now()
                start_week =  date - timedelta(date.weekday())
                end_week = start_week + timedelta(7)

                for i in rrule.rrule(rrule.DAILY, dtstart=start_week, until=end_week):
                    year = i.strftime('%Y')
                    month = i.strftime('%m')
                    day = i.strftime('%d')

                    transactions_instance = TransactionReceipt.objects.filter(location_id = location,  date_created__date= i.date() )

                    name_of_day = calendar.day_name[calendar.weekday(int(year),int(month),int(day))]

                    if transactions_instance.exists():
                        total_amount = { "label": name_of_day,
                                          "value": transactions_instance.aggregate(total=Sum("amount"))["total"]}
                    else:
                        total_amount = { "label": name_of_day,
                                         "value": 0 }
                        
                    response_data.append(total_amount)

            elif option == 3:
                # This options get the sales for each month - today date
                for datetime_month in range(1, datetime_month+1):
                    transactions_instance = TransactionReceipt.objects.filter(location_id = location, date_created__month=datetime_month)

                    month_name =  calendar.month_name[datetime_month]
                    if transactions_instance.exists():
                        total_amount = { "label": month_name , 
                                         "value" :transactions_instance.aggregate(total=Sum("amount"))["total"]}
                    else:
                        total_amount = { "label" : month_name,
                                         "value" : 0 }

                    response_data.append(total_amount)
                    
            elif option == 4:
                # datetime.now().year
                # this options only gets the quaterly or yearly sales
                # quarters = rrule.rrule(
                #     rrule.MONTHLY,
                #     bymonth=(1, 4, 7, 10),
                #     bysetpos=-1,
                #     dtstart = datetime(datetime.now().year, 1, 1),
                #     count=4
                #     )
                
                # for i in quarters:
                #     print(i.date())
                #     print(i)
                print("Select a diferent Option, this option is not available yet.")
            else:
                raise Exception("Something went wrong")

        except Exception as e:
            return Response({'data':  e}, status=status.HTTP_400_BAD_REQUEST) 

        return Response({'data': response_data }, status=status.HTTP_200_OK)


# TODO: Check all of the exprenses for the store location
class Expenses(APIView):
   
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
   
   pass 
# return Order


#TODO: ADD WHO CAN ACCES THIS CLASS
#TODO: ADD TRANSACTION ID OR ORDER ID Auto Generated
class TransactionHistory(ListAPIView):
   
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset =  TransactionReceipt.objects.all().order_by('date_created')
    serializer_class =  pos_serializer.TransactionReceiptSerializer

    def  get(self, request, format=None):

        try:
            location =  request.user.location.id
        except:
            return Response({'data': "you are not assign to a location" }, status=status.HTTP_400_BAD_REQUEST)
        

        # date = datetime.now()

        # salesOrder_instance = TransactionReceipt.objects.filter(location_id = location, date_created__date=datetime.now().date())

        queryset = self.queryset.filter(location_id = location, date_created__date=datetime.now().date())

        if not queryset.exists():
            return Response({'message': "Not Transactions Found"}, status=status.HTTP_204_NO_CONTENT)
        
        # results =  self.paginate_queryset(productsAttr, request, view=self)
        serializer = self.serializer_class(queryset, many=True)

        # else return all of the sales order

        return Response(serializer.data , status=status.HTTP_200_OK)
        



# return Order