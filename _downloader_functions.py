import io
from googleapiclient.discovery import build
from PyPDF2 import PdfWriter
from googleapiclient.http import MediaIoBaseDownload
import traceback
from fpdf import FPDF
import os
import subprocess
from zipfile import ZipFile
import comtypes.client
from docx2pdf import convert


def category_folder_create(category_path):
    try:
        if not (os.path.exists(category_path)):
            os.makedirs(category_path)
    except OSError as error:
        file1 = open("log.txt", "a")  # append mode
        file1.write(f"{category_path} is invalid")
        traceback.print_exc(file=file1)
        file1.close()

        # means category_path is invalid


def stepwise_downloader(file_full_path, downloader, file):
    done = False
    while done is False:
        status, done = downloader.next_chunk()

    with open(file_full_path, 'wb') as output_file:

        output_file.write(file.getvalue())

    extension = file_full_path.split(".")[-1]
    if (extension == "docx"):
        file_full_path = docx2pdf(file_full_path)
    elif (extension == "pptx"):
        file_full_path = pptx2pdf(file_full_path)
    else:
        print("stepwise_downloader only expects google doc ot ppt")

    return file_full_path


def download_google_doc(file_id, creds, docx_file_path):
    try:
        # Create Google Drive API client using the obtained credentials
        service = build('drive', 'v3', credentials=creds)
        # Download the document file
        request = service.files().export_media(fileId=file_id,
                                               mimeType='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        document = io.BytesIO()
        downloader = MediaIoBaseDownload(document, request)

        return stepwise_downloader(docx_file_path, downloader, document)

    except Exception as e:
        file1 = open("log.txt", "a")  # append mode
        file1.write(f'error at download_google_doc:\n{e}\n')
        traceback.print_exc(file=file1)
        file1.close()


def download_google_presentation(file_id, creds, pptx_file_path):

    try:
        # Create Google Drive API client using the obtained credentials
        service = build('drive', 'v3', credentials=creds)

        # Download the presentation file
        request = service.files().export_media(fileId=file_id,
                                               mimeType='application/vnd.openxmlformats-officedocument.presentationml.presentation')
        presentation = io.BytesIO()
        downloader = MediaIoBaseDownload(presentation, request)

        return stepwise_downloader(pptx_file_path, downloader, presentation)

    except Exception as e:
        file1 = open("log.txt", "a")  # append mode
        file1.write(f'error at download_google_presentation:\n{e}\n')
        traceback.print_exc(file=file1)
        file1.close()


def download_file(file_id, creds, folder_path, file_name):
    try:
        # Create Drive API client using the obtained credentials
        service = build('drive', 'v3', credentials=creds)

        # file_name = service.files().get(fileId=file_id).execute()['name']

        request = service.files().get_media(fileId=file_id)
        file = io.BytesIO()
        downloader = MediaIoBaseDownload(file, request)

        done = False
        while done is False:
            status, done = downloader.next_chunk()

        # Save the  file
        else:
            with open(folder_path+"/"+file_name, 'wb') as output_file:
                output_file.write(file.getvalue())

        return folder_path+"/"+file_name

    except Exception as e:
        file1 = open("log.txt", "a")  # append mode
        file1.write(f'error at download_file:\n{e}\n')
        traceback.print_exc(file=file1)
        file1.close()


def name_cleaner(a):
    not_allowed_characters = ["\\", "/", ":", "*", "?", "\"", "<", ">", "|"]
    cleaned_name = []

    for char in a:
        if (char.isascii()) and (char not in not_allowed_characters):
            cleaned_name.append(char)

    return "".join(cleaned_name)


def name_splitter(file_name):
    idx = file_name.rindex('.')
    return file_name[:idx], file_name[idx+1:]


def get_type_id(file_link):
    try:
        file_id = file_link.split("/")[5]
        file_type = file_link.split("/")[3]
        return file_type, file_id
    except:
        print(f"Invalid link: {file_link}")
        return False


class PDFWithWatermark(FPDF):
    def header(self):
        self.set_font("helvetica", "I", 150)
        self.set_text_color(200)
        x = 50
        y = self.h

        # Print the watermark text
        self.text(x, y, "Recco Bot")
        # Reset font and color
        self.set_font("helvetica", "", 7)
        self.set_text_color(0)


def txt2pdf_create(txt_to_add, destination_file_path):

    pdf = PDFWithWatermark()
    pdf.add_page(orientation="L")
    pdf.set_font("helvetica", size=50)
    if len(txt_to_add) < 20:
        pdf.cell(w=0, h=10, txt=txt_to_add,
                 align='C', link="https://www.linktr.ee/reccobot")
    else:
        pdf.set_font("helvetica", size=20)
        pdf.cell(w=0, h=10, txt=txt_to_add,
                 align='C', link="https://www.linktr.ee/reccobot")
    pdf.ln()
    pdf.ln()
    pdf.set_font("helvetica", size=15)
    pdf.cell(w=0, h=10, txt="Please watch our tutorial on how to use our bot in best way. ",
             align='C', link="https://www.linktr.ee/reccobot")

    pdf.ln()
    pdf.cell(w=0, h=10, txt="https://www.linktr.ee/reccobot",
             align='C', link="https://www.linktr.ee/reccobot")

    pdf_name = f"title_pg_{txt_to_add}.pdf"
    pdf.output(name=pdf_name, dest=destination_file_path)
    return os.path.join(destination_file_path, pdf_name)


def pdf_mrger(filePaths_list: list, dest_folder_name: str, output_pdf_name: str):
    merger = PdfWriter()
    filePaths_list.reverse()
    for pdf_file_full_path in filePaths_list:

        try:
            merger.append(pdf_file_full_path)
            os.remove(pdf_file_full_path)
        except Exception as e:
            if str(e) not in ["'DictionaryObject' object has no attribute 'indirect_reference'", "'NullObject' object has no attribute 'get'"]:
                file1 = open("log.txt", "a")  # append mode
                file1.write(f'cant append:{pdf_file_full_path}\n{e}\n')
                traceback.print_exc(file=file1)
                file1.close()

    output_pdf_path = dest_folder_name+"/"+output_pdf_name
    merger.write(output_pdf_path)
    merger.close()
    return output_pdf_path


def edit2view(file_link):
    # edit?usp=drive_web&authuser=0": "Quiz1-Set B Solution",
    link_boxes = file_link.split("/")
    if (link_boxes[6][:4] == "edit"):
        link_boxes[6] = "view"+file_link.split("/")[6][4:]
        return "/".join(link_boxes)
    else:
        return file_link

# for windows and for mac


def docx2pdf(input_docx_path):
    try:
        output_file_name = os.path.splitext(
            os.path.basename(input_docx_path))[0] + ".pdf"

        if os.name == 'nt':
            convert(input_docx_path, output_file_name)
            converted_path = f"C:\\Users\\hp\\Documents\\{output_file_name}"
            os.remove(input_docx_path)
            return converted_path

        else:
            # brew install unoconv
            subprocess.run(["brew", "install", "unoconv"])
            subprocess.run(["unoconv", "-f", "pdf", input_docx_path])
            os.remove(input_docx_path)
            return output_file_name

    except Exception as e:

        file1 = open("log.txt", "a")  # append mode
        file1.write(f'Conversion failed at docx2pdf:{input_docx_path}\n{e}\n')
        traceback.print_exc(file=file1)
        file1.close()


def reset_eof_of_pdf_return_stream(pdf_stream_in: list):
    # find the line position of the EOF
    for i, x in enumerate(pdf_stream_in[::-1]):
        if b'%%EOF' in x:
            actual_line = len(pdf_stream_in)-i
            break
    # return the list up to that point
    return pdf_stream_in[:actual_line]


def javascript_post_EOF_remover(pptx_path):

    with open(pptx_path, 'rb') as p:
        txt = (p.readlines())

    # get the new list terminating correctly
    txtx = reset_eof_of_pdf_return_stream(txt)

    # write to new pdf
    with open(pptx_path, 'wb') as f:
        f.writelines(txtx)

# # for windows


def pptx2pdf(input_pptx_path):
    try:
        powerpoint = comtypes.client.CreateObject("Powerpoint.Application")
        powerpoint.Visible = 1

        presentation = powerpoint.Presentations.Open(
            os.path.abspath(input_pptx_path))
        output_file_name = os.path.splitext(
            os.path.basename(input_pptx_path))[0] + ".pdf"

        output_path = (output_file_name)
        try:
            presentation.ExportAsFixedFormat(os.path.abspath(
                output_path), 2)  # 2 represents PDF format
        except Exception as e:
            file1 = open("log.txt", "a")  # append mode
            file1.write(f'error at pptx2pdf:\n{input_pptx_path}\n{e}\n')
            traceback.print_exc(file=file1)
            file1.close()

        presentation.Close()
        powerpoint.Quit()

        javascript_post_EOF_remover(output_path)
        os.remove(input_pptx_path)
        return output_path

    except Exception as e:
        file1 = open("log.txt", "a")  # append mode
        file1.write(f'error at pptx2pdf:\n{e}\n')
        traceback.print_exc(file=file1)
        file1.close()


# # for mac
# def pptx2pdf(input_pptx_path):
#     subprocess.run(["brew", "install", "unoconv"])
#     subprocess.run(["brew", "install", "libreoffice"])
#     try:
#         # Convert PPTX to PDF using unoconv
#         subprocess.run(["unoconv", "-f", "pdf", input_pptx_path])

#     except Exception as e:
        # print(f"An error occurred at pptx2pdf: \n{e}")
        # traceback.print_exc()


# for Ubuntu


# def pptx2pdf(input_pptx_path):
#     command = "sudo apt install libreoffice"
#     subprocess.check_call(command, shell=True)

#     command = "sudo apt install unoconv"
#     subprocess.check_call(command, shell=True)

#     try:
#         # Convert PPTX to PDF using unoconv
#         subprocess.run(["unoconv", "-f", "pdf", input_pptx_path])

#     except Exception as e:
#         print(f"An error occurred at pptx2pdf: \n{e}")
        # traceback.print_exc()


#     print()
#     print(f"Ignore prev text, just doing pptx2pdf ")


def zip_compression_tree(root, zip_name):
    with ZipFile(zip_name, 'w') as z:
        for root, dirs, files in os.walk(root):
            for file in files:
                z.write(os.path.join(root, file))
            for directory in dirs:
                z.write(os.path.join(root, directory))


# ............................................................................................................................................................
# ............................................................................................................................................................
# ............................................................................................................................................................
if __name__ == '__main__':

    # credentials_path = "client_secret_358097454024-7s3tq97pb4cu71atb31k72higg14cf7b.apps.googleusercontent.com.json"

    # # Set up the OAuth 2.0 flow
    # flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
    #     credentials_path,
    #     scopes=['https://www.googleapis.com/auth/documents.readonly','https://www.googleapis.com/auth/presentations.readonly', 'https://www.googleapis.com/auth/drive.readonly']
    # )

    # creds = flow.run_local_server()
    # if(zip_compression_tree("CSE101_2022", "CSE101_2022.ZIP")):
    #     print("OK")

    # file = download_file('1h_YmWjljbtsiHpy4K_r4JS9y5KlroruE', creds, "1.pdf")
    # if  file:
    #     print(f"Downloaded  file: {file}")

    # doc_file = download_google_doc('1E_9Up1oKlm8ZTUBpOlsn76FTGZgfmC88O3duhHa-6nU', creds, "2.docx")
    # if doc_file:
    #     print(f"Downloaded Google Docs file as .docx: {doc_file}")

    # presentation_file = download_google_presentation('1x89Pv9j2JowGZxjqzkxGBT8il2qc1aah1JuJ5Gg3dF4', creds, "3.pptx")
    # if presentation_file:
    #     print(f"Downloaded Google Presentation as .pptx: {presentation_file}")

    # Replace with your .docx file path
    docx_file = "Assignment-1___[[Assignment 1]].docx"

    # pptx_file = "L10.pptx"  # Replace with your .pptx file path
    # p1 = pptx2pdf(pptx_file)
    # txt2pdf_create(
    #     txt_to_add="Material_name", destination_file_path="")

    docx2pdf(docx_file)
    pdf_mrger([docx2pdf(docx_file), txt2pdf_create(
        txt_to_add="Hello", destination_file_path="")], "CHANDAN", "hello.pdf")

    # output_pdf = docx2pdf(docx_file)
    # print("Output PDF path:", output_pdf)

    # print(edit2view("https://docs.google.com/document/d/1MlQeldQbUbkqWG-Qvh70LQXsg4s4m65fiAhSERvJMBw/edit?usp=drive_web&authuser=0"))
