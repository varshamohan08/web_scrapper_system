from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import transaction
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
from .models import EntitiesMaster
from .serializers import EntitiesMasterSerializer

class SaveEntitiesMaster(APIView):
    def get(self, request):
        try:
            # import pdb;pdb.set_trace()
            # chrome_driver_path = '/home/.../chromedriver-linux64/chromedriver'
            chrome_driver_path = ''

            service = Service(chrome_driver_path)
            options = webdriver.ChromeOptions()
            driver = webdriver.Chrome(service=service, options=options)

            # webpage_url = "https://k12.sfsymphony.org/Buy-Tickets/2023-24/Chamber-Jun-16"
            webpage_url = request.GET.get('webpage_url')
            driver.get(webpage_url)

            # time.sleep(1)
            # import pdb;pdb.set_trace()

            artist_elements = driver.find_elements(By.XPATH, "//div[@class='event-detail-artist margin-bottom-1']/p[@class='subhead4 margin-bottom-0']/a")
            role_elements = driver.find_elements(By.XPATH, "//div[@class='event-detail-artist margin-bottom-1']/p[@class='subhead6 margin-bottom-0']")

            artists = []
            for artist, role in zip(artist_elements, role_elements):
                artists.append({"name": artist.text.strip(), "role": role.text.strip()})

            program_elements = driver.find_elements(By.XPATH, "//div[@class='text-left  ']/div[@class='subhead4 margin-bottom:0']")
            composer_elements = driver.find_elements(By.XPATH, "//div[@class='text-left  ']/div[@class='margin-bottom-1 ']")

            programs = []
            for program, composer in zip(program_elements, composer_elements):
                programs.append({"name": program.text.strip(), "composer": composer.text.strip()})

            date_time_element = driver.find_element(By.XPATH, "//div[@class='performance-card margin-bottom-2']/div[@class='content']/p[@class='body-text3']")
            auditorium_element = driver.find_element(By.XPATH, "//div[@class='performance-card margin-bottom-2']/div[@class='content']/p[@class='location subhead6']/strong")

            performance = {
                "date_time": date_time_element.text.strip(),
                "auditorium": auditorium_element.text.strip()
            }

            driver.quit()

            data = {
                "web_url" : webpage_url,
                "details_json": {
                    "artists": artists,
                    "programs": programs,
                    "performance": performance
                }
            }

            # print(data)

            with transaction.atomic():
                serializer = EntitiesMasterSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    return Response({"success":True, 'details': serializer.data}, status=status.HTTP_201_CREATED)
                return Response({"success":False, 'details': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"success":False, 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class GetEntitiesMaster(APIView):
    def get(self, request):
        try:
            if request.GET.get('id'):
                entities = EntitiesMaster.objects.get(id = request.GET.get('id'))
                serializer = EntitiesMasterSerializer(entities)
            elif request.GET.get('webpage_url'):
                entities = EntitiesMaster.objects.filter(web_url = request.GET.get('webpage_url')).first()
                serializer = EntitiesMasterSerializer(entities)
            else:
                entities = EntitiesMaster.objects.all()
                serializer = EntitiesMasterSerializer(entities, many=True)
            return Response({"success":True, 'details': serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"success":False, 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)