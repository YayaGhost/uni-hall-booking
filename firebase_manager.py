import firebase_admin
from firebase_admin import credentials,firestore
from PyQt6.QtCore import pyqtSignal, QObject

class FirebaseManager(QObject):
    #send hall data to main.py ui for realtime updates        
    halls_updated = pyqtSignal(dict)
    
    def __init__(self):
        super().__init__()
        
        if not firebase_admin._apps:
            cred = credentials.Certificate("serviceAccountKey.json")
            firebase_admin.initialize_app(cred)
            
        self.db = firestore.client()
        self.listener = None

    def start_listener(self):
        col_ref = self.db.collection('halls')
        self.listener = col_ref.on_snapshot(self._on_snapshot_callback)
    
    def _on_snapshot_callback(self,col_snapshot,changes,read_time):
        hall_data = {}
        for doc in col_snapshot:
            hall_data[doc.id] = doc.to_dict().get('status','unknown')
        self.halls_updated.emit(hall_data)
    def book_hall(self, hall_id):
        try:
            doc_ref = self.db.collection('halls').document(hall_id)
            doc_ref.update({'status': 'booked'})
        except Exception as e:
            return False, str(e)
        return True, "Hall booked successfully"