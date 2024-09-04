import PyPDF2
import re

def pdf_to_text_chunks(pdf_path, chunk_size=500):
    with open(pdf_path, 'rb') as file: #open pdf, rb means "read binary" --> opening in binary read mode (less error/corruption than text mode)
        reader = PyPDF2.PdfReader(file) #pdf reader object
        text = '' 
        for page in reader.pages:  #loop through each pdf page
            text += page.extract_text() #concatenate the text on the page and add to the text string
    
    #Now split into chunks:
    chunks = split_text(text, chunk_size) #chunk is not character size, it is word count
    return chunks #return list of chunks


#chunk splitter function
def split_text(text, chunk_size):
    # chunks = []
    # for i in range(0, len(text), chunk_size):  #iterate through text, step size = chunk size
    #     chunk = text[i:i + chunk_size]  #take chunk from the curr pos to curr pos + chunk size
    #     chunks.append(chunk)  #add to list
    # return chunks 
    words = re.findall(r'\b\w+\b', text)  # Split text into words
    chunks = []
    current_chunk = ''
    word_count = 0

    for word in words:
        if word_count + len(word.split()) > chunk_size:
            chunks.append(current_chunk.strip())
            current_chunk = ''
            word_count = 0

        current_chunk += word + ' '
        word_count += len(word.split())

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks