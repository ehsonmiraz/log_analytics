import os
import json
import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from .models import Log
from .serializers import LogSerializer

from django.conf import settings

logger = logging.getLogger(__name__)

class LogIngest(APIView):
    def post(self, request, format=None):
        try:
            # Get data from request body
            data = request.data          
            # Validate data
            if not data.get('level') or not data.get('log_string') or not data.get('timestamp') or not data.get('metadata'):
                raise ParseError('Invalid log entry data')
            log_directory = 'log_files'
            if not os.path.exists(log_directory):
                os.makedirs(log_directory)
            # Create Log object
            log_entry = Log.objects.create(
                level=data.get('level'),
                log_string=data.get('log_string'),
                timestamp=data.get('timestamp'),
                source=data.get('metadata').get('source')
            )

            # Write log entry to specified log file
            log_filename = log_entry.source
            log_path = os.path.join('log_files', log_filename)

            # Configure logger
            logging.SUCCESS = 25  # between WARNING and INFO
            logging.addLevelName(logging.SUCCESS, 'SUCCESS')
            setattr(logger, 'success', lambda message, *args: logger._log(logging.SUCCESS, message, args))

            logger.setLevel(logging.DEBUG)
       
            file_handler = logging.FileHandler(log_path)
            if (logger.hasHandlers()):
                  logger.handlers.clear()
            logger.addHandler(file_handler)
            
            # Format log entry
            log_message = f"{log_entry.timestamp} - {log_entry.level} - {log_entry.log_string}"
          
            # Write log entry to file
    
            levels={
                "info":logger.info,
                "success":logger.success,
                "error":logger.error
                }

            levels.get(log_entry.level)(log_message)
            # index_log_entry(log_message)
            return Response({'message': 'Log entry saved successfully'}, status=201)
        except ParseError as e:
            return Response({'error': str(e)}, status=400)
        except Exception as e:
            return Response({'error': str(e)}, status=500)
        
