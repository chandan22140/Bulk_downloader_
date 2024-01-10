import traceback
from _downloader_functions import edit2view, name_splitter, category_folder_create, get_type_id, download_file, download_google_doc, download_google_presentation, name_cleaner, docx2pdf, pptx2pdf, pdf_mrger, zip_compression_tree, txt2pdf_create
import google_auth_oauthlib.flow
import shutil
import telebot
from googleapiclient.discovery import build
import json
import os
API_KEY = "5991202973:AAG8u83Knyd2fDz8x7jJ99UuNa0fKihZWOY"
bot = telebot.TeleBot(API_KEY, parse_mode=None)


def do_seconary_phase():
    file1 = open("log.txt", "w")  # write mode
    file1.write(f'log Started')
    traceback.print_exc(file=file1)
    file1.close()

    credentials_path = "_client_secret_358097454024-7s3tq97pb4cu71atb31k72higg14cf7b.apps.googleusercontent.com.json"
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        credentials_path,
        scopes=['https://www.googleapis.com/auth/documents.readonly',
                'https://www.googleapis.com/auth/presentations.readonly', 'https://www.googleapis.com/auth/drive.readonly']
    )

    creds = flow.run_local_server()

    json_data_file = open('final.json')
    data = json.load(json_data_file)

    for classroom_name in data.keys():
        if "__cc_ay_sec__" in classroom_name:
            continue

        batch = classroom_name.split("_")[-1]
        classroom_name_wo_year = classroom_name.split("_")[0]

        file1 = open("log.txt", "a")  # append mode
        file1.write(f"Entered: {classroom_name}\n")
        file1.close()

        classwork_categories_list = list(data[classroom_name].keys())

        for category_name in classwork_categories_list:
            this_category_flag = True
            valid_file = False
            list_of_merged_materials = []
            matrial_or_assignmt_list = list(
                data[classroom_name][category_name].keys())
            category_path = f'{(classroom_name_wo_year)}/{name_cleaner(category_name)}'
            index = 0
            for matrial_name in ((matrial_or_assignmt_list)):
                # matrial_name = name_cleaner(matrial_name)
                file_link_collection = list(
                    data[classroom_name][category_name][matrial_name].keys())
                entire_matrial_pdf_flag = True
                entire_matrial_pdf_list = []

                for file_link in reversed(file_link_collection):
                    index += 1

                    file1 = open("log.txt", "a")  # append mode
                    file1.write(
                        f"-----------------------------------------------------------------------------------------------\n")
                    file1.close()
                    # file_name = name_cleaner(
                    #     data[classroom_name][category_name][matrial_name][file_link])

                    try:
                        file_type, file_id = get_type_id(file_link=file_link)
                    except Exception as e:
                        # coming here means tuple is being assigned boolean value, so, continue this loop
                        continue

                    if file_type not in ["file", "document", "presentation"]:
                        continue

                    file_link = edit2view(file_link)
                    service = build('drive', 'v3', credentials=creds)

                    try:
                        file_name = (str(
                            index))+"_" + name_cleaner(service.files().get(fileId=file_id).execute()['name'])
                    except Exception as e:
                        # coming here means the file doesn't exist
                        continue

                    if (file_type == "file"):

                        try:
                            name_without_extension, extension = name_splitter(
                                file_name)
                            file_name = f'{name_without_extension}___[[{name_cleaner(matrial_name)}]].{extension}'
                        except:
                            #  coming here means theres no extension, so, continue this loop
                            continue

                        if extension in ['vtt', 'mp4', 'mp3', 'm4a', 'srt', 'subtitle', 'crdownload', 'p4']:
                            continue
                        if extension.lower() not in ['vtt', 'mp4', 'mp3', 'm4a', 'srt', 'subtitle', 'crdownload', 'p4', 'pdf', 'docx', 'odt', 'txt', 'pptx', 'xlsx', 'jpg', 'png', 'jpeg', 'zip', 'ipynb', 'py', 'csv', 'java', 'c', 'cpp']:
                            bot.send_message(
                                800851598, f"new extensiom:  {extension}")

                        valid_file = True

                        category_folder_create(category_path)
                        file_path = download_file(
                            file_id, creds, category_path, file_name)
                        # print(file_path)
                        if (extension == "docx"):
                            file_path = docx2pdf(file_path)
                            extension = "pdf"

                        elif (extension == "pptx"):
                            file_path = pptx2pdf(file_path)
                            extension = "pdf"

                        elif (extension != "pdf"):
                            # print("camee here")
                            # print(extension)
                            entire_matrial_pdf_flag = False
                            this_category_flag = False

                        if entire_matrial_pdf_flag:
                            entire_matrial_pdf_list.append(file_path)
                            entire_matrial_pdf_list.append(txt2pdf_create(
                                "Filename:"+name_without_extension, ""))

                    elif file_type == "document":

                        name_without_extension = file_name
                        file_name = f'{name_cleaner(file_name)}___[[{name_cleaner(matrial_name)}]].docx'
                        category_folder_create(category_path)
                        file_path = category_path+"/"+file_name
                        file_path = download_google_doc(
                            file_id, creds, file_path)
                        valid_file = True

                        if file_path:
                            # print(f"Downloaded Google Docs file as .docx: {file_full_path}")
                            entire_matrial_pdf_list.append(file_path)
                            entire_matrial_pdf_list.append(txt2pdf_create(
                                "Filename:"+name_without_extension, ""))

                    elif file_type == "presentation":
                        name_without_extension = file_name
                        file_name = f'{name_cleaner(file_name)}___[[{name_cleaner(matrial_name)}]].pptx'
                        category_folder_create(category_path)
                        file_path = category_path+"/"+file_name
                        presentation_file_as_pdf_path = download_google_presentation(
                            file_id, creds, file_path)
                        valid_file = True

                        if presentation_file_as_pdf_path:
                            entire_matrial_pdf_list.append(
                                presentation_file_as_pdf_path)
                            entire_matrial_pdf_list.append(txt2pdf_create(
                                "Filename_"+name_without_extension, ""))

                if ((file_link_collection) == []):
                    continue
                # jk??
                elif (entire_matrial_pdf_list == []):
                    continue
                if (entire_matrial_pdf_flag) and (entire_matrial_pdf_list):
                    # means no imposter files and there and pdfs to merge
                    try:
                        merged_pdf_path = pdf_mrger(filePaths_list=entire_matrial_pdf_list, output_pdf_name=name_cleaner(
                            matrial_name)+".pdf", dest_folder_name=category_path)
                        list_of_merged_materials.append(merged_pdf_path)
                        list_of_merged_materials.append(txt2pdf_create(
                            "Material name_"+name_cleaner(matrial_name), ""))
                    except Exception as e:

                        file1 = open("log.txt", "a")  # append mode
                        file1.write(f'cant merge the material into 1: \n{e}\n')
                        traceback.print_exc(file=file1)
                        file1.close()

                elif not (entire_matrial_pdf_flag):
                    this_category_flag = False
                elif not (entire_matrial_pdf_list):
                    valid_file = False

            if matrial_or_assignmt_list == []:
                continue
            if (not (valid_file)):
                continue

            if valid_file and this_category_flag and list_of_merged_materials:
                try:
                    pdf_name = name_cleaner(category_name+"_"+batch)+".pdf"
                    pdf_mrger(filePaths_list=list_of_merged_materials, dest_folder_name=name_cleaner(
                        classroom_name_wo_year), output_pdf_name=pdf_name)
                    shutil.rmtree(category_path)
                except Exception as e:

                    file1 = open("log.txt", "a")  # append mode
                    file1.write(f'cant merge the category into 1: \n{e}\n')
                    traceback.print_exc(file=file1)
                    file1.close()

            elif not (this_category_flag):
                try:
                    zip_compression_tree(
                        category_path, (category_path+"_"+batch)+".zip")
                    shutil.rmtree(category_path)
                except Exception as e:
                    file1 = open("log.txt", "a")  # append mode
                    file1.write(f'cant merge the category into 1 zip: \n{e}\n')
                    traceback.print_exc(file=file1)
                    file1.close()
    json_data_file.close()
    print("licsenced by Chandan S. ")

    bot.send_message(800851598, "bulk_download_done!1")
    # os.remove("final.json")
    # os.remove("_main_phase.py")
    # os.remove("_seconary_phase.py")
    # os.remove("_req.txt")
    # os.remove("_downloader_functions.py")
    # try:
    #     os.remove(
    #         "_client_secret_358097454024-7s3tq97pb4cu71atb31k72higg14cf7b.apps.googleusercontent.com.json")
    #     os.remove("_link_collector.py")
    # except:
    #     pass
