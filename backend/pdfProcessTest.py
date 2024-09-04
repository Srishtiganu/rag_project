from pdf_process import pdf_to_text_chunks
from embeddings import create_embeddings, store_embeddings

pdf_path = "./pdfs/ELIT10FinalEssay.pdf"

def test_pdf_processing(pdf_path):
    try:
        # Process PDF
        text_chunks = pdf_to_text_chunks(pdf_path)
        num_chunks = len(text_chunks)
        print(f"Number of chunks: {num_chunks}")
        
        # if text_chunks: #test print first chunk
        #     print("\nFirst chunk:\n", text_chunks[0])

        embeddings = create_embeddings(text_chunks)
        store_embeddings(embeddings, text_chunks)
        
        print("\n\nPDF and embeddings processed successfully.")
        
    except Exception as e:
        print(f"Error processing PDF: {str(e)}")

if __name__ == "__main__":
    test_pdf_processing(pdf_path)