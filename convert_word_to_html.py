# pip install pywin32
import win32com.client
import os

base_dir = os.path.dirname(__file__)
doc_file = os.path.join(base_dir, 'Статья 1 - развод через суд.docx') 
html_file = os.path.join(base_dir, 'article.html')

doc = win32com.client.GetObject(doc_file)
doc.SaveAs (FileName=html_file, FileFormat=8)
doc.Close ()
print(f"{html_file} saved successfully!")
