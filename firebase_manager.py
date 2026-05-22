import firebase_admin
import datetime
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
        self.check_daily_reset()

    def start_listener(self):
        col_ref = self.db.collection('halls')
        self.listener = col_ref.on_snapshot(self._on_snapshot_callback)
    
    def _on_snapshot_callback(self,col_snapshot,changes,read_time):
        hall_data = {}
        for doc in col_snapshot:
            hall_data[doc.id] = doc.to_dict().get('periods', {})
        self.halls_updated.emit(hall_data)
    def book_hall(self, hall_id, period, user_id):
        try:
            doc_ref = self.db.collection('halls').document(hall_id)
            doc_ref.update({f'periods.{period}': user_id})
        except Exception as e:
            return False, str(e)
        return True, "Hall booked successfully"
    def unbook_hall(self, hall_id, period):
        try:
            doc_ref = self.db.collection('halls').document(hall_id)
            doc_ref.update({f'periods.{period}': 'available'})
        except Exception as e:
            return False, str(e)
        return True, "Hall unbooked successfully"
    def check_daily_reset(self):
        #method lazily resets booked halls when first person logs in a new day
        #cost efficient
        today = datetime.date.today().isoformat()
        
        #get time halls were last reset
        sys_ref = self.db.collection('system').document('settings')
        sys_doc = sys_ref.get()

        last_reset = ""
        if sys_doc.exists:
            last_reset = sys_doc.to_dict().get('last_reset_date', '')
        
        #new day -> reset booked halls
        if today != last_reset:
            self._execute_full_reset()
            sys_ref.set({'last_reset_date': today}, merge=True) #next person to log in does not retrigger reset
    def _execute_full_reset(self):
        halls_ref = self.db.collection("halls")
        docs = halls_ref.stream()
        batch = self.db.batch()
        for doc in docs:
            batch.update(doc.reference,{
                'periods.08:30 AM - 10:00 AM': 'available',
                'periods.10:15 AM - 11:45 AM': 'available',
                'periods.12:15 PM - 01:45 PM': 'available',
                'periods.02:00 PM - 03:30 PM': 'available',
                'periods.03:30 PM - 05:00 PM': 'available'
            })
        batch.commit()