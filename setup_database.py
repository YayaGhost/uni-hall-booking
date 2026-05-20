import firebase_admin
from firebase_admin import credentials, firestore

def setup_halls():
    print("Connecting to Firebase...")
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)
    db = firestore.client()

    # The official list of halls for the Electrical Dept
    halls_to_create = ['501', '502', '503', '504', '508', '509', '511', '512', '515', '518']
    
    print("Uploading halls to database...")
    batch = db.batch()
    
    for hall_id in halls_to_create:
        doc_ref = db.collection('halls').document(hall_id)
        # We set everything to 'available' by default
        batch.set(doc_ref, {
            'status': 'available',
            'room_name': f'Hall {hall_id}'
        })
        
    # Commit the batch write to Firebase
    batch.commit()
    print(f"Successfully added {len(halls_to_create)} halls to Firestore!")

if __name__ == "__main__":
    setup_halls()