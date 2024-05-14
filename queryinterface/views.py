import os
from django.http import JsonResponse
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


class LogSearch(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request):
        try:
            print(request.GET.get('level', ''))  
            level = request.GET.get('level', '')
            log_string = request.GET.get('log_string', '')
            timestamp = request.GET.get('timestamp', '')
            source = request.GET.get('source', '')
            print(source)
            print(level)
            # Perform search in log files
            results = self.search_logs( level, log_string, timestamp, source)

            return JsonResponse({'results': results}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    def search_logs(self, level, log_string, timestamp, source):
        log_files_directory = 'log_files'
        results = []
        if source:
            retrive_result_from_log_file(log_files_directory,source,results,level,log_string,timestamp)
        else:
         for filename in os.listdir(log_files_directory):
            if filename.endswith('.log'):
                retrive_result_from_log_file(log_files_directory,filename,results,level,log_string,timestamp)
        
        return results

def retrive_result_from_log_file(log_files_directory,filename,results,level,log_string,timestamp):
    with open(os.path.join(log_files_directory, filename), 'r') as file:
                    for line in file:
                        try:
                         line=line.split(" - ")
                         log_entry = {"timestamp":line[0],
                                      "level":line[1],
                                      "log_string":line[2]
                                      }  # Convert string to dictionary
                        
                        except Exception as e:
                         print(e)
                        if (not level or level == log_entry.get('level', '')) and \
                                (not log_string or log_string in log_entry.get('log_string', '')) and \
                                (not timestamp or timestamp == log_entry.get('timestamp', '')):
                            results.append(log_entry)
