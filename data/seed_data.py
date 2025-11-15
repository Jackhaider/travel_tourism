from app import create_app
from models import db, Destination

app = create_app()

with app.app_context():
    db.create_all()

    # Only add sample data if database is empty
    if Destination.query.count() == 0:
        sample = [
            {
                'name': 'Goa Beach Escape',
                'location': 'Goa',
                'price': 5000,
                'description': 'Relax on sunny beaches and enjoy water sports.',
                'image': 'https://images.unsplash.com/photo-1507525428034-b723cf961d3e'
            },
            {
                'name': 'Himalayan Trek',
                'location': 'Manali',
                'price': 12000,
                'description': '7-day guided trek in the Himalayas.',
                'image': 'https://images.unsplash.com/photo-1501785888041-af3ef285b470'
            },
            {
                'name': 'Kerala Backwaters',
                'location': 'Alleppey',
                'price': 8000,
                'description': 'Houseboat stay and village tours.',
                'image': 'https://images.unsplash.com/photo-1502082553048-f009c37129b9'
            }
        ]

        for s in sample:
            d = Destination(**s)
            db.session.add(d)

        db.session.commit()
        print('Seeded data')
    else:
        print('Data already exists')
