#encoding=utf-8
from flask import Flask, render_template, request, redirect, url_for, send_file
import os
from werkzeug.utils import secure_filename
import docx
from bs4 import BeautifulSoup
from datetime import datetime
from flask_socketio import SocketIO, emit, join_room
import pypandoc

def get_current_time():
    # Get the current time
    now = datetime.now()

    # Format the time as a string
    current_time = now.strftime("%H:%M")

    # Return the current time
    return current_time

def extract_file_names(folder_path):
    """
        Extract all file names from the specified folder.

        Args:
        folder_path (str): The path to the folder from which to extract file names.

        Returns:
        list: A list containing the names of all files in the specified folder.
        """
    # List to store file names
    file_names = []

    # Iterating over all entries in the specified folder
    for entry in os.listdir(folder_path):
        # Full path of the entry
        full_path = os.path.join(folder_path, entry)
        # Check if the entry is a file and not a directory
        if os.path.isfile(full_path):
            # Add the file name to the list
            file_names.append(entry)

    return file_names


def get_ilvl_elements(paragraph):
    # Accessing the XML of the paragraph
    p_xml = paragraph._element
    ilvl_elements = []
        # Find <w:ilvl> elements within the paragraph XML
    ilvl_xml_elements = p_xml.findall('.//w:ilvl', namespaces={'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'})
    if ilvl_xml_elements:
        # Extract the value attribute from the <w:ilvl> elements
        for ilvl in ilvl_xml_elements:
            ilvl_val = ilvl.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val')
            ilvl_elements.append(ilvl_val)
        return ilvl_elements[0]
    else:
        return 'None'

#out of date function, keeping it just to remenber my stupid work, replaced by a function with same name
# def docx_to_html(docx_path):
#
#     # Load the Word document
#     doc = docx.Document(docx_path)
#     #checked
#     # Create a new BeautifulSoup object
#     soup = BeautifulSoup('<body></body>', 'html.parser')
#
#     # Create the HTML 'body' element
#     body = soup.body
#
#     div = soup.new_tag('div')
#     div['style'] = 'margin: 20px; font-family: Arial, sans-serif;'
#     # Iterate through the paragraphs in the document
#     ul_tag = soup.new_tag('ul')
#     ul_tag['style'] = 'list-style-type: decimal;'
#     ul_tag1 = soup.new_tag('ul')
#     ul_tag1['style'] = 'margin-left: 20px; list-style-type: lower-alpha;'
#     ul_tag2 = soup.new_tag('ul')
#     ul_tag2['style'] = 'margin-left: 40px; list-style-type: lower-roman;'
#     for para in doc.paragraphs:
#         #checked
#         ilvl_elements = get_ilvl_elements(para)
#         #checked
#         if ilvl_elements == '0':
#             #checked
#             # check if the line break is already been added
#             br_is_been_added = 0
#             print(ul_tag2.contents)
#             if ul_tag1.contents:
#                 br_is_been_added=1
#                 if ul_tag2.contents:
#                     br=soup.new_tag('br')
#                     ul_tag2.append(br)
#                     ul_tag1.append(ul_tag2)
#                     ul_tag2=soup.new_tag('ul')
#                     ul_tag2['style'] = 'margin-left: 40px; list-style-type: lower-roman;'
#                     ul_tag.append(ul_tag1)
#                     ul_tag1=soup.new_tag('ul')
#                     ul_tag1['style'] = 'margin-left: 20px; list-style-type: lower-alpha;'
#                 else:
#                     br = soup.new_tag('br')
#                     ul_tag1.append(br)
#                     ul_tag.append(ul_tag1)
#                     ul_tag1 = soup.new_tag('ul')
#                     ul_tag1['style'] = 'margin-left: 20px; list-style-type: lower-alpha;'
#             li_tag = soup.new_tag('li')
#             # Check each run in the paragraph for underlined and italic text
#             for run in para.runs:
#                 #checked
#                 text_element = soup.new_tag('span')  # Use span as a base for text styling
#                 text_element.string = run.text
#
#                 # Apply underlining if the text is underlined
#                 if run.underline:
#                     text_element.name = 'u'
#
#                 # Apply italics if the text is italicized
#                 if run.italic:
#                     # If already underlined, wrap with 'i' tag, else just convert to 'i'
#                     if text_element.name == 'u':
#                         i_tag = soup.new_tag('i')
#                         i_tag.append(text_element.string)
#                         text_element.string = ''
#                         text_element.append(i_tag)
#                     else:
#                         text_element.name = 'i'
#
#                 li_tag.append(text_element)
#                 #print(li_tag.name)
#             if br_is_been_added==0:
#                 br = soup.new_tag('br')
#                 ul_tag.append(br)
#             ul_tag.append(li_tag)
#             #print(ul_tag.string)
#         elif ilvl_elements == '1':
#             if ul_tag2.string:
#                 ul_tag1.append(ul_tag2)
#                 ul_tag2 = soup.new_tag('ul')
#                 ul_tag2['style'] = 'margin-left: 40px; list-style-type: lower-roman;'
#             li_tag = soup.new_tag('li')
#             # Check each run in the paragraph for underlined and italic text
#             for run in para.runs:
#                 text_element = soup.new_tag('span')  # Use span as a base for text styling
#                 text_element.string = run.text
#
#                 # Apply underlining if the text is underlined
#                 if run.underline:
#                     text_element.name = 'u'
#
#                 # Apply italics if the text is italicized
#                 if run.italic:
#                     # If already underlined, wrap with 'i' tag, else just convert to 'i'
#                     if text_element.name == 'u':
#                         i_tag = soup.new_tag('i')
#                         i_tag.append(text_element.string)
#                         text_element.string = ''
#                         text_element.append(i_tag)
#                     else:
#                         text_element.name = 'i'
#                 li_tag.append(text_element)
#             ul_tag1.append(li_tag)
#         elif ilvl_elements == '2':
#             li_tag = soup.new_tag('li')
#             # Check each run in the paragraph for underlined and italic text
#             for run in para.runs:
#                 text_element = soup.new_tag('span')  # Use span as a base for text styling
#                 text_element.string = run.text
#
#                 # Apply underlining if the text is underlined
#                 if run.underline:
#                     text_element.name = 'u'
#
#                 # Apply italics if the text is italicized
#                 if run.italic:
#                     # If already underlined, wrap with 'i' tag, else just convert to 'i'
#                     if text_element.name == 'u':
#                         i_tag = soup.new_tag('i')
#                         i_tag.append(text_element.string)
#                         text_element.string = ''
#                         text_element.append(i_tag)
#                     else:
#                         text_element.name = 'i'
#                 li_tag.append(text_element)
#             ul_tag2.append(li_tag)
#
#         else:
#             p_tag = soup.new_tag('p')
#             for run in para.runs:
#                 text_element = soup.new_tag('span')  # Use span as a base for text styling
#                 text_element.string = run.text
#
#                 # Apply underlining if the text is underlined
#                 if run.underline:
#                     text_element.name = 'u'
#
#                 # Apply italics if the text is italicized
#                 if run.italic:
#                     # If already underlined, wrap with 'i' tag, else just convert to 'i'
#                     if text_element.name == 'u':
#                         i_tag = soup.new_tag('i')
#                         i_tag.append(text_element.string)
#                         text_element.string = ''
#                         text_element.append(i_tag)
#                     else:
#                         text_element.name = 'i'
#                 p_tag.append(text_element)
#                 if '\n' in text_element.contents:
#                     br=soup.new_tag('br')
#                     p_tag.append(br)
#             div.append(p_tag)
#     ul_tag1.append(ul_tag2)
#     ul_tag.append(ul_tag1)
#     div.append(ul_tag)
#     body.append(div)
#     return soup.prettify()

def docx_to_html(docx_path):
    html_content = pypandoc.convert_file(docx_path, 'html5')
    return html_content


def send_reload_signal():
    # Emit a 'reload' event to all connected clients
    socketio.emit('message', {'data': 'reload'})



app = Flask(__name__)
app.config['SECRET_KEY'] = '192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf'
socketio = SocketIO(app)
#socketio = SocketIO(app)

# Global dictionary to store amendments, now including timestamps
amendments = {'senior': {}, 'junior': {}, 'security_council': {}}
current_content = {'senior':'', 'junior':'', 'security_council': ''}




@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        comittee=request.form.get('radio')
        file = request.files['file']
        file.save(os.path.join("uploads/"+comittee+'/'+secure_filename(file.filename)))
        return render_template("registration.html",messageFromFlask='submit succeed')
    return render_template("registration.html",messageFromFlask='')





@app.route('/publish/<comittee>/<filename>')
def publish_docx(comittee,filename):
    html_content = '''<style>.underline {text-decoration: underline;}</style>''' + '<p>last update:' + get_current_time() + '</p>'
    html_content += docx_to_html(f'uploads/{comittee}/{filename}')
    current_content[comittee] = html_content
    socketio.emit('updateContent'+comittee, html_content)
    return render_template('display_'+comittee+'.html', html_content=html_content)


@app.route('/publishGoogleDoc/<comittee>/<filename>')
def publish_googleDocx(comittee,filename):
    send_reload_signal()
    html_content = docx_to_html(f'uploads/{comittee}/{filename}')
    return render_template('display_' + comittee + '.html', html_content=html_content)


@app.route('/download/<comittee>/<filename>')
def download(comittee, filename):
    return send_file("uploads/"+comittee+"/"+filename, as_attachment=True)


#display selected files from chairs
@app.route('/display/<comittee>/<filename>')
def display_docx(comittee,filename):
    html_content = docx_to_html(f'uploads/{comittee}/{filename}')
    return render_template('display_'+comittee+'.html', html_content=html_content)


#backstage for chairs to see the clauses
@app.route('/chairs/<comittee>')
def senior_clauses(comittee):
    filenames = extract_file_names("uploads/"+comittee)
    return render_template("chairs.html",filenames=filenames, comittee=comittee)


@app.route('/current/<comittee>')
def current_showing(comittee):
    return render_template('current_debate_'+comittee+'.html',html_content=current_content[comittee])

@app.route('/submit-amendments', methods=['GET', 'POST'])
def submit_amendments():
    if request.method == 'POST':
        committee_id = request.form['radio']
        amendment_type = request.form['rodioammendments']
        amendment_text = request.form['amendmentText']
        country = request.form['country']
        current_time = datetime.now()  # Get the current time and date

        committee_amendments = amendments.get(committee_id, {})
        if amendment_type in committee_amendments:
            committee_amendments[amendment_type].append((amendment_text, current_time, country))
        else:
            committee_amendments[amendment_type] = [(amendment_text, current_time, country)]
        amendments[committee_id] = committee_amendments  # Update the main dictionary
        socketio.emit('messageamendments', {'data': 'reload'})
        return render_template('submitamendments.html',messageFromFlask='submit succeed')
    else:
        return render_template('submitamendments.html',messageFromFlask='')


@app.route('/view-amendments/<comittee>')
def view_amendment(comittee):
    if comittee in amendments:
        all_amendments = []
        # Combine all amendments into a single list, including their types
        for amendment_type, texts_with_times in amendments[comittee].items():
            for text, timestamp, country in texts_with_times:
                all_amendments.append((amendment_type, text, timestamp, country))
        # Sort the combined list of amendments by timestamp, earliest to latest
        sorted_amendments = sorted(all_amendments, key=lambda x: x[2],reverse=True)

        return render_template('amendments.html', comittee=comittee, amendments=sorted_amendments)
    else:
        return f"No records found for committee: {comittee}", 404



#-----------------------------------------------------------------------------------------------------------------------
#upload page for senior delegates
@app.route('/chair_upload_senior', methods=['POST'])
def chair_upload_file_senior():
    if request.method == 'POST':
        file = request.files['file']
        file.save(os.path.join("uploads/senior/"+secure_filename(file.filename)))
        return redirect(url_for('display_docx',comittee='senior',filename=secure_filename(file.filename)))

#-----------------------------------------------------------------------------------------------------------------------
#upload page for junior delegates
@app.route('/chair_upload_junior', methods=['POST'])
def chair_upload_file_junior():
    if request.method == 'POST':
        file = request.files['file']
        file.save(os.path.join("uploads/junior/"+secure_filename(file.filename)))
        return redirect(url_for('display_docx',comittee='junior',filename=secure_filename(file.filename)))


#-----------------------------------------------------------------------------------------------------------------------
#upload page for security council delegates
@app.route('/chair_upload_security_council', methods=['POST'])
def chair_upload_file_security_council():
    if request.method == 'POST':
        file = request.files['file']
        file.save(os.path.join("uploads/security_council/"+secure_filename(file.filename)))
        return redirect(url_for('display_docx',comittee='security_council',filename=secure_filename(file.filename)))


#if __name__ == "__main__":
#     socketio.run(app,debug=True,allow_unsafe_werkzeug=True,port=8000)
