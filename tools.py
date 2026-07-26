from langchain_core.tools import tool
import mysql.connector
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

@tool
def get_order_status(order_id : str) -> str:
    """
    Search the customer database to fetch real-time order status, 
    estimated delivery dates, and tracking URLs using an order_id.
    """
    try:
        connection = mysql.connector.connect(
            host = "127.0.0.1",
            user = "root",
            database = "astra_db",
            port = "3306"
        )

        if connection.is_connected():
            print("MySQL is connected sucessfully")
            cursor = connection.cursor(dictionary=True)
            query = "SELECT * FROM orders WHERE order_id = %s;"
            cursor.execute(query, (order_id,))
            record = cursor.fetchone()
            print("connected to database")

            if record:
                return (
                    f"Order ID: {record['order_id']}\n"
                    f"Status: {record['status']}\n"
                    f"Estimated Delivery: {record['estimated_delivery']}\n"
                    f"Tracking URL: {record['tracking_url']}"
                )
            else:
                return f"Order ID {order_id} was not found in the database."


    except Exception as e:
        print(f"couldn't connect to MySQL: {e}")
    
    finally:
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'connection' in locals() and connection.is_connected():
            connection.close()
            # print("MySQL connection is closed.")


embedding_model = HuggingFaceEmbeddings(model_name = "all-MiniLM-L6-v2")
chromadb = Chroma(persist_directory = "./chroma_db", embedding_function = embedding_model)

@tool
def search_kb(query : str) -> str:
    """
    Use this tool to search the technical knowledge base for troubleshooting steps,
    repair costs, or product manuals.
    """
    results = chromadb.similarity_search(query, k=2)

    if not results:
        return "no documentation found related to it"
    
    total_texts = ""

    for i in results:
        texts = i.page_content
        total_texts += texts + "\n\n"
    return total_texts

if __name__ == "__main__":
    print(get_order_status.invoke({"order_id": "010"}))
    print(search_kb.invoke({"query" : "how do i get refund"}))