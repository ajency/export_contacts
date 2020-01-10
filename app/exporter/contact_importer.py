from app.base.models import Batch, Contact
import pandas as pd
from app import db

class ContactImporter():

    def create_batch(self, file):
        df = pd.read_csv(file)

        batch = Batch(count=df.shape[0], status="PENDING")
        db.session.add(batch)
        db.session.commit()

        for _, row in df.iterrows():
            print(row["email"])
            contact = Contact(batch_id=batch.id, email=row["email"], status="PENDING")
            db.session.add(contact)
        db.session.commit()
        return batch.id