import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

def test_firestore_connection():
    try:
        cred = credentials.Certificate("serviceAccountKey.json")
        firebase_admin.initialize_app(cred)
        
        db = firestore.client()
        print("Successful Connection!")

        hall_ref = db.collection('halls').document('501')
        hall_ref.set({
            'name': 'Hall 501',
            'capacity': 100,
            'location': 'Building A'
        })

        halls_ref = db.collection('halls')
        docs = halls_ref.stream()
        for doc in docs:
            print(f'{doc.id} => {doc.to_dict()}')
    except Exception as e:
        print(f"Error connecting to Firestore: {e}")
if __name__ == "__main__":
    test_firestore_connection()
        