import os
import datetime
import json
import magic
import shutil
from pathlib import Path	

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, tsv, timeline, kmlgen, is_platform_windows, utf8_in_extended_ascii, media_to_html

def get_instagramPending(files_found, report_folder, seeker, wrap_text, time_offset):
    data_list = []
    for file_found in files_found:
        file_found = str(file_found)
        
        filename = os.path.basename(file_found)
        
        if filename.startswith('pending_follow_requests.json'):
            
            with open(file_found, "r") as fp:
                deserialized = json.load(fp)
        
            for x in deserialized['relationships_follow_requests_sent']:
                href = x['string_list_data'][0].get('href', '')
                value = x['string_list_data'][0].get('value', '')
                timestamp = x['string_list_data'][0].get('timestamp', '')
                if timestamp > 0:
                    timestamp = (datetime.datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S'))
                
                data_list.append((timestamp, value, href))
    
                
    if data_list:
        report = ArtifactHtmlReport('Instagram Archive - Pending Follow Req')
        report.start_artifact_report(report_folder, 'Instagram Archive - Pending Follow Req')
        report.add_script()
        data_headers = ('Timestamp','User', 'Href')
        report.write_artifact_data_table(data_headers, data_list, file_found, html_no_escape=['Media'])
        report.end_artifact_report()
        
        tsvname = f'Instagram Archive - Pending Follow Req'
        tsv(report_folder, data_headers, data_list, tsvname)
        
        tlactivity = f'Instagram Archive - Pending Follow Req'
        timeline(report_folder, tlactivity, data_list, data_headers)

    else:
        logfunc('No Instagram Archive - Pending Follow Req')
                
__artifacts__ = {
        "instagramPending": (
            "Instagram Archive",
            ('*/followers_and_following/pending_follow_requests.json'),
            get_instagramPending)
}